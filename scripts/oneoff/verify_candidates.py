# -*- coding: utf-8 -*-
"""Verify candidate entries against the live web before they are added.

Read-only: for each candidate URL, record the final HTTP status, the resolved
host and the page title. Nothing is written to data/ by this script.

Usage:
    python scripts/oneoff/verify_candidates.py
"""
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "candidates.json")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# ------------------------------------------------------------------ candidates
# kind: toolkit | learning | dataset | benchmark
TOOLKITS = [
    ("PyLops", "https://github.com/equinor/pylops", ["Python", "operator", "solver"]),
    ("mumott", "https://github.com/mumott/mumott", ["tensor", "tomography", "Python"]),
    ("Ettention", "https://github.com/c3di/ettention", ["C++", "CUDA", "iterative"]),
    ("XrayPhysics", "https://github.com/hoelzer/xrayphysics", ["physics", "spectra", "MATLAB"]),
    ("pyHST2", "https://gitlab.esrf.fr/tomotools/pyhst2", ["synchrotron", "reconstruction"]),
    ("TomoPy (docs)", "https://tomopy.readthedocs.io/en/latest/", ["synchrotron", "docs"]),
]

LEARNING = [
    ("NIST X-Ray Mass Attenuation Coefficients",
     "https://www.nist.gov/pml/x-ray-mass-attenuation-coefficients",
     "tool", "Authoritative tabulation of mu/rho, mu_en/rho and the mass energy-absorption "
             "coefficients every polychromatic simulation needs."),
    ("X-Ray Data Booklet (LBNL)",
     "https://xdb.lbl.gov/",
     "tool", "The standard quick reference for X-ray properties of the elements: absorption "
             "edges, fluorescence yields, scattering cross-sections."),
    ("CT Principles and Algorithms (Zhuang Tiange)",
     "https://www.google.com/search?q=%E5%BA%84%E5%A4%A9%E6%88%88+CT%E5%8E%9F%E7%90%86%E4%B8%8E%E7%AE%97%E6%B3%95",
     "book", "Chinese-language classic on CT principles and algorithms."),
    ("Industrial CT Technology and Principles (Zhang Chaozong)",
     "https://www.google.com/search?q=%E5%BC%A0%E6%9C%9D%E5%AE%97+%E5%B7%A5%E4%B8%9ACT%E6%8A%80%E6%9C%AF%E5%92%8C%E5%8E%9F%E7%90%86",
     "book", "Chinese-language reference devoted to industrial (NDT) CT."),
    ("Medical Tomographic Image Reconstruction Simulation Experiments (Huang Liyu)",
     "https://www.google.com/search?q=%E9%BB%84%E5%8A%9B%E5%AE%87+%E5%8C%BB%E5%AD%A6%E6%96%AD%E5%B1%82%E5%9B%BE%E5%83%8F%E9%87%8D%E5%BB%BA%E4%BB%BF%E7%9C%9F%E5%AE%9E%E9%AA%8C",
     "book", "Chinese-language lab manual for reconstruction simulation."),
    ("Tomography notes (Tom Roelandts)",
     "https://tomroelandts.com/tags/tomography",
     "tutorial", "Short, concrete walkthroughs of the Radon transform and FBP."),
]


def fetch(url, tries=3, timeout=25):
    """Return (status, final_url, title|None, error|None)."""
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                raw = r.read(400000)
                body = raw.decode("utf-8", "replace")
                m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
                title = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
                return r.getcode(), r.geturl(), title, None
        except urllib.error.HTTPError as e:
            return e.code, url, None, "HTTP %s" % e.code
        except Exception as e:
            last = "%s: %s" % (type(e).__name__, e)
            time.sleep(1.5 + k)
    return None, url, None, last


def main():
    rows = []
    total = 0
    for kind, items in (("toolkit", TOOLKITS), ("learning", LEARNING)):
        for it in items:
            total += 1
            name, url = it[0], it[1]
            st, fin, title, err = fetch(url)
            ok = st is not None and (200 <= st < 400 or st in (403, 405, 429))
            rows.append({"kind": kind, "name": name, "url": url, "status": st,
                         "final": fin, "title": title, "error": err, "reachable": ok})
            print("%-6s %-4s %-38s %s" % (kind, st if st else "ERR", name[:38],
                                          (title or err or "")[:58]))
            time.sleep(1.2)
    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=2))
    print("\n%d candidates -> %s" % (total, OUT))
    bad = [r for r in rows if not r["reachable"]]
    print("unreachable: %d %s" % (len(bad), [r["name"] for r in bad]))


if __name__ == "__main__":
    main()
