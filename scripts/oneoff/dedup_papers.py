# -*- coding: utf-8 -*-
"""Remove duplicate works from data/papers.yaml.

Context: the round-1 merge (scripts/oneoff/apply_candidates.py) deduplicated by
`id` alone, and the candidate list it consumed had been filtered against
scripts/oneoff/papers_supp.yaml instead of data/papers.yaml. Because the
original 146 entries use short acronym ids (lpd, dip, super) while the
candidates used slugs, almost nothing collided and 88 papers were inserted a
second time.

This script repairs that:
  * clusters entries by canonical identity, not by id:
        - shared arXiv id
        - shared DOI
        - an entry's DOI equals the <arxiv:doi> of another entry's arXiv id
        - identical normalised title AND identical year
  * keeps the entry that already exists in git HEAD (so ids, positions and the
    curated wording survive) and drops the copies;
  * folds useful links (code / project / venue) from a dropped copy into the
    keeper when the keeper lacks them;
  * corrects the keeper's year only when a dropped copy's year matches the
    arXiv publication year and the keeper's does not.

Everything else in the file is left byte-for-byte untouched.

Usage:
    python scripts/oneoff/dedup_papers.py            # print the plan
    python scripts/oneoff/dedup_papers.py --write    # apply + assert
"""
import io
import os
import re
import subprocess
import sys
import collections

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from find_duplicates import norm, doi_of, ax_of, arxiv_meta   # noqa: E402

PAPERS = os.path.join(ROOT, "data", "papers.yaml")
OUT = os.path.join(HERE, "dedup-plan.txt")

ORDER = ["id", "abbr", "title", "year", "venue", "topics", "paper", "code", "project"]

# Rows whose year/venue contradict arXiv's <arxiv:journal_ref>. The journal
# reference wins, because the list credits the venue, not the preprint. Both
# values below were read straight out of the arXiv API response.
ROW_FIX = {
    # journal_ref: "Biomedical Signal Processing and Control 75(2022) 103598"
    # the row claimed year 2025 / venue ICCV, inherited from the unrelated
    # ICCV-2025 paper (id "dgr") whose short id it collided with.
    "dgr-2": {"year": 2022,
              "venue": "Biomedical Signal Processing and Control"},
    # journal_ref: "J. Oper. Res. Soc. China 8(2020) 311-340"
    "a-review-on-deep-learning-in-medical-image-reconstruction": {"year": 2020},
}


def head_ids():
    """ids present in the committed data/papers.yaml."""
    try:
        txt = subprocess.check_output(
            ["git", "show", "HEAD:data/papers.yaml"], cwd=ROOT,
            stderr=subprocess.DEVNULL).decode("utf-8")
    except Exception:
        return set()
    return {e["id"] for e in yaml.safe_load(txt)}


def split_blocks(raw):
    """-> (preamble, [block_text, ...])  Blocks keep their trailing blank line."""
    m = re.search(r"(?m)^- id: ", raw)
    if not m:
        return raw, []
    pre = raw[:m.start()]
    rest = raw[m.start():]
    parts = re.split(r"(?m)^(?=- id: )", rest)
    return pre, parts


def field(block, name):
    # the first line of a block is "- id: ..." and the rest are "  key: ..."
    m = re.search(r"(?m)^[ \t]*(?:-[ \t]*)?%s:[ \t]*(.*)$" % name, block)
    if not m:
        return None
    v = m.group(1).strip()
    v = re.sub(r'^"(.*)"$', r"\1", v)
    v = re.sub(r"^'(.*)'$", r"\1", v)
    return v


def set_year(block, year):
    return re.sub(r"(?m)^  year: \d+$", "  year: %d" % year, block, count=1)


def set_topics(block, topics):
    return re.sub(r"(?m)^  topics: \[.*\]$",
                  "  topics: [%s]" % ", ".join(topics), block, count=1)


def set_scalar(block, name, value):
    """Replace (or insert after `paper:`) a scalar field, correctly typed."""
    if name == "year":
        if re.search(r"(?m)^  year: ", block):
            return set_year(block, int(value))
        insert = "  year: %d" % int(value)
    elif name == "topics":
        if re.search(r"(?m)^  topics: ", block):
            return set_topics(block, value)
        insert = "  topics: [%s]" % ", ".join(value)
    else:
        q = '"%s"' % str(value).replace('"', '\\"')
        if re.search(r"(?m)^  %s: " % name, block):
            return re.sub(r"(?m)^  %s: .*$" % name,
                          "  %s: %s" % (name, q), block, count=1)
        insert = "  %s: %s" % (name, q)
    anchor = re.search(r"(?m)^  (paper: .*)$", block)
    if not anchor:
        anchor = re.search(r"(?m)^  (title: .*)$", block)
    if not anchor:
        return block
    return block[:anchor.end(1)] + "\n" + insert + block[anchor.end(1):]


def set_field(block, name, value):
    """Back-compat alias used by the planner."""
    return set_scalar(block, name, value)


def main():
    write = "--write" in sys.argv
    raw = io.open(PAPERS, encoding="utf-8", newline="").read()
    entries = yaml.safe_load(raw)
    by_id = {e["id"]: e for e in entries}
    hex_ = head_ids()

    # ---- canonical keys ----------------------------------------------------
    ax_ids = set()
    for e in entries:
        ax_ids |= ax_of(e)
    meta = arxiv_meta(ax_ids)

    # ---- union-find --------------------------------------------------------
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for e in entries:
        find(e["id"])
    key_owner = {}
    for e in entries:
        keys = ["ax:" + a for a in ax_of(e)] + ["doi:" + d for d in doi_of(e)]
        for a in ax_of(e):
            d = meta.get(a, {}).get("doi")
            if d:
                keys.append("doi:" + d)
        for k in keys:
            if k in key_owner:
                union(e["id"], key_owner[k])
            else:
                key_owner[k] = e["id"]
    # identical title + identical year => same work (journal vs preprint that
    # arXiv does not cross-link, e.g. MAGIC, TFU-Net, WavResNet)
    ty = collections.defaultdict(list)
    for e in entries:
        ty[(norm(e["title"]), e.get("year"))].append(e["id"])
    for ids in ty.values():
        for i in ids[1:]:
            union(ids[0], i)

    clusters = collections.defaultdict(list)
    for e in entries:
        clusters[find(e["id"])].append(e)

    dups = {k: v for k, v in clusters.items() if len(v) > 1}

    # ---- keeper selection --------------------------------------------------
    plan = []
    forced = set()
    for k, cl in sorted(dups.items(), key=lambda kv: kv[1][0]["title"].lower()):
        # keeper: the HEAD entry if present, else the richest, else the first
        head_members = [e for e in cl if e["id"] in hex_]
        if len(head_members) == 1:
            keep = head_members[0]
        else:
            def score(e):
                return (sum(1 for f in ("venue", "code", "project", "abbr")
                            if e.get(f)) * 10
                        + (1 if e["id"] in hex_ else 0))
            keep = max(cl, key=score)
        losers = [e for e in cl if e is not keep]

        axfy = set()
        for e in cl:
            for a in ax_of(e):
                if meta.get(a, {}).get("year"):
                    axfy.add(meta[a]["year"])
        new_year = None
        if len(axfy) == 1:
            ay = next(iter(axfy))
            if keep.get("year") != ay and any(x.get("year") == ay for x in losers):
                new_year = ay

        fill = {}
        for f in ("venue", "code", "project", "abbr"):
            if not keep.get(f):
                for x in losers:
                    if x.get(f):
                        fill[f] = x[f]
                        break
        # a keeper that sits in the catch-all bucket takes the losers' topics
        if keep.get("topics") in (["other"], ["other", ], ["Other"]):
            for x in losers:
                if x.get("topics") and x["topics"] != ["other"]:
                    fill["topics"] = x["topics"]
                    break
        for f, v in (ROW_FIX.get(keep["id"]) or {}).items():
            if keep.get(f) != v:
                fill[f] = v
                forced.add((keep["id"], f, keep.get(f), v))
        plan.append((keep, losers, new_year, fill))

    # ---- report ------------------------------------------------------------
    lines = ["DUPLICATE CLUSTERS: %d   entries removed: %d"
             % (len(plan), sum(len(l) for _, l, _, _ in plan)), ""]
    no_head = 0
    for keep, losers, new_year, fill in plan:
        if keep["id"] not in hex_:
            no_head += 1
        lines.append("KEEP %-46s year=%-5s %s"
                     % (keep["id"][:46], keep.get("year"),
                        ("venue=" + str(keep.get("venue"))) if keep.get("venue") else ""))
        for x in losers:
            lines.append("  drop %-44s year=%-5s %s"
                         % (x["id"][:44], x.get("year"),
                            ("venue=" + str(x.get("venue"))) if x.get("venue") else ""))
        if new_year:
            lines.append("       year  %s -> %s   (matches arXiv publication year)"
                         % (keep.get("year"), new_year))
        for f, v in fill.items():
            if (keep["id"], f, keep.get(f), v) in forced:
                lines.append("       FIX  %s: %s -> %s   (contradicts arXiv journal_ref)"
                             % (f, keep.get(f), v))
            else:
                lines.append("       +%s %s" % (f, v))
    lines.append("")
    lines.append("clusters whose keeper is not in HEAD: %d" % no_head)
    txt = "\n".join(lines)
    io.open(OUT, "w", encoding="utf-8").write(txt + "\n")
    print(txt)
    print("\nplan -> %s" % os.path.relpath(OUT, ROOT))

    if not write:
        print("\n(dry run — pass --write to apply)")
        return 0

    # ---- apply -------------------------------------------------------------
    pre, blocks = split_blocks(raw)
    assert blocks, "could not split the file into blocks"
    drop_ids = {x["id"] for _, losers, _, _ in plan for x in losers}
    patch = {}
    for keep, _, new_year, fill in plan:
        b = None
        for blk in blocks:
            if field(blk, "id") == keep["id"]:
                b = blk
                break
        assert b is not None, "keeper block not found: %s" % keep["id"]
        nb = b
        if new_year:
            nb = set_year(nb, new_year)
        for f, v in fill.items():
            nb = set_field(nb, f, v)
        if nb != b:
            patch[keep["id"]] = nb

    kept = []
    for blk in blocks:
        bid = field(blk, "id")
        if bid in drop_ids:
            continue
        kept.append(patch.get(bid, blk))

    text = pre + "".join(kept)
    if not text.endswith("\n"):
        text += "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)

    io.open(PAPERS, "w", encoding="utf-8", newline="").write(text)

    # ---- read back and assert, never trust the write -----------------------
    back = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    assert isinstance(back, list), "papers.yaml is not a list"
    expected = len(entries) - len(drop_ids)
    assert len(back) == expected, \
        "expected %d entries, parsed %d" % (expected, len(back))

    ids = [e["id"] for e in back]
    assert len(ids) == len(set(ids)), "duplicate ids after dedup"

    t = collections.Counter(norm(e["title"]) for e in back)
    assert max(t.values()) == 1, \
        "duplicate titles remain: %s" % [k for k, v in t.items() if v > 1][:3]

    axs = collections.Counter()
    ds = collections.Counter()
    for e in back:
        for a in ax_of(e):
            axs[a] += 1
        for d in doi_of(e):
            ds[d] += 1
    assert max(axs.values() or [0]) == 1, \
        "duplicate arXiv ids remain: %s" % [k for k, v in axs.items() if v > 1][:3]
    assert max(ds.values() or [0]) == 1, \
        "duplicate DOIs remain: %s" % [k for k, v in ds.items() if v > 1][:3]

    bare = re.findall(r"(?m)^(?!- )(  id: .+)$", text)
    assert not bare, "entry block without a leading '- ': %s" % bare[:3]

    for e in back:
        for f in ("id", "title", "year", "topics", "paper"):
            assert e.get(f) not in (None, "", []), \
                "%s missing field %s" % (e.get("id"), f)

    print("")
    print("wrote %s" % os.path.relpath(PAPERS, ROOT))
    print("entries: %d -> %d  (removed %d duplicates)"
          % (len(entries), len(back), len(drop_ids)))
    print("read-back OK: ids, titles, arXiv ids and DOIs all unique; "
          "every entry has id/title/year/topics/paper")
    return 0


if __name__ == "__main__":
    sys.exit(main())
