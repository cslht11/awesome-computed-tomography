# -*- coding: utf-8 -*-
"""Merge verified candidates into data/papers.yaml and add the LoDoPaB-CT dataset.

Idempotent. Skipping on `id` alone was not enough: the entries already in
data/papers.yaml use short acronym ids (lpd, dip, super) while candidates get
slugs, so 88 papers that were already in the list were appended a second time.
A candidate is now rejected when its normalised title, arXiv id or DOI is
already present, whichever form of link the existing entry carries.

Every candidate carries a `_via` audit trail recording how its paper link was
resolved (crossref / arxiv), and `_sim` the title-match score.

Usage:
    python scripts/oneoff/apply_candidates.py            # dry run
    python scripts/oneoff/apply_candidates.py --write    # apply
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
DATASETS = os.path.join(ROOT, "data", "datasets.yaml")
MERGED = os.path.join(HERE, "candidates_merged.json")

FIELDS = ["id", "abbr", "title", "year", "venue", "topics", "paper", "code", "project", "data"]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def canon_keys(e):
    out = set()
    for f in ("paper", "project"):
        u = str(e.get(f) or "")
        for m in re.finditer(r"arxiv\.org/abs/([A-Za-z0-9.\-/]+)", u, re.I):
            out.add("arxiv:" + re.sub(r"v\d+$", "", m.group(1)))
        for m in re.finditer(r"10\.\d{4,9}/[^\s\"'<>()\[\],;]+", u):
            out.add("doi:" + m.group(0).lower().rstrip("."))
    return out


def q(v):
    return json.dumps(v, ensure_ascii=False)


def emit(e, order=FIELDS):
    """Emit one list item. The leading '- ' marker is mandatory — without it the
    block is parsed as a continuation of the previous entry and silently lost."""
    out = []
    first = True
    for k in order:
        if e.get(k) is None:
            continue
        v = e[k]
        if k == "topics":
            body = "topics: [%s]" % ", ".join(v)
        elif k == "year":
            body = "year: %d" % v
        else:
            body = "%s: %s" % (k, q(v))
        out.append(("- " + body) if first else ("  " + body))
        first = False
    return "\n".join(out)


def main():
    write = "--write" in sys.argv
    entries = json.load(io.open(MERGED, encoding="utf-8"))

    src = io.open(PAPERS, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    have = set(re.findall(r'^- id:\s*"([^"]+)"', src, re.M))

    import yaml
    existing = yaml.safe_load(src) or []
    have_titles = {norm(e.get("title")) for e in existing}
    have_keys = set()
    for e in existing:
        have_keys |= canon_keys(e)

    new, skipped, dupes = [], [], []
    for e in entries:
        keys = canon_keys(e)
        if e["id"] in have:
            skipped.append(e["id"])
            continue
        if norm(e.get("title")) in have_titles or (keys & have_keys):
            dupes.append(e["id"])
            continue
        have_titles.add(norm(e.get("title")))
        have_keys |= keys
        new.append(e)

    blocks = []
    for e in new:
        blocks.append(emit(e))
    text = (src.rstrip("\r\n") + nl + nl + (nl + nl).join(blocks) + nl)

    print("candidates : %d" % len(entries))
    print("new        : %d" % len(new))
    print("skipped    : %d (id already present) %s" % (len(skipped), skipped[:8]))
    print("rejected   : %d (title/arxiv/doi already present) %s"
          % (len(dupes), dupes[:8]))
    from collections import Counter
    c = Counter(t for e in new for t in e["topics"])
    print("topics     : %s" % dict(c.most_common()))
    print("by year    : %s" % dict(sorted(Counter(e["year"] for e in new).items(), reverse=True)))

    if not write:
        print("\n(dry run — pass --write to apply)")
        return
    io.open(PAPERS, "w", encoding="utf-8", newline="").write(text)

    # ---- read back and assert, never trust the write
    import yaml
    back = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    assert isinstance(back, list), "papers.yaml did not parse as a list"
    assert len(back) == len(have) + len(new), (
        "expected %d entries, parsed %d — check the list-item markers"
        % (len(have) + len(new), len(back)))
    ids = [e["id"] for e in back]
    assert len(ids) == len(set(ids)), "duplicate ids after merge"
    bare = re.findall(r"^(?!- )(  id: .+)$", text, re.M)
    assert not bare, "entry block without a leading '- ': %s" % bare[:3]
    print("\nwrote %s (+%d entries)" % (PAPERS, len(new)))
    print("read-back OK: %d entries, ids unique" % len(back))


if __name__ == "__main__":
    main()
