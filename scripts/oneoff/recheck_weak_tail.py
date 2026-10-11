"""Re-fetch arXiv metadata for the 11 pre-2025 entries that still have no venue
and no code, and report any <arxiv:journal_ref> / <arxiv:doi> the arXiv record
now carries. Pairing is done by <id>, never by position in the response.
"""
import io
import json
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = [
    "2412.03036", "2401.16039", "1910.05375", "2209.15136", "1801.09533",
    "2202.10847", "2211.07804", "2211.17048", "2012.04743", "2009.01782",
    "2008.02839",
]
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
UA = "ct-awesome venue check (mailto:noreply@example.com)"


def fetch(ids):
    url = ("http://export.arxiv.org/api/query?id_list=%s&max_results=%d"
           % (",".join(ids), len(ids)))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    raw = urllib.request.urlopen(req, timeout=60).read()
    root = ET.fromstring(raw)
    out = {}
    for e in root.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[-1]
        aid = re.sub(r"v\d+$", "", aid)
        jr = e.find("arxiv:journal_ref", NS)
        doi = e.find("arxiv:doi", NS)
        out[aid] = {
            "title": re.sub(r"\s+", " ", e.find("a:title", NS).text).strip(),
            "published": (e.find("a:published", NS).text or "")[:10],
            "journal_ref": (jr.text.strip() if jr is not None and jr.text else ""),
            "doi": (doi.text.strip() if doi is not None and doi.text else ""),
        }
    return out


def main():
    got = fetch(IDS)
    print("requested %d, resolved %d" % (len(IDS), len(got)))
    missing = [i for i in IDS if i not in got]
    if missing:
        print("MISSING:", missing)
    rows = []
    for aid in IDS:
        r = got.get(aid)
        if not r:
            continue
        print("\n%-12s %s" % (aid, r["title"][:78]))
        print("   published=%s  journal_ref=%r  doi=%r"
              % (r["published"], r["journal_ref"], r["doi"]))
        rows.append(dict(arxiv_id=aid, **r))
    io.open(os.path.join(HERE, "weak-tail-arxiv.json"), "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=2))
    n = sum(1 for r in rows if r["journal_ref"] or r["doi"])
    print("\n%d of %d now carry a journal_ref or doi" % (n, len(rows)))
    time.sleep(3)


if __name__ == "__main__":
    main()
