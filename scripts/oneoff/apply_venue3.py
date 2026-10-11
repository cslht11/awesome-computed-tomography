"""Fill the three venue labels that were verified DOI-by-DOI (Crossref) in
scripts/oneoff/verify_venue3.py, plus the two year corrections that follow from
the verified publication records.

Evidence (scripts/oneoff/venue3-verify.json):
  epi-naf      -> 10.1109/isbi60581.2025.10981301  ISBI 2025     (sim 0.93)
  generative-  -> 10.1109/trpms.2023.3309474        TRPMS 2024    (sim 1.00)
  cocodiff     -> 10.1117/12.2634939                SPIE DXRT 2022(sim 1.00)

Writes via <file>.tmp, re-reads and asserts, then os.replace().
"""
import io
import os
import re
import sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PATH = os.path.join(ROOT, "data", "papers.yaml")
EXPECT_COUNT = 240

# id -> (venue, year or None to keep)
PLAN = {
    "epi-naf": ("ISBI", 2025),
    "generative-modeling-in-sinogram-domain-for-sparse-view-ct-": ("TRPMS", 2024),
    "cocodiff-a-contextual-conditional-diffusion-model-for-low-": ("SPIE DXRT", 2022),
}


def q(s):
    return '"%s"' % str(s).replace('"', '\\"')


def block_span(text, eid):
    """Return (start, end) of the '- id: ...' block for eid."""
    pat = re.compile(r"(?m)^- id: %s[ \t]*$" % re.escape(q(eid)))
    m = pat.search(text)
    if not m:
        # tolerate unquoted id
        pat2 = re.compile(r"(?m)^- id: %s[ \t]*$" % re.escape(eid))
        m = pat2.search(text)
    if not m:
        return None
    nxt = re.compile(r"(?m)^- id: ").search(text, m.end())
    return (m.start(), nxt.start() if nxt else len(text))


def set_scalar(blk, name, value):
    if value is None:
        return blk
    if re.search(r"(?m)^[ \t]*%s: " % name, blk):
        return re.sub(r"(?m)^[ \t]*%s: .*$" % name, "  %s: %s" % (name, value), blk, count=1)
    anchor = re.search(r"(?m)^  (year: .*)$", blk)
    if not anchor:
        raise AssertionError("no anchor for %s" % name)
    return blk[:anchor.end(1)] + "\n  %s: %s" % (name, value) + blk[anchor.end(1):]


def set_venue(blk, value):
    if re.search(r"(?m)^  venue: ", blk):
        return re.sub(r"(?m)^  venue: .*$", "  venue: %s" % q(value), blk, count=1)
    anchor = re.search(r"(?m)^  (year: .*)$", blk)
    if not anchor:
        raise AssertionError("no anchor for venue")
    return blk[:anchor.end(1)] + "\n  venue: %s" % q(value) + blk[anchor.end(1):]


def main():
    text = io.open(PATH, encoding="utf-8").read()
    before = yaml.safe_load(text)
    assert len(before) == EXPECT_COUNT, "expected %d entries, got %d" % (EXPECT_COUNT, len(before))

    out = text
    for eid, (venue, year) in PLAN.items():
        span = block_span(out, eid)
        assert span, "block not found: %s" % eid
        blk = out[span[0]:span[1]]
        new = set_venue(blk, venue)
        new = set_scalar(new, "year", year)
        assert new != blk, "no change applied for %s" % eid
        out = out[:span[0]] + new + out[span[1]:]

    tmp = PATH + ".tmp"
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(out)

    # ---- verify before replacing ----
    after = yaml.safe_load(io.open(tmp, encoding="utf-8").read())
    assert len(after) == EXPECT_COUNT, "count changed: %d" % len(after)
    by = {e["id"]: e for e in after}
    for eid, (venue, year) in PLAN.items():
        e = by[eid]
        assert e.get("venue") == venue, "%s venue=%r want %r" % (eid, e.get("venue"), venue)
        assert e.get("year") == year, "%s year=%r want %r" % (eid, e.get("year"), year)
        print("OK  %-60s %-11s %s" % (eid, venue, year))
    # ids unchanged / unique
    ids = [e["id"] for e in after]
    assert len(set(ids)) == len(ids), "duplicate id after patch"
    assert [e["id"] for e in before] == ids, "entry order changed"
    # no non-target entry changed
    b_by = {e["id"]: e for e in before}
    changed = [eid for eid in ids if b_by[eid] != by[eid]]
    assert set(changed) == set(PLAN), "unexpected changes: %s" % sorted(set(changed) - set(PLAN))

    os.replace(tmp, PATH)
    print("\nwritten: %s" % PATH)
    print("changed entries: %s" % ", ".join(sorted(changed)))


if __name__ == "__main__":
    sys.exit(main())
