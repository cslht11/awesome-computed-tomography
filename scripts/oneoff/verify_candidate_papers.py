# -*- coding: utf-8 -*-
"""Resolve and verify candidate papers against Crossref then arXiv.

Same two-channel strategy as `build_supp.py` / `verify_supp.py`:
Crossref first (title search), arXiv as a fallback for venues without DOIs
(NeurIPS / ICLR / ICML / TMLR). A candidate is only kept when the returned
title is a close match, so nothing enters the list unverified.

Read-only for `data/`; writes `candidates_papers.json` for review.

Usage:
    python scripts/oneoff/verify_candidate_papers.py [--limit N]
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
OUT = os.path.join(HERE, "candidates_papers.json")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

PREPRINT = ("techrxiv", "researchsquare", "ssrn", "preprints.org", "biorxiv", "medrxiv")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def get(url, tries=4, timeout=35, accept="application/json"):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                return None
            time.sleep(2 + 2 * k)
        except Exception:
            time.sleep(2 + 2 * k)
    return None


def cr_search(title, year):
    q = urllib.parse.quote(title)
    url = ("https://api.crossref.org/works?rows=8&select=DOI,title,type,container-title,"
           "published-print,published-online,issued&query.bibliographic=" + q)
    txt = get(url)
    if not txt:
        return []
    try:
        items = json.loads(txt)["message"]["items"]
    except Exception:
        return []
    out = []
    for it in items:
        ts = it.get("title") or []
        if not ts:
            continue
        s = similar(title, ts[0])
        yr = None
        for k in ("published-print", "published-online", "issued"):
            dp = (it.get(k) or {}).get("date-parts") or []
            if dp and dp[0] and dp[0][0]:
                yr = dp[0][0]
                break
        cont = (it.get("container-title") or [""])[0]
        low = cont.lower()
        pen = 0.15 if any(p in low for p in PREPRINT) else 0.0
        if it.get("type") == "posted-content":
            pen += 0.1
        dy = abs((yr or year) - year)
        out.append({"score": s - pen - 0.02 * min(dy, 5), "sim": s, "doi": it["DOI"],
                    "title": ts[0], "year": yr, "container": cont,
                    "type": it.get("type")})
    out.sort(key=lambda x: -x["score"])
    return out


def _ax_parse(txt, title):
    best, bs = None, 0.0
    for e in re.findall(r"<entry>(.*?)</entry>", txt, re.S):
        ids = re.findall(r"<id>(http://arxiv\.org/abs/[^<]+)</id>", e)
        ts = re.findall(r"<title>([^<]*)</title>", e)
        if not ids or not ts:
            continue
        got = re.sub(r"\s+", " ", ts[0]).strip()
        s = similar(title, got)
        if s > bs:
            bs, best = s, (ids[0].replace("http://", "https://"), got)
    if best and bs >= 0.75:
        return {"url": best[0], "title": best[1], "sim": bs}
    return None


def ax_lookup(title):
    """Phrase search first; fall back to a keyword search for paraphrased titles."""
    url = ("https://export.arxiv.org/api/query?search_query=all:%s&max_results=6"
           % urllib.parse.quote('"%s"' % title))
    txt = get(url, accept="application/atom+xml")
    if txt:
        hit = _ax_parse(txt, title)
        if hit:
            return hit
    # keyword fallback: drop punctuation, search on the longest words
    words = [w for w in norm(title).split() if len(w) > 3][:12]
    if not words:
        return None
    url2 = ("https://export.arxiv.org/api/query?search_query=all:%s&max_results=10"
            % urllib.parse.quote(" AND ".join(words)))
    txt2 = get(url2, accept="application/atom+xml")
    return _ax_parse(txt2, title) if txt2 else None


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    # import the candidate list from diff_existing.py
    sys.path.insert(0, HERE)
    import diff_existing  # noqa: E402
    import io as _io

    lines = _io.open(diff_existing.SRC, encoding="utf-8", errors="replace").read().split("\n")
    have = diff_existing.existing_titles()
    year = None
    cands = []
    for ln in lines:
        h = re.match(r"^###\s+(\d{4})\s*$", ln)
        if h:
            year = int(h.group(1))
            continue
        if not ln.strip().startswith("- "):
            continue
        body = ln.strip()[2:]
        if not re.search(r"\[\[(?:paper|Paper|pdf|PDF|Pdf)\]\((https?://[^)]+)\)\]", body):
            continue
        abbr = re.search(r"\*\*\[([^\]]{1,40})\]\*\*", body)
        title = diff_existing.strip_link(body)
        if {diff_existing.norm(title),
                diff_existing.norm(abbr.group(1) if abbr else "")} & have:
            continue
        cands.append({"abbr": abbr.group(1) if abbr else "",
                      "title": title, "year": year or 0})

    # de-duplicate by normalised title
    seen, uniq = set(), []
    for c in cands:
        k = diff_existing.norm(c["title"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(c)
    if limit:
        uniq = uniq[:limit]

    print("verifying %d candidates\n" % len(uniq))
    rows = []
    for i, c in enumerate(uniq, 1):
        title, year = c["title"], c["year"]
        rec = dict(c)
        cands_cr = cr_search(title, year) if year else []
        pick = None
        for cc in cands_cr:
            if cc["sim"] >= 0.90 and (not year or abs((cc["year"] or year) - year) <= 3):
                pick = cc
                break
        if pick:
            rec.update({"paper": "https://doi.org/" + pick["doi"],
                        "year": pick["year"] or year, "venue": pick["container"],
                        "sim": round(pick["sim"], 2), "via": "crossref"})
        else:
            ax = ax_lookup(title)
            if ax:
                rec.update({"paper": ax["url"], "year": year,
                            "venue": None, "sim": round(ax["sim"], 2),
                            "via": "arxiv"})
            else:
                rec.update({"paper": None, "venue": None, "sim": 0.0, "via": "none"})
        rows.append(rec)
        print("%3d/%d  %-14s %-9s %s" % (i, len(uniq), (rec.get("abbr") or "?")[:14],
                                         (rec.get("via") or "?"), title[:62]))
        time.sleep(0.9)
        if i % 20 == 0:
            io.open(OUT, "w", encoding="utf-8").write(
                json.dumps(rows, ensure_ascii=False, indent=2))

    io.open(OUT, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, indent=2))
    ok = [r for r in rows if r["paper"]]
    print("\nresolved %d/%d -> %s" % (len(ok), len(rows), OUT))
    print("unresolved: %s" % [r["abbr"] or r["title"][:24] for r in rows if not r["paper"]])


if __name__ == "__main__":
    main()
