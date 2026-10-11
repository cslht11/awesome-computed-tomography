"""Classify every paper by the standing of its venue, so "is the list too long?"
can be answered with numbers instead of opinion.

Tiers (my judgement, stated explicitly so it can be audited/changed):
  A  top conference            - the venue is a first-tier ML/CV/medical-imaging meeting
  B  flagship journal          - a leading journal in the field
  C  other peer-reviewed venue - solid but not flagship meetings/journals + workshops
  D  preprint, has code        - no venue, but a public implementation exists
  E  preprint, no code         - no venue, no code (the frontier tail)

Output: scripts/oneoff/venue-tier.txt
"""
import collections
import io
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
OUT = os.path.join(HERE, "venue-tier.txt")

A = {
    "CVPR", "ICCV", "ECCV", "NeurIPS", "ICML", "ICLR", "AAAI", "IJCAI",
    "ACM MM", "MICCAI", "ICASSP", "ISBI", "WACV", "ICIP", "BMVC", "ICPR",
}
B = {
    "TMI", "Med Image Anal", "PMB", "TRPMS", "TCI", "JBHI", "IEEE SPM",
    "TPAMI", "TNNLS", "TMLR", "Nature", "Nat Mach Intell", "Nat Biomed Eng",
    "Proc. IEEE", "Acta Numerica", "Inverse Problems", "Med Phys", "CGF",
    "PR", "Patterns", "Scientific Data", "JORSC", "MELBA", "CBM", "CMPB",
    "BSPC", "Eur Radiol",
}
# everything else with a venue falls through to C


def tier(e):
    v = e.get("venue")
    if v in A:
        return "A"
    if v in B:
        return "B"
    if v:
        return "C"
    return "D" if e.get("code") else "E"


def main():
    d = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    n = len(d)
    groups = collections.defaultdict(list)
    for e in d:
        groups[tier(e)].append(e)

    lines = []
    lines.append("papers total            : %d" % n)
    lines.append("")
    names = {"A": "top conference", "B": "flagship journal",
             "C": "other peer-reviewed venue", "D": "preprint + code",
             "E": "preprint, no code"}
    for t in "ABCDE":
        lines.append("%s. %-26s %3d  (%5.1f%%)" % (t, names[t], len(groups[t]), 100.0 * len(groups[t]) / n))

    with_venue = len(groups["A"]) + len(groups["B"]) + len(groups["C"])
    lines.append("")
    lines.append("venue-backed            : %d / %d  (%.1f%%)" % (with_venue, n, 100.0 * with_venue / n))
    lines.append("preprint-only           : %d / %d  (%.1f%%)" % (n - with_venue, n, 100.0 * (n - with_venue) / n))

    # the E tail split by recency: 2025-26 preprints are the frontier, old ones are the weak tail
    e_old = [e for e in groups["E"] if int(e.get("year") or 0) < 2025]
    e_new = [e for e in groups["E"] if int(e.get("year") or 0) >= 2025]
    lines.append("")
    lines.append("E tail: 2025-2026 (frontier) %d | pre-2025 (weak tail) %d" % (len(e_new), len(e_old)))

    lines.append("")
    lines.append("== C tier venues (what 'other peer-reviewed' covers) ==")
    cv = collections.Counter(e["venue"] for e in groups["C"])
    for v, c in sorted(cv.items()):
        lines.append("  %-22s %d" % (v, c))

    lines.append("")
    lines.append("== E, pre-2025 (the only real candidate for pruning) ==")
    for e in sorted(e_old, key=lambda x: (x.get("year"), x["id"])):
        lines.append("  %-4s %-58s %s" % (e.get("year"), e["id"][:58], str(e.get("title"))[:60]))

    lines.append("")
    lines.append("== E, 2025-2026 (frontier, keep) ==")
    for e in sorted(e_new, key=lambda x: (-int(x.get("year") or 0), x["id"])):
        lines.append("  %-4s %-58s %s" % (e.get("year"), e["id"][:58], str(e.get("title"))[:60]))

    txt = "\n".join(lines)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(txt + "\n")
    print(txt)
    print("\nreport -> scripts/oneoff/venue-tier.txt")


if __name__ == "__main__":
    main()
