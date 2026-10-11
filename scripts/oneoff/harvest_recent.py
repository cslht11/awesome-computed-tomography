# -*- coding: utf-8 -*-
"""Harvest recent CT-reconstruction papers from the arXiv API.

Why arXiv and not a web search: the API is authoritative (it *is* the source),
it returns a stable id we can re-verify, and it lets us window by submission
date so we only pick up the 2025-2026 frontier the list was missing.

Read-only for data/; writes recent_candidates.json.

Usage:
    python scripts/oneoff/harvest_recent.py [--from 20250101] [--to 20261231]
"""
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "recent_candidates.json")
UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# Each query is one facet of "CT reconstruction". Kept deliberately narrow so
# we do not drag in general low-level-vision work that merely says "3D".
QUERIES = [
    'abs:"CT reconstruction"',
    'abs:"sparse-view CT"',
    'abs:"sparse view CT"',
    'abs:"limited-angle"',
    'abs:"limited angle tomography"',
    'abs:"low-dose CT"',
    'abs:"cone-beam CT"',
    'abs:"cone beam computed tomography"',
    'abs:"CBCT reconstruction"',
    'abs:"tomographic reconstruction"',
    'abs:"tooth"  AND abs:"CT reconstruction"',
    'abs:"neural attenuation field"',
    'abs:"Gaussian splatting" AND abs:tomography',
    'abs:"Gaussian splatting" AND abs:"X-ray"',
    'abs:"metal artifact" AND abs:CT',
    'abs:"spectral CT" AND abs:reconstruction',
    'abs:"4D CBCT"',
    'abs:"phase-contrast tomography"',
    'abs:"CT" AND abs:"diffusion model" AND abs:reconstruction',
    'abs:"computed tomography" AND abs:"implicit neural representation"',
]

CAT = "(cat:eess.IV OR cat:cs.CV OR cat:physics.med-ph)"


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def fetch(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "application/atom+xml"})
            with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(2 + 2 * k)
    return None


def parse(xml):
    out = []
    if not xml:
        return out
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        aid = re.findall(r"<id>http://arxiv\.org/abs/([^<]+)</id>", e)
        ti = re.findall(r"<title>([^<]*)</title>", e)
        pub = re.findall(r"<published>(\d{4})-(\d{2})-(\d{2})", e)
        summ = re.findall(r"<summary>([^<]*)</summary>", e, re.S)
        cat = re.findall(r'<arxiv:primary_category[^>]*term="([^"]+)"', e)
        # a comment field often carries the venue ("Accepted to MICCAI 2025")
        com = re.findall(r"<arxiv:comment[^>]*>([^<]*)</arxiv:comment>", e)
        if not aid or not ti:
            continue
        out.append({
            "arxiv_id": re.sub(r"v\d+$", "", aid[0]),
            "title": re.sub(r"\s+", " ", ti[0]).strip(),
            "year": int(pub[0][0]) if pub else None,
            "date": "-".join(pub[0]) if pub else None,
            "primary_category": cat[0] if cat else None,
            "comment": re.sub(r"\s+", " ", com[0]).strip() if com else None,
            "abstract": re.sub(r"\s+", " ", summ[0]).strip() if summ else "",
        })
    return out


def main():
    lo = "20250101"
    hi = "20261231"
    if "--from" in sys.argv:
        lo = sys.argv[sys.argv.index("--from") + 1]
    if "--to" in sys.argv:
        hi = sys.argv[sys.argv.index("--to") + 1]

    seen, rows = set(), []
    for q in QUERIES:
        full = "(%s) AND %s AND submittedDate:[%s0000 TO %s2359]" % (q, CAT, lo, hi)
        url = ("https://export.arxiv.org/api/query?search_query=%s"
               "&sortBy=submittedDate&sortOrder=descending&max_results=100"
               % urllib.parse.quote(full))
        items = parse(fetch(url))
        new = 0
        for it in items:
            if it["arxiv_id"] in seen:
                continue
            seen.add(it["arxiv_id"])
            rows.append(it)
            new += 1
        print("%-62s %3d new (total %d)" % (q[:62], new, len(rows)))
        time.sleep(3.2)          # arXiv asks for >= 3s between requests

    rows.sort(key=lambda r: r["date"] or "", reverse=True)
    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=2))
    print("\n%d unique papers -> %s" % (len(rows), OUT))
    from collections import Counter
    print("by year: %s" % dict(sorted(Counter(r["year"] for r in rows).items(), reverse=True)))


if __name__ == "__main__":
    main()
