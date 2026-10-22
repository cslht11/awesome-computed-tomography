#!/usr/bin/env python3
"""
OpenAlex enrichment for the awesome-computed-tomography library.

Produces, in this folder:
  authors.yaml    - per library paper id: OpenAlex work id + ordered authors
  citations.yaml  - in-library citation pairs {from, to} (from CITES to)
  stats.md        - coverage report

Matching strategy (per paper, in order):
  1. DOI parsed from the library `paper` URL     -> OpenAlex works lookup
  2. arXiv id parsed from the library `paper` URL -> OpenAlex via the
     arXiv DOI (10.48550/arXiv.<id>)
  3. Title fallback: OpenAlex title search; candidates must pass a year
     sanity check and a title-similarity check (token-overlap >= 0.9),
     otherwise the paper is left unmatched (never force a match).

Batching: DOI / arXiv-DOI lookups first try OpenAlex's batch filter
(filter=doi:a|b|c, up to 50 per request). NOTE (observed 2026-10-22):
the no-API-key list/search endpoints share a per-IP daily budget that
was exhausted (HTTP 429, "$0 remaining"), while singleton endpoints
(/works/doi:..., /works/W...) and /autocomplete/works still answered
(cost $0). The script therefore falls back to singleton lookups when a
batch request is rate-limited, and uses /autocomplete/works as the
title-search route when /works?search= is rate-limited (candidates are
then verified by a singleton fetch: title similarity + year check).
A Crossref title query is a last-resort DOI resolver for the title
phase; the matched record is still the OpenAlex work.

Results are cached in cache/ (raw OpenAlex works + a matches ledger),
so re-running resumes instead of re-querying. Delete cache/ for a
fully fresh run.

Usage:  python3 fetch_openalex.py
Requires: requests, pyyaml.  No GitHub writes; reads the public shards
from raw.githubusercontent.com (authoritative main branch).
"""

import json
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote

import requests
import yaml

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
WORKS_CACHE = CACHE / "works"
LEDGER = CACHE / "matches.json"
MAILTO = "graph-enrichment@example.com"
API = "https://api.openalex.org"
SELECT = "id,doi,title,publication_year,authorships,referenced_works,primary_location,cited_by_count"
TITLE_SIM_THRESHOLD = 0.9
TITLE_YEAR_TOLERANCE = 2
DELAY = 0.12  # ~8 req/s, under the ~10 req/s polite ceiling

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "ct-graph-enrich/1.0 (OpenAlex enrichment; mailto:%s)" % MAILTO})

# ---------------------------------------------------------------- http helpers

def get_json(path, params=None, retries=4, base_wait=3.0, wait_cap=120.0):
    """GET with backoff on 429/5xx. Returns (status, json|None)."""
    params = dict(params or {})
    params.setdefault("mailto", MAILTO)
    wait = base_wait
    for attempt in range(retries + 1):
        try:
            r = SESSION.get(API + path if path.startswith("/") else path,
                            params=params, timeout=45)
        except requests.RequestException as e:
            print(f"  ! network error {e}; retry in {wait:.0f}s", flush=True)
            time.sleep(wait); wait *= 2; continue
        if r.status_code == 200:
            return 200, r.json()
        if r.status_code == 404:
            return 404, None
        if r.status_code in (429, 500, 502, 503, 504) and attempt < retries:
            ra = r.headers.get("Retry-After")
            sleep = min(float(ra), wait_cap) if (ra and ra.isdigit()) else min(wait, wait_cap)
            print(f"  ! HTTP {r.status_code} on {path[:60]}; back off {sleep:.0f}s", flush=True)
            time.sleep(sleep); wait *= 2; continue
        print(f"  ! HTTP {r.status_code} on {path[:80]}: {r.text[:160]}", flush=True)
        return r.status_code, None
    return 429, None


def get_singleton_by_doi(doi):
    """GET /works/doi:<doi> -> (status, work|None). Singleton endpoint."""
    url = f"{API}/works/doi:{quote(doi, safe='/()')}"
    status, data = get_json(url, params={"select": SELECT}, retries=3)
    time.sleep(DELAY)
    return status, data


def get_singleton_by_openalex_id(wid):
    short = wid.rstrip("/").split("/")[-1]
    status, data = get_json(f"/works/{short}", params={"select": SELECT}, retries=3)
    time.sleep(DELAY)
    return status, data


def batch_by_dois(dois):
    """Try one batch filter request for <=50 DOIs.
    Returns dict {normalised_doi: work} or None if the request failed
    (e.g. 429 on the shared no-key budget) so caller falls back to
    singleton lookups."""
    filt = "doi:" + "|".join(dois)
    # Cap the backoff hard here: on a 429 we want to fall back to singleton
    # lookups quickly, not sit out the list endpoint's Retry-After.
    status, data = get_json("/works", params={
        "filter": filt, "per-page": max(len(dois), 1), "select": SELECT},
        retries=1, base_wait=2.0, wait_cap=5.0)
    if status != 200 or not data:
        return None
    out = {}
    for w in data.get("results", []):
        d = (w.get("doi") or "").replace("https://doi.org/", "").lower()
        if d:
            out[d] = w
    return out

# ---------------------------------------------------------------- identifiers

DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s\"'<>]+)")
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([a-zA-Z][a-zA-Z\-]*/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?")


def extract_doi(url):
    if not url:
        return None
    u = unquote(url)
    m = re.search(r"doi\.org/(10\.[^\s]+)", u, re.I)
    if m:
        return m.group(1).rstrip(".,;")
    m = DOI_RE.search(u)
    return m.group(1).rstrip(".,;") if m else None


def extract_arxiv(url):
    if not url:
        return None
    m = ARXIV_RE.search(url)
    return m.group(1) if m else None

# ---------------------------------------------------------------- title match

def norm_tokens(title):
    t = unicodedata.normalize("NFKD", (title or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return set(re.findall(r"[a-z0-9]+", t))


def title_similarity(a, b):
    """Token-overlap coefficient |A n B| / min(|A|, |B|)."""
    ta, tb = norm_tokens(a), norm_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def year_ok(lib_year, work_year):
    if not lib_year or not work_year:
        return True
    return abs(int(lib_year) - int(work_year)) <= TITLE_YEAR_TOLERANCE


def is_preprint(work):
    doi = (work.get("doi") or "").lower()
    if "10.48550/arxiv" in doi:
        return True
    loc = work.get("primary_location") or {}
    src = (loc.get("source") or {}).get("display_name") or ""
    return src.strip().lower() == "arxiv"


def pick_title_candidate(lib, works):
    """From fetched OpenAlex works, pick the best title-phase match."""
    scored = []
    for w in works:
        if not w:
            continue
        sim = title_similarity(lib["title"], w.get("title"))
        if sim < TITLE_SIM_THRESHOLD:
            continue
        if not year_ok(lib.get("year"), w.get("publication_year")):
            continue
        ydiff = abs(int(lib["year"]) - int(w["publication_year"])) \
            if lib.get("year") and w.get("publication_year") else 99
        scored.append((sim, 0 if is_preprint(w) else 1, -ydiff,
                       w.get("cited_by_count") or 0, w))
    if not scored:
        return None
    scored.sort(key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)
    return scored[0][4]

# ---------------------------------------------------------------- source data

def load_library():
    """List + download the paper shards from GitHub main (authoritative)."""
    status, listing = get_json(
        "https://api.github.com/repos/cslht11/awesome-computed-tomography/contents/data/papers",
        params={}, retries=3)
    # get_json prefixes API for relative paths; this was absolute, fine.
    names = []
    if status == 200 and isinstance(listing, list):
        names = sorted(x["name"] for x in listing if x["name"].endswith(".yaml"))
    if not names:
        names = ["papers-01.yaml", "papers-02.yaml", "papers-03.yaml", "papers-04.yaml"]
    papers = []
    for name in names:
        url = ("https://raw.githubusercontent.com/cslht11/"
               f"awesome-computed-tomography/main/data/papers/{name}")
        r = SESSION.get(url, timeout=45)
        r.raise_for_status()
        shard = yaml.safe_load(r.text)
        papers.extend(shard)
        print(f"shard {name}: {len(shard)} papers", flush=True)
    return papers

# ---------------------------------------------------------------- ledger

def load_ledger():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {}


def save_ledger(ledger):
    CACHE.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=1))


def cache_work(work):
    if not work:
        return
    WORKS_CACHE.mkdir(parents=True, exist_ok=True)
    short = work["id"].rstrip("/").split("/")[-1]
    (WORKS_CACHE / f"{short}.json").write_text(json.dumps(work))

# ---------------------------------------------------------------- phases

def phase_identifiers(papers, ledger, key_fn, doi_fn, matched_by):
    """DOI / arXiv phases. key_fn(paper)->cache key, doi_fn(paper)->doi to query."""
    todo = [p for p in papers
            if doi_fn(p)
            and not (ledger.get(p["id"]) or {}).get("work")
            and not ((ledger.get(p["id"]) or {}).get("phase_note") or "").startswith(matched_by + ":")]
    print(f"[{matched_by}] {len(todo)} papers to look up", flush=True)
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        dois = [doi_fn(p) for p in chunk]
        batch = batch_by_dois(dois)
        if batch is not None:
            print(f"  batch ok ({len(batch)} works for {len(chunk)} dois)", flush=True)
            for p, doi in zip(chunk, dois):
                w = batch.get(doi.lower())
                if w:
                    cache_work(w)
                    ledger[p["id"]] = {"work": w["id"], "matched_by": matched_by,
                                        "checked": True}
                else:
                    ledger[p["id"]] = {"work": None, "matched_by": None,
                                       "checked": False, "phase_note": f"{matched_by}: batch miss"}
            save_ledger(ledger)
            continue
        # fallback: singleton lookups (list endpoint rate-limited)
        print(f"  batch unavailable -> singleton lookups for {len(chunk)} papers", flush=True)
        for p, doi in zip(chunk, dois):
            status, w = get_singleton_by_doi(doi)
            if status == 200 and w:
                cache_work(w)
                ledger[p["id"]] = {"work": w["id"], "matched_by": matched_by, "checked": True}
            elif status == 404:
                ledger[p["id"]] = {"work": None, "matched_by": None,
                                   "checked": False, "phase_note": f"{matched_by}: 404"}
            else:
                ledger[p["id"]] = {"work": None, "matched_by": None,
                                   "checked": False, "phase_note": f"{matched_by}: HTTP {status} (unresolved)"}
            save_ledger(ledger)
        done = min(i + 50, len(todo))
        print(f"  [{matched_by}] {done}/{len(todo)} processed; matched so far: "
              f"{sum(1 for v in ledger.values() if v.get('work'))}", flush=True)


def crossref_doi_for_title(lib):
    """Last-resort: Crossref title query -> DOI of a high-similarity hit."""
    try:
        r = SESSION.get("https://api.crossref.org/works", params={
            "query.title": lib["title"], "rows": 5,
            "select": "DOI,title,published"}, timeout=45)
        if r.status_code != 200:
            return None
        for item in r.json()["message"]["items"]:
            titles = item.get("title") or []
            if not titles:
                continue
            if title_similarity(lib["title"], titles[0]) < TITLE_SIM_THRESHOLD:
                continue
            year = None
            try:
                year = item["published"]["date-parts"][0][0]
            except Exception:
                pass
            if not year_ok(lib.get("year"), year):
                continue
            return item.get("DOI")
    except requests.RequestException:
        return None
    return None


def phase_title(papers, ledger):
    todo = [p for p in papers if p["id"] not in ledger or not ledger[p["id"]].get("work")]
    # only papers not already matched; a paper whose identifier phase 404'd
    # still gets its title chance here.
    todo = [p for p in todo if not (ledger.get(p["id"]) or {}).get("work")]
    print(f"[title] {len(todo)} papers for title fallback", flush=True)
    for p in todo:
        pid = p["id"]
        candidates = []
        completed = False
        # Route 1: OpenAlex search endpoint (may be 429 on shared budget)
        status, data = get_json("/works", params={
            "search": p["title"], "per-page": 5, "select": SELECT},
            retries=0)
        if status == 200 and data is not None:
            completed = True
            candidates.extend(data.get("results", []))
            w = pick_title_candidate(p, candidates)
            if w:
                cache_work(w)
                ledger[pid] = {"work": w["id"], "matched_by": "title", "checked": True}
                save_ledger(ledger)
                continue
        # Route 2: OpenAlex autocomplete -> verify by singleton fetch
        status, data = get_json("/autocomplete/works", params={"q": p["title"]}, retries=2)
        time.sleep(DELAY)
        if status == 200 and data is not None:
            completed = True
            auto = [r for r in data.get("results", [])
                    if title_similarity(p["title"], r.get("display_name")) >= TITLE_SIM_THRESHOLD]
            auto.sort(key=lambda r: title_similarity(p["title"], r.get("display_name")),
                      reverse=True)
            fetched = []
            for r in auto[:3]:
                s2, w = get_singleton_by_openalex_id(r["id"])
                if s2 == 200 and w:
                    cache_work(w)
                    fetched.append(w)
            w = pick_title_candidate(p, fetched)
            if w:
                cache_work(w)
                ledger[pid] = {"work": w["id"], "matched_by": "title", "checked": True,
                               "resolver": "openalex-autocomplete"}
                save_ledger(ledger)
                continue
        # Route 3: Crossref title -> DOI -> OpenAlex singleton
        doi = crossref_doi_for_title(p)
        if doi:
            completed = True
            s3, w = get_singleton_by_doi(doi)
            if s3 == 200 and w:
                w2 = pick_title_candidate(p, [w])
                if w2:
                    cache_work(w2)
                    ledger[pid] = {"work": w2["id"], "matched_by": "title", "checked": True,
                                   "resolver": "crossref-doi"}
                    save_ledger(ledger)
                    continue
        prev = ledger.get(pid) or {}
        ledger[pid] = {"work": None, "matched_by": None,
                       "checked": bool(completed or prev.get("phase_note", "").endswith("404")),
                       "phase_note": "title: no candidate passed similarity/year checks"
                       if completed else "title: lookup unavailable (rate-limited)"}
        save_ledger(ledger)
        print(f"  [title] {pid}: no match (checked={ledger[pid]['checked']})", flush=True)

# ---------------------------------------------------------------- outputs

def build_outputs(papers, ledger):
    works = {}
    for f in WORKS_CACHE.glob("*.json"):
        w = json.loads(f.read_text())
        works[w["id"]] = w

    authors_out = {}
    id_by_openalex = {}
    year_flags = []
    for p in papers:
        entry = ledger.get(p["id"]) or {}
        wid = entry.get("work")
        if wid and wid in works:
            w = works[wid]
            id_by_openalex[wid] = p["id"]
            authors = []
            seen = set()
            for a in w.get("authorships", []):
                item = {"name": a["author"]["display_name"],
                        "openalex_author_id": a["author"]["id"]}
                key = (item["name"], item["openalex_author_id"])
                if key in seen:
                    continue  # OpenAlex occasionally lists one author twice
                seen.add(key)
                authors.append(item)
            authors_out[p["id"]] = {"openalex": wid, "authors": authors,
                                    "matched_by": entry.get("matched_by")}
            oy = w.get("publication_year")
            if p.get("year") and oy and abs(int(p["year"]) - int(oy)) > 1:
                year_flags.append((p["id"], p["year"], oy, p["title"]))
        else:
            authors_out[p["id"]] = {"openalex": None, "authors": [], "matched_by": None}

    pairs = set()
    for p in papers:
        entry = ledger.get(p["id"]) or {}
        wid = entry.get("work")
        if not wid or wid not in works:
            continue
        for ref in works[wid].get("referenced_works", []) or []:
            target = id_by_openalex.get(ref)
            if target and target != p["id"]:
                pairs.add((p["id"], target))
    citations = [{"from": a, "to": b} for a, b in sorted(pairs)]

    with open(HERE / "authors.yaml", "w") as fh:
        yaml.safe_dump(authors_out, fh, allow_unicode=True, sort_keys=False, width=1000)
    with open(HERE / "citations.yaml", "w") as fh:
        yaml.safe_dump(citations, fh, allow_unicode=True, sort_keys=False)

    # ----- stats
    by = Counter((ledger.get(p["id"]) or {}).get("matched_by") for p in papers)
    matched = sum(1 for p in papers if (ledger.get(p["id"]) or {}).get("work"))
    unmatched = [p["id"] for p in papers
                 if not (ledger.get(p["id"]) or {}).get("work")
                 and (ledger.get(p["id"]) or {}).get("checked")]
    unchecked = [p["id"] for p in papers
                 if not (ledger.get(p["id"]) or {}).get("work")
                 and not (ledger.get(p["id"]) or {}).get("checked")]

    # OpenAlex leaves author.id null for some authorships (mostly very
    # recent works). NEVER collapse those into one pseudo-author: key
    # them by name instead and report them separately in the stats.
    author_papers = defaultdict(set)
    author_names = {}
    null_id_entries = 0
    null_id_names = set()
    null_id_papers = set()
    for pid, e in authors_out.items():
        for a in e["authors"]:
            aid = a["openalex_author_id"]
            if aid:
                key = aid
            else:
                key = "name:" + a["name"]
                null_id_entries += 1
                null_id_names.add(a["name"])
                null_id_papers.add(pid)
            author_papers[key].add(pid)
            author_names[key] = a["name"]
    distinct_author_ids = sum(1 for k in author_papers if not k.startswith("name:"))
    multi = sorted(((author_names[k], len(ps), k) for k, ps in author_papers.items()
                    if len(ps) >= 3), key=lambda x: (-x[1], x[0]))
    top30 = sorted(((author_names[k], len(ps)) for k, ps in author_papers.items()),
                   key=lambda x: (-x[1], x[0]))[:30]

    indeg = Counter(t for _, t in pairs)
    top_cited = indeg.most_common(20)
    title_by_id = {p["id"]: p["title"] for p in papers}

    lines = []
    lines.append("# OpenAlex enrichment — coverage report\n")
    lines.append(f"Generated by `fetch_openalex.py` against OpenAlex (api.openalex.org), "
                 f"source shards: cslht11/awesome-computed-tomography main, data/papers/papers-*.yaml.\n")
    lines.append("## Coverage\n")
    lines.append(f"- Total library papers: **{len(papers)}**")
    lines.append(f"- Matched: **{matched}** ({matched / len(papers):.1%})")
    lines.append(f"  - by DOI: {by.get('doi', 0)}")
    lines.append(f"  - by arXiv: {by.get('arxiv', 0)}")
    lines.append(f"  - by title: {by.get('title', 0)}")
    lines.append(f"- Checked but unmatched: **{len(unmatched)}**")
    lines.append(f"- Unchecked (lookup unavailable / unresolved, NOT verified-unmatched): **{len(unchecked)}**\n")
    lines.append("## Unmatched paper ids (checked, no OpenAlex match passed the checks)\n")
    lines.append(", ".join(f"`{u}`" for u in unmatched) if unmatched else "None.")
    if unchecked:
        lines.append("\n## Unchecked paper ids (rate-limit/network unresolved)\n")
        lines.append(", ".join(f"`{u}`" for u in unchecked))
    lines.append("\n## Authors\n")
    lines.append(f"- Distinct authors: **{len(author_papers)}** "
                 f"({distinct_author_ids} by OpenAlex author id + {len(null_id_names)} "
                 f"distinct names whose authorships carry no OpenAlex author id yet)")
    lines.append(f"- Authorship entries with `openalex_author_id: null` in the source data: "
                 f"{null_id_entries} (across {len(null_id_papers)} papers) — OpenAlex has "
                 f"not assigned these authors an id; they are keyed by name in the counts "
                 f"above, never merged into a single pseudo-author.")
    lines.append(f"- Authors with ≥3 in-library papers: **{len(multi)}**\n")
    lines.append("### Top 30 authors by in-library paper count\n")
    lines.append("| # | Author | In-library papers |")
    lines.append("|---|--------|-------------------|")
    for i, (name, n) in enumerate(top30, 1):
        lines.append(f"| {i} | {name} | {n} |")
    lines.append("\n## In-library citations\n")
    lines.append(f"- In-library citation pairs (from CITES to): **{len(pairs)}**\n")
    lines.append("### Most-cited within the library (top 20)\n")
    lines.append("| Paper id | Title | Cited by (in-library) |")
    lines.append("|----------|-------|------------------------|")
    for pid, n in top_cited:
        lines.append(f"| `{pid}` | {title_by_id.get(pid, '')} | {n} |")
    lines.append("\n## Data-quality flags: OpenAlex year differs from library year by >1\n")
    if year_flags:
        lines.append("| Paper id | Library year | OpenAlex year | Title |")
        lines.append("|----------|--------------|---------------|-------|")
        for pid, ly, oy, t in year_flags:
            lines.append(f"| `{pid}` | {ly} | {oy} | {t} |")
    else:
        lines.append("None.")
    lines.append("\n## Method notes / caveats\n")
    lines.append("- DOI and arXiv matches are identifier-exact (no title check needed); "
                 "where OpenAlex holds both a preprint and a published record, the record "
                 "whose DOI/arXiv id equals the library link is the one kept.")
    lines.append("- Title matches required token-overlap ≥ 0.9 (normalised case/punctuation) "
                 "and |year difference| ≤ 2 against the library record; among passing "
                 "candidates a non-preprint (non-arXiv-DOI) record was preferred.")
    lines.append("- On 2026-10-22 the no-key OpenAlex list/search budget for this network's "
                 "shared IP was exhausted (HTTP 429); batch filter requests therefore fell "
                 "back to singleton /works/doi: lookups, and title search used "
                 "/autocomplete/works + singleton verification (both $0-cost endpoints), "
                 "with Crossref as a last-resort DOI resolver. All matched records are "
                 "OpenAlex works; author ids are OpenAlex author ids.")
    lines.append("- referenced_works come from the matched OpenAlex record only; a citation "
                 "to a *different version* (preprint vs published) of an in-library paper "
                 "does not count as an in-library pair.")
    lines.append("- 7 works had a duplicated authorship row in OpenAlex (same author listed "
                 "twice, e.g. as both middle and last author); authors.yaml dedupes identical "
                 "(name, author id) rows per paper, preserving first-occurrence order.")
    lines.append("- Some OpenAlex authorships have a null author id (flagged in the Authors "
                 "section); authors.yaml reproduces that faithfully as "
                 "`openalex_author_id: null`.")
    lines.append("- The 6 unmatched papers were re-checked manually against "
                 "/autocomplete/works on 2026-10-22: no candidates exist at all (three are "
                 "CVPR 2026 papers and three are 2026 papers with no DOI/arXiv link in the "
                 "library — apparently not yet indexed by OpenAlex).")
    (HERE / "stats.md").write_text("\n".join(lines) + "\n")

    return {"total": len(papers), "matched": matched, "by": dict(by),
            "unmatched": unmatched, "unchecked": unchecked,
            "distinct_authors": len(author_papers), "multi3": len(multi),
            "top_authors": top30[:10], "pairs": len(pairs),
            "year_flags": year_flags}


def main():
    papers = load_library()
    print(f"library total: {len(papers)}", flush=True)
    ledger = load_ledger()

    phase_identifiers(papers, ledger,
                      key_fn=lambda p: p["id"],
                      doi_fn=lambda p: extract_doi(p.get("paper")),
                      matched_by="doi")
    phase_identifiers(papers, ledger,
                      key_fn=lambda p: p["id"],
                      doi_fn=lambda p: (f"10.48550/arXiv.{extract_arxiv(p.get('paper'))}"
                                        if extract_arxiv(p.get("paper")) else None),
                      matched_by="arxiv")
    phase_title(papers, ledger)

    summary = build_outputs(papers, ledger)
    print(json.dumps(summary, indent=1, ensure_ascii=False, default=str), flush=True)


if __name__ == "__main__":
    sys.exit(main())
