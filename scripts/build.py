#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build README.md for awesome-computed-tomography from data/*.yaml.

Usage:
    python scripts/build.py            # write README.md
    python scripts/build.py --check    # validate only, do not write
"""

import argparse
import datetime
import glob
import io
import os
import re
import sys
from collections import Counter

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install -r requirements.txt")

# Every user-facing string comes from data/i18n/<code>.yaml through
# scripts/i18n.py, so nothing here hard-codes English. i18n lives beside this
# script, hence the path insert.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
README = os.path.join(ROOT, "README.md")

REPO = "cslht11/awesome-computed-tomography"
BADGE = "https://awesome.re/badge.svg"
DEFAULT_TITLE = "Awesome Computed Tomography"


# ---------------------------------------------------------------- helpers
def fill(text, subs):
    """Replace {placeholders}. Only ever fed numbers and known-safe tokens."""
    for k, v in subs.items():
        text = text.replace("{%s}" % k, str(v))
    return text


def write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def counts(papers, toolkits, datasets, benchmarks, learning, teams=None):
    years = [int(e["year"]) for e in papers] or [0]
    n = len(papers)
    return {
        "papers": n,
        "toolkits": len(toolkits or []),
        "datasets": len(datasets or []),
        "benchmarks": len(benchmarks or []),
        "learning": len(learning or []),
        "teams": len(teams or []),
        "year_min": min(years),
        "year_max": max(years),
    }


def switcher(langs, current):
    """The language line under the H1.

    Emitted only when more than one language is registered, so a monolingual
    checkout still produces exactly the README it produced before.
    """
    if len(langs) < 2:
        return ""
    bits = []
    for e in langs:
        if e["code"] == current:
            bits.append("**%s**" % e["label"])
        else:
            bits.append("[%s](%s)" % (e["label"], e["readme"]))
    return " \u00b7 ".join(bits)


def load(name):
    """Load a data file, transparently merging shards when the single file
    is gone.

    papers.yaml / summaries.yaml / summaries.zh.yaml are sharded into
    data/<stem>/<stem>-NN.yaml (NN = 01, 02, ...) because a single file
    outgrew the ~131 KB per-file push limit. The shards are contiguous
    slices of the old single file in sorted order, so merging them in
    sorted filename order reproduces the old file exactly. New entries go
    on the LAST shard; split it again if it approaches the push limit.

    A plain data/<name> still wins when it exists, so every other data
    file keeps working unchanged. Duplicate ids (list shards) or keys
    (mapping shards) fail loudly instead of silently shadowing.
    """
    path = os.path.join(DATA, name)
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    stem, ext = os.path.splitext(name)
    shard_dir = os.path.join(DATA, stem)
    if not os.path.isdir(shard_dir):
        return None
    docs = []
    for shard in sorted(glob.glob(os.path.join(shard_dir, stem + "-*" + ext))):
        with io.open(shard, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        if doc is not None:
            docs.append((shard, doc))
    if not docs:
        return None
    if isinstance(docs[0][1], list):
        merged, seen = [], set()
        for shard, doc in docs:
            if not isinstance(doc, list):
                raise ValueError("%s: shard %s is not a list" % (name, shard))
            for e in doc:
                if isinstance(e, dict) and "id" in e:
                    if e["id"] in seen:
                        raise ValueError(
                            "%s: duplicate id '%s' across shards"
                            % (name, e["id"]))
                    seen.add(e["id"])
                merged.append(e)
        return merged
    if isinstance(docs[0][1], dict):
        merged = {}
        for shard, doc in docs:
            if not isinstance(doc, dict):
                raise ValueError("%s: shard %s is not a mapping"
                                 % (name, shard))
            for k, v in doc.items():
                if k in merged:
                    raise ValueError(
                        "%s: duplicate key '%s' across shards" % (name, k))
                merged[k] = v
        return merged
    raise ValueError("%s: shards have unsupported type %s"
                     % (name, type(docs[0][1]).__name__))


def slug(text):
    """GitHub-compatible heading anchor.

    GitHub lowercases, drops punctuation, then turns *each* space into its
    own hyphen. Runs of spaces therefore yield consecutive hyphens: the
    anchor for "Surveys & Reviews" is `surveys--reviews`, not
    `surveys-reviews`. Collapsing the run breaks the link.
    """
    s = re.sub(r"[^\w\- ]", "", text.lower(), flags=re.UNICODE)
    return s.replace(" ", "-")


def url_of(e, *keys):
    """Resolve the first available URL. Accepts a bare `owner/name` as a GitHub repo."""
    for k in keys:
        v = e.get(k)
        if not v:
            continue
        v = str(v).strip()
        if re.match(r"^https?://", v):
            return v
        if re.match(r"^[\w.\-]+/[\w.\-]+$", v):
            return "https://github.com/" + v
    return None


# ---------------------------------------------------------------- validate
class Problems(list):
    def add(self, where, msg):
        self.append("%s: %s" % (where, msg))


def canonical_keys(e):
    """Identity keys for a paper, independent of how it is linked.

    Covers both the arXiv preprint id and the journal DOI, so a preprint and
    its published version collapse onto the same identity even though the two
    entries carry different URLs.
    """
    out = set()
    for f in ("paper", "project"):
        u = str(e.get(f) or "")
        for m in re.finditer(r"arxiv\.org/abs/([A-Za-z0-9.\-/]+)", u, re.I):
            out.add("arxiv:" + re.sub(r"v\d+$", "", m.group(1)))
        for m in re.finditer(r"10\.\d{4,9}/[^\s\"'<>()\[\],;]+", u):
            out.add("doi:" + m.group(0).lower().rstrip("."))
    return out


TEAM_REGIONS = ("north-america", "europe", "asia")
TEAM_STATUSES = ("active", "legacy")
TEAM_INTRO_MAX = 1000


def validate(meta, papers, toolkits, datasets, benchmarks, learning, teams=None):
    p = Problems()
    topics = [t["id"] for t in meta["topics"]]
    tset = set(topics)

    # last_updated is the maintenance date shown in the stats strip and on
    # the site; it must be a real calendar date, not free text.
    upd = meta.get("last_updated")
    if not upd:
        p.add("meta", "missing required field 'last_updated' (YYYY-MM-DD)")
    else:
        try:
            datetime.date.fromisoformat(str(upd))
        except ValueError:
            p.add("meta", "last_updated '%s' is not a YYYY-MM-DD date" % upd)

    seen = set()
    seen_titles = {}
    seen_keys = {}
    for i, e in enumerate(papers or []):
        w = "papers[%d]" % i
        for f in ("id", "title", "year", "topics"):
            if not e.get(f):
                p.add(w, "missing required field '%s'" % f)
        if e.get("id") in seen:
            p.add(w, "duplicate id '%s'" % e["id"])
        seen.add(e.get("id"))
        for t in e.get("topics") or []:
            if t not in tset:
                p.add(w, "unknown topic '%s'" % t)
        if not (e.get("paper") or e.get("code") or e.get("project")):
            p.add(w, "no link at all (paper/code/project)")
        for k in ("paper", "code", "project"):
            v = e.get(k)
            if v and not re.match(r"^https?://", str(v)):
                p.add(w, "%s is not an http(s) url" % k)

        # The same work must appear once. Two entries that differ only in the
        # form of the link they carry (arXiv preprint vs journal DOI) are the
        # same paper: an earlier import pass deduplicated by `id` alone and
        # silently added 88 papers twice. Key on the canonical identity, not
        # on the id, so this cannot come back.
        title_key = re.sub(r"[^a-z0-9]+", " ", str(e.get("title") or "").lower()).strip()
        if title_key in seen_titles:
            p.add(w, "duplicate work: same title as '%s'" % seen_titles[title_key])
        else:
            seen_titles[title_key] = e.get("id")
        for key in canonical_keys(e):
            if key in seen_keys:
                p.add(w, "duplicate work: same %s as '%s'"
                      % (key.split(":", 1)[0], seen_keys[key]))
            else:
                seen_keys[key] = e.get("id")

    for name, items, key in (("toolkits", toolkits, "name"),
                             ("datasets", datasets, "name"),
                             ("benchmarks", benchmarks, "name"),
                             ("learning", learning, "name")):
        seen2 = set()
        for i, e in enumerate(items or []):
            w = "%s[%d]" % (name, i)
            if not e.get(key):
                p.add(w, "missing '%s'" % key)
            if e.get(key) in seen2:
                p.add(w, "duplicate '%s' = %s" % (key, e[key]))
            seen2.add(e.get(key))
            if not (url_of(e, "url", "repo")):
                p.add(w, "no url/repo")

    validate_teams(p, meta, papers, toolkits, datasets, benchmarks, teams)
    return p


def validate_teams(p, meta, papers, toolkits, datasets, benchmarks, teams):
    """Rules for data/teams.yaml.

    Backward compatible by construction: teams is None (or empty) when the
    file does not exist yet, and a file that does not exist adds no problems.
    """
    if not teams:
        return
    topics = [t["id"] for t in meta["topics"]]
    tset = set(topics)
    paper_ids = set(e["id"] for e in (papers or []))
    side_names = {
        "toolkits": set(e["name"] for e in (toolkits or [])),
        "datasets": set(e["name"] for e in (datasets or [])),
        "benchmarks": set(e["name"] for e in (benchmarks or [])),
    }
    seen = set()
    for i, e in enumerate(teams):
        w = "teams[%d]" % i
        for f in ("id", "name", "institution", "country", "region", "pi",
                  "homepage", "focus", "status", "intro"):
            if not e.get(f):
                p.add(w, "missing required field '%s'" % f)
        tid = e.get("id")
        if tid in seen:
            p.add(w, "duplicate id '%s'" % tid)
        seen.add(tid)
        if tid and not re.match(r"^[a-z0-9-]+$", str(tid)):
            p.add(w, "id '%s' must be lower-case kebab-case" % tid)
        if e.get("region") not in TEAM_REGIONS:
            p.add(w, "region '%s' must be one of %s"
                  % (e.get("region"), "/".join(TEAM_REGIONS)))
        if e.get("status") not in TEAM_STATUSES:
            p.add(w, "status '%s' must be one of %s"
                  % (e.get("status"), "/".join(TEAM_STATUSES)))
        hp = e.get("homepage")
        if hp and not re.match(r"^https?://", str(hp)):
            p.add(w, "homepage is not an http(s) url")
        for t in e.get("focus") or []:
            if t not in tset:
                p.add(w, "unknown topic '%s'" % t)
        works = e.get("works") or {}
        for pid in works.get("papers") or []:
            if pid not in paper_ids:
                p.add(w, "works.papers '%s' does not exist in papers" % pid)
        for table in ("toolkits", "datasets", "benchmarks"):
            for n in works.get(table) or []:
                if n not in side_names[table]:
                    p.add(w, "works.%s '%s' does not exist in %s"
                          % (table, n, table))
        intro = str(e.get("intro") or "")
        if len(intro) > TEAM_INTRO_MAX:
            p.add(w, "intro is %d chars, over the %d cap"
                  % (len(intro), TEAM_INTRO_MAX))
        ver = e.get("verified")
        if ver:
            try:
                datetime.date.fromisoformat(str(ver))
            except ValueError:
                p.add(w, "verified '%s' is not a YYYY-MM-DD date" % ver)


# ---------------------------------------------------------------- render
# The README links back to the site, so the origin is read from the same single
# place the site build uses (site.config.yml -> `url`). Hardcoding it here would
# mean a domain change silently left the README badge and nav pointing at the
# old address — the docs promise the origin is configured in exactly one spot.
SITE_CONFIG = os.path.join(ROOT, "site.config.yml")
SITE_URL_FALLBACK = "https://computedtomography.org/"


def site_url():
    try:
        with io.open(SITE_CONFIG, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    except (IOError, OSError):
        return SITE_URL_FALLBACK
    url = (cfg.get("url") or "").strip()
    if url and not url.endswith("/"):
        url += "/"
    return url or SITE_URL_FALLBACK


SITE_URL = site_url()


def render_topic_grid(papers, meta, ov, site_base, cols=3):
    # Same 3-column grid as before, but each cell now links to the site with
    # that topic already selected instead of to an in-page anchor: the
    # per-topic paper lists live on the website, not in the README.
    cells = []
    for t in meta["topics"]:
        n = sum(1 for e in papers if t["id"] in e["topics"])
        if n:
            nm = ov.topic(t["id"]).get("name") or t["name"]
            cells.append("[%s](%s?tab=papers&topic=%s) <sub>%d</sub>" % (nm, site_base, t["id"], n))
    while len(cells) % cols:
        cells.append("")
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    out = ["|" + " |" * cols, "|" + " --- |" * cols]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out) + "\n"


def build(meta, papers, toolkits, datasets, benchmarks, learning, ov, langs,
          teams=None):
    subs = counts(papers, toolkits, datasets, benchmarks, learning, teams)
    subs["updated"] = str(meta["last_updated"])
    subs["repo"] = REPO
    subs["repo_url"] = "https://github.com/" + REPO
    subs["site_url"] = SITE_URL
    subs["title"] = ov.top("title") or DEFAULT_TITLE
    subs["tagline"] = ov.top("tagline")
    subs["content_license"] = "CC BY-NC-SA 4.0"
    subs["code_license"] = "MIT"

    def badge(label, msg, color):
        q = lambda x: str(x).replace("-", "--").replace(" ", "%20").replace("_", "__")
        return "https://img.shields.io/badge/%s-%s-%s?style=flat-square" % (q(label), q(msg), color)

    heads = {}
    for key, default in (("papersHeading", "Papers"),
                         ("toolkitsHeading", "Toolkits"),
                         ("datasetsHeading", "Datasets"),
                         ("benchmarksHeading", "Benchmarks"),
                         ("learningHeading", "Learning"),
                         ("teamsHeading", "Research Teams"),
                         ("contactHeading", "Contact"),
                         ("licenseHeading", "License")):
        heads[key] = ov.readme(key, default)

    def anchor(key):
        return slug(heads[key])

    def head(key):
        return "## %s\n" % heads[key]

    # Browse rows link to the reader's own language on the site: the English
    # README points at the site root, the Chinese one at /zh/.
    lang_path = next((e.get("path") or "" for e in langs if e["code"] == ov.code), "")
    site_base = SITE_URL + lang_path

    # The five-number stats strip. Every cell carries its own unit wording, so
    # a language can put the unit first, or drop the plural, without any of this
    # code having to know about it.
    cells = [fill(ov.readme("statPapersCell", "{papers} papers"), subs),
             fill(ov.readme("statToolkitsCell", "{toolkits} toolkits"), subs),
             fill(ov.readme("statDatasetsCell", "{datasets} datasets"), subs),
             fill(ov.readme("statBenchmarksCell", "{benchmarks} benchmarks"), subs),
             fill(ov.readme("statSpanCell", "Updated {updated}"), subs)]
    # Centered: a bare Markdown table is left-aligned on GitHub, and with
    # five cells it no longer spans the page, so without the wrapper it
    # reads as a stray line of text instead of the summary strip.
    strip = ("<div align=\"center\">\n\n"
             "| " + " | ".join(cells) + " |\n|" + "|".join([" :-: "] * len(cells)) + "|\n"
             "\n</div>\n")

    # The Teams section only exists once data/teams.yaml does. A checkout
    # without it (or an empty one) still produces exactly the README it
    # produced before the section was added.
    has_teams = bool(teams)
    nav_keys = ["papersHeading", "toolkitsHeading", "datasetsHeading",
                "benchmarksHeading", "learningHeading"]
    if has_teams:
        nav_keys.append("teamsHeading")
    nav = " \u00b7 ".join(
        ["**[{}]({})**".format(ov.readme("navWebsite", "Website"), SITE_URL)] +
        ["[%s](#%s)" % (heads[k], anchor(k)) for k in nav_keys])

    badges = " ".join([
        "[![Awesome](%s)](https://awesome.re)" % BADGE,
        "[![Website](%s)](%s)" % (badge(ov.readme("badgeWebsite", "website"),
                                        "computedtomography.org", "3f51b5"), SITE_URL),
        "[![Papers](%s)](#%s)" % (badge(ov.readme("badgePapers", "papers"),
                                        subs["papers"], "555"), anchor("papersHeading")),
        "[![License](%s)](#%s)" % (badge(ov.readme("badgeLicense", "license"),
                                         subs["content_license"], "555"),
                                   anchor("licenseHeading"))])

    parts = []
    parts.append('<a id="top"></a>\n<div align="center">\n\n'
                 '<img src="assets/logo.svg" width="88" alt="">\n\n'
                 "# %s\n\n%s\n\n%s\n\n%s\n\n</div>\n"
                 % (subs["title"], fill(ov.readme("heroTagline", ""), subs),
                    badges, nav))
    if len(langs) > 1:
        parts.append(switcher(langs, ov.code) + "\n")
    parts.append(strip)
    parts.append(fill(ov.readme("blurb", ""), subs) + "\n")
    # No keyword block here on purpose. GitHub's repository search only reads
    # the name, the description and the topics — it does not index README
    # bodies (measured: terms living only in this file return zero hits), so a
    # pasted wall of keywords buys nothing and just breaks up the page. The
    # findable words live in the repository description and the topic list.
    parts.append(head("papersHeading"))
    parts.append(render_topic_grid(papers, meta, ov, site_base))

    # The entries themselves live on the website; each section keeps its
    # heading and points at the site tab with that collection selected.
    # No back-to-top link here: these sections are one line each, so the
    # link would be more chrome than content (it stays after the Papers
    # grid and at the bottom of the page, where it is actually useful).
    sections = [("toolkitsHeading", "toolkits", subs["toolkits"]),
                ("datasetsHeading", "datasets", subs["datasets"]),
                ("benchmarksHeading", "benchmarks", subs["benchmarks"]),
                ("learningHeading", "learning", subs["learning"])]
    if has_teams:
        sections.append(("teamsHeading", "teams", subs["teams"]))
    for key, tab, n in sections:
        parts.append(head(key))
        parts.append(fill(ov.readme("browseCollection", ""),
                          {"n": n, "url": site_base + "?tab=" + tab}) + "\n")

    parts.append(head("contactHeading"))
    parts.append(fill(ov.readme("contactBody", ""), subs) + "\n")

    parts.append(head("licenseHeading"))
    parts.append(fill(ov.readme("licenseIntro", ""), subs) + "\n\n"
                 + "- " + fill(ov.readme("licenseAttribution", ""), subs) + "\n"
                 + "- " + fill(ov.readme("licenseNonCommercial", ""), subs) + "\n"
                 + "- " + fill(ov.readme("licenseShareAlike", ""), subs) + "\n\n"
                 + fill(ov.readme("licenseCodeColumn", ""), subs) + "\n")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only")
    ap.add_argument("--lang", default="all",
                    help="language code, comma-separated list, or 'all'")
    args = ap.parse_args()

    meta = load("meta.yaml")
    papers = load("papers.yaml") or []
    toolkits = load("toolkits.yaml") or []
    datasets = load("datasets.yaml") or []
    benchmarks = load("benchmarks.yaml") or []
    learning = load("learning.yaml") or []
    teams = load("teams.yaml") or []

    if not meta:
        sys.exit("data/meta.yaml is required")

    problems = validate(meta, papers, toolkits, datasets, benchmarks, learning,
                        teams)

    langs = i18n.languages(meta)
    by_code = dict((e["code"], e) for e in langs)
    if args.lang == "all":
        want = [e["code"] for e in langs]
    else:
        want = [c.strip() for c in args.lang.split(",") if c.strip()]
        for c in want:
            if c not in by_code:
                sys.exit("data/meta.yaml declares no language '%s'" % c)
    langs = [by_code[c] for c in want]

    tables = {"toolkits": toolkits, "datasets": datasets,
              "benchmarks": benchmarks, "learning": learning}

    # An orphan is a translation for something that no longer exists - a renamed
    # topic id, a dropped dataset. Those silently stop applying, so they fail
    # the build; a merely *missing* translation does not (see scripts/i18n.py).
    names = dict((t, [e["name"] for e in items]) for t, items in tables.items())
    # Teams are keyed by their permanent id, not by name.
    names["teams"] = [e["id"] for e in teams]
    topic_ids = [t["id"] for t in meta["topics"]]
    overlays = {}
    for e in langs:
        ov = i18n.load(e["code"])
        overlays[e["code"]] = ov
        problems.extend(i18n.check(ov, topic_ids, names))

    if problems:
        print("VALIDATION FAILED (%d problem(s)):" % len(problems))
        for x in problems:
            print("  -", x)
        sys.exit(1)
    print("validation OK: %d papers / %d toolkits / %d datasets / %d benchmarks / %d learning / %d teams"
          % (len(papers), len(toolkits), len(datasets), len(benchmarks), len(learning), len(teams)))

    tc = Counter(t for e in papers for t in e["topics"])
    print("topic distribution:")
    for t in meta["topics"]:
        print("  %-22s %3d" % (t["name"], tc.get(t["id"], 0)))

    if args.check:
        return

    # How much of each language is still English. Reported rather than enforced:
    # a missing string falls back cleanly, but it should not go unnoticed.
    ref = i18n.load(i18n.SOURCE)
    expected = {}
    for k, v in (ref.data.get("ui") or {}).items():
        expected[("ui", k)] = 1
    for k in (ref.data.get("readme") or {}):
        expected[("readme", k)] = 1

    for e in langs:
        ov = overlays[e["code"]]
        text = build(meta, papers, toolkits, datasets, benchmarks, learning,
                     ov, langs, teams)
        write(os.path.join(ROOT, e["readme"]), text)
        note = ""
        if e["code"] != i18n.SOURCE:
            gap = len(ov.untranslated(expected))
            missing = sum(1 for t, items in tables.items() for x in items
                          if not ov.item(t, x["name"]).get("note"))
            note = ("  [%d prose/UI strings and %d of %d table notes still "
                    "fall back to English]" % (gap, missing,
                                               sum(len(v) for v in tables.values())))
        print("wrote %s (%d bytes)%s"
              % (e["readme"], len(text.encode("utf-8")), note))
if __name__ == "__main__":
    main()
