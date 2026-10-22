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
import i18n  # noqa: E402

# 2 — dropped the per-paper `_q` blob. It was a lower-cased concatenation of
#     title + abbr + venue + topic names + note + link hosts, shipped purely so
#     the client could run substring matching over one string. web/search.js now
#     builds a weighted index in the browser from the structured fields instead,
#     which is both better (field weights, ranking) and smaller (the blob was
#     ~68k characters, duplicated content that was also in the payload). A
#     consumer that still wants a flat haystack should join those fields itself.
SCHEMA = 2
OUT_DEFAULT = os.path.join(ROOT, "site", "data.json")

PAPER_URL_FIELDS = ("paper", "code", "project", "data")


def build_payload(lang=None):
    """The site payload for one language.

    ``lang`` selects the i18n overlay used for the per-entry ``note`` text.
    Every note lives in English in data/*.yaml and may be overridden in
    data/i18n/<code>.yaml under the table's own section, exactly like the
    README build, so a translated site shows translated notes instead of
    silently falling back. ``None`` means the source language (English).
    """
    code = lang or i18n.SOURCE
    ov = i18n.load(code)

    meta = load("meta.yaml")
    if not meta:
        sys.exit("data/meta.yaml is required")

    papers = load("papers.yaml") or []
    toolkits = load("toolkits.yaml") or []
    datasets = load("datasets.yaml") or []
    benchmarks = load("benchmarks.yaml") or []
    learning = load("learning.yaml") or []
    # The Teams table is optional: a checkout that predates data/teams.yaml
    # still exports, with an empty team list.
    teams = load("teams.yaml") or []
    # One-paragraph "what is this paper" blurbs, keyed by paper id. Optional by
    # design: papers without one simply get no hover card, and the list must
    # still build if the file is absent.
    blurbs = load("summaries.yaml") or {}
    # Translations live in their own file rather than inside the overlay
    # (`data/i18n/zh.yaml`): that file is hand-maintained and comment-rich, and
    # a few hundred translated blurbs would swamp it. A missing translation
    # just falls back to the English blurb, so the gap stays visible.
    local_blurbs = ({} if code == i18n.SOURCE
                    else (load("summaries.%s.yaml" % code) or {}))

    problems = validate(meta, papers, toolkits, datasets, benchmarks, learning,
                        teams)
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
        # A landmark entry may carry a note; it is shown under the entry and
        # folded into the search blob, so its words are findable too. The
        # overlay is consulted first so a translated site shows the note in
        # its own language; the English in data/papers.yaml is the fallback.
        note = ov.item("papers", e["id"]).get("note") or e.get("note")
        if note:
            rec["note"] = re.sub(r"\s+", " ", note).strip()
        # Blurb for the hover card. Overlay first, exactly like `note`, so a
        # translated site can supply its own wording later without touching the
        # generated English.
        blurb = (ov.item("papers", e["id"]).get("blurb")
                 or local_blurbs.get(e["id"]) or blurbs.get(e["id"]))
        if blurb:
            rec["blurb"] = re.sub(r"\s+", " ", blurb).strip()
        for k in PAPER_URL_FIELDS:
            if e.get(k):
                rec["links"][k] = e[k]
        out_papers.append(rec)

    def side(items, table, key, urlkeys, extra):
        rows = []
        for e in items:
            # `key` stays the English name — it is the stable identifier the
            # overlay lookups and the site self-check are keyed on. A
            # translation that *renames* a row (learning's Chinese book titles)
            # rides alongside as `label`, which app.js prefers for display.
            item = ov.item(table, e[key])
            r = {key: e[key]}
            if item.get("name"):
                r["label"] = item["name"]
            u = url_of(e, *urlkeys)
            if u:
                r["url"] = u
            for f in extra:
                if f == "note":
                    # Same overlay-first rule as papers: a translation may
                    # override just the note and keep the English name.
                    n = ov.item(table, e[key]).get("note") or e.get("note")
                    if n:
                        r["note"] = n
                elif e.get(f):
                    r[f] = e[f]
            rows.append(r)
        return rows

    years = [int(e["year"]) for e in papers] or [0]
    nvenue = sum(1 for e in papers if e.get("venue"))

    out_teams = []
    for e in teams:
        # The overlay is keyed by team id (see scripts/i18n.py): a translation
        # may override the intro (and the institution name) and keep everything
        # else in English.
        item = ov.item("teams", e["id"])
        r = {
            "id": e["id"],
            "name": e["name"],
            "institution": e["institution"],
            "city": e.get("city") or "",
            "country": e["country"],
            "region": e["region"],
            "pi": list(e["pi"]),
            "homepage": e["homepage"],
            "focus": list(e["focus"]),
            "status": e["status"],
            "intro": re.sub(r"\s+", " ", (item.get("intro") or e["intro"])).strip(),
            "works": dict(e.get("works") or {}),
        }
        if item.get("name"):
            r["label"] = item["name"]
        if item.get("institution"):
            r["institution"] = item["institution"]
        if e.get("name_zh"):
            r["name_zh"] = e["name_zh"]
        if e.get("software"):
            r["software"] = re.sub(r"\s+", " ", e["software"]).strip()
        out_teams.append(r)

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
            "teams": len(out_teams),
            "peer_reviewed": nvenue,
            "preprints": len(papers) - nvenue,
            "year_min": min(years),
            "year_max": max(years),
            "updated": str(meta["last_updated"]),
        },
        "topics": [{"id": t["id"], "name": t["name"], "desc": t.get("desc", ""),
                    "count": counts.get(t["id"], 0)} for t in topics],
        "papers": out_papers,
        "toolkits": side(toolkits, "toolkits", "name", ("repo", "url"),
                         ("language", "license", "stars", "tags", "note", "homepage")),
        "datasets": side(datasets, "datasets", "name", ("url", "repo"),
                         ("modality", "tasks", "license", "note", "homepage", "year")),
        "benchmarks": side(benchmarks, "benchmarks", "name", ("url", "repo"),
                           ("year", "tasks", "note")),
        "learning": side(learning, "learning", "name", ("url", "repo"), ("type", "note", "tasks")),
        "teams": out_teams,
        # web/app.js reads DATA.ui and falls back to {} — omit it and every
        # label it renders goes blank. build_site.py adds the same block, so
        # both producers emit one identical payload shape.
        "ui": i18n.js_ui(ov),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT,
                    help="output path (default: site/data.json)")
    ap.add_argument("--lang", default=i18n.SOURCE,
                    help="language code whose overlay supplies the notes "
                         "(default: %s)" % i18n.SOURCE)
    ap.add_argument("--compact", action="store_true", help="minified JSON")
    ap.add_argument("--stdout", action="store_true", help="write to stdout only")
    args = ap.parse_args()

    payload = build_payload(args.lang)
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
