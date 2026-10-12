# -*- coding: utf-8 -*-
"""Resolve the CT foundation-model works against Crossref, then arXiv.

Written for the batch harvested from H:/test/pdf-md/2md/AII in one_md — eight
CT foundation-model papers converted from PDF, whose own identifiers are not
reliably present in the markdown (the arXiv ids in those files are mostly
*references*, which is exactly the trap that put a wrong DOI on two earlier
entries).

Same discipline as verify_candidate_papers.py:

  - Crossref first, queried by title; a hit is accepted only when the returned
    title matches at >= 0.90 after normalisation. `query.bibliographic` is not
    used: at low similarity it happily returns a different paper.
  - arXiv as the fallback for venues Crossref does not carry (ICLR / NeurIPS /
    preprint servers), with the same title gate.
  - Nothing is written to data/. Results land in foundation-papers-verify.json
    for a human to read before anything enters the list.

Usage:
    HTTPS_PROXY=http://127.0.0.1:7890 python scripts/oneoff/verify_foundation_papers.py
"""
import io
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "foundation-papers-verify.json")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
THRESH = 0.90
TRIES = 5

# (key, title as printed on the paper, code link found in the markdown)
WORKS = [
    ("tamp", "Imaging foundation model for universal enhancement of non-ideal measurement CT",
     "https://github.com/YutingHe-list/TAMP"),
    ("deepsparse", "DeepSparse: A Foundation Model for Sparse-View CBCT Reconstruction",
     "https://github.com/xmed-lab/DeepSparse"),
    ("dm4ct", "DM4CT: Benchmarking Diffusion Models for Computed Tomography Reconstruction",
     "https://github.com/DM4CT/DM4CT"),
    ("ct-rate", "Generalist foundation models from a multimodal dataset for 3D computed tomography",
     "https://github.com/ibrahimethemhamamci/CT-FM"),
    ("horuseye", "HorusEye: a self-supervised foundation model for generalizable X-ray tomography restoration",
     "https://github.com/Arturia-Pendragon-Iris/HorusEye"),
    ("lctfound", "A lung CT vision foundation model facilitating disease diagnosis and medical imaging",
     ""),
    ("merlin", "Merlin: a computed tomography vision-language foundation model and dataset",
     ""),
    ("tap-ct", "TAP-CT: 3D Task-Agnostic Pretraining of Computed Tomography Foundation Models",
     "https://huggingface.co/fomofo/tap-ct-b-3d"),
]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def fetch(url, timeout=45):
    """GET with retries. This machine drops connections, and an empty body
    looks exactly like a miss -- so retry rather than conclude 'not found'."""
    last = None
    for i in range(TRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:                      # noqa: BLE001
            last = exc
            time.sleep(4)
    raise RuntimeError("could not fetch %s: %s" % (url, last))


def crossref(title):
    url = ("https://api.crossref.org/works?rows=5"
           "&select=DOI,title,container-title,issued,type,URL"
           "&query.title=" + urllib.parse.quote(title))
    items = json.loads(fetch(url))["message"]["items"]
    best = None
    for it in items:
        got = (it.get("title") or [""])[0]
        s = similar(title, got)
        if best is None or s > best["similarity"]:
            best = {
                "source": "crossref",
                "similarity": round(s, 3),
                "title": got,
                "doi": it.get("DOI", ""),
                "container": (it.get("container-title") or [""])[0],
                "type": it.get("type", ""),
                "year": ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0],
            }
    return best


def arxiv(title):
    url = ("http://export.arxiv.org/api/query?search_query=ti:%22"
           + urllib.parse.quote(title) + "%22&max_results=5")
    body = fetch(url)
    entries = re.findall(r"<entry>(.*?)</entry>", body, re.S)
    best = None
    for e in entries:
        got = re.search(r"<title>(.*?)</title>", e, re.S)
        got = re.sub(r"\s+", " ", (got.group(1) if got else "")).strip()
        aid = re.search(r"<id>http://arxiv\.org/abs/([^<]+)</id>", e)
        pub = re.search(r"<published>(\d{4})-\d{2}-\d{2}", e)
        s = similar(title, got)
        if best is None or s > best["similarity"]:
            best = {
                "source": "arxiv",
                "similarity": round(s, 3),
                "title": got,
                "arxiv": aid.group(1) if aid else "",
                "year": int(pub.group(1)) if pub else None,
            }
    return best


def main():
    out = []
    for key, title, code in WORKS:
        print("--- %s" % key, flush=True)
        row = {"key": key, "title": title, "code": code}
        try:
            cr = crossref(title)
        except Exception as exc:                       # noqa: BLE001
            cr = None
            row["crossref_error"] = str(exc)[:200]
        if cr:
            row["crossref"] = cr
            print("    crossref %.3f  %s  %s (%s) %s"
                  % (cr["similarity"], cr["doi"], cr["container"],
                     cr["year"], "ACCEPT" if cr["similarity"] >= THRESH else "reject"),
                  flush=True)
        try:
            ax = arxiv(title)
        except Exception as exc:                       # noqa: BLE001
            ax = None
            row["arxiv_error"] = str(exc)[:200]
        if ax:
            row["arxiv"] = ax
            print("    arxiv    %.3f  %s (%s) %s"
                  % (ax["similarity"], ax.get("arxiv"), ax.get("year"),
                     "ACCEPT" if ax["similarity"] >= THRESH else "reject"),
                  flush=True)
        out.append(row)
        time.sleep(2)

    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(out, indent=2, ensure_ascii=False))
    print("\nwrote %s" % OUT)


if __name__ == "__main__":
    main()
