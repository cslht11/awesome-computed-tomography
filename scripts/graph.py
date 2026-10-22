#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge-graph projection of the directory, for /graph/ and /zh/graph/.

Everything here is *derived*: the graph is computed at build time from the
same payload the rest of the site renders (plus the optional enrichment
files under data/graph/), so it can never drift away from the directory
the way a hand-maintained graph file would.

Node types: paper, toolkit, dataset, benchmark, learning, team, topic,
venue, author, guide. Edge kinds:

    topic     paper/dataset/benchmark/guide belongs to a topic (also used
              for the topic pages' resource lists: topic -> toolkit)
    start     a topic page's hand-picked "start here" paper (subset of the
              paper -> topic memberships, kept distinct so the UI can
              weight it)
    focus     team -> topic, the team's declared research focus
    works     team -> paper/toolkit/dataset/benchmark it is known for
    uses      paper uses or describes a dataset/benchmark (resource-page
              evidence: named in the paper's title/note/blurb, linked from
              it, or its citation paper)
    cite      the paper a resource page names as its citation
    sibling   two resources sharing an official link or naming each other
    code      a paper's code repository *is* a toolkit in the directory
    venue     paper -> the venue it appeared in (venues with >= 2 papers)
    authored  author -> paper (OpenAlex enrichment, data/graph/)
    leads     author -> team, when the author is the team's listed PI
              (exact normalised-name match only; nothing is guessed)
    coauthor  two included authors sharing a paper (derived)
    cites     paper -> paper it cites, both in the library (OpenAlex
              referenced_works intersected with the library)

The enrichment files are graph-side only. The library entries themselves
still carry no authors field; authorship lives here, keyed by paper id,
sourced from OpenAlex, and is allowed to be absent: without the files the
graph is exactly the P0 graph (no author/venue enrichment loss — venue
comes from the payload — and no citation edges).
"""

import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import load, url_of  # noqa: E402

VENUE_MIN_PAPERS = 2       # a venue becomes a node at this many papers
AUTHOR_MIN_PAPERS = 3      # an author becomes a node at this many papers
                           # (team PIs are always included, see build_graph)


# ------------------------------------------------------------------ loading
def load_enrichment():
    """(authors_doc, citations_doc); either may be None when absent."""
    authors = load("graph/authors.yaml")
    citations = load("graph/citations.yaml")
    return authors, citations


def norm_person(name):
    """'Emil Y. Sidky' -> 'emil y sidky': the only normalisation the PI
    matching is allowed to use — case, full stops, extra spaces, unicode
    dashes (OpenAlex prints 'Guang\u2010Hong Chen' with U+2010), and a
    parenthetical suffix (teams.yaml PIs carry one: 'Yang Chen (\u9648\u9633)').
    Matching after this normalisation is still exact; nothing is guessed."""
    s = str(name or "")
    s = re.sub(r"[(（][^)）]*[)）]", " ", s)
    s = re.sub(r"[\u2010-\u2015\u2212]", "-", s.lower())
    s = re.sub(r"[.\uFF0E]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _openalex_tail(url_or_id):
    """'https://openalex.org/A5012345678' -> 'A5012345678'."""
    s = str(url_or_id or "").rstrip("/")
    return s.rsplit("/", 1)[-1] if s else ""


# ---------------------------------------------------------------- validation
def validate_graph(papers, teams, authors_doc, citations_doc):
    """Integrity rules for data/graph/*.yaml, in build.py's Problems style.

    Both files are optional; when present, every reference must resolve.
    Returns a list of problem strings (empty when all is well).
    """
    problems = []
    paper_ids = set(e["id"] for e in (papers or []))
    if authors_doc is not None:
        if not isinstance(authors_doc, dict):
            problems.append("graph/authors: top level must be a mapping "
                            "keyed by paper id")
        else:
            for pid, rec in sorted(authors_doc.items()):
                w = "graph/authors[%s]" % pid
                if pid not in paper_ids:
                    problems.append("%s: no such paper in the library" % w)
                    continue
                if not isinstance(rec, dict):
                    problems.append("%s: entry must be a mapping" % w)
                    continue
                if rec.get("matched_by") not in ("doi", "arxiv", "title", None):
                    problems.append("%s: matched_by %r is not "
                                    "doi/arxiv/title/null"
                                    % (w, rec.get("matched_by")))
                authors = rec.get("authors")
                if authors is None:
                    authors = []
                if not isinstance(authors, list):
                    problems.append("%s: authors must be a list" % w)
                    continue
                for a in authors:
                    if not isinstance(a, dict) or not a.get("name"):
                        problems.append("%s: every author needs a name" % w)
                        break
    if citations_doc is not None:
        if not isinstance(citations_doc, list):
            problems.append("graph/citations: top level must be a list of "
                            "{from, to} pairs")
        else:
            seen = set()
            for i, pair in enumerate(citations_doc):
                w = "graph/citations[%d]" % i
                if not isinstance(pair, dict):
                    problems.append("%s: pair must be a mapping" % w)
                    continue
                a, b = pair.get("from"), pair.get("to")
                for k, v in (("from", a), ("to", b)):
                    if v not in paper_ids:
                        problems.append("%s: %s %r is not a paper in the "
                                        "library" % (w, k, v))
                if a and a == b:
                    problems.append("%s: a paper cannot cite itself" % w)
                if (a, b) in seen:
                    problems.append("%s: duplicate pair %s -> %s" % (w, a, b))
                seen.add((a, b))
    return problems


def check_graph(graph):
    """Referential integrity of a built graph: endpoints exist, ids unique."""
    problems = []
    ids = [n["id"] for n in graph["nodes"]]
    if len(ids) != len(set(ids)):
        problems.append("graph: duplicate node ids")
    known = set(ids)
    for s, t, k in graph["edges"]:
        if s not in known:
            problems.append("graph: edge source %r has no node" % s)
        if t not in known:
            problems.append("graph: edge target %r has no node" % t)
    for b in graph["backbone"]:
        if b not in known:
            problems.append("graph: backbone node %r has no node" % b)
    return problems


# ------------------------------------------------------------------- helpers
def _gh_key(url):
    """Normalise a GitHub repo URL for the paper-code == toolkit test."""
    if not url:
        return None
    s = str(url).strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = s.rstrip("/")
    if s.endswith(".git"):
        s = s[:-4]
    return s or None


def _paper_url(p):
    l = p["links"]
    return l.get("paper") or l.get("project") or l.get("code") or l.get("data")


# -------------------------------------------------------------------- build
def build_graph(payload, payload_zh, topic_doc, topic_resources, rp_pages,
                guides, authors_doc=None, citations_doc=None):
    """Project the payloads into {nodes, edges, backbone, stats}.

    ``payload`` / ``payload_zh`` are export_site_data payloads (English and
    Chinese) so every node can carry both labels. ``topic_resources`` is
    build_site.topic_resources (the topic pages' own resource matcher, so
    the graph and the topic pages can never disagree about which resource
    belongs to a topic). ``rp_pages`` is resource_pages.select's page list
    (the paper -> resource evidence). ``guides`` is data/guides.yaml's list.
    """
    nodes = {}
    edges = []
    edge_seen = set()

    def node(nid, t, label, label_zh=None, year=None, href=None, meta=None):
        if nid in nodes:
            return nodes[nid]
        n = {"id": nid, "t": t, "l": label}
        if label_zh and label_zh != label:
            n["lz"] = label_zh
        if year:
            n["y"] = int(year)
        if href:
            n["href"] = href
        if meta:
            n["m"] = meta
        nodes[nid] = n
        return n

    def edge(s, t, kind):
        key = (s, t, kind)
        if s == t or key in edge_seen:
            return
        edge_seen.add(key)
        edges.append([s, t, kind])

    zh_topics = dict((t["id"], t["name"]) for t in payload_zh["topics"])
    zh_side = {}
    for tbl in ("toolkits", "datasets", "benchmarks", "learning"):
        for r in payload_zh[tbl]:
            zh_side[(tbl, r["name"])] = r.get("label") or r["name"]
    zh_teams = dict((tm["id"], tm) for tm in payload_zh["teams"])

    # ------------------------------------------------------------ topics
    for t in payload["topics"]:
        node("topic:" + t["id"], "topic", t["name"], zh_topics.get(t["id"]),
             href=("topics/%s/" % t["id"]) if t["id"] != "other"
             else "?tab=papers&topic=other",
             meta={"count": t.get("count", 0)})

    # ------------------------------------------------------------ papers
    venue_counts = Counter(p["venue"] for p in payload["papers"] if p.get("venue"))
    venues = set(v for v, n in venue_counts.items() if n >= VENUE_MIN_PAPERS)
    for v in venues:
        node("venue:" + v, "venue", v, meta={"count": venue_counts[v]})

    starts = defaultdict(set)      # topic id -> paper ids it picks as starters
    if topic_doc:
        for tid, tp in (topic_doc.get("topics") or {}).items():
            for s in tp.get("start") or []:
                if s.get("id"):
                    starts[tid].add(s["id"])

    papers_by_id = {}
    for p in payload["papers"]:
        papers_by_id[p["id"]] = p
        label = p.get("abbr") or p["title"]
        meta = {"topics": list(p["topics"])}
        if p.get("abbr"):
            meta["title"] = p["title"]
        if p.get("venue"):
            meta["venue"] = p["venue"]
        if p["links"].get("code"):
            meta["code"] = True
        node("paper:" + p["id"], "paper", label, year=p["year"],
             href=_paper_url(p), meta=meta)
        for tid in p["topics"]:
            edge("paper:" + p["id"], "topic:" + tid,
                 "start" if p["id"] in starts.get(tid, ()) else "topic")
        if p.get("venue") in venues:
            edge("paper:" + p["id"], "venue:" + p["venue"], "venue")

    # ------------------------------------------- toolkits / datasets / etc.
    page_of = {}
    for pg in rp_pages or []:
        page_of[(pg["table"], pg["name"])] = pg["rel"]

    side_meta = {
        "toolkits": lambda r: dict((k, r[k]) for k in ("language", "license", "stars") if r.get(k)),
        "datasets": lambda r: dict((k, r[k]) for k in ("modality", "license", "year") if r.get(k)),
        "benchmarks": lambda r: dict((k, r[k]) for k in ("year",) if r.get(k)),
        "learning": lambda r: dict((k, r[k]) for k in ("type",) if r.get(k)),
    }
    side_href = {
        "toolkits": lambda r: "?tab=toolkits",
        "datasets": lambda r: page_of.get(("datasets", r["name"])) or "?tab=datasets",
        "benchmarks": lambda r: page_of.get(("benchmarks", r["name"])) or "?tab=benchmarks",
        "learning": lambda r: "?tab=learning",
    }
    topic_ids = set(t["id"] for t in payload["topics"])
    side_kind = {"toolkits": "toolkit", "datasets": "dataset",
                 "benchmarks": "benchmark", "learning": "learning"}
    for tbl in ("toolkits", "datasets", "benchmarks", "learning"):
        kind = side_kind[tbl]
        for r in payload[tbl]:
            node("%s:%s" % (kind, r["name"]), kind,
                 r.get("label") or r["name"], zh_side.get((tbl, r["name"])),
                 href=side_href[tbl](r), meta=side_meta[tbl](r) or None)
            for task in r.get("tasks") or []:
                if task in topic_ids:
                    edge("%s:%s" % (kind, r["name"]), "topic:" + task, "topic")

    # Topic pages' resource lists: topic -> toolkit/dataset/benchmark.
    # (Datasets and benchmarks mostly duplicate the tasks edges above and
    # dedupe away; toolkits only ever arrive through this route.)
    if topic_doc:
        for t in payload["topics"]:
            tp = (topic_doc.get("topics") or {}).get(t["id"])
            if not tp:
                continue
            for kind_word, r in topic_resources(tp, payload):
                tbl = {"kindDataset": "dataset", "kindBenchmark": "benchmark",
                       "kindToolkit": "toolkit"}[kind_word]
                edge("%s:%s" % (tbl, r["name"]), "topic:" + t["id"], "topic")

    # ------------------------------------------------------------- teams
    for tm in payload["teams"]:
        ztm = zh_teams.get(tm["id"]) or {}
        meta = {"institution": tm["institution"], "country": tm["country"],
                "region": tm["region"], "pi": list(tm["pi"])}
        if tm.get("city"):
            meta["city"] = tm["city"]
        node("team:" + tm["id"], "team", tm.get("label") or tm["name"],
             ztm.get("label") or tm.get("name_zh"), href="?tab=teams",
             meta=meta)
        for tid in tm["focus"]:
            edge("team:" + tm["id"], "topic:" + tid, "focus")
        works = tm.get("works") or {}
        for pid in works.get("papers") or []:
            if pid in papers_by_id:
                edge("team:" + tm["id"], "paper:" + pid, "works")
        for tbl, kind in (("toolkits", "toolkit"), ("datasets", "dataset"),
                          ("benchmarks", "benchmark")):
            for name in works.get(tbl) or []:
                edge("team:" + tm["id"], "%s:%s" % (kind, name), "works")

    # ------------------------------------------- papers <-> resources
    for pg in rp_pages or []:
        kind = "dataset" if pg["table"] == "datasets" else "benchmark"
        target = "%s:%s" % (kind, pg["name"])
        cites = set(pg.get("cite") or [])
        for pid in pg.get("papers") or []:
            if pid in papers_by_id:
                edge("paper:" + pid, target, "cite" if pid in cites else "uses")
        for tbl2, name2 in pg.get("related") or []:
            kind2 = "dataset" if tbl2 == "datasets" else "benchmark"
            a, b = sorted((target, "%s:%s" % (kind2, name2)))
            edge(a, b, "sibling")

    # ------------------------------------------- paper code == toolkit
    repo_owner = {}
    for r in payload["toolkits"]:
        for u in (r.get("url"),):
            k = _gh_key(u)
            if k and k.startswith("github.com/"):
                repo_owner[k] = r["name"]
    for p in payload["papers"]:
        k = _gh_key(p["links"].get("code"))
        if k and k in repo_owner:
            edge("paper:" + p["id"], "toolkit:" + repo_owner[k], "code")

    # ------------------------------------------------------------- guides
    for g in guides or []:
        title = ((g.get("en") or {}).get("title") or "").strip()
        if not title:
            continue
        node("guide:" + g["slug"], "guide", title,
             ((g.get("zh") or {}).get("title") or "").strip() or None,
             href="guides/%s/" % g["slug"])
        for tid in g.get("topics") or []:
            if tid in topic_ids:
                edge("guide:" + g["slug"], "topic:" + tid, "topic")

    # ------------------------------------------------- authors + citations
    author_stats = {"matched": 0, "nodes": 0, "authored": 0, "leads": 0,
                    "coauthor": 0}
    if authors_doc:
        pi_names = {}
        for tm in payload["teams"]:
            for name in tm["pi"]:
                pi_names.setdefault(norm_person(name), tm["id"])
        def author_key(a, by_name):
            """Canonical key for one authorship: the OpenAlex author id
            when the record carries one; otherwise the normalised name —
            merged into the id-keyed author when exactly one exists with
            that name (OpenAlex leaves some authorships id-less)."""
            tail = _openalex_tail(a.get("openalex_author_id") or a.get("openalex"))
            if tail:
                return tail
            named = by_name.get(norm_person(a.get("name")) or "")
            if named and len(named) == 1:
                return next(iter(named))
            n = norm_person(a.get("name"))
            return ("name:" + n) if n else ""

        counts = Counter()
        names = {}
        oa_ids = {}
        per_paper = {}
        raw = {}
        for pid, rec in authors_doc.items():
            if pid not in papers_by_id or not isinstance(rec, dict):
                continue
            authors = rec.get("authors") or []
            if authors:
                author_stats["matched"] += 1
            raw[pid] = authors
        by_name = defaultdict(set)
        for authors in raw.values():
            for a in authors:
                tail = _openalex_tail(a.get("openalex_author_id") or a.get("openalex"))
                if tail:
                    by_name[norm_person(a.get("name"))].add(tail)
        for pid, authors in raw.items():
            keys = []
            for a in authors:
                key = author_key(a, by_name)
                if not key:
                    continue
                keys.append(key)
                counts[key] += 1
                names[key] = a.get("name") or key
                oa = a.get("openalex_author_id") or a.get("openalex")
                if oa:
                    oa_ids[key] = oa
            per_paper[pid] = keys
        included = set(k for k, n in counts.items()
                       if n >= AUTHOR_MIN_PAPERS or norm_person(names[k]) in pi_names)
        for key in included:
            meta = {"papers": counts[key]}
            oa_url = None
            if key in oa_ids:
                oa_url = oa_ids[key]
                if not oa_url.startswith("http"):
                    oa_url = "https://openalex.org/" + _openalex_tail(oa_url)
                meta["openalex"] = oa_url
            node("author:" + key, "author", names[key],
                 href=oa_url, meta=meta)
            author_stats["nodes"] += 1
            team_id = pi_names.get(norm_person(names[key]))
            if team_id:
                edge("author:" + key, "team:" + team_id, "leads")
                author_stats["leads"] += 1
        for pid, keys in per_paper.items():
            keys = [k for k in keys if k in included]
            for key in keys:
                edge("author:" + key, "paper:" + pid, "authored")
                author_stats["authored"] += 1
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    a, b = sorted((keys[i], keys[j]))
                    if ("author:" + a, "author:" + b, "coauthor") not in edge_seen:
                        edge("author:" + a, "author:" + b, "coauthor")
                        author_stats["coauthor"] += 1

    cite_stats = 0
    if citations_doc:
        for pair in citations_doc:
            if not isinstance(pair, dict):
                continue
            a, b = pair.get("from"), pair.get("to")
            if a in papers_by_id and b in papers_by_id and a != b:
                before = len(edges)
                edge("paper:" + a, "paper:" + b, "cites")
                cite_stats += len(edges) - before

    backbone = [n["id"] for n in nodes.values()
                if n["t"] in ("team", "topic", "toolkit")]
    stats = {
        "nodes": dict(Counter(n["t"] for n in nodes.values())),
        "edges": dict(Counter(k for _, _, k in edges)),
        "authors": author_stats,
        "cites": cite_stats,
    }
    return {"nodes": list(nodes.values()), "edges": edges,
            "backbone": backbone, "stats": stats}
