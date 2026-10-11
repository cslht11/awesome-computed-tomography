# -*- coding: utf-8 -*-
"""Find duplicate works in data/papers.yaml and classify them.

Read-only. Groups entries by normalised title, then decides whether the members
of a group are the same *work* or two different papers that happen to share a
title. The join is done on canonical identifiers, not on the title alone:

    arxiv id  <- arxiv.org/abs/<id>
    doi       <- doi.org/10.x/y (or a bare 10.x/y inside any link field)
    arxiv->doi  taken from the <arxiv:doi> element the arXiv API returns for
                every preprint that has since been published

Two entries are the same work when they share an arxiv id, share a doi, or one
side's doi is the other side's arxiv-reported journal doi.

Outputs a classification table to stdout and scripts/oneoff/duplicates-report.txt

Usage:
    python scripts/oneoff/find_duplicates.py
"""
import io
import os
import re
import sys
import json
import collections

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import time                                 # noqa: E402

from audit_arxiv import GAP                 # noqa: E402

PAPERS = os.path.join(ROOT, "data", "papers.yaml")
OUT = os.path.join(HERE, "duplicates-report.txt")
CACHE = os.path.join(HERE, "arxiv-meta.json")

LINK_FIELDS = ("paper", "project", "code")
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>()\[\],;]+")
AX_RE = re.compile(r"arxiv\.org/abs/([A-Za-z0-9.\-/]+)", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def doi_of(e):
    out = set()
    for f in LINK_FIELDS:
        for m in DOI_RE.finditer(e.get(f) or ""):
            out.add(m.group(0).lower().rstrip("."))
    return out


def ax_of(e):
    out = set()
    for f in LINK_FIELDS:
        for m in AX_RE.finditer(e.get(f) or ""):
            out.add(re.sub(r"v\d+$", "", m.group(1)))
    return out


def load():
    return yaml.safe_load(io.open(PAPERS, encoding="utf-8"))


def arxiv_meta(ids, cache=CACHE):
    """id -> {title, doi, journal, year}. Cached so re-runs cost nothing."""
    ids = sorted(ids)
    out = {}
    if os.path.exists(cache):
        try:
            out = json.load(io.open(cache, encoding="utf-8"))
        except Exception:
            out = {}
    todo = [i for i in ids if i not in out]
    if not todo:
        return out
    batches = [todo[i:i + 20] for i in range(0, len(todo), 20)]
    for n, batch in enumerate(batches, 1):
        xml = ""
        for attempt in range(3):
            xml = _raw(batch)
            if xml.count("<entry>") >= max(1, len(batch) // 2):
                break
            time.sleep(GAP * (attempt + 2))
        for m in re.finditer(r"<entry>(.*?)</entry>", xml or "", re.S):
            b = m.group(1)
            i = re.search(r"<id>\s*https?://arxiv\.org/abs/([^<\s]+)\s*</id>", b)
            if not i:
                continue
            aid = re.sub(r"v\d+$", "", i.group(1).strip())
            t = re.search(r"<title>(.*?)</title>", b, re.S)
            d = re.search(r"<arxiv:doi[^>]*>(.*?)</arxiv:doi>", b, re.S)
            j = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", b, re.S)
            p = re.search(r"<published>(\d{4})", b)
            out[aid] = {
                "title": re.sub(r"\s+", " ", t.group(1)).strip() if t else "",
                "doi": (d.group(1).strip().lower() if d else ""),
                "journal": re.sub(r"\s+", " ", j.group(1)).strip() if j else "",
                "year": int(p.group(1)) if p else None,
            }
        print("  arxiv meta %d/%d -> %d" % (n, len(batches), len(out)))
        time.sleep(GAP)
    io.open(cache, "w", encoding="utf-8").write(json.dumps(out, indent=1))
    return out


def _raw(ids):
    import urllib.request
    import urllib.parse
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = ("https://export.arxiv.org/api/query?id_list=%s&max_results=%d"
           % (urllib.parse.quote(",".join(ids)), len(ids)))
    req = urllib.request.Request(
        url, headers={"User-Agent": "awesome-computed-tomography/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return ""


def main():
    d = load()
    fam = collections.defaultdict(list)
    for e in d:
        fam[norm(e["title"])].append(e)

    ax_ids = set()
    for e in d:
        ax_ids |= ax_of(e)
    print("entries: %d   distinct titles: %d   arxiv ids: %d"
          % (len(d), len(fam), len(ax_ids)))
    print("fetching arXiv metadata ...")
    meta = arxiv_meta(ax_ids)

    lines = []
    same_work, distinct = [], []
    for key, members in sorted(fam.items()):
        if len(members) < 2:
            continue
        # canonical identity sets, after folding arxiv->doi
        dois, axs = set(), set()
        for e in members:
            for a in ax_of(e):
                axs.add(a)
                if meta.get(a, {}).get("doi"):
                    dois.add(meta[a]["doi"])
            dois |= doi_of(e)
        # link every member to a canonical key
        linked = set()
        for e in members:
            for a in ax_of(e):
                linked.add("ax:" + a)
                if meta.get(a, {}).get("doi"):
                    linked.add("doi:" + meta[a]["doi"])
            for x in doi_of(e):
                linked.add("doi:" + x)
        groups = {}
        for e in members:
            ks = set()
            for a in ax_of(e):
                ks.add("ax:" + a)
                if meta.get(a, {}).get("doi"):
                    ks.add("doi:" + meta[a]["doi"])
            for x in doi_of(e):
                ks.add("doi:" + x)
            groups.setdefault(frozenset(ks), []).append(e)

        # members sharing a key (transitively) are the same work
        parent = {}
        def find(x):
            while parent.get(x, x) != x:
                x = parent[x]
            return x
        def union(a, b):
            parent.setdefault(a, a); parent.setdefault(b, b)
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
        for e in members:
            ks = sorted(k for k in
                        ["ax:" + a for a in ax_of(e)] +
                        ["doi:" + x for x in doi_of(e)] +
                        (["doi:" + meta[a]["doi"]] if any(
                            meta.get(a, {}).get("doi") for a in ax_of(e)) else []))
            ek = "e:" + e["id"]
            parent.setdefault(ek, ek)
            for k in ks:
                union(ek, k)
        clusters = collections.defaultdict(list)
        for e in members:
            clusters[find("e:" + e["id"])].append(e)

        for _, cl in sorted(clusters.items()):
            if len(cl) > 1:
                same_work.append((key, cl))
            else:
                distinct.append((key, cl))

    lines.append("SAME-WORK CLUSTERS: %d  (entries removed: %d)"
                 % (len(same_work), sum(len(c) - 1 for _, c in same_work)))
    lines.append("")
    for key, cl in same_work:
        lines.append("=" * 96)
        lines.append("TITLE  %s   [%d copies]" % (key[:88], len(cl)))
        for e in cl:
            lines.append("   id=%-58s year=%s" % (e["id"][:58], e.get("year")))
            lines.append("       venue=%-46s paper=%s"
                         % (str(e.get("venue") or "-")[:46], e.get("paper")))
            extra = []
            for f in ("code", "project", "abbr"):
                if e.get(f):
                    extra.append("%s=%s" % (f, e[f]))
            if extra:
                lines.append("       " + "  ".join(extra))
    if distinct:
        lines.append("")
        lines.append("SHARED TITLE BUT DIFFERENT WORK: %d" % len(distinct))
        for key, cl in distinct:
            lines.append("   %s -> %s" % (key[:70], [e["id"] for e in cl]))

    txt = "\n".join(lines)
    io.open(OUT, "w", encoding="utf-8").write(txt + "\n")
    print(txt[:4000])
    print("\n... full report -> %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
