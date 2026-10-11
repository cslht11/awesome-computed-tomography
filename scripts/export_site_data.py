#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export data/*.yaml to a single site-ready JSON file.

The website is a rendering of the same corpus that scripts/build.py turns
into README.md, so both read from one source of truth. This script only
*reads* data/*.yaml; it never writes to them.

Usage:
    python scripts/export_site_data.py              # -> site/data.json
    python scripts/export_site_data.py --compact    # minified
    python scripts/export_site_data.py --out X.json
    python scripts/export_site_data.py --stdout

Permanent-link rule (IMPORTANT):
    `id` is the permanent URL key for a paper, e.g. /p/dm4ct/.
    - Never rename an existing id; external links would break.
    - New ids must be lower-case kebab-case ASCII and globally unique.
    Display text comes from `abbr` (short name, e.g. DM4CT) and `title`
    (full title). Both may change freely; `id` may not.
"""

import argparse
import datetime
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import load, url_of, validate, REPO, ROOT  # noqa: E402

SCHEMA = 1
OUT_DEFAULT = os.path.join(ROOT, "site", "data.json")

PAPER_URL_FIELDS = ("paper", "code", "project", "data")


def link_host(url):
    """Host plus last path segment, for the client-side search blob."""
    if not url:
        return ""
    m = re.match(r"^https?://([^/]+)/(.*)$", str(url))
    if not m:
        return ""
    host, rest = m.group(1), m.group(2).rstrip("/")
    tail = rest.split("/")[-1] if rest else ""
    tail = re.sub(r"v\d+$", "", tail)
    return "%s %s" % (host, tail)


def build_payload():
    meta = load("meta.yaml")
    if not meta:
        sys.exit("data/meta.yaml is required")

    papers = load("papers.yaml") or []
    toolkits = load("toolkits.yaml") or []
    datasets = load("datasets.yaml") or []
    benchmarks = load("benchmarks.yaml") or []
    learning = load("learning.yaml") or []

    problems = validate(meta, papers, toolkits, datasets, benchmarks, learning)
    if problems:
        print("VALIDATION FAILED (%d problem(s)):" % len(problems))
        for x in problems:
            print("  -", x)
        sys.exit(1)

    topics = meta["topics"]
    topic_name = {t["id"]: t["name"] for t in topics}

    counts = {t["id"]: 0 for t in topics}
    for e in papers:
        for t in e["topics"]:
            counts[t] = counts.get(t, 0) + 1

    # Same ordering as README.md: newest first, then alphabetical by abbr/title.
    ordered = sorted(papers, key=lambda e: (-int(e["year"]),
                                            (e.get("abbr") or e["title"]).lower()))

    out_papers = []
    for e in ordered:
        venue = e.get("venue")
        rec = {
            "id": e["id"],
            "title": e["title"],
            "year": int(e["year"]),
            "venue": venue,                 # None == preprint
            "preprint": not venue,
            "topics": list(e["topics"]),
            "links": {},
        }
        if e.get("abbr"):
            rec["abbr"] = e["abbr"]
        for k in PAPER_URL_FIELDS:
            if e.get(k):
                rec["links"][k] = e[k]

        blob = [e["title"], e.get("abbr") or "", venue or "preprint"]
        blob += [topic_name.get(t, t) for t in e["topics"]]
        blob += [link_host(e.get(k)) for k in PAPER_URL_FIELDS if e.get(k)]
        rec["_q"] = re.sub(r"\s+", " ", " ".join(blob)).strip().lower()
        out_papers.append(rec)

    def side(items, key, urlkeys, extra):
        rows = []
        for e in items:
            r = {key: e[key]}
            u = url_of(e, *urlkeys)
            if u:
                r["url"] = u
            for f in extra:
                if e.get(f):
                    r[f] = e[f]
            rows.append(r)
        return rows

    years = [int(e["year"]) for e in papers] or [0]
    nvenue = sum(1 for e in papers if e.get("venue"))

    return {
        "schema": SCHEMA,
        "generated": datetime.date.today().isoformat(),
        "repo": REPO,
        "source": "data/*.yaml",
        "counts": {
            "papers": len(papers),
            "toolkits": len(toolkits),
            "datasets": len(datasets),
            "benchmarks": len(benchmarks),
            "learning": len(learning),
            "peer_reviewed": nvenue,
            "preprints": len(papers) - nvenue,
            "year_min": min(years),
            "year_max": max(years),
        },
        "topics": [{"id": t["id"], "name": t["name"], "desc": t.get("desc", ""),
                    "count": counts.get(t["id"], 0)} for t in topics],
        "papers": out_papers,
        "toolkits": side(toolkits, "name", ("repo", "url"),
                         ("language", "license", "stars", "tags", "note", "homepage")),
        "datasets": side(datasets, "name", ("url", "repo"),
                         ("modality", "tasks", "license", "note", "homepage", "year")),
        "benchmarks": side(benchmarks, "name", ("url", "repo"),
                           ("year", "tasks", "note")),
        "learning": side(learning, "name", ("url", "repo"), ("type", "note")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT,
                    help="output path (default: site/data.json)")
    ap.add_argument("--compact", action="store_true", help="minified JSON")
    ap.add_argument("--stdout", action="store_true", help="write to stdout only")
    args = ap.parse_args()

    payload = build_payload()
    if args.compact:
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    else:
        text = json.dumps(payload, ensure_ascii=False, indent=1)

    c = payload["counts"]
    if args.stdout:
        try:
            sys.stdout.write(text + "\n")
            sys.stdout.flush()
        except BrokenPipeError:
            # `... --stdout | head` closes the pipe early; not an error.
            try:
                sys.stdout.close()
            except BrokenPipeError:
                pass
            os._exit(0)
        return

    d = os.path.dirname(args.out)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    try:
        shown = os.path.relpath(args.out, ROOT)
    except ValueError:
        shown = args.out          # --out on another drive
    print("wrote %s (%d bytes, %d papers / %d toolkits / %d datasets / "
          "%d benchmarks / %d learning)"
          % (shown, len(text.encode("utf-8")),
             c["papers"], c["toolkits"], c["datasets"], c["benchmarks"], c["learning"]))


if __name__ == "__main__":
    main()
