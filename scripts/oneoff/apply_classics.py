# -*- coding: utf-8 -*-
"""Add the field's foundational papers to the three thinnest sections.

Spectral (6 entries), scatter (6) and dynamic/4D (9) were thin for a specific
reason: they were missing the works the sub-field is built on. Every candidate
in this script was resolved against Crossref by FULL TITLE with a >= 0.90
similarity gate and then read back by DOI a second time (`verify_classics.py`,
output in `classics-verify.json`); the venue and year below are the version of
record, not the online-first date.

Three things the second pass caught, which is why it exists:

  - The Med Phys 2011 scatter review in the list (`scatter-rev`) carries Part 1
    in its title but Part 2's DOI (10.1118/1.3589140). `PART1_FIX` repairs it to
    10.1118/1.3599033 and the pair is completed with Part 2.
  - A guessed DOI for the Rit paper (10.1118/1.3121505) resolves to an unrelated
    AAPM task-group report. The real journal version is 10.1118/1.3115691, whose
    title says "respiratory motion", not "the motion".
  - Crossref reports Maier 2019 as issued 2018-11-26 (online first). The print
    issue is 46(1), January 2019, and the list's rule is that the year belongs
    to the version of record.

Titles are house-styled (title case, ASCII hyphens, markup stripped): Crossref
returns `x‐ray` with a U+2010 and `an <i>a priori</i> model`, neither of which
belongs in the list.

Read-only unless --write is passed.
"""
import io
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")

# --- the existing entry whose DOI points at the wrong part of the pair -------
PART1_FIX = dict(
    id="scatter-rev",
    expect_paper="https://doi.org/10.1118/1.3589140",
    paper="https://doi.org/10.1118/1.3599033",
    expect_title="A General Framework and Review of Scatter Correction Methods "
                 "in X-Ray Cone-Beam CT: Part 1",
    title="A General Framework and Review of Scatter Correction Methods "
          "in X-Ray Cone-Beam CT: Part 1 \u2014 Scatter Compensation Approaches",
)

# --- new entries, oldest first within each group -----------------------------
ADDITIONS = [
    # ---- spectral / dual-energy ------------------------------------------
    dict(id="alvarez-1976", topics=["spectral"], year=1976, venue="PMB",
         title="Energy-Selective Reconstructions in X-Ray Computerised Tomography",
         doi="10.1088/0031-9155/21/5/002"),
    dict(id="deman-2001", topics=["spectral"], year=2001, venue="TMI",
         title="An Iterative Maximum-Likelihood Polychromatic Algorithm for CT",
         doi="10.1109/42.959297"),
    dict(id="elbakri-2002", topics=["spectral"], year=2002, venue="TMI",
         title="Statistical Image Reconstruction for Polyenergetic X-Ray Computed Tomography",
         doi="10.1109/42.993128"),
    dict(id="roessl-2007", topics=["spectral"], year=2007, venue="PMB",
         title="K-Edge Imaging in X-Ray Computed Tomography Using Multi-Bin Photon Counting Detectors",
         doi="10.1088/0031-9155/52/15/020"),
    dict(id="schlomka-2008", topics=["spectral"], year=2008, venue="PMB",
         title="Experimental Feasibility of Multi-Energy Photon-Counting K-Edge Imaging in Pre-Clinical Computed Tomography",
         doi="10.1088/0031-9155/53/15/002"),
    dict(id="mccollough-2015", topics=["spectral", "survey"], year=2015,
         venue="Radiology",
         title="Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications",
         doi="10.1148/radiol.2015142631"),
    # ---- scatter ---------------------------------------------------------
    dict(id="siewerdsen-2001", topics=["scatter", "cbct"], year=2001,
         venue="Med Phys",
         title="Cone-Beam Computed Tomography with a Flat-Panel Imager: Magnitude and Effects of X-Ray Scatter",
         doi="10.1118/1.1339879"),
    dict(id="zbijewski-2006", topics=["scatter"], year=2006, venue="TMI",
         title="Efficient Monte Carlo Based Scatter Artifact Reduction in Cone-Beam Micro-CT",
         doi="10.1109/tmi.2006.872328"),
    dict(id="zhu-2006", topics=["scatter"], year=2006, venue="TMI",
         title="Scatter Correction Method for X-Ray CT Using Primary Modulation: Theory and Preliminary Results",
         doi="10.1109/tmi.2006.884636"),
    dict(id="scatter-rev-p2", topics=["scatter", "survey"], year=2011,
         venue="Med Phys",
         title="A General Framework and Review of Scatter Correction Methods in Cone-Beam CT: Part 2 \u2014 Scatter Estimation Approaches",
         doi="10.1118/1.3589140"),
    dict(id="maier-2019", topics=["scatter"], year=2019, venue="Med Phys",
         title="Real-Time Scatter Estimation for Medical CT Using the Deep Scatter Estimation: Method and Robustness Analysis with Respect to Different Anatomies, Dose Levels, Tube Voltages, and Data Truncation",
         doi="10.1002/mp.13274"),
    # ---- dynamic / 4D ----------------------------------------------------
    dict(id="sonke-2005", topics=["dynamic", "cbct"], year=2005, venue="Med Phys",
         title="Respiratory Correlated Cone Beam CT",
         doi="10.1118/1.1869074"),
    dict(id="piccs", abbr="PICCS", topics=["dynamic"], year=2008, venue="Med Phys",
         title="Prior Image Constrained Compressed Sensing (PICCS): A Method to Accurately Reconstruct Dynamic CT Images from Highly Undersampled Projection Data Sets",
         doi="10.1118/1.2836423"),
    dict(id="leng-2008", topics=["dynamic", "cbct"], year=2008, venue="PMB",
         title="High Temporal Resolution and Streak-Free Four-Dimensional Cone-Beam Computed Tomography",
         doi="10.1088/0031-9155/53/20/006"),
    dict(id="rit-2009", topics=["dynamic"], year=2009, venue="Med Phys",
         title="On-the-Fly Motion-Compensated Cone-Beam CT Using an A Priori Model of the Respiratory Motion",
         doi="10.1118/1.3115691"),
    dict(id="bergner-2010", topics=["dynamic"], year=2010, venue="Med Phys",
         title="An Investigation of 4D Cone-Beam CT Algorithms for Slowly Rotating Scanners",
         doi="10.1118/1.3480986"),
    dict(id="gao-2012", topics=["dynamic"], year=2012, venue="Med Phys",
         title="4D Cone Beam CT via Spatiotemporal Tensor Framelet",
         doi="10.1118/1.4762288"),
]

FIELDS = ("id", "abbr", "title", "year", "venue", "topics", "paper", "code",
          "project", "data", "note")


def title_key(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def doi_of(s):
    m = re.search(r"10\.\d{4,9}/[^\s\"'<>()\[\],;]+", str(s or ""))
    return m.group(0).lower().rstrip(".") if m else None


def render_block(e):
    L = ['- id: "%s"' % e["id"]]
    if e.get("abbr"):
        L.append('  abbr: "%s"' % e["abbr"])
    L.append('  title: "%s"' % e["title"])
    L.append("  year: %d" % e["year"])
    L.append('  venue: "%s"' % e["venue"])
    L.append("  topics: [%s]" % ", ".join(e["topics"]))
    L.append('  paper: "https://doi.org/%s"' % e["doi"])
    return "\n".join(L) + "\n"


def main():
    write = "--write" in sys.argv
    raw = io.open(PAPERS, encoding="utf-8", newline="").read()
    entries = yaml.safe_load(raw)
    by_id = {e["id"]: e for e in entries}

    problems = []

    # ---- pre-checks: nothing may collide ---------------------------------
    seen_ids = set(by_id)
    seen_dois, seen_titles = set(), set()
    for e in entries:
        d = doi_of(e.get("paper")) or doi_of(e.get("project"))
        if d:
            seen_dois.add(d)
        seen_titles.add(title_key(e["title"]))

    # The repair moves a DOI, so the one it vacates is free for Part 2. Without
    # this the Part 2 entry looks like a collision with the entry being fixed.
    vacated = doi_of(PART1_FIX["expect_paper"])
    seen_dois.discard(vacated)
    if doi_of(PART1_FIX["paper"]) in seen_dois:
        problems.append("Part 1 DOI %s is already used by another entry" % PART1_FIX["paper"])
    seen_dois.add(doi_of(PART1_FIX["paper"]))

    for a in ADDITIONS:
        if a["id"] in seen_ids:
            problems.append("id already present: %s" % a["id"])
        seen_ids.add(a["id"])
        if a["doi"].lower() in seen_dois:
            problems.append("DOI already present: %s (%s)" % (a["doi"], a["id"]))
        seen_dois.add(a["doi"].lower())
        if title_key(a["title"]) in seen_titles:
            problems.append("title already present: %s" % a["title"])
        seen_titles.add(title_key(a["title"]))

    # the pair's DOIs must end up on the right entries
    p1 = by_id.get("scatter-rev")
    if p1 is None:
        problems.append("scatter-rev not found")
    elif p1.get("paper") != PART1_FIX["expect_paper"]:
        problems.append("scatter-rev paper is %r, expected %r"
                        % (p1.get("paper"), PART1_FIX["expect_paper"]))
    if vacated != "10.1118/1.3589140":
        problems.append("scatter-rev should currently point at Part 2 "
                        "(10.1118/1.3589140), but its DOI is %r" % vacated)

    if problems:
        print("PRE-CHECK FAILED")
        for x in problems:
            print("  -", x)
        return 1

    print("pre-checks OK: %d new entries, no id/DOI/title collision" % len(ADDITIONS))
    print("  scatter-rev paper  %s  ->  %s"
          % (PART1_FIX["expect_paper"].split("doi.org/")[-1], PART1_FIX["paper"].split("doi.org/")[-1]))
    print("  total entries      %d  ->  %d" % (len(entries), len(entries) + len(ADDITIONS)))
    new_topics = {}
    for a in ADDITIONS:
        for t in a["topics"]:
            new_topics[t] = new_topics.get(t, 0) + 1
    print("  topic deltas       %s" % ", ".join("+%d %s" % (v, k) for k, v in sorted(new_topics.items())))

    if not write:
        print("\n--- blocks that would be appended ---")
        for a in ADDITIONS:
            print(render_block(a))
        print("(dry run \u2014 pass --write to apply)")
        return 0

    # ---- apply ----------------------------------------------------------
    # 1) repair the Part 1 entry: DOI and the title that goes with it
    blocks = re.split(r"(?m)^(?=- id: )", raw)
    out = []
    fixed = 0
    for blk in blocks:
        m = re.search(r'(?m)^- id: "([^"]+)"', blk)
        if m and m.group(1) == PART1_FIX["id"]:
            before = blk
            blk = re.sub(r"(?m)^  title: .*$",
                         '  title: "%s"' % PART1_FIX["title"], blk, count=1)
            blk = re.sub(r"(?m)^  paper: .*$",
                         '  paper: "%s"' % PART1_FIX["paper"], blk, count=1)
            if blk == before:
                print("!! scatter-rev unchanged - pattern did not match")
                return 1
            fixed += 1
        out.append(blk)
    if fixed != 1:
        print("!! expected to patch exactly 1 block, patched %d" % fixed)
        return 1
    text = "".join(out)
    if not text.endswith("\n"):
        text += "\n"

    # 2) append the new entries
    text += "\n" + "\n".join(render_block(a) for a in ADDITIONS)

    io.open(PAPERS, "w", encoding="utf-8", newline="").write(text)

    # ---- read back and assert -------------------------------------------
    back = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    assert isinstance(back, list), "papers.yaml is not a list"
    assert len(back) == len(entries) + len(ADDITIONS), \
        "count %d -> %d (expected %d)" % (len(entries), len(back), len(entries) + len(ADDITIONS))
    assert [e["id"] for e in back[:len(entries)]] == [e["id"] for e in entries], \
        "existing entries changed order"
    assert [e["id"] for e in back[len(entries):]] == [a["id"] for a in ADDITIONS], \
        "appended entries are not in the expected order"

    fin = {e["id"]: e for e in back}
    for a in ADDITIONS:
        got = fin[a["id"]]
        assert got["title"] == a["title"], a["id"]
        assert got["year"] == a["year"], a["id"]
        assert got.get("venue") == a["venue"], a["id"]
        assert got["topics"] == a["topics"], a["id"]
        assert got["paper"] == "https://doi.org/" + a["doi"], a["id"]
    assert fin["scatter-rev"]["paper"] == PART1_FIX["paper"], "Part 1 DOI not applied"
    assert fin["scatter-rev"]["title"] == PART1_FIX["title"], "Part 1 title not applied"

    # no unicode hyphens or markup leaked in
    for e in back[len(entries):]:
        for f in ("title", "venue"):
            v = e.get(f) or ""
            assert not re.search(r"[\u2010\u2011\u2012]", v), "%s has a unicode hyphen" % e["id"]
            assert "<" not in v, "%s has markup" % e["id"]
    for a in ADDITIONS:
        assert a["venue"] not in ("arXiv", "TechRxiv")

    print("")
    print("wrote %s" % os.path.relpath(PAPERS, ROOT))
    print("read-back OK: %d entries, existing order intact, every field matches, "
          "no unicode hyphens or markup" % len(back))
    return 0


if __name__ == "__main__":
    sys.exit(main())
