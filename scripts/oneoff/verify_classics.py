# -*- coding: utf-8 -*-
"""Verify candidate *classic* papers before adding them to the list.

The three thinnest sections (spectral 6 entries, scatter 6, dynamic 9) are thin
mostly because they are missing the works the field is built on, not because
nothing exists. This script takes a hand-written candidate list and resolves
each one against Crossref, so every venue/year/DOI written into `data/*.yaml`
comes from the authoritative record rather than from memory.

Method, and why:

  - `query.title` with the FULL title, not `query.bibliographic`. The loose
    bibliographic query returns a plausible-looking *different* paper at low
    similarity (it once "matched" a limited-view entry to an unrelated TMI
    paper). Only a hit whose title matches after normalisation is accepted.
  - Threshold 0.90 on a token-set Jaccard. Below that the hit is reported but
    rejected; a human then reads the abstract page.
  - Every accepted DOI is fetched back a second time as `works/<doi>` and its
    title re-compared. A DOI that resolves to a different title is dropped --
    this is the check that catches a wrong id, and it is cheap.

Output: `classics-verify.json`, plus a printable accept/reject table.

Nothing here writes to `data/`. Adding the accepted entries is a separate,
reviewable step.
"""
import io
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "ct-awesome classics check (mailto:noreply@example.com)"
THRESH = 0.90

# key -> the work, with the topics it would carry. Titles are written as the
# paper's own title; the script reports the authoritative spelling.
CANDIDATES = [
    # ---- spectral / dual-energy -------------------------------------------
    dict(key="alvarez1976", topics=["spectral"],
         title="Energy-selective reconstructions in X-ray computerised tomography"),
    dict(key="elbakri2002", topics=["spectral"],
         title="Statistical image reconstruction for polyenergetic X-ray computed tomography"),
    dict(key="deman2001", topics=["spectral"],
         title="An iterative maximum-likelihood polychromatic algorithm for CT"),
    dict(key="roessl2007", topics=["spectral"],
         title="K-edge imaging in x-ray computed tomography using multi-bin photon counting detectors"),
    dict(key="schlomka2008", topics=["spectral"],
         title="Experimental feasibility of multi-energy photon-counting K-edge imaging in pre-clinical computed tomography"),
    dict(key="mccollough2015", topics=["spectral"],
         title="Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications"),
    # ---- scatter ----------------------------------------------------------
    dict(key="siewerdsen2001", topics=["scatter", "cbct"],
         title="Cone-beam computed tomography with a flat-panel imager: magnitude and effects of x-ray scatter"),
    dict(key="zbijewski2006", topics=["scatter"],
         title="Efficient Monte Carlo based scatter artifact reduction in cone-beam micro-CT"),
    dict(key="zhu2006", topics=["scatter"],
         title="Scatter correction method for X-ray CT using primary modulation: theory and preliminary results"),
    dict(key="ruhrnschopf2011b", topics=["scatter"],
         title="A general framework and review of scatter correction methods in x-ray cone-beam computerized tomography. Part 2: Scatter artifact correction approaches"),
    dict(key="maier2019", topics=["scatter"],
         title="Real-time scatter estimation for medical CT using the deep scatter estimation: method and robustness analysis with respect to different anatomies, dose levels, tube voltages, and data truncation"),
    # ---- dynamic / 4D -----------------------------------------------------
    dict(key="sonke2005", topics=["dynamic", "cbct"],
         title="Respiratory correlated cone beam CT"),
    dict(key="chen2008piccs", topics=["dynamic"],
         title="Prior image constrained compressed sensing (PICCS): a method to accurately reconstruct dynamic CT images from highly undersampled projection data sets"),
    dict(key="leng2008", topics=["dynamic", "cbct"],
         title="High temporal resolution and streak-free four-dimensional cone-beam computed tomography"),
    dict(key="rit2009", topics=["dynamic"],
         title="On-the-fly motion-compensated cone-beam CT using an a priori model of the motion"),
    dict(key="gao2013", topics=["dynamic"],
         title="Four-dimensional cone beam CT via spatiotemporal tensor framelet"),
    dict(key="bergner2009", topics=["dynamic"],
         title="An investigation of 4D cone-beam CT algorithms for slowly rotating scanners"),
    dict(key="lixing2007", topics=["dynamic"],
         title="Optimizing 4D cone-beam CT acquisition protocol for external beam radiotherapy"),
]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def sim(a, b):
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


def search(title, rows=5):
    url = ("https://api.crossref.org/works?rows=%d"
           "&select=DOI,title,container-title,issued,type,author"
           "&query.title=" % rows) + urllib.parse.quote(title)
    return get(url)["message"]["items"]


def by_doi(doi):
    return get("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]


def year_of(msg):
    parts = (msg.get("issued") or {}).get("date-parts") or [[None]]
    return parts[0][0] if parts and parts[0] else None


def main():
    out = []
    for c in CANDIDATES:
        title = c["title"]
        rec = dict(key=c["key"], topics=c["topics"], local_title=title)
        try:
            items = search(title)
        except Exception as ex:  # noqa: BLE001
            print("!! %-16s search failed: %s" % (c["key"], ex))
            rec["error"] = str(ex)
            out.append(rec)
            time.sleep(2)
            continue

        best = None
        for it in items:
            t = (it.get("title") or [""])[0]
            s = sim(title, t)
            if best is None or s > best[0]:
                best = (s, t, it.get("DOI"), year_of(it),
                        (it.get("container-title") or [""])[0], it.get("type"))
        rec["search_best"] = (dict(sim=round(best[0], 3), title=best[1], doi=best[2],
                                  year=best[3], container=best[4], type=best[5])
                              if best else None)

        status = "reject"
        if best and best[0] >= THRESH:
            # second pass: read the DOI back and re-check the title
            try:
                m = by_doi(best[2])
                t2 = (m.get("title") or [""])[0]
                s2 = sim(title, t2)
                rec["doi_readback"] = dict(sim=round(s2, 3), title=t2, doi=best[2],
                                           year=year_of(m),
                                           container=(m.get("container-title") or [""])[0],
                                           type=m.get("type"))
                if s2 >= THRESH:
                    status = "ACCEPT"
                else:
                    status = "doi-mismatch"
            except Exception as ex:  # noqa: BLE001
                rec["doi_readback"] = {"error": str(ex)}
                status = "readback-failed"
            time.sleep(1.0)

        rec["status"] = status
        out.append(rec)

        print("%-8s %-16s" % (status, c["key"]))
        print("    local : %s" % title[:92])
        if rec.get("search_best"):
            b = rec["search_best"]
            print("    xref  : %.2f  %s" % (b["sim"], b["doi"]))
            print("            %s" % b["title"][:88])
            print("            %s | %s | %s" % (b["container"][:38], b["year"], b["type"]))
        if rec.get("doi_readback") and "sim" in rec["doi_readback"]:
            d = rec["doi_readback"]
            print("    readbk: %.2f  %s | %s" % (d["sim"], d["container"][:38], d["year"]))
        print()
        time.sleep(1.2)

    io.open(os.path.join(HERE, "classics-verify.json"), "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2))

    acc = [r for r in out if r.get("status") == "ACCEPT"]
    print("=" * 78)
    print("ACCEPTED %d / %d" % (len(acc), len(out)))
    print("=" * 78)
    for r in acc:
        d = r["doi_readback"]
        print("  %-16s %-9s %-34s %s" % (r["key"], d["year"], d["container"][:34], d["doi"]))
    bad = [r for r in out if r.get("status") != "ACCEPT"]
    if bad:
        print("\nNOT ACCEPTED:")
        for r in bad:
            print("  %-16s %s" % (r["key"], r.get("status")))


if __name__ == "__main__":
    main()
