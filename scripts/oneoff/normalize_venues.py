# -*- coding: utf-8 -*-
"""Normalise the `venue` field of data/papers.yaml.

85 distinct venue strings for 240 papers is not a vocabulary, it is an artifact.
Three separate problems were visible in the rendered README:

  1. **Truncation.** An earlier field-length cut left ~57-character stubs, so
     the README printed `(**the Journal of Machine Learning for Biomedical
     Imaging (MELB**, 2026)` and `(**Physics in Medicine &amp**, 2025)`. The
     second is also an undecoded HTML entity.
  2. **One venue, several spellings.** `TMI` (37) vs `IEEE Transactions on
     Medical Imaging` (1); `BSPC` vs `Biomedical Signal Processing and
     Control`; `Med Phys` vs `Medical Physics`; `BMVC2026` vs `BMVC 2026`;
     four different strings for ISBI. Since the field is what a reader
     recognises a journal by, fragmentation makes the list harder to scan,
     not easier.
  3. **The year written twice.** build.py renders `(**venue**, year)`, so
     `(**MICCAI 2025**, 2025)` and `(**AAAI 2026**, 2026)` repeat themselves.
     Conferences now carry the acronym only; the year already has a field.

It also fills the 11 entries that had no venue at all even though arXiv or
Crossref reports one, and corrects four years that contradict the journal
reference. Every filled value below is traceable to an arXiv journal_ref or a
Crossref lookup; the source is quoted in the comment next to it.

Read-only unless --write is passed.

Usage:
    python scripts/oneoff/normalize_venues.py            # print the plan
    python scripts/oneoff/normalize_venues.py --write    # apply + assert
"""
import io
import os
import re
import sys
import collections

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
PLAN = os.path.join(HERE, "venue-plan.txt")

# ---------------------------------------------------------------- vocabulary
# House style: short journal abbreviation, or a conference acronym. Lower-case
# "the " prefixes and trailing years belong to neither.
VENUE_MAP = {
    # --- truncated by a 57-character cut -------------------------------------
    "23rd International Conference on Image Analysis and Processi": "ICIAP",
    "IEEE International Symposium on Biomedical Imaging (ISBI) 20": "ISBI",
    "IEEE 18th International Symposium on Biomedical Imaging (ISBI)": "ISBI",
    "International Joint Conference on Neural Networks (IJCNN 202": "IJCNN",
    "the 2025 IEEE International Conference on Image Processing (": "ICIP",
    "the IEEE Transactions on Radiation and Plasma Medical Scienc": "TRPMS",
    "the Journal of Machine Learning for Biomedical Imaging (MELB": "MELBA",
    "the German Conference on Pattern Recognition proceedings": "GCPR",
    "the 28th International Conference on Pattern Recognition": "ICPR",
    "the IEEE International Conference on Acoustics": "ICASSP",
    "the European Conference on Computer Vision (ECCV) 2026": "ECCV",
    "CVPRW 2026 Med-Reasoner": "CVPRW",
    "SC26 Workshops proceedings": "SC Workshops",
    # --- undecoded HTML entity ----------------------------------------------
    "Physics in Medicine &amp": "PMB",
    # --- one venue, several spellings ---------------------------------------
    "IEEE Transactions on Medical Imaging": "TMI",
    "IEEE Transactions on Radiation and Plasma Medical Sciences": "TRPMS",
    "Medical Physics": "Med Phys",
    "Medical Image Analysis": "Med Image Anal",
    "Biomedical Signal Processing and Control": "BSPC",
    "Nature Biomedical Engineering": "Nat Biomed Eng",
    "Medical Imaging": "SPIE MI",
    # --- the year is already its own field ----------------------------------
    "AAAI 2026": "AAAI",
    "MICCAI 2025": "MICCAI",
    "ICCV 2025": "ICCV",
    "ECCV 2026": "ECCV",
    "Fully3D 2025": "Fully3D",
    "CAIP 2025": "CAIP",
    "MICAD 2026": "MICAD",
    "BHI 2026": "BHI",
    "DGM4MICCAI 2025": "DGM4MICCAI",
    "DGM4MICCAI 2026": "DGM4MICCAI",
    "BMVC 2026": "BMVC",
    "BMVC2026": "BMVC",
    "IEEE ISBI 2025": "ISBI",
    "ISBI2025": "ISBI",
}

# A preprint server is not a venue. The paper link is already an arXiv URL, so
# repeating "arXiv" in the venue slot adds nothing; 5 entries did exactly that.
DROP_VENUE = {"arXiv", "TechRxiv"}

# Per-entry overrides, for the cases a single string cannot decide.
VENUE_FIX = {
    # The community list filed this under the SPIE meeting, and the same authors
    # do have a SPIE Medical Imaging 2018 paper, but Crossref resolves
    # 10.1109/tmi.2018.2823756 (the DOI that sat on the duplicate) to
    # "IEEE Transactions on Medical Imaging" with this exact title.
    "wavresnet": "TMI",
    # Filled from the arXiv journal reference or the Crossref record. See the
    # quoted source above each group.
    "synergizing-physics-model-based-and-data-driven-methods-fo": "IEEE SPM",
    #   journal_ref: "IEEE Signal Processing Magazine, 40(2), 89-100, 2023"
    "splat-based-metal-artifact-reduction-in-cone-beam-ct-via-pol": "CGF",
    #   journal_ref: "Computer Graphics forum, Volume 45 (2026), Number 2"
    "revisiting-pose-sensitivity-in-splat-based-computed-tomograp": "CVPR",
    "splat-based-metal-artifact-reduction-in-cone-beam-ct-via-com": "CVPR",
    #   journal_ref: "... Conference on Computer Vision and Pattern Recognition (CVPR) 2026"
    "limited-angle-spect-image-reconstruction-using-deep-image-pr": "PMB",
    #   journal_ref: "Phys. Med. Biol. 70 (2025) 145005"
    "complex-wavelet-based-sinogram-segmentation-for-metal-artifa": "PMB",
    #   doi 10.1088/1361-6560/ae8fb3 -> Crossref "Physics in Medicine & Biology"
    "adaptive-diffusion-models-for-sparse-view-motion-corrected-h": "TRPMS",
    #   doi 10.1109/trpms.2025.3637124 -> Crossref "IEEE TRPMS"
    "computed-tomography-reconstruction-algorithm-using-markov-ra": "J. Phys. Soc. Jpn.",
    #   journal_ref: "J. Phys. Soc. Jpn. 95, 104001 (2026)"
    "equivariance2inverse-a-practical-self-supervised-ct-reconstr": "TCI",
    #   journal_ref: "IEEE Transactions on Computational Imaging (Volume 12, year 2026, ...)"
    "unsupervised-metal-artifact-reduction-in-dental-cbct-using-f": "Digital",
    #   journal_ref: "... Digital 2026, 6, 31"  (MDPI Digital)
}

# Year disagreeing with the journal reference. The list credits the venue, so
# the venue's year wins over the preprint's.
YEAR_FIX = {
    # journal_ref: "Lecture Notes in Computer Science, vol. 16128, Springer, 2025, pp. 244-253"
    "3d-cbct-artefact-removal-using-perpendicular-score-based-dif": 2025,
    # journal_ref: "IEEE Transactions on Medical Imaging, 2026"
    "cross-distribution-diffusion-priors-driven-iterative-reconst": 2026,
    # journal_ref: "IEEE Transactions on Computational Imaging (Volume 12, year 2026, ...)"
    "equivariance2inverse-a-practical-self-supervised-ct-reconstr": 2026,
    # journal_ref: "IEEE Signal Processing Magazine, 40(2), 89-100, 2023"
    "synergizing-physics-model-based-and-data-driven-methods-fo": 2023,
}

# Left without a venue on purpose: this is a congress abstract whose DOI
# (10.26044/ecr2026/c-28213) is not registered with Crossref, so it cannot be
# verified the way the rest of the list is. Flagged for review, not filled.
UNVERIFIED = ["toward-ct-equivalent-image-quality-in-low-dose-radiotherapy-"]

# ---- resolved after this run (see scripts/oneoff/apply_venue3.py) -----------
# Kept here as a record so the same three are not re-investigated next round.
VERIFIED_LATER = {
    # id                                                     -> (venue, year, DOI)
    "epi-naf": ("ISBI", 2025, "10.1109/isbi60581.2025.10981301"),
    "generative-modeling-in-sinogram-domain-for-sparse-view-ct-":
        ("TRPMS", 2024, "10.1109/trpms.2023.3309474"),
    "cocodiff-a-contextual-conditional-diffusion-model-for-low-":
        ("SPIE DXRT", 2022, "10.1117/12.2634939"),
}

# ---- investigated and REJECTED: candidate DOI belongs to a different work ---
# Crossref `query.bibliographic` returns low-similarity hits that look plausible
# but are a different paper. Confirmed by reading the candidate DOI's real title.
NOT_A_MATCH = {
    "diffmed": (
        "10.1016/j.media.2023.102846",
        "candidate is 'Diffusion models in medical imaging: A comprehensive survey' "
        "(Med Image Anal 2023); ours is 'Diffusion Models for Medical Image Analysis: "
        "A Comprehensive Survey' (arXiv 2211.07804) — different survey, do not merge",
    ),
    "learned-convex-regularizers-for-inverse-problems": (
        "10.1007/978-3-030-98661-2_68",
        "candidate is the book chapter 'Learned Regularizers for Inverse Problems' "
        "(2023); ours is 'Learned convex regularizers for inverse problems' "
        "(arXiv 2008.02839) — related but not the same record",
    ),
    "baggagect": (
        "10.1117/12.2309509",
        "candidate title 'Deep learning based sparse view x-ray CT reconstruction for "
        "checked baggage screening' differs from ours 'Fan-Beam CT Reconstruction for "
        "Unaligned Sparse-View X-Ray Baggage Data' (arXiv 2412.03036)",
    ),
}


def norm_venue(v):
    if v is None:
        return None
    return VENUE_MAP.get(v, v)


def main():
    write = "--write" in sys.argv
    raw = io.open(PAPERS, encoding="utf-8", newline="").read()
    entries = yaml.safe_load(raw)
    by_id = {}
    for e in entries:
        by_id.setdefault(e["id"], e)

    # ---- plan --------------------------------------------------------------
    drop, refill, reyear, unmapped = [], [], [], set()
    for e in entries:
        v = e.get("venue")
        if v is None:
            continue
        if v in DROP_VENUE:
            drop.append((e["id"], v))
            continue
        if e["id"] in VENUE_FIX:
            continue                      # per-entry override, reported below
        nv = norm_venue(v)
        if nv != v:
            refill.append((e["id"], v, nv))
        elif v not in VENUE_MAP.values() and v not in ("TMI", "TRPMS", "TCI",
                "TPAMI", "TNNLS", "TIM", "JBHI", "PMB", "Med Phys", "PR", "CBM",
                "CMPB", "BSPC", "JORSC", "SSVM", "MLMIR", "ASARI", "ICSP",
                "ICIFXCT", "DL4X-ray", "TOMOG", "MLMIR", "TMLR", "ICLR", "ICML",
                "IJCAI", "WACV", "ACM MM", "IEEE Access", "Proc. IEEE",
                "IEEE JSAIT", "IEEE SPM", "Acta Numerica", "Eur Radiol",
                "Inverse Problems", "JDI", "Patterns", "Tomography",
                "Scientific Data", "Nat Mach Intell", "Med Image Anal",
                "BJR|AI", "Off-Grid Workshop"):
            unmapped.add(v)
    for eid, v in VENUE_FIX.items():
        e = by_id.get(eid)
        if e is None:
            print("!! VENUE_FIX id not found: %s" % eid)
            continue
        if e.get("venue") != v:
            refill.append((eid, e.get("venue"), v))
    for eid, y in YEAR_FIX.items():
        e = by_id.get(eid)
        if e is None:
            print("!! YEAR_FIX id not found: %s" % eid)
            continue
        if e.get("year") != y:
            reyear.append((eid, e.get("year"), y))

    lines = []
    lines.append("entries            : %d" % len(entries))
    lines.append("venue set          : %d" % sum(1 for e in entries if e.get("venue")))
    lines.append("venues rewritten   : %d" % len(refill))
    lines.append("venues dropped     : %d  %s" % (len(drop), sorted({v for _, v in drop})))
    lines.append("years corrected    : %d" % len(reyear))
    lines.append("")
    lines.append("== rewritten ==")
    for eid, old, new in sorted(refill):
        lines.append("  %-58s %s  ->  %s" % (eid[:58], old, new))
    lines.append("")
    lines.append("== dropped (preprint server is not a venue) ==")
    for eid, v in sorted(drop):
        lines.append("  %-58s %s" % (eid[:58], v))
    lines.append("")
    lines.append("== years corrected ==")
    for eid, old, new in sorted(reyear):
        lines.append("  %-58s %s -> %s" % (eid[:58], old, new))
    lines.append("")
    lines.append("== venue strings not in the known vocabulary (%d) ==" % len(unmapped))
    for v in sorted(unmapped):
        lines.append("  %s" % v)
    lines.append("")
    lines.append("== left unverified (flagged, not filled) ==")
    for eid in UNVERIFIED:
        lines.append("  %s" % eid)
    txt = "\n".join(lines)
    io.open(PLAN, "w", encoding="utf-8").write(txt + "\n")
    print(txt)
    print("\nplan -> %s" % os.path.relpath(PLAN, ROOT))

    if not write:
        print("\n(dry run — pass --write to apply)")
        return 0

    # ---- apply: field surgery per block, everything else byte-identical -----
    def q(s):
        return '"%s"' % str(s).replace('"', '\\"')

    def set_venue(blk, value):
        """Replace the venue line, or insert one after `year:` if absent.

        Replacing alone is not enough: the 11 entries this script exists to
        fill have no venue line at all, so the first dry run wrote the file
        with those fields still missing.
        """
        if re.search(r"(?m)^  venue: ", blk):
            return re.sub(r"(?m)^  venue: .*$", "  venue: %s" % q(value),
                          blk, count=1)
        anchor = re.search(r"(?m)^  (year: .*)$", blk)
        if not anchor:
            anchor = re.search(r"(?m)^  (title: .*)$", blk)
        if not anchor:
            return blk
        return (blk[:anchor.end(1)] + "\n  venue: %s" % q(value)
                + blk[anchor.end(1):])

    def drop_venue(blk):
        return re.sub(r"(?m)^  venue: .*\n", "", blk, count=1)

    blocks = re.split(r"(?m)^(?=- id: )", raw)
    out = []
    touched = 0
    for blk in blocks:
        m = re.search(r'(?m)^- id: "([^"]+)"', blk)
        if not m:
            out.append(blk)
            continue
        eid = m.group(1)
        e = by_id.get(eid, {})
        nb = blk
        if e.get("venue") in DROP_VENUE:
            nb = drop_venue(nb)
        elif eid in VENUE_FIX:
            nb = set_venue(nb, VENUE_FIX[eid])
        elif e.get("venue") and norm_venue(e["venue"]) != e["venue"]:
            nb = set_venue(nb, norm_venue(e["venue"]))
        if eid in YEAR_FIX:
            nb = re.sub(r"(?m)^  year: \d+$", "  year: %d" % YEAR_FIX[eid], nb, count=1)
        if nb != blk:
            touched += 1
        out.append(nb)

    text = "".join(out)
    if not text.endswith("\n"):
        text += "\n"
    io.open(PAPERS, "w", encoding="utf-8", newline="").write(text)

    # ---- read back and assert ---------------------------------------------
    back = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    assert isinstance(back, list), "papers.yaml is not a list"
    assert len(back) == len(entries), \
        "entry count changed: %d -> %d" % (len(entries), len(back))
    assert [e["id"] for e in back] == [e["id"] for e in entries], "order changed"

    for e in back:
        v = e.get("venue")
        assert v not in DROP_VENUE, "%s still carries venue %r" % (e["id"], v)
        assert v != "Medical Imaging", "%s kept the ambiguous venue" % e["id"]
        if v:
            assert "&amp" not in v, "%s has an undecoded entity" % e["id"]
            assert not re.search(r"[,\s]\d{4}$", v), \
                "%s has a year inside the venue: %r" % (e["id"], v)
            assert "(" not in v or v.count("(") == v.count(")"), \
                "%s has unbalanced brackets: %r" % (e["id"], v)
            assert len(v) <= 60, "%s venue looks truncated: %r" % (e["id"], v)
    for eid, y in YEAR_FIX.items():
        assert eid in by_id, "YEAR_FIX id missing: %s" % eid
    final = {e["id"]: e for e in back}
    for eid, y in YEAR_FIX.items():
        assert final[eid]["year"] == y, "%s year not applied" % eid
    for eid, v in VENUE_FIX.items():
        assert final[eid].get("venue") == v, "%s venue not applied" % eid

    cnt = collections.Counter(e["venue"] for e in back if e.get("venue"))
    print("")
    print("wrote %s  (%d blocks touched)" % (os.path.relpath(PAPERS, ROOT), touched))
    print("distinct venue strings: %d -> %d" % (
        len(set(e.get("venue") for e in entries if e.get("venue"))), len(cnt)))
    print("entries with a venue : %d -> %d" % (
        sum(1 for e in entries if e.get("venue")),
        sum(1 for e in back if e.get("venue"))))
    print("read-back OK: count and order unchanged, no truncated/ambiguous venues, "
          "every fix applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
