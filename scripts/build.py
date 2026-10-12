#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build README.md for awesome-computed-tomography from data/*.yaml.

Usage:
    python scripts/build.py            # write README.md
    python scripts/build.py --check    # validate only, do not write
"""

import argparse
import io
import os
import re
import sys
from collections import OrderedDict, Counter

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


def counts(papers, toolkits, datasets, benchmarks, learning):
    years = [int(e["year"]) for e in papers] or [0]
    n = len(papers)
    nvenue = sum(1 for e in papers if e.get("venue"))
    return {
        "papers": n,
        "peer": nvenue,
        "peer_pct": round(100.0 * nvenue / n) if n else 0,
        "preprints": n - nvenue,
        "toolkits": len(toolkits or []),
        "datasets": len(datasets or []),
        "benchmarks": len(benchmarks or []),
        "learning": len(learning or []),
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
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def slug(text):
    """GitHub-compatible heading anchor.

    GitHub lowercases, drops punctuation, then turns *each* space into its
    own hyphen. Runs of spaces therefore yield consecutive hyphens: the
    anchor for "Surveys & Reviews" is `surveys--reviews`, not
    `surveys-reviews`. Collapsing the run breaks the link.
    """
    s = re.sub(r"[^\w\- ]", "", text.lower(), flags=re.UNICODE)
    return s.replace(" ", "-")


def esc(text):
    """Escape pipes so table cells do not break."""
    return str(text).replace("|", "\\|").strip()


def link(url, label):
    return "[%s](%s)" % (label, url) if url else ""


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


def validate(meta, papers, toolkits, datasets, benchmarks, learning):
    p = Problems()
    topics = [t["id"] for t in meta["topics"]]
    tset = set(topics)

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
    return p


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


def top_link(ov):
    return ('<div align="right"><a href="#top">%s ↑</a></div>\n'
            % ov.readme("backToTop", "back to top"))


def head_token(title):
    """First whitespace-delimited token of a title, punctuation trimmed.

    Used to decide whether an abbreviation is really the head of the title.
    "A benchmark ..." has head token "A", so abbr "A" qualifies; "ART ..."
    has head token "ART", so abbr "AR" does not.
    """
    first = title.strip().split()
    return first[0].rstrip(".,:;").lower() if first else ""


def drop_trailing_parens(rest, name):
    """Remove an abbreviation repeated in trailing parentheses.

    Titles harvested from Crossref often end with the abbreviation again
    ("... reconstruction (LoDoPaB-CT)"). The head already prints it, so the
    parentheses are pure clutter. Only drops a trailing group whose body is
    the abbreviation, optionally prefixed by a venue.
    """
    m = re.search(r"\(([^()]*)\)\s*$", rest)
    if not m:
        return rest
    body = m.group(1).strip()
    if body.lower() == name.lower() or body.lower().endswith(": " + name.lower()) \
            or body.lower().split(", ")[-1] == name.lower():
        return rest[:m.start()].rstrip(" ,;")
    return rest


def paper_head(e):
    name = e.get("abbr")
    title = e["title"]
    if name and title.lower().startswith(name.lower()) \
            and head_token(title) == name.lower():
        # avoid "**[DM4CT]** DM4CT: ..." duplication
        rest = title[len(name):].lstrip(" :—–-,")
        rest = drop_trailing_parens(rest, name)
        return "**%s: %s**" % (name, rest) if rest else "**%s**" % name
    if name:
        return "**%s: %s**" % (name, title)
    return "**%s**" % title


LINK_LABELS = (("paper", "linkPaper", "Paper"), ("code", "linkCode", "Code"),
               ("project", "linkProject", "Project"), ("data", "linkData", "Data"))


def render_papers(papers, meta, ov):
    out = []
    by_topic = OrderedDict((t["id"], []) for t in meta["topics"])
    for e in papers:
        for t in e["topics"]:
            by_topic[t].append(e)

    for t in meta["topics"]:
        items = by_topic[t["id"]]
        if not items:
            continue
        items.sort(key=lambda e: (-int(e["year"]), (e.get("abbr") or e["title"]).lower()))
        local = ov.topic(t["id"])
        out.append("### %s\n" % (local.get("name") or t["name"]))
        desc = local.get("desc") or t.get("desc")
        if desc:
            # Strip both the ASCII and the full-width full stop: an English
            # topic description ends in ".", its Chinese translation in "。",
            # and the count follows on the same line.
            out.append(fill(ov.readme("topicCount", "<sub>{desc} · {n} papers</sub>"),
                            {"desc": desc.rstrip(".\u3002"), "n": len(items)}) + "\n")
        for e in items:
            # Venue first in italics, preprints say so: the two are told apart at a glance.
            where = "_%s %s_" % (e["venue"], e["year"]) if e.get("venue") \
                else "_%s %s_" % (ov.readme("preprintLabel", "preprint"), e["year"])
            links = []
            for k, ikey, lab in LINK_LABELS:
                if e.get(k):
                    links.append("[%s](%s)" % (ov.readme(ikey, lab), e[k]))
            out.append("- %s — %s%s" % (paper_head(e), where,
                                         (" · " + " · ".join(links)) if links else ""))
            # A few landmark entries carry a `note`. It is rendered as an
            # indented paragraph tied to the bullet above, so an entry can say
            # why it matters without breaking the one-line-per-paper rhythm.
            # Only entries that actually have one emit the blank line, so the
            # ordinary one-line-per-paper spacing stays untouched.
            note = ov.item("papers", e["id"]).get("note") or e.get("note")
            if note:
                out.append("")
                out.append("  " + " ".join(note.split()))
        out.append("")
    return "\n".join(out)


def render_table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join([" --- "] * len(header)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out) + "\n"


def render_topic_grid(papers, meta, ov, cols=3):
    cells = []
    for t in meta["topics"]:
        n = sum(1 for e in papers if t["id"] in e["topics"])
        if n:
            nm = ov.topic(t["id"]).get("name") or t["name"]
            cells.append("[%s](#%s) <sub>%d</sub>" % (nm, slug(nm), n))
    while len(cells) % cols:
        cells.append("")
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    out = ["|" + " |" * cols, "|" + " --- |" * cols]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out) + "\n"


def item_name(e, table, ov):
    """Display name for a table row.

    An overlay normally translates only a row's ``note``, but it may also
    rename the row itself — ``learning."CT Principles and Algorithms".name``
    exists precisely to show the Chinese title. Falls back to the English name
    in ``data/*.yaml``.
    """
    return ov.item(table, e["name"]).get("name") or e["name"]


def render_toolkits(items, ov):
    if not items:
        return ""
    items = sorted(items, key=lambda e: -(e.get("stars") or 0))
    rows = []
    for e in items:
        nm = "[**%s**](%s)" % (item_name(e, "toolkits", ov), url_of(e, "repo", "url"))
        note = ov.item("toolkits", e["name"]).get("note") or e.get("note", "")
        rows.append([nm, esc(e.get("language", "-")), str(e.get("stars", "-")),
                     esc(note)])
    return render_table([ov.ui("tableToolkit", "Toolkit"),
                         ov.ui("tableLanguage", "Language"),
                         ov.ui("tableStars", "Stars"),
                         ov.ui("tableDescription", "Description")], rows)


_MARKERS = (("**Projection + image.**", "proj + image"),
            ("**Projection only.**", "projections"))


def _dataset_kind(note):
    note = note or ""
    for m, kind in _MARKERS:
        if note.startswith(m):
            return kind, note[len(m):].strip()
    # The marker itself stays English in every language (see render_datasets),
    # but the sentence it introduces ends in "." in English and "。" in
    # Chinese, so both terminators have to be accepted.
    note = re.sub(r"\s*\*\*Image domain only\*\*[^.]*[.\u3002]", "", note).strip()
    return "image", note


def render_datasets(items, ov):
    if not items:
        return ""
    rows = []
    kind_labels = {"proj + image": ov.readme("kindProjImage", "proj + image"),
                   "projections": ov.readme("kindProjections", "projections"),
                   "image": ov.readme("kindImage", "image")}
    for e in items:
        # The leading marker is a data-format convention and stays English, so
        # it can be stripped here whatever language it sits in; the label shown
        # in the Data column is what gets translated.
        shown = ov.item("datasets", e["name"]).get("note") or e.get("note", "")
        kind, shown = _dataset_kind(shown)
        nm = "[**%s**](%s)" % (item_name(e, "datasets", ov), url_of(e, "url", "repo"))
        rows.append([nm, esc(e.get("modality", "-")), kind_labels.get(kind, kind),
                     esc(e.get("license", "-")), esc(shown)])
    return ov.readme("legendDatasets") + "\n\n" + render_table(
        [ov.ui("tableDataset", "Dataset"), ov.ui("tableModality", "Modality"),
         ov.readme("colData", "Data"), ov.ui("tableLicense", "License"),
         ov.ui("tableDescription", "Description")], rows)


def render_benchmarks(items, ov):
    if not items:
        return ""
    rows = []
    for e in sorted(items, key=lambda x: -(x.get("year") or 0)):
        nm = "[**%s**](%s)" % (item_name(e, "benchmarks", ov), url_of(e, "url", "repo"))
        note = ov.item("benchmarks", e["name"]).get("note") or e.get("note", "")
        rows.append([nm, str(e.get("year", "-")),
                     esc(", ".join(e.get("tasks") or []) or "-"),
                     esc(note)])
    return render_table([ov.ui("tableBenchmark", "Benchmark / Challenge"),
                         ov.ui("tableYear", "Year"), ov.ui("tableTasks", "Tasks"),
                         ov.ui("tableDescription", "Description")], rows)


LEARN_GROUPS = (("book", "learnBooks", "Books"), ("course", "learnCourses", "Courses"),
                ("tutorial", "learnTutorials", "Tutorials"),
                ("tool", "learnTools", "Tools"), ("list", "learnLists", "Other lists"))


def render_learning(items, ov):
    if not items:
        return ""
    out = []
    known = {k for k, _, _ in LEARN_GROUPS}
    groups = list(LEARN_GROUPS) + [("_other", "learnMore", "More")]
    for key, ikey, label in groups:
        g = [e for e in items if (e.get("type") == key) or
             (key == "_other" and e.get("type") not in known)]
        if not g:
            continue
        out.append("**%s**\n" % ov.readme(ikey, label))
        for e in sorted(g, key=lambda e: e["name"].lower()):
            note = ov.item("learning", e["name"]).get("note") or e.get("note", "")
            out.append("- [%s](%s) — %s"
                       % (item_name(e, "learning", ov), url_of(e, "url", "repo"),
                          note))
        out.append("")
    return "\n".join(out)


def build(meta, papers, toolkits, datasets, benchmarks, learning, ov, langs):
    subs = counts(papers, toolkits, datasets, benchmarks, learning)
    subs["repo"] = REPO
    subs["repo_url"] = "https://github.com/" + REPO
    subs["site_url"] = SITE_URL
    subs["title"] = ov.top("title") or DEFAULT_TITLE
    subs["tagline"] = ov.top("tagline")
    subs["content_license"] = "CC BY-NC-SA 4.0"
    subs["code_license"] = "MIT"
    subs["ncode"] = sum(1 for e in papers if e.get("code"))

    def badge(label, msg, color):
        q = lambda x: str(x).replace("-", "--").replace(" ", "%20").replace("_", "__")
        return "https://img.shields.io/badge/%s-%s-%s?style=flat-square" % (q(label), q(msg), color)

    heads = {}
    for key, default in (("papersHeading", "Papers"),
                         ("toolkitsHeading", "Toolkits"),
                         ("datasetsHeading", "Datasets"),
                         ("benchmarksHeading", "Benchmarks"),
                         ("learningHeading", "Learning"),
                         ("contactHeading", "Contact"),
                         ("licenseHeading", "License")):
        heads[key] = ov.readme(key, default)

    def anchor(key):
        return slug(heads[key])

    def head(key):
        return "## %s\n" % heads[key]

    # The seven-number stats strip. Every cell carries its own unit wording, so
    # a language can put the unit first, or drop the plural, without any of this
    # code having to know about it.
    cells = [fill(ov.readme("statPapersCell", "{papers} papers"), subs),
             fill(ov.readme("statPeerCell", "{peer_pct}% peer-reviewed"), subs),
             fill(ov.readme("statCodeCell", "{ncode} with code"), subs),
             fill(ov.readme("statToolkitsCell", "{toolkits} toolkits"), subs),
             fill(ov.readme("statDatasetsCell", "{datasets} datasets"), subs),
             fill(ov.readme("statBenchmarksCell", "{benchmarks} benchmarks"), subs),
             fill(ov.readme("statSpanCell", "{year_min}\u2013{year_max}"), subs)]
    strip = "| " + " | ".join(cells) + " |\n|" + "|".join([" :-: "] * len(cells)) + "|\n"

    nav = " \u00b7 ".join(
        ["**[{}]({})**".format(ov.readme("navWebsite", "Website"), SITE_URL)] +
        ["[%s](#%s)" % (heads[k], anchor(k))
         for k in ("papersHeading", "toolkitsHeading", "datasetsHeading",
                   "benchmarksHeading", "learningHeading")])

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
    parts.append(render_topic_grid(papers, meta, ov))
    parts.append(ov.readme("legendPapers", "") + "\n")
    parts.append(render_papers(papers, meta, ov))
    parts.append(top_link(ov))

    parts.append(head("toolkitsHeading"))
    parts.append(render_toolkits(toolkits, ov))
    parts.append(top_link(ov))

    parts.append(head("datasetsHeading"))
    parts.append(render_datasets(datasets, ov))
    parts.append(top_link(ov))

    parts.append(head("benchmarksHeading"))
    parts.append(render_benchmarks(benchmarks, ov))
    parts.append(top_link(ov))

    parts.append(head("learningHeading"))
    parts.append(render_learning(learning, ov))
    parts.append(top_link(ov))

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

    if not meta:
        sys.exit("data/meta.yaml is required")

    problems = validate(meta, papers, toolkits, datasets, benchmarks, learning)

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
    print("validation OK: %d papers / %d toolkits / %d datasets / %d benchmarks / %d learning"
          % (len(papers), len(toolkits), len(datasets), len(benchmarks), len(learning)))

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
                     ov, langs)
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
