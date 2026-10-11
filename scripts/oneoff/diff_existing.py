#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare the community CT list against our papers.yaml and list what we lack.

Read-only. Prints a candidate list (abbr | year | venue | title | link) plus a
per-year histogram, so the entries worth fetching can be picked before any
network verification happens.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WSC = os.path.dirname(ROOT)  # the 2026-10-09-15-24-19 workspace
SRC = os.path.join(WSC, "awesome-lists", "existing-ct-README.md")

CURATED = os.path.join(ROOT, "scripts", "oneoff", "papers_supp.yaml")
PAPERS = os.path.join(ROOT, "data", "papers.yaml")


def existing_titles():
    """Titles already in the list.

    This once read only papers_supp.yaml — the hand-curated supplement — while
    the 146 entries that actually ship live in data/papers.yaml. The diff was
    therefore blind to them and reported ~96 candidates that were already in
    the list, of which 88 got appended a second time. Both sources are read now.
    """
    out = set()
    for path in (PAPERS, CURATED):
        if not os.path.exists(path):
            continue
        txt = io.open(path, encoding="utf-8").read()
        try:
            import yaml
            data = yaml.safe_load(txt)
        except Exception:
            data = None
        if isinstance(data, list):
            for e in data:
                if isinstance(e, dict) and e.get("title"):
                    out.add(norm(e["title"]))
        for m in re.finditer(r'^\s*title:\s*"(.+?)"\s*$', txt, re.M):
            out.add(norm(m.group(1)))
    return out


def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_link(body):
    """Remove every [[label](url)] and (**venue**) so the title is left over."""
    t = re.sub(r"<a name=\"[^\"]*\"></a>", "", body)
    t = re.sub(r"\[\[[^\]]*\]\([^)]*\)\]", "", t)
    t = re.sub(r"\*\*\[[^\]]*\]\*\*", "", t)      # **[ABBR]**
    t = re.sub(r"\*\*\(([^)]*)\)\*\*", "", t)      # (**venue**)
    t = re.sub(r"\((?:\*\*)?[^()]*?(?:\*\*)?\)\s*$", "", t)
    return re.sub(r"\s+", " ", t.strip().strip("*")).strip()


def main():
    lines = io.open(SRC, encoding="utf-8", errors="replace").read().split("\n")
    have = existing_titles()
    year = None
    rows = []
    for ln in lines:
        h = re.match(r"^###\s+(\d{4})\s*$", ln)
        if h:
            year = int(h.group(1))
            continue
        if not ln.strip().startswith("- "):
            continue
        body = ln.strip()[2:]
        paper = re.search(r"\[\[(?:paper|Paper|pdf|PDF|Pdf)\]\((https?://[^)]+)\)\]", body)
        if not paper:
            continue
        abbr = re.search(r"\*\*\[([^\]]{1,40})\]\*\*", body)
        title = strip_link(body)
        cands = {norm(title)}
        if abbr:
            cands.add(norm(abbr.group(1)))
        if cands & have:
            continue
        rows.append((year or 0, abbr.group(1) if abbr else "?", title,
                     paper.group(1)))

    rows.sort(key=lambda r: (-r[0], r[1].lower()))
    print("=== candidates: %d ===" % len(rows))
    for y, a, t, u in rows:
        print("%d\t[%s]\t%s\t%s" % (y, a, t[:95], u))

    print()
    print("=== per-year counts ===")
    from collections import Counter
    c = Counter(r[0] for r in rows)
    for y in sorted(c, reverse=True):
        print("  %s: %d" % (y, c[y]))


if __name__ == "__main__":
    main()
