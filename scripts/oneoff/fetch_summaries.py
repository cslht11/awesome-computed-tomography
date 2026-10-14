"""One-off: fetch a short "what is this paper" blurb for every paper.

Why this exists
---------------
The site shows a paper's title as a link to the same URL as the `paper` link
next to it — clicking either goes to the same place. We want the title to stop
being a link and to explain itself on hover instead, so readers can tell what a
work is about without leaving the page.

How it works
------------
1. Read `data/papers.yaml`, pull an arXiv id or a DOI out of each entry's links.
2. Ask arXiv (batched, `id_list`) or Crossref (one DOI at a time) for the
   abstract. Both are polite, rate-limited public APIs: **arXiv asks for ~3 s
   between calls, Crossref rewards a `mailto` and ~1 s spacing.** Every request
   here goes through `sleep()` first, and failures are recorded rather than
   retried in a tight loop — a 429 or a timeout means back off, not hammer.
3. Reduce the abstract to a couple of sentences (~320 chars) with
   `condense()`, which keeps *verbatim sentences* — it never paraphrases, so a
   blurb can mislead by omission but never by invention.
4. Write `data/summaries.yaml` (id -> blurb) plus a raw cache under
   `local/` so a re-run does not re-hit the APIs.

Nothing here touches `data/papers.yaml`; summaries live in their own file so
they can be regenerated, hand-edited or pruned without touching the list.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
OUT = os.path.join(ROOT, "data", "summaries.yaml")
CACHE = os.path.join(ROOT, "..", "local", "summaries_raw.json")

ARXIV = "https://export.arxiv.org/api/query"
CROSSREF = "https://api.crossref.org/works/"
MAILTO = "heitieya@163.com"          # Crossref polite pool
ARXIV_GAP = 3.1                      # arXiv's own guidance: 3 s between calls
CROSSREF_GAP = 1.2
BATCH = 40                           # arXiv ids per request
MAX_CHARS = 320

UA = "awesome-computed-tomography/1.0 (summary fetcher; +https://computedtomography.org/)"

# Sentences that state what the paper actually contributes — these are the ones
# worth keeping when we have to drop most of the abstract.
CONTRIB = re.compile(
    r"\b(we (propose|present|introduce|develop|design|describe|formulate)"
    r"|this (paper|work) (proposes|presents|introduces)|we (show|demonstrate)"
    r"|our (method|approach|results?))\b", re.I)
RESULT = re.compile(r"\b(results?|experiments?|demonstrat|outperform|"
                    r"state of the art|sota|improv)\w*\b", re.I)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
ARXIV_ID = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})")
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+")
TAG = re.compile(r"<[^>]+>")


def log(msg):
    print(msg, flush=True)


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    proxies = urllib.request.getproxies()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s):
    return " ".join(TAG.sub(" ", s).split())


# Crossref returns JATS XML flattened to text, which leaves the section label
# welded to the front of the first sentence: "Purpose Computed tomography …",
# "Abstract In the real applications …". Strip those, repeatedly — some
# abstracts stack two of them.
LEADING_LABEL = re.compile(
    r"^\s*(abstract|summary|purpose|objectives?|background|introduction|"
    r"methods?|results?|conclusions?)\s*[:.\u2013\u2014-]?\s*", re.I)


def clean(text):
    s = " ".join(str(text or "").split())
    prev = None
    while prev != s:
        prev = s
        s = LEADING_LABEL.sub("", s)
    # JATS is full of typographic dashes; fold them to ASCII so "sparse‐view"
    # reads and searches as "sparse-view".
    return re.sub("[\u2010\u2011\u2012\u2013\u2014]", "-", s)


def condense(text, limit=MAX_CHARS):
    """Keep the most informative whole sentences, verbatim, under `limit`.

    Order of preference: a contribution sentence ("we propose …"), then the
    opening sentence for context, then a result sentence. Everything kept is a
    complete sentence from the source, so nothing is fabricated.
    """
    s = clean(text)
    if not s:
        return ""
    if len(s) <= limit:
        return s
    # JATS labels also start *later* sentences — a flattened abstract reads
    # "… Abstract Background In recent years … Purpose Deep learning …" — so
    # they are stripped per sentence, not only at the head of the string.
    sents = [LEADING_LABEL.sub("", x.strip())
             for x in SENT_SPLIT.split(s) if x.strip()]
    picked, used = [], 0
    for want in (CONTRIB, None, RESULT):
        for i, st in enumerate(sents):
            if i in picked:
                continue
            if want is not None and not want.search(st):
                continue
            if used + len(st) > limit:
                continue
            picked.append(i)
            used += len(st) + 1
        if used >= limit * 0.6:
            break
    if not picked:                      # nothing matched: just keep the opening
        picked, used = [], 0
        for i, st in enumerate(sents):
            if used + len(st) > limit:
                break
            picked.append(i)
            used += len(st) + 1
    out = " ".join(sents[i] for i in sorted(picked))
    return out[:limit].rsplit(" ", 1)[0] + "\u2026" if len(out) > limit else out


def read_papers():
    with open(PAPERS, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data if isinstance(data, list) else data.get("papers", [])
    out = []
    for p in papers:
        links = " ".join(str(p.get(k) or "") for k in ("paper", "project", "code"))
        m = ARXIV_ID.search(links)
        doi = None
        # NB: a regex, not `u.split("10.")` — splitting on the literal eats the
        # "10." prefix and turns 10.1038/xxx into 1038/xxx, which Crossref
        # answers 404 for, silently, for every single entry.
        d = DOI_RE.search(links)
        if d:
            doi = d.group(0).rstrip(".,)")
        out.append({"id": p.get("id"), "arxiv": m.group(1) if m else None,
                    "doi": doi})
    return out


def fetch_arxiv(ids):
    """`ids`: list of arXiv ids. Returns {id: abstract}."""
    found = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        time.sleep(ARXIV_GAP)
        url = ARXIV + "?" + urllib.parse.urlencode(
            {"id_list": ",".join(chunk), "max_results": len(chunk)})
        try:
            body = get(url)
        except Exception as e:                     # noqa: BLE001 - report & skip
            log("  arXiv batch failed: %s" % e)
            continue
        for m in re.finditer(
                r"<entry>.*?<id>http[s]?://arxiv\.org/abs/([^<]+)</id>"
                r".*?<summary[^>]*>(.*?)</summary>", body, re.S):
            key = m.group(1).split("v")[0]
            found[key] = " ".join(m.group(2).split())
        log("  arXiv %d/%d" % (min(i + BATCH, len(ids)), len(ids)))
    return found


def fetch_crossref(item):
    if not item["doi"]:
        return None
    time.sleep(CROSSREF_GAP)
    url = CROSSREF + urllib.parse.quote(item["doi"]) + "?mailto=" + MAILTO
    try:
        body = json.loads(get(url))
    except Exception:                              # noqa: BLE001
        return None
    ab = (body.get("message") or {}).get("abstract")
    if not ab:
        return None
    return strip_tags(ab)


def main():
    papers = read_papers()
    todo_ax = [p["arxiv"] for p in papers if p["arxiv"]]
    todo_doi = [p for p in papers if not p["arxiv"] and p["doi"]]
    log("papers: %d | arXiv: %d | DOI-only: %d"
        % (len(papers), len(todo_ax), len(todo_doi)))

    # `--offline` re-derives the YAML from the cache without touching the
    # network — for when only the condensing rules changed.
    offline = "--offline" in sys.argv

    cache = {}
    if os.path.exists(CACHE):
        try:
            cache = json.load(open(CACHE, encoding="utf-8"))
        except Exception:                          # noqa: BLE001
            cache = {}

    abstracts = dict(cache.get("abstracts", {}))

    need_ax = [] if offline else [i for i in todo_ax if i not in abstracts]
    log("arXiv ids to fetch: %d (cached %d)" % (len(need_ax), len(todo_ax) - len(need_ax)))
    if need_ax:
        abstracts.update(fetch_arxiv(need_ax))

    need_doi = [] if offline else [p for p in todo_doi if p["id"] not in abstracts]
    log("DOI lookups: %d" % len(need_doi))
    for n, p in enumerate(need_doi, 1):
        ab = fetch_crossref(p)
        if ab:
            abstracts[p["id"]] = ab
        if n % 25 == 0:
            log("  DOI %d/%d (got %d)" % (n, len(need_doi), len(abstracts)))
            json.dump({"abstracts": abstracts}, open(CACHE, "w", encoding="utf-8"),
                      ensure_ascii=False)

    json.dump({"abstracts": abstracts}, open(CACHE, "w", encoding="utf-8"),
              ensure_ascii=False)

    summaries, missing = {}, []
    for p in papers:
        raw = abstracts.get(p["arxiv"]) or abstracts.get(p["id"])
        if raw:
            txt = condense(raw)
            if txt:
                summaries[p["id"]] = txt
                continue
        missing.append(p["id"])

    log("summaries: %d | without: %d" % (len(summaries), len(missing)))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# One-paragraph \"what is this paper\" blurbs, keyed by paper id.\n")
        f.write("# Generated by scripts/oneoff/fetch_summaries.py from the arXiv and\n")
        f.write("# Crossref APIs. Every blurb is built from **verbatim sentences** of\n")
        f.write("# the official abstract, so it can be incomplete but never invented.\n")
        f.write("# Safe to hand-edit: a manual entry here overrides the generated one\n")
        f.write("# on the next run only if you delete it from the cache.\n\n")
        for k in sorted(summaries):
            f.write("%s: >-\n  %s\n" % (k, summaries[k]))
    log("wrote %s" % OUT)
    if missing:
        log("no blurb for: %s" % ", ".join(missing[:20]))


if __name__ == "__main__":
    main()
