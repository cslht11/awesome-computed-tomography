# -*- coding: utf-8 -*-
"""Read every paper DOI back from Crossref and check `year` and `title`.

The year rule (MAINTENANCE.md, "Verify venues by DOI"): a journal article
takes the year of the issue it appears in (`published-print`), or the year
it went online while it has no issue yet; a conference paper, chapter or
monograph takes the year Crossref records for it (`issued`, the conference
or publication year). Preprints (no `venue`) are dated by their first
posting and are not checked here.

The title check catches a DOI that resolves to a different work (an arXiv
link upgraded to a DOI without reading the title back, or a book edition
linked in place of the journal article).

Usage:  python scripts/check_years.py [--strict]

--strict exits 1 on any mismatch; the weekly link-check workflow uses it.
Writes scripts/oneoff/year-report.txt. Standard library only (plus PyYAML
through build.load).
"""
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import load  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "awesome-computed-tomography year check (https://computedtomography.org/)"

# Entries whose DOI deliberately points at a different edition than the
# year they carry.
EXEMPT = {
    "radon-1917": "the DOI is the 1986 English translation of the 1917 paper",
}


def norm(s):
    s = re.sub(r"<[^>]+>|\$", "", str(s or ""))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    return len(wa & wb) / max(len(wa), len(wb)) if wa and wb else 0.0


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)["message"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(3 + 3 * k)
        except Exception:
            time.sleep(3 + 3 * k)
    raise RuntimeError("Crossref unreachable for " + doi)


def year_of(msg, field):
    parts = (msg.get(field) or {}).get("date-parts") or [[None]]
    return parts[0][0] if parts and parts[0] else None


def main():
    rows, bad, skipped = 0, [], []
    for p in load("papers.yaml") or []:
        m = re.match(r"https?://(?:dx\.)?doi\.org/(.+)$", p.get("paper") or "")
        if not m or not p.get("venue") or p["id"] in EXEMPT:
            continue
        doi = urllib.parse.unquote(m.group(1))
        try:
            msg = crossref(doi)
        except RuntimeError as e:
            skipped.append("%s: %s" % (p["id"], e))
            continue
        rows += 1
        if msg is None:
            bad.append("%s: DOI %s is not in Crossref" % (p["id"], doi))
            continue
        if msg.get("type") == "journal-article":
            want = year_of(msg, "published-print") or year_of(msg, "issued")
        else:
            want = year_of(msg, "issued")
        if want and p["year"] != want:
            bad.append("%s: year %s, Crossref says %s (%s)"
                       % (p["id"], p["year"], want, msg.get("type")))
        got = (msg.get("title") or [""])[0]
        if got and similar(p["title"], got) < 0.6:
            bad.append("%s: title differs from the DOI's: %r" % (p["id"], got[:90]))
        time.sleep(0.3)

    out = ["checked %d DOIs; %d problems; %d skipped (Crossref unreachable)"
           % (rows, len(bad), len(skipped))]
    out += ["  " + b for b in bad]
    if skipped:
        out += ["skipped:"] + ["  " + s for s in skipped]
    text = "\n".join(out)
    print(text)
    with io.open(os.path.join(ROOT, "scripts", "oneoff", "year-report.txt"),
                 "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    if bad and "--strict" in sys.argv:
        sys.exit(1)


if __name__ == "__main__":
    main()
