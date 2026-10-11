# -*- coding: utf-8 -*-
"""Audit the `year` field of every arXiv-linked paper against arXiv metadata.

Two independent signals come back from the arXiv API for each preprint:

    <published>          the year the v1 preprint appeared
    <arxiv:journal_ref>  e.g. "J. Oper. Res. Soc. China 8(2020) 311-340"

The journal reference is the better witness for a published paper, because the
list shows the venue. A year that is *earlier* than the preprint date is an
error only when the entry has no venue: with a venue, the conference can
precede the preprint, which is routine (a DGM4MICCAI 2025 paper posted to
arXiv in 2026). Those are reported separately as informational.

Read-only. Uses scripts/oneoff/arxiv-meta.json when present so re-runs are free.

Usage:
    python scripts/oneoff/audit_years.py
"""
import io
import os
import re
import sys
import collections

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from find_duplicates import ax_of, arxiv_meta, PAPERS, OUT  # noqa: E402

REPORT = os.path.join(HERE, "year-audit.txt")

# <arxiv:journal_ref> is free text and the year sits in several shapes:
#     "J. Oper. Res. Soc. China 8(2020) 311-340"          -> (2020)
#     "Phys. Med. Biol. 70 (2025) 145005"                 ->  (2025)
#     "IEEE Signal Processing Magazine, 40(2), 89-100, 2023" -> bare 2023
#     "IEEE Transactions on Computational Imaging (Volume 12, year 2026, ...)"
# Matching only the parenthesised form silently skipped the last two, so the
# audit under-reported. Any plausible 4-digit year will do.
YEAR_ANY = re.compile(r"(?<!\d)(19[5-9]\d|20[0-4]\d)(?!\d)")
JYEAR = re.compile(r"\((\d{4})\)")


def journal_year(ref):
    """Best-effort year out of an arXiv journal reference, else None."""
    if not ref:
        return None
    m = JYEAR.search(ref)
    if m:
        return int(m.group(1))
    years = [int(y) for y in YEAR_ANY.findall(ref)]
    # a volume number can be four digits but is never in this range
    return max(years) if years else None


def main():
    d = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    ids = set()
    for e in d:
        ids |= ax_of(e)
    meta = arxiv_meta(ids)

    impossible, differs, earlier, unknown = [], [], [], []
    for e in sorted(d, key=lambda x: x["id"]):
        axs = sorted(ax_of(e))
        if not axs:
            continue
        a = axs[0]
        m = meta.get(a) or {}
        pub, jr = m.get("year"), (m.get("journal") or "")
        jy = journal_year(jr)
        y = e.get("year")
        if y is None:
            unknown.append((e, a, pub, jy))
        elif pub and y < pub:
            # only an error without a venue to explain the earlier year
            (earlier if e.get("venue") else impossible).append((e, a, pub, jy))
        elif jy and abs(y - jy) >= 1:
            differs.append((e, a, pub, jy, jr))

    lines = []
    lines.append("papers checked          : %d" % sum(1 for e in d if ax_of(e)))
    lines.append("year earlier than arXiv, no venue to explain it : %d" % len(impossible))
    lines.append("year earlier than the arXiv posting, venue given: %d (informational)" % len(earlier))
    lines.append("disagrees with journal  : %d" % len(differs))
    lines.append("")
    lines.append("== year earlier than the preprint and no venue (mis-parse) ==")
    for e, a, pub, jy in impossible:
        lines.append("  %-52s year=%s  arxiv published=%s  journal=%s"
                     % (e["id"][:52], e.get("year"), pub, jy))
    lines.append("")
    lines.append("== venue year precedes the arXiv posting (plausible, listed for review) ==")
    for e, a, pub, jy in earlier:
        lines.append("  %-52s year=%-5s arxiv published=%s  venue=%s"
                     % (e["id"][:52], e.get("year"), pub, e.get("venue")))
    lines.append("")
    lines.append("== year differs from journal_ref ==")
    for e, a, pub, jy, jr in differs:
        lines.append("  %-52s year=%-5s journal_ref=%s(%s)  [%s]"
                     % (e["id"][:52], e.get("year"), jr.split("(")[0].strip(),
                        jy, e.get("venue") or "-"))
    txt = "\n".join(lines)
    io.open(REPORT, "w", encoding="utf-8").write(txt + "\n")
    print(txt)
    print("\nreport -> %s" % os.path.relpath(REPORT, ROOT))


if __name__ == "__main__":
    main()
