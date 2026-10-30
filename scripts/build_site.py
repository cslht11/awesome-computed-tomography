#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the static website into site/.

Reads data/*.yaml (via export_site_data.build_payload, so the site and
README.md can never disagree) plus site.config.yml, and writes:

    site/index.html     the page; paper list is server-rendered so it works
                        without JavaScript and is crawlable
    site/styles.css
    site/search.js     the search core (shared by the paper tab and the top box)
    site/app.js
    site/data.json      the same payload as a standalone file
    site/robots.txt
    site/sitemap.xml
    site/.nojekyll
    site/CNAME          only when a custom domain is configured

Switching to a custom domain is a one-line change in site.config.yml followed
by a rebuild — every absolute URL (canonical, og:url, JSON-LD, sitemap,
robots.txt) is derived from that single origin.

Usage:
    python scripts/build_site.py
    python scripts/build_site.py --url https://ct-awesome.org/
"""

import argparse
import datetime
import hashlib
import html
import io
import json
import os
import re
import sys
from collections import Counter

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import load, validate, fill, validate_lineages  # noqa: E402
from export_site_data import build_payload  # noqa: E402
import i18n  # noqa: E402
import changelog  # noqa: E402
import resource_pages as RP  # noqa: E402
import brand_assets  # noqa: E402
import graph as graph_mod  # noqa: E402
import lineage_tree  # noqa: E402
import graph_slices as graph_slices_mod  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "site")
CONFIG = os.path.join(ROOT, "site.config.yml")

# The two legends used to be constants in build.py; they now live in
# data/i18n/en.yaml so the README can render them in any language. Until the
# site grows its own per-language pages it simply uses the English ones, and
# both outputs stay in step because they read the same source.
_EN = i18n.load(i18n.SOURCE)
PAPERS_LEGEND = _EN.readme("legendPapers", "")
DATASET_LEGEND = _EN.readme("legendDatasets", "")

PAPER_LINK_LABELS = ("paper", "code", "project", "data")

# ui.* keys that are inserted verbatim: they carry their own markup and would
# be broken by escaping. Everything else is HTML-escaped on the way out.
RAW_UI = {"footLegal", "pressSlash"}
# ui.* keys written as inline Markdown, so they may use `code`, **bold**,
# [link](url).
MD_UI = {"noscript"}
# The payload.ui key set (JS_UI) now lives in i18n.py, so the site build and
# the standalone data export publish identical `ui` dictionaries.

# <meta name="keywords"> when an overlay does not carry its own.
DEFAULT_KEYWORDS = ("computed tomography, CT reconstruction, sparse-view CT, "
                    "limited-angle tomography, low-dose CT, metal artifact reduction, "
                    "cone-beam CT, deep learning, awesome list")


# ------------------------------------------------------------------ helpers
def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_bytes(path, data):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(path, "wb") as f:
        f.write(data)


def esc(s):
    return html.escape(str(s), quote=True)


def md_inline(text):
    """The legends in build.py are Markdown; the site needs HTML. Same words,
    so the README and the page cannot drift apart."""
    out = esc(text)
    out = out.replace("`", "\x00")
    out = re.sub(r"\x00([^\x00]+)\x00", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = italics(out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


# *emphasis* and _emphasis_. Kept identical to mdInline() in web/app.js. The
# delimiters must sit at word edges, so snake_case names, URLs and products
# such as 3*4 are left alone (a scan of every note and legend found only
# intended emphasis when this was added).
_EM_STAR = re.compile(r"(?<![\w*])\*(?![\s*])([^*\n]+?)(?<!\s)\*(?![\w*])", re.ASCII)
_EM_UNDER = re.compile(r"(?<![\w])_(?![\s_])([^_\n]+?)(?<!\s)_(?![\w])", re.ASCII)


def italics(out):
    out = _EM_STAR.sub(r"<em>\1</em>", out)
    return _EM_UNDER.sub(r"<em>\1</em>", out)


def top_for(ov, code, key, fallback):
    """Top-level strings (tagline, description): English keeps the wording in
    site.config.yml, which is what the site has always shipped; the other
    languages take the overlay, falling back through English to that same value.
    """
    if code == i18n.SOURCE:
        return fallback
    return ov.top(key, fallback)


def ui_placeholder(key):
    """``menuAria`` -> ``{{UI_MENU_ARIA}}``."""
    return "{{UI_%s}}" % re.sub(r"(?<!^)(?=[A-Z])", "_", key).upper()


def ui_subs(ov, shared):
    """Every ``{{UI_*}}`` placeholder filled for one language.

    The key set comes from English, the source of truth, so a template cannot
    ask for a string that no translation will ever carry.
    """
    out = {}
    for key in sorted((i18n.load(i18n.SOURCE).data.get("ui") or {})):
        v = fill(ov.ui(key), shared)
        if key in MD_UI:
            v = md_inline(v)
        elif key not in RAW_UI:
            v = esc(v)
        out[ui_placeholder(key)] = v
    return out


def js_ui(ov):
    """payload.ui: the strings web/app.js renders at run time."""
    return i18n.js_ui(ov)


def abbr_title(p):
    """Mirror build.py: 'DM4CT: Benchmarking ...' -> abbr DM4CT + rest."""
    name = p.get("abbr")
    # Inline TeX like "$K$-NeAS" shows as plain text: drop the $ delimiters.
    title = re.sub(r"\$([^$]+)\$", r"\1", p["title"])
    if name and title.lower().startswith(name.lower()):
        rest = title[len(name):].lstrip(" :\u2014\u2013-")
        if rest:
            return name, rest
        return name, title
    return name, title


def safe_json(obj, indent=None):
    """JSON that is safe to inline in a <script> block.

    '<' cannot legally appear outside a string in JSON, so escaping every one
    of them as \\u003c is lossless and makes '</script>' (or '<!--') impossible.
    """
    text = json.dumps(obj, ensure_ascii=False, indent=indent,
                      separators=None if indent else (",", ":"))
    return text.replace("<", "\\u003c")


# ------------------------------------------------------------------ rendering
def page_payload(payload):
    """The payload as embedded in the homepage: paper blurbs left out,
    because render_static_papers() already puts each one in its title's
    `title=` and app.js reads them back from there. data.json keeps them."""
    out = dict(payload)
    out["papers"] = [dict((k, v) for k, v in p.items() if k != "blurb")
                     for p in payload["papers"]]
    return out


def render_static_papers(payload, ov):
    rows = []
    for p in payload["papers"]:
        name, title = abbr_title(p)
        # The title is plain text now: it used to be a link to the same URL as
        # the `paper` link below it. Where we have a blurb, `title=` gives
        # readers without JavaScript the browser's own tooltip, and app.js
        # upgrades it to a hover card when it runs.
        blurb = p.get("blurb")
        head = ""
        if name:
            head += '<span class="abbr">%s</span>' % esc(name)
        if blurb:
            # No aria-label: it would replace the title as the accessible
            # name, so a screen reader heard every paper as the same phrase.
            # This `title=` is also the only copy of the blurb in the page:
            # the embedded JSON leaves blurbs out and app.js reads them back
            # from here by data-id (they were ~200 KB stored twice).
            head += ('<span class="p-titletext has-blurb" tabindex="0"'
                     ' role="button" data-id="%s" title="%s">%s</span>'
                     % (esc(p["id"]), esc(blurb), esc(title)))
        else:
            head += '<span class="p-titletext">%s</span>' % esc(title)

        meta = ['<span class="venue%s">%s</span>'
                % (" is-preprint" if p["preprint"] else "",
                   esc(p["venue"] or ov.ui("venuePreprint", "preprint"))),
                '<span class="sep">\u00b7</span>',
                str(p["year"])]
        if p["topics"]:
            names = " \u00b7 ".join(
                dict((t["id"], t["name"]) for t in payload["topics"]).get(t, t)
                for t in p["topics"])
            meta += ['<span class="sep">\u00b7</span>',
                     '<span class="topics">%s</span>' % esc(names)]

        links = "".join(
            '<a href="%s" class="%s" target="_blank" rel="noopener">%s</a>'
            % (esc(p["links"][k]), k, k)
            for k in PAPER_LINK_LABELS if p["links"].get(k))

        rows.append(
            '<li class="paper">\n'
            '<p class="p-title">%s</p>\n'
            '<p class="p-meta">%s</p>\n'
            '<div class="p-links">%s</div>\n'
            '</li>' % (head, "".join(meta), links))
    return "\n".join(rows)


TEAM_REGIONS = (("north-america", "regionNorthAmerica", "North America"),
                ("europe", "regionEurope", "Europe"),
                ("asia", "regionAsia", "Asia"))


def render_static_teams(payload, ov):
    """Server-rendered team cards, grouped by region (like the paper list:
    readable and crawlable without JavaScript).

    Work references point at the work itself: a paper links to its primary
    URL (there is no /p/<id>/ page on this site), the other tables link to
    their tab, where the entry lives.
    """
    teams = payload.get("teams") or []
    if not teams:
        return ""
    by_id = dict((p["id"], p) for p in payload["papers"])
    topic_names = dict((t["id"], t["name"]) for t in payload["topics"])

    def work_links(tm):
        works = tm.get("works") or {}
        out = []
        for pid in works.get("papers") or []:
            p = by_id.get(pid)
            if not p:
                continue
            url = paper_url(p)
            label = esc(paper_label(p))
            out.append('<a href="%s" target="_blank" rel="noopener">%s</a>'
                       % (esc(url), label) if url else label)
        for table in ("toolkits", "datasets", "benchmarks"):
            for n in works.get(table) or []:
                out.append('<a href="?tab=%s">%s</a>' % (table, esc(n)))
        return out

    bits = []
    for region, key, default in TEAM_REGIONS:
        group = [tm for tm in teams if tm["region"] == region]
        if not group:
            continue
        bits.append('<h3 class="region-head">%s</h3>'
                    % esc(ov.ui(key, default)))
        bits.append('<ul class="teams">')
        for tm in group:
            name = tm.get("label") or tm["name"]
            head = '<a href="%s" target="_blank" rel="noopener">%s</a>' \
                % (esc(tm["homepage"]), esc(name))
            if tm.get("name_zh"):
                head += ' <span class="t-namezh">%s</span>' % esc(tm["name_zh"])
            if tm["status"] == "legacy":
                head += ' <span class="t-badge">%s</span>' \
                    % esc(ov.ui("teamsLegacy", "Legacy"))
            where = " \u00b7 ".join(x for x in (tm["institution"],
                                               ", ".join(y for y in
                                                         (tm["city"], tm["country"]) if y)) if x)
            meta = ['<span class="t-where">%s</span>' % esc(where)]
            meta += ['<span class="sep">\u00b7</span>',
                     '<span class="t-pi">%s %s</span>'
                     % (esc(ov.ui("teamsLead", "Led by")),
                        esc(", ".join(tm["pi"])))]
            if tm["focus"]:
                meta += ['<span class="sep">\u00b7</span>',
                         '<span class="topics">%s</span>' % esc(" \u00b7 ".join(
                             topic_names.get(t, t) for t in tm["focus"]))]
            rows = ['<li class="team" id="team-%s">' % esc(tm["id"]),
                    '<p class="t-name">%s</p>' % head,
                    '<p class="t-meta">%s</p>' % "".join(meta),
                    '<p class="t-intro">%s</p>' % esc(tm["intro"])]
            links = work_links(tm)
            if links:
                rows.append('<p class="t-works"><span class="t-works-label">%s</span> %s</p>'
                            % (esc(ov.ui("teamsInLibrary", "In this library:")),
                               " \u00b7 ".join(links)))
            if tm.get("software"):
                rows.append('<p class="t-software">%s</p>' % md_inline(tm["software"]))
            rows.append("</li>")
            bits.append("\n".join(rows))
        bits.append("</ul>")
    return "\n".join(bits)


def render_head(cfg, payload, base, root, entry, langs, ov, tokens):
    """``base`` is this language's own canonical URL, ``root`` the site origin
    the hreflang alternates are built from. ``tokens`` holds the live counts,
    so a description can say {papers} instead of a number that goes stale."""
    c = payload["counts"]
    title = top_for(ov, entry["code"], "title", cfg["title"])
    # Counts are filled in rather than written out: a description that spells
    # out "289 papers" is stale the moment the next paper lands, and this text
    # is what search engines show. site.config.yml's own description carries no
    # placeholders, so filling it is a no-op.
    desc = re.sub(r"\s+", " ",
                  fill(top_for(ov, entry["code"], "description",
                               cfg["description"]), tokens)).strip()
    canonical = base
    default = i18n.default_language(langs)
    hreflang = "".join(
        '<link rel="alternate" hreflang="%s" href="%s">'
        % (esc(e["hreflang"]), esc(i18n.url_for(root, e)))
        for e in langs)
    hreflang += ('<link rel="alternate" hreflang="x-default" href="%s">'
                 % esc(i18n.url_for(root, default)))
    ld_org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": base + "#organization",
        "name": cfg["title"],
        "url": base,
        "sameAs": [cfg["repo_url"]],
    }
    ld_site = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": title,
        "url": base,
        "description": desc,
        "inLanguage": entry["hreflang"],
        "publisher": {"@id": base + "#organization"},
        "license": cfg["content_license_url"],
        "copyrightHolder": {"@id": base + "#organization"},
    }
    # No ItemList of the papers: every item pointed off-site (DOIs, arXiv),
    # which no search feature uses, and it was the page's third copy of the
    # titles (~120 KB). The DataCatalog below and data.json describe them.

    ld_catalog = render_datacatalog(cfg, payload, base, entry, ov, tokens,
                                    title, desc)

    bits = [
        "<title>%s \u2014 %s</title>" % (esc(title), esc(top_for(ov, entry["code"], "tagline", cfg["tagline"]))),
        '<meta name="description" content="%s">' % esc(desc),
        '<link rel="canonical" href="%s">' % esc(canonical),
        hreflang,
        '<meta name="robots" content="index,follow,max-snippet:180,max-image-preview:large">',
        '<meta name="googlebot" content="index,follow,max-snippet:180,max-image-preview:large">',
        '<meta name="author" content="%s">' % esc(cfg.get("author", "")),
        '<meta name="keywords" content="%s">'
        % esc(re.sub(r"\s+", " ", ov.top("keywords", DEFAULT_KEYWORDS)).strip()),
        '<meta property="og:site_name" content="%s">' % esc(title),
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="%s">' % esc(canonical),
        '<meta property="og:title" content="%s \u2014 %s">' % (esc(title), esc(top_for(ov, entry["code"], "tagline", cfg["tagline"]))),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:locale" content="%s">' % esc(entry["og_locale"]),
        brand_assets.head_brand(root),
        '<meta name="twitter:title" content="%s \u2014 %s">' % (esc(title), esc(top_for(ov, entry["code"], "tagline", cfg["tagline"]))),
        '<meta name="twitter:description" content="%s">' % esc(desc),
        '<link rel="license" href="%s">' % esc(cfg["content_license_url"]),
        '<link rel="alternate" type="application/json" href="./data.json" title="Machine-readable dataset">',
        '<script type="application/ld+json">%s</script>' % safe_json(ld_org),
        '<script type="application/ld+json">%s</script>' % safe_json(ld_site),
        '<script type="application/ld+json">%s</script>' % safe_json(ld_catalog),
    ]

    # Search-engine ownership tags (Google Search Console HTML-tag method).
    # Removing this un-verifies the site, so keep it.
    gsv = cfg.get("google_site_verification")
    if gsv:
        bits.append('<meta name="google-site-verification" content="%s">' % esc(gsv))
    msv = cfg.get("bing_site_verification")
    if msv:
        bits.append('<meta name="msvalidate.01" content="%s">' % esc(msv))

    token = cfg.get("analytics_token")
    if token:
        bits.append(
            "<script>if(location.hostname===new URL(%s).hostname){"
            "var s=document.createElement('script');"
            "s.src='https://static.cloudflareinsights.com/beacon.min.js';"
            "s.dataset.cfBeacon=JSON.stringify({token:%s});"
            "document.head.appendChild(s);}</script>"
            % (json.dumps(base), json.dumps(token)))
    return "\n".join(bits)


def render_datacatalog(cfg, payload, base, entry, ov, tokens, title, desc):
    """Homepage DataCatalog JSON-LD.

    Every number is filled from the live payload (the same counts as the stat
    tiles), dateModified is data/meta.yaml's last_updated (the "Updated" tile),
    and name/description are the page's own <title> and meta description, so
    the structured data cannot say anything the page does not. The three
    datasets are the three tables the homepage shows: papers, datasets and
    benchmarks.
    """
    org = {"@id": base + "#organization"}
    updated = str(tokens["updated"])
    common = {
        "inLanguage": entry["hreflang"],
        "license": cfg["content_license_url"],
        "isAccessibleForFree": True,
        "creator": org,
        "publisher": org,
        "dateModified": updated,
        "distribution": {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": base + "data.json",
        },
    }

    def dataset(key, url):
        d = {
            "@type": "Dataset",
            "@id": base + "#dataset-" + key,
            "name": ov.ui("ld%sName" % key.title()),
            "description": re.sub(r"\s+", " ", fill(ov.ui("ld%sDesc" % key.title()), tokens)).strip(),
            "url": url,
        }
        d.update(common)
        return d

    return {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "@id": base + "#datacatalog",
        "name": title,
        "url": base,
        "description": desc,
        "inLanguage": entry["hreflang"],
        "license": cfg["content_license_url"],
        "isAccessibleForFree": True,
        "dateModified": updated,
        "creator": org,
        "publisher": org,
        "dataset": [
            dataset("papers", base),
            dataset("datasets", base + "?tab=datasets"),
            dataset("benchmarks", base + "?tab=benchmarks"),
        ],
    }


PAGES = ("about", "contact", "privacy")


def render_sitemap(urls, lastmod):
    body = "".join(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>\n"
        % (esc(u), lastmod, f, pr) for u, f, pr in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + '</urlset>\n')


def render_robots(base):
    return "User-agent: *\nAllow: /\nCrawl-delay: 1\n\nSitemap: %ssitemap.xml\n" % base


def render_llms(cfg, base, c, topics, topic_pages=(), rp_pages=(), rp_guides=(), payload=None, lineages=()):
    """site/llms.txt: a plain-Markdown map of the site for AI answer engines
    (llmstxt.org proposal). Counts and topics come from the same payload as the
    page, so it cannot go stale. Cheap to ship; its effect is unproven."""
    lines = [
        "# %s" % cfg["title"], "",
        "> A curated, verified directory of computed tomography (CT / CBCT /",
        "> micro-CT) reconstruction research: %d papers (%d-%d), %d toolkits,"
        % (c["papers"], c["year_min"], c["year_max"], c["toolkits"]),
        "> %d datasets, %d benchmarks and %d learning resources, grouped by"
        % (c["datasets"], c["benchmarks"], c["learning"]),
        "> problem and method family. Content licence: %s." % cfg["content_license"],
        "",
        "Entries are checked against Crossref, arXiv and publisher records. "
        "Last updated %s." % c["updated"], "",
        "## Directory", "",
        "- [Paper directory (English)](%s): searchable list of all papers, "
        "toolkits, datasets and benchmarks" % base,
        "- [Research teams](%s?tab=teams): %d research groups and labs behind "
        "the papers, toolkits and datasets in this directory"
        % (base, c.get("teams", 0)),
        "- [Knowledge graph](%sgraph/): how the papers, toolkits, datasets, "
        "benchmarks, teams, topics and authors in this directory connect, "
        "as small per-category graphs: a team backbone, dataset relations "
        "and one graph per topic (Chinese edition: %szh/graph/)"
        % (base, base),
        "- [Team backbone graph](%sgraph/backbone/): the knowledge graph's "
        "backbone — research teams, topics, toolkits and guides, and how "
        "they connect" % base,
        "- [Dataset relations graph](%sgraph/datasets/): which papers in "
        "the directory use which datasets and benchmarks, as a graph" % base,
    ]
    for lin in lineages or ():
        lines.append("- [Curated lineage: %s](%sgraph/lineage/%s/): %s "
                     "(Chinese edition: %szh/graph/lineage/%s/)"
                     % (lin_text(lin["title"], i18n.SOURCE), base, lin["id"],
                        re.sub(r"\s+", " ",
                               lin_text(lin["description"], i18n.SOURCE)).strip(),
                        base, lin["id"]))
    lines += [
        "- [论文目录（中文）](%szh/): Chinese edition of the same directory" % base,
        "- [About](%sabout/): scope, sourcing, verification and how to cite" % base,
        "- [Contact](%scontact/): how to suggest or correct an entry" % base,
        "- [Changelog](%schangelog/): every dated change to the list and the "
        "site, newest first (Chinese edition: %szh/changelog/)" % (base, base),
        "", "## Data", "",
        "- [data.json](%sdata.json): machine-readable export of the full "
        "catalogue (English)" % base,
        "- [data.json (中文)](%szh/data.json): the same catalogue with Chinese "
        "notes" % base,
        "- [GitHub repository](%s): source YAML data; the site is generated "
        "from it" % cfg["repo_url"],
        "", "## Topics", "",
    ]
    for t in topics:
        if t["id"] in topic_pages:
            lines.append("- [%s](%stopics/%s/) (%d papers): %s"
                         % (t["name"], base, t["id"], t["count"], t["desc"]))
        else:
            lines.append("- %s (%d papers): %s" % (t["name"], t["count"], t["desc"]))
    if topic_pages:
        lines += ["", "Each linked topic page is a guide: a short introduction, "
                  "a start-here reading list, the topic's newest papers and the "
                  "matching datasets, benchmarks and toolkits. Chinese editions "
                  "are at %szh/topics/<topic>/." % base]
    if rp_guides:
        lines += ["", "## Guides", "",
                  "- [Guides index](%sguides/): practical guides built from the "
                  "directory (Chinese editions under %szh/guides/)" % (base, base)]
        for g in rp_guides:
            lines.append("- [%s](%sguides/%s/): %s"
                         % (g["en"]["title"], base, g["slug"], re.sub(r"\s+", " ", g["en"]["description"]).strip()))
    if rp_pages:
        rows = dict(((t, r["name"]), r) for t in ("datasets", "benchmarks") for r in payload[t])
        lines += ["", "## Datasets and benchmarks", "",
                  "- [Datasets and benchmarks index](%sdatasets/): every dataset and "
                  "benchmark with a page of its own (Chinese editions under %szh/)" % (base, base)]
        for pg in rp_pages:
            r = rows[(pg["table"], pg["name"])]
            bits = [x for x in (r.get("modality"), r.get("license"),
                                str(r["year"]) if pg["table"] == "benchmarks" and r.get("year") else None) if x]
            lines.append("- [%s](%s%s) (%s%s)" % (pg["name"], base, pg["rel"],
                         "dataset" if pg["table"] == "datasets" else "benchmark",
                         (", " + ", ".join(bits)) if bits else ""))
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------- topic pages
# One hub page per topic at /topics/<id>/ (and /zh/topics/<id>/). The prose
# (intro, "Start here" reasons, page strings) is hand-written in
# data/topics.yaml; the paper table, counts and related resources come from the
# same payload as the directory, so a page cannot fall out of step with it.
TOPICS_FILE = os.path.join(ROOT, "data", "topics.yaml")
# A catch-all is not a topic worth a hub page, and `related` is outside the
# list's scope (context only), so neither gets one.
TOPIC_SKIP = ("other", "related")
TOPIC_PAPER_CAP = 30
RESOURCE_TABLES = (("datasets", "tasks", "kindDataset"),
                   ("benchmarks", "tasks", "kindBenchmark"),
                   ("toolkits", "tags", "kindToolkit"))


def load_topic_pages(payload):
    """data/topics.yaml, checked against the payload so a renamed paper id or
    dataset name fails the build instead of silently vanishing from a page."""
    if not os.path.exists(TOPICS_FILE):
        return None
    with io.open(TOPICS_FILE, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    pages = doc.get("topics") or {}
    known = [t["id"] for t in payload["topics"]]
    paper_ids = set(p["id"] for p in payload["papers"])
    names = dict((tbl, set(r["name"] for r in payload[tbl]))
                 for tbl, _, _ in RESOURCE_TABLES)
    problems = []
    for tid, tp in pages.items():
        where = "data/topics.yaml: topic '%s'" % tid
        if tid not in known:
            problems.append("%s is not in data/meta.yaml" % where)
            continue
        for s in tp.get("start") or []:
            if s.get("id") not in paper_ids:
                problems.append("%s: start paper '%s' does not exist" % (where, s.get("id")))
        for tbl, extra in (tp.get("also") or {}).items():
            if tbl not in names:
                problems.append("%s: also.%s is not a table" % (where, tbl))
                continue
            for n in extra or []:
                if n not in names[tbl]:
                    problems.append("%s: also.%s '%s' does not exist" % (where, tbl, n))
        for lang in ("en", "zh"):
            for k in ("title", "description", "intro"):
                if not ((tp.get(lang) or {}).get(k) or "").strip():
                    problems.append("%s: %s.%s is empty" % (where, lang, k))
    for tid in known:
        if tid not in TOPIC_SKIP and tid not in pages:
            problems.append("data/topics.yaml: topic '%s' has no entry" % tid)
    if problems:
        print("TOPIC DATA INVALID:")
        for x in problems:
            print("  -", x)
        sys.exit(1)
    return doc


def topic_text(tp, code, key):
    """A topic's own text in this language, falling back to English."""
    return ((tp.get(code) or {}).get(key) or (tp.get(i18n.SOURCE) or {}).get(key) or "").strip()


def topic_strings(doc, code):
    s = dict((doc.get("strings") or {}).get(i18n.SOURCE) or {})
    s.update((doc.get("strings") or {}).get(code) or {})
    return s


def short_note(text, limit=240):
    """First sentence or two of a directory note, for a one-line list item."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    out = ""
    for sent in re.split(r"(?<=[.!?。])\s+", text):
        if out and len(out) + len(sent) + 1 > limit:
            break
        out = (out + " " + sent).strip()
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0] + "\u2026"
    return out


def topic_resources(tp, payload):
    want = set(m.lower() for m in (tp.get("match") or []))
    also = tp.get("also") or {}
    out = []
    for tbl, field, kind in RESOURCE_TABLES:
        extra = set(also.get(tbl) or [])
        for r in payload[tbl]:
            tags = set(str(x).lower() for x in (r.get(field) or []))
            if (tags & want) or r["name"] in extra:
                out.append((kind, r))
    return out


def paper_url(p):
    l = p["links"]
    return l.get("paper") or l.get("project") or l.get("code") or l.get("data")


def paper_label(p):
    name, rest = abbr_title(p)
    if rest.startswith(","):
        # "LoDoPaB-CT, a benchmark dataset ..." is not "LoDoPaB-CT: , a ...".
        return re.sub(r"\$([^$]+)\$", r"\1", p["title"])
    return ("%s: %s" % (name, rest)) if name and rest != p["title"] and rest != name else (
        re.sub(r"\$([^$]+)\$", r"\1", p["title"]))


def topic_url(lang_base, tid):
    return "%stopics/%s/" % (lang_base, tid)


def render_topic_body(tid, tp, payload, code, s, ov, res_pages=None, guides=None, rs=None):
    """The <main> of one topic page. Links are relative ({{ROOT}} is ../../)."""
    topic = dict((t["id"], t) for t in payload["topics"])[tid]
    papers = [p for p in payload["papers"] if tid in p["topics"]]
    n = len(papers)
    shown = papers[:TOPIC_PAPER_CAP]
    by_id = dict((p["id"], p) for p in payload["papers"])
    pre = s.get("preprint", "preprint")
    fmt = lambda key, **kw: esc(s.get(key, "").replace("{n}", str(kw.get("n", n)))
                                .replace("{shown}", str(kw.get("shown", len(shown))))
                                .replace("{name}", kw.get("name", topic["name"])))

    def venue(p):
        return esc(p["venue"]) if p["venue"] else '<em>%s</em>' % esc(pre)

    def links(p):
        return " \u00b7 ".join(
            '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(p["links"][k]), k)
            for k in PAPER_LINK_LABELS if p["links"].get(k))

    def ext(url, text):
        if not url:
            return esc(text)
        return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(text))

    out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
           '<a href="{{ROOT}}">%s</a> / <a href="{{ROOT}}topics/">%s</a></p></nav>'
           % (esc(s.get("home", "Home")), esc(s.get("kicker", "Topic"))),
           '<h1>%s</h1>' % esc(topic["name"])]
    paras = [x.strip() for x in re.split(r"\n\s*\n", topic_text(tp, code, "intro")) if x.strip()]
    for i, para in enumerate(paras):
        out.append('<p%s>%s</p>' % (' class="lede"' if i == 0 else "",
                                    esc(re.sub(r"\s+", " ", para))))
    out.append('<p><a href="{{ROOT}}?topic=%s">%s</a></p>' % (esc(tid), fmt("viewAll")))

    start = tp.get("start") or []
    if start:
        out += ['<h2 id="start-here">%s</h2>' % esc(s.get("startHere", "Start here")),
                '<p>%s</p>' % esc(s.get("startHereLede", "")), "<ul>"]
        for item in start:
            p = by_id[item["id"]]
            why = (item.get(code) or item.get(i18n.SOURCE) or "").strip()
            extra = ""
            if p["links"].get("code"):
                extra = ' \u00b7 <a href="%s" target="_blank" rel="noopener">code</a>' % esc(p["links"]["code"])
            out.append('<li><strong>%s</strong> <span class="sep">(%s, %d%s)</span><br>%s</li>'
                       % (ext(paper_url(p), paper_label(p)), venue(p), p["year"], extra, esc(why)))
        out.append("</ul>")

    out += ['<h2 id="papers">%s</h2>' % esc(s.get("papers", "Papers")),
            '<p>%s</p>' % (fmt("papersLede") if n > len(shown) else fmt("papersLedeAll")),
            '<table class="grid"><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>'
            % (esc(s["colPaper"]), esc(s["colVenue"]), esc(s["colYear"]), esc(s["colLinks"]))]
    for p in shown:
        out.append('<tr><td>%s</td><td data-label="%s">%s</td><td class="n" data-label="%s">%d</td>'
                   '<td data-label="%s">%s</td></tr>'
                   % (ext(paper_url(p), paper_label(p)), esc(s["colVenue"]), venue(p),
                      esc(s["colYear"]), p["year"], esc(s["colLinks"]), links(p)))
    out.append("</tbody></table>")
    out.append('<p><a href="{{ROOT}}?topic=%s">%s</a></p>' % (esc(tid), fmt("viewAll")))

    res = topic_resources(tp, payload)
    if res:
        out += ['<h2 id="resources">%s</h2>' % esc(s.get("resources", "")),
                '<p>%s</p>' % esc(s.get("resourcesLede", "")), "<ul>"]
        for kind, r in res:
            note = short_note(r.get("note") or "")
            own = (res_pages or {}).get((kind, r["name"]))
            if own:
                # A dataset or benchmark with a page of its own: link the page,
                # keep the official site one click away.
                name = ('<a href="{{ROOT}}%s">%s</a>' % (own, esc(r.get("label") or r["name"]))
                        + ' <span class="sep">(%s)</span>' % ext(r.get("url"), (rs or {}).get("official", "official page")))
            else:
                name = ext(r.get("url"), r.get("label") or r["name"])
            out.append('<li><strong>%s</strong> <span class="sep">\u00b7 %s</span>%s</li>'
                       % (name, esc(s.get(kind, "")),
                          (" \u2014 " + md_inline(note)) if note else ""))
        out.append("</ul>")

    if guides:
        out += ['<h2 id="guides">%s</h2>' % esc((rs or {}).get("topicGuides", "Guides")),
                '<p>%s</p>' % esc((rs or {}).get("topicGuidesLede", "")), "<ul>"]
        for slug, gtitle in guides:
            out.append('<li><a href="{{ROOT}}guides/%s/">%s</a></li>' % (esc(slug), esc(gtitle)))
        out.append("</ul>")

    out += ['<h2 id="topics">%s</h2>' % esc(s.get("siblings", "Other topics")),
            render_topic_links(payload, tid, "{{ROOT}}")]
    return "\n".join(out)


def render_topics_index(payload, topic_ids, s):
    """The <main> of /topics/: every topic hub page with its paper count and
    one-line description. Links are relative ({{ROOT}} is ../)."""
    by_id = dict((t["id"], t) for t in payload["topics"])
    out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
           '<a href="{{ROOT}}">%s</a> / %s</p></nav>'
           % (esc(s.get("home", "Home")), esc(s.get("kicker", "Topic"))),
           '<h1>%s</h1>' % esc(s.get("indexTitle", "Topics")),
           '<p class="lede">%s</p>' % esc(s.get("indexLede", "")),
           '<ul class="topic-index">']
    for tid in topic_ids:
        t = by_id[tid]
        desc = (" \u2014 %s" % esc(t["desc"])) if t.get("desc") else ""
        out.append('<li><a href="{{ROOT}}topics/%s/">%s</a> <span class="sep">(%d)</span>%s</li>'
                   % (esc(tid), esc(t["name"]), t["count"], desc))
    out.append("</ul>")
    return "\n".join(out)


def render_topic_links(payload, current, root):
    """The list of topic hub pages, used on every topic page and on About."""
    items = []
    for t in payload["topics"]:
        if t["id"] in TOPIC_SKIP or t["id"] == current:
            continue
        items.append('<li><a href="%stopics/%s/">%s</a> <span class="sep">(%d)</span></li>'
                     % (root, esc(t["id"]), esc(t["name"]), t["count"]))
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def head_extra_topic(cfg, base, langs, entry, tid, title, desc, payload):
    """hreflang alternates + og + JSON-LD for one topic page."""
    default = i18n.default_language(langs)
    url = topic_url(i18n.url_for(base, entry), tid)
    bits = ['<link rel="alternate" hreflang="%s" href="%s">'
            % (esc(e["hreflang"]), esc(topic_url(i18n.url_for(base, e), tid))) for e in langs]
    bits.append('<link rel="alternate" hreflang="x-default" href="%s">'
                % esc(topic_url(i18n.url_for(base, default), tid)))
    bits += ['<meta property="og:type" content="website">',
             '<meta property="og:url" content="%s">' % esc(url),
             '<meta property="og:title" content="%s">' % esc(title),
             '<meta property="og:description" content="%s">' % esc(desc),
             '<meta property="og:locale" content="%s">' % esc(entry["og_locale"])]
    bits.append(brand_assets.head_brand(base))
    home = i18n.url_for(base, entry)
    topic = dict((t["id"], t) for t in payload["topics"])[tid]
    papers = [p for p in payload["papers"] if tid in p["topics"]][:TOPIC_PAPER_CAP]
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": cfg["title"], "item": home},
            {"@type": "ListItem", "position": 2, "name": topic["name"], "item": url},
        ],
    }
    coll = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "@id": url, "url": url, "name": title, "description": desc,
        "inLanguage": entry["hreflang"],
        "isPartOf": {"@type": "WebSite", "name": cfg["title"], "url": home},
        "about": {"@type": "Thing", "name": topic["name"]},
        "license": cfg["content_license_url"],
        "mainEntity": {
            "@type": "ItemList", "numberOfItems": len(papers),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": re.sub(r"\$([^$]+)\$", r"\1", p["title"]),
                 "url": paper_url(p) or url}
                for i, p in enumerate(papers)],
        },
    }
    bits.append('<script type="application/ld+json">%s</script>' % safe_json(crumbs))
    bits.append('<script type="application/ld+json">%s</script>' % safe_json(coll))
    return "\n".join(bits)


def faq_jsonld(html_):
    """FAQPage JSON-LD built from the visible FAQ on the About page, so the
    structured data can never say something the page does not."""
    m = re.search(r'<section class="faq"[^>]*>(.*?)</section>', html_, re.S)
    if not m:
        return None, 0
    pairs = re.findall(r"<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>", m.group(1), re.S)

    def text(h):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": text(q),
                          "acceptedAnswer": {"@type": "Answer", "text": text(a)}}
                         for q, a in pairs]}
    return '<script type="application/ld+json">%s</script>' % safe_json(ld), len(pairs)


# ---------------------------------------------------------- changelog page
# /changelog/ and /zh/changelog/, generated from CHANGELOG.md on every build
# (scripts/changelog.py parses it). The entries are written in English; a
# translated edition reads each entry's translation from that language's
# CHANGELOG.<suffix>.md (e.g. CHANGELOG.zh-CN.md) and shows any entry not yet
# translated in English, with a note saying how many.
CHANGELOG_PATH = "changelog/"


def changelog_for(entries, entry):
    """(entries for this language, number left in English)."""
    if entry["code"] == i18n.SOURCE:
        return entries, 0
    path = os.path.join(ROOT, entry["changelog"])
    try:
        out, missing = changelog.translate(
            entries, changelog.load_translations(path), entry["html"], path)
    except changelog.ChangelogError as e:
        sys.exit(str(e))
    return out, len(missing)


def render_changelog_body(entries, code, ov, strings, cfg, page_lang=None, untranslated=0,
                          translation_file=None):
    first, latest = entries[-1]["date"].isoformat(), entries[0]["date"].isoformat()
    src = '<a href="%s/blob/main/CHANGELOG.md" target="_blank" rel="noopener"><code>CHANGELOG.md</code></a>' % esc(cfg["repo_url"])
    # A translated edition also links its translation file ({translation}).
    tsrc = ""
    if translation_file:
        tsrc = ('<a href="%s/blob/main/%s" target="_blank" rel="noopener"><code>%s</code></a>'
                % (esc(cfg["repo_url"]), esc(translation_file), esc(translation_file)))
    counts = esc(ov.ui("changelogEntries")).replace("{n}", str(len(entries))) \
        .replace("{first}", first).replace("{latest}", latest)
    body = changelog.render_entries(entries, cfg["repo_url"], page_lang)
    # The entries quote template placeholders such as {{N_PAPERS}} in code
    # spans; neutralise every brace so the page substitution leaves them alone.
    body = body.replace("{", "&#123;").replace("}", "&#125;")
    title = ov.ui("pageChangelogTitle", "Changelog")
    out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
           '<a href="{{ROOT}}">%s</a> / %s</p></nav>' % (esc(strings.get("home", "Home")), esc(title)),
           "<h1>%s</h1>" % esc(title),
           '<p class="lede">%s</p>' % esc(ov.ui("changelogLede")),
           "<p>%s %s</p>" % (esc(ov.ui("changelogSource")).replace("{source}", src)
                             .replace("{translation}", tsrc), counts)]
    if untranslated:
        out.append("<p>%s</p>" % esc(ov.ui("changelogUntranslated"))
                   .replace("{n}", str(untranslated)))
    out += ['<div class="changelog">', body, "</div>"]
    return "\n".join(out)


def head_extra_changelog(cfg, base, langs, entry, ov, desc):
    """hreflang alternates + og + BreadcrumbList for the changelog page."""
    default = i18n.default_language(langs)
    home = i18n.url_for(base, entry)
    url = home + CHANGELOG_PATH
    title = "%s \u2014 %s" % (ov.ui("pageChangelogTitle", "Changelog"),
                               top_for(ov, entry["code"], "title", cfg["title"]))
    bits = ['<link rel="alternate" hreflang="%s" href="%s">'
            % (esc(e["hreflang"]), esc(i18n.url_for(base, e) + CHANGELOG_PATH)) for e in langs]
    bits.append('<link rel="alternate" hreflang="x-default" href="%s">'
                % esc(i18n.url_for(base, default) + CHANGELOG_PATH))
    bits += ['<meta property="og:type" content="website">',
             '<meta property="og:url" content="%s">' % esc(url),
             '<meta property="og:title" content="%s">' % esc(title),
             '<meta property="og:description" content="%s">' % esc(desc),
             '<meta property="og:locale" content="%s">' % esc(entry["og_locale"])]
    bits.append(brand_assets.head_brand(base))
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "name": top_for(ov, entry["code"], "title", cfg["title"]), "item": home},
            {"@type": "ListItem", "position": 2,
             "name": ov.ui("pageChangelogTitle", "Changelog"), "item": url},
        ],
    }
    bits.append('<script type="application/ld+json">%s</script>' % safe_json(crumbs))
    return "\n".join(bits)


# ------------------------------------------------------------ graph pages
# /graph/ and /zh/graph/: the knowledge graph, split into small
# per-category graphs (user decision, 2026-10-22: the single-page
# 1,004-node graph was too big and too slow to use). /graph/ itself is
# now an index of category cards; each category is its own page —
# /graph/backbone/, /graph/datasets/, /graph/topic/<id>/ — loading
# only its own slice (scripts/graph.py projects the full graph,
# scripts/graph_slices.py cuts it and precomputes positions with
# scripts/graph_layout.py, web/graph.js renders one slice with the
# vendored sigma.js — WebGL, batched, no runtime force simulation
# anywhere, and no full-graph mode anywhere). Each page degrades to a
# static list of its entries when JavaScript or the vendor files are
# unavailable, so no build state can ship a blank page.
GRAPH_PATH = "graph/"


def head_extra_graph(cfg, base, langs, entry, ov, desc, rel=GRAPH_PATH,
                     title=None, parent=False):
    """hreflang alternates + og + brand + BreadcrumbList for a graph page.

    `rel` is the page's path under the language root ("graph/" for the
    index, "graph/backbone/" etc. for a category page); `title` is the
    page's own title (the index defaults to the graph title); `parent`
    adds the graph index as a middle breadcrumb on category pages.
    """
    default = i18n.default_language(langs)
    home = i18n.url_for(base, entry)
    url = home + rel
    site_title = top_for(ov, entry["code"], "title", cfg["title"])
    if title is None:
        title = ov.ui("pageGraphTitle", "Knowledge Graph")
    bits = ['<link rel="alternate" hreflang="%s" href="%s">'
            % (esc(e["hreflang"]), esc(i18n.url_for(base, e) + rel)) for e in langs]
    bits.append('<link rel="alternate" hreflang="x-default" href="%s">'
                % esc(i18n.url_for(base, default) + rel))
    bits += ['<meta property="og:type" content="website">',
             '<meta property="og:url" content="%s">' % esc(url),
             '<meta property="og:title" content="%s">'
             % esc("%s \u2014 %s" % (title, site_title)),
             '<meta property="og:description" content="%s">' % esc(desc),
             '<meta property="og:locale" content="%s">' % esc(entry["og_locale"])]
    bits.append(brand_assets.head_brand(base))
    items = [{"@type": "ListItem", "position": 1,
              "name": site_title, "item": home}]
    if parent:
        items.append({"@type": "ListItem", "position": 2,
                      "name": ov.ui("pageGraphTitle", "Knowledge Graph"),
                      "item": home + GRAPH_PATH})
    items.append({"@type": "ListItem", "position": len(items) + 1,
                  "name": title, "item": url})
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": items}
    bits.append('<script type="application/ld+json">%s</script>' % safe_json(crumbs))
    return "\n".join(bits)


def lin_text(field, code):
    """A {en, zh} text field from data/lineages.yaml in this language.

    build.py's validate_lineages guarantees both languages are present,
    so the English fallback here is only a belt over those braces.
    """
    if isinstance(field, dict):
        return (field.get(code) or field.get(i18n.SOURCE) or "").strip()
    return str(field or "").strip()


def lin_rich(text):
    """Lineage prose is written with light Markdown emphasis; render it
    like the legends (md_inline) plus the single-star emphasis that
    md_inline does not handle."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", md_inline(text))


def render_lineage_body(payload, ov, code, lineage):
    """The <main> of one /graph/lineage/<id>/ page: the family tree on
    a pan/zoom canvas, with every node's full text in a reading list
    below it. Card facts come from the payload, never the data file."""
    by_id = dict((p["id"], p) for p in payload["papers"])
    # normalize_nodes: v2 tree data passes through; the retired v1 chain
    # shape is synthesized into a single-chain tree (push sequencing).
    nodes = lineage_tree.normalize_nodes(lineage)
    by_key = dict((n["key"], n) for n in nodes)
    pos, edges, width, height = lineage_tree.layout(nodes)
    num = lineage_tree.num

    def head_of(p):
        url = paper_url(p)
        label = esc(paper_label(p))
        return ('<a href="%s" target="_blank" rel="noopener">%s</a>'
                % (esc(url), label)) if url else label

    def meta_of(p):
        # "venue · year", or the year alone for a preprint.
        return ("%s \u00b7 %d" % (esc(p["venue"]), p["year"])) if p["venue"] \
            else str(p["year"])

    def links_of(p):
        return " \u00b7 ".join(
            '<a href="%s" target="_blank" rel="noopener">%s</a>'
            % (esc(p["links"][k]), k.capitalize())
            for k in PAPER_LINK_LABELS if p["links"].get(k))

    def prose_of(n, cls):
        return ('<p class="%s">%s</p>' % (cls, lin_rich(lin_text(n["prose"], code)))) if n.get("prose") else ""

    bits = ['<p class="graph-back"><a href="{{ROOT}}?tab=graph">%s</a></p>'
            % esc(ov.ui("graphBackToIndex", "\u2190 All graph categories")),
            '<h1>%s</h1>' % esc(lin_text(lineage["title"], code)),
            '<p class="lede">%s</p>'
            % lin_rich(lin_text(lineage["intro"], code))]

    # A parent link is the curators' reading of the field, not a citation:
    # most children do not cite their parent. Links where the child does
    # cite it (data/graph/citations.yaml) are drawn solid, the rest dashed,
    # and the legend under the lede says which is which.
    cites = set((c["from"], c["to"]) for c in (load("graph/citations.yaml") or []))

    def cited(par, key):
        a, b = by_key[key].get("paper"), by_key[par].get("paper")
        return bool(a and b and (a, b) in cites)
    n_cited = sum(1 for par, key, _lx, _ly, _d in edges if cited(par, key))
    bits.append('<p class="tree-legend"><span class="lg-item"><span class="lg lg-cited" aria-hidden="true"></span>%s</span>'
                '<span class="lg-item"><span class="lg" aria-hidden="true"></span>%s</span></p>'
                % (esc(fill(ov.ui("treeLegendCited", "Solid: the later paper cites the earlier one ({n})."),
                            {"n": n_cited})),
                   esc(fill(ov.ui("treeLegendEditorial", "Dashed: a step the curators drew between related work, not a citation ({n})."),
                            {"n": len(edges) - n_cited}))))

    # ---- the canvas: positioned cards + one SVG connector layer.
    stage = ['<div class="tree-stage" style="width:%spx;height:%spx">'
             % (num(width), num(height))]
    paths, heads = [], []
    for par, key, _lx, _ly, d in edges:
        cls = ' class="cited"' if cited(par, key) else ""
        paths.append('<path%s d="%s"/>' % (cls, d))
        x2, y2 = pos[key][0] + pos[key][2] / 2.0, pos[key][1]
        heads.append('<polygon class="tn-arrowhead%s" points="%s,%s %s,%s %s,%s"/>'
                     % (" cited" if cls else "",
                        num(x2 - 5), num(y2 - 9), num(x2 + 5), num(y2 - 9), num(x2), num(y2)))
    stage.append('<svg class="tree-edges" width="%s" height="%s" viewBox="0 0 %s %s" aria-hidden="true">%s%s</svg>'
                 % (num(width), num(height), num(width), num(height), "".join(paths), "".join(heads)))
    for _par, key, lx, ly, _d in edges:
        stage.append('<span class="tn-label" style="left:%spx;top:%spx">%s</span>'
                     % (num(lx), num(ly), esc(lin_text(by_key[key]["label"], code))))
    for n in nodes:
        x, y, w, h = pos[n["key"]]
        box = ('style="left:%spx;top:%spx;width:%spx;height:%spx"'
               % (num(x), num(y), num(w), num(h)))
        if "group" in n:
            stage.append('<div class="tn-group" id="%s" %s><h3>%s</h3><p class="tn-blurb">%s</p></div>'
                         % (esc(n["key"]), box, esc(lin_text(n["group"], code)), esc(lin_text(n["blurb"], code))))
        else:
            p = by_id[n["paper"]]
            rows = ['<span class="tn-year">%d</span>' % p["year"],
                    '<h3>%s</h3>' % head_of(p), '<p class="tn-meta">%s</p>' % meta_of(p),
                    '<p class="tn-note">%s</p>' % lin_rich(lin_text(n["note"], code))]
            lk = links_of(p)
            if lk:
                rows.append('<p class="tn-links">%s</p>' % lk)
            stage.append('<article class="tn-node" id="%s" %s>%s</article>'
                         % (esc(n["paper"]), box, "".join(rows)))
    stage.append("</div>")
    layout = {"width": num(width), "height": num(height),
              "nodes": [dict(key=n["key"], paper=n.get("paper"),
                             group=("group" in n), x=num(pos[n["key"]][0]),
                             y=num(pos[n["key"]][1]), w=num(pos[n["key"]][2]),
                             h=num(pos[n["key"]][3])) for n in nodes],
              "edges": [dict([("from", par), ("to", key)])
                        for par, key, _lx, _ly, _d in edges]}
    # The cards carry <h3>s; this heading (read by screen readers, not shown)
    # gives them a parent level below the page's <h1>.
    bits.append('<h2 class="sr-only">%s</h2>' % esc(ov.ui("treeHeading", "The tree")))
    bits.append(
        '<div class="tree-ui"><div class="tree-bar"><span class="tree-hint">%s</span>'
        '<span class="tree-btns"><button type="button" class="tree-btn" data-act="out" aria-label="Zoom out">\u2212</button>'
        '<button type="button" class="tree-btn" data-act="in" aria-label="Zoom in">+</button>'
        '<button type="button" class="tree-btn" data-act="reset">%s</button></span></div>'
        '<div class="tree-viewport" tabindex="0">%s</div>'
        '<script type="application/json" class="tree-layout">%s</script>'
        '<script src="{{ROOT}}lineage.js?v=%s"></script></div>'
        % (esc(ov.ui("treeHint", "Drag to pan \u00b7 scroll to zoom")),
           esc(ov.ui("treeReset", "Reset view")), "".join(stage),
           safe_json(layout), _asset_version("lineage.js")))

    # ---- the reading list: every node's full text, in file order
    # (the data file is written depth-first, so this reads root-down).
    items = []
    for n in nodes:
        if "group" in n:
            items.append('<li class="lr-group" id="read-%s"><h3>%s</h3><p class="lr-blurb">%s</p>%s</li>'
                         % (esc(n["key"]), esc(lin_text(n["group"], code)),
                            esc(lin_text(n["blurb"], code)), prose_of(n, "lr-prose")))
        else:
            p = by_id[n["paper"]]
            rows = ['<span class="lr-year">%d</span>' % p["year"],
                    '<h3>%s</h3>' % head_of(p), '<p class="lr-meta">%s</p>' % meta_of(p),
                    '<p class="lr-note">%s</p>' % lin_rich(lin_text(n["note"], code)),
                    prose_of(n, "lr-prose")]
            lk = links_of(p)
            if lk:
                rows.append('<p class="lr-links">%s</p>' % lk)
            items.append('<li class="lr-item" id="read-%s">%s</li>' % (esc(n["paper"]), "".join(rows)))
    bits.append('<section class="lineage-reading"><ol>%s</ol></section>' % "".join(items))
    return "\n".join(bits)


def graph_strings(ov):
    """The string table web/graph.js renders with, keyed as the JS expects.

    Values come from the language overlay (ui.graph* keys), reusing the
    existing kind*/region* keys where the site already has the word.
    """
    def u(key, default=""):
        return ov.ui(key, default)
    out = {
        "counts": u("graphCounts"),
        "mYear": u("graphYear", "Year"), "mTitle": u("graphTitle", "Title"),
        "mVenue": u("graphVenue", "Venue"),
        "mInstitution": u("graphInstitution", "Institution"),
        "mPi": u("graphPi", "Lead"), "mLanguage": u("graphLanguage", "Language"),
        "mLicense": u("graphLicense", "License"),
        "mStars": u("graphStars", "Stars"),
        "mModality": u("graphModality", "Modality"),
        "mKind": u("graphKind", "Kind"),
        "mPapersHere": u("graphPapersHere", "Papers here"),
        "mCount": u("graphCount", "Entries"),
    }
    for tname, key in (("paper", "kindPaper"), ("toolkit", "kindToolkit"),
                       ("dataset", "kindDataset"), ("benchmark", "kindBenchmark"),
                       ("learning", "kindLearning"), ("team", "kindTeam"),
                       ("topic", "graphTypeTopic"), ("venue", "graphTypeVenue"),
                       ("author", "graphTypeAuthor"), ("guide", "graphTypeGuide")):
        out["type_" + tname] = u(key, tname)
    for kind in ("topic", "start", "focus", "works", "uses", "cite",
                 "sibling", "code", "venue", "authored", "leads",
                 "coauthor", "cites"):
        out["edge_" + kind] = u("graphEdge" + kind.capitalize(), kind)
    return out


def _graph_card(href, title, desc, counts):
    return ('<a class="g-card" href="%s"><h3>%s</h3><p>%s</p>'
            '<span class="g-counts">%s</span></a>'
            % (esc(href), esc(title), esc(desc), esc(counts)))


def render_graph_index_body(payload, ov, code, slices, lineages=(), prefix="", panel=False):
    """The <main> of /graph/: an index of the per-category small
    graphs — overview cards (backbone, datasets, lineage trees), one
    card per topic — over the static team -> works list the page has
    always carried (it is also the no-JS content of the index; there
    is no canvas here any more)."""
    def counts_of(name):
        sl = slices[name]
        return ov.ui("graphCardCounts", "{nodes} nodes \u00b7 {edges} relations") \
            .replace("{nodes}", str(len(sl["nodes"]))) \
            .replace("{edges}", str(len(sl["edges"])))

    by_id = dict((p["id"], p) for p in payload["papers"])
    # One overview section: the library-wide views (backbone, datasets)
    # plus the curated lineage trees. Lineages used to sit under their
    # own heading, which left a single-card section and made the index
    # look fragmented; they are index cards like the others, so they
    # live in the same row now. Topics stay a section of their own:
    # 17 cards would drown the three overview cards.
    # Rendered twice from this one function: as the homepage's Graph tab
    # (panel=True: links prefixed with "graph/", headed by the panel's CSS
    # heading like the other tabs, no team list -- the Teams tab has it) and
    # as the standalone /graph/ page, kept for search engines and old links,
    # which opens with the shared intro (web/hero.html, whose <h1> is the
    # site title) and so is headed like a tab panel too.
    bits = ([] if panel else
            ['<h2 class="panel-heading">%s</h2>' % esc(ov.ui("pageGraphTitle", "Knowledge Graph"))])
    bits += ['<p class="panel-intro">%s</p>' % esc(ov.ui("graphIntro", "")),
            '<h2>%s</h2>' % esc(ov.ui("graphSectionOverview", "Overview")),
            '<div class="graph-cards">',
            _graph_card(prefix + "backbone/", ov.ui("graphBackboneTitle", "Team backbone"),
                        ov.ui("graphBackboneDesc", ""), counts_of("backbone")),
            _graph_card(prefix + "datasets/",
                        ov.ui("graphDatasetsTitle", "Datasets & the papers that use them"),
                        ov.ui("graphDatasetsDesc", ""), counts_of("datasets"))]
    for lin in lineages:
        # Milestones are the paper nodes; group boxes are structure.
        pnodes = [n for n in lin["nodes"] if n.get("paper") in by_id]
        years = [by_id[n["paper"]]["year"] for n in pnodes]
        counts = ov.ui("graphLineageCounts",
                       "{n} milestones \u00b7 {y0}\u2013{y1}") \
            .replace("{n}", str(len(pnodes))) \
            .replace("{y0}", str(min(years))) \
            .replace("{y1}", str(max(years)))
        bits.append(_graph_card(prefix + "lineage/%s/" % lin["id"],
                                lin_text(lin["title"], code),
                                lin_text(lin["description"], code),
                                counts))
    bits.append('</div>')
    bits += ['<h2>%s</h2>' % esc(ov.ui("graphSectionTopics", "By topic")),
             '<div class="graph-cards">']
    for t in payload["topics"]:
        bits.append(_graph_card(prefix + "topic/%s/" % t["id"], t["name"],
                                ov.ui("graphTopicDesc", ""),
                                counts_of("topic/" + t["id"])))
    bits.append('</div>')
    if panel:
        return "\n".join(bits)
    bits += ['<div id="graph-fallback" class="graph-fallback">',
             '<h2>%s</h2>' % esc(ov.ui("graphFallbackTitle",
                                       "Teams and their works in the library"))]
    for tm in payload.get("teams") or []:
        works = tm.get("works") or {}
        links = []
        for pid in works.get("papers") or []:
            p = by_id.get(pid)
            if p:
                links.append('<a href="%s" target="_blank" rel="noopener">%s</a>'
                             % (esc(paper_url(p)), esc(paper_label(p))))
        for table in ("toolkits", "datasets", "benchmarks"):
            for n in works.get(table) or []:
                links.append('<a href="?tab=%s">%s</a>' % (table, esc(n)))
        bits.append('<p class="gf-team"><a href="%s" target="_blank" '
                    'rel="noopener"><strong>%s</strong></a> \u00b7 %s%s</p>'
                    % (esc(tm["homepage"]),
                       esc(tm.get("label") or tm["name"]),
                       esc(tm["institution"]),
                       (" \u2014 " + " \u00b7 ".join(links)) if links else ""))
    bits.append('</div>')
    return "\n".join(bits)


def _slice_label(n, code):
    return (n.get("lz") if code == "zh" else None) or n["l"]


_ASSET_V = {}

# Shared stylesheet and scripts referenced by the homepage and the standalone
# pages; main() appends ?v=<content hash> to every reference to them.
CORE_ASSETS = ("styles.css", "search.js", "app.js", "chrome.js", "lang.js")


def _asset_version(rel):
    """Short content hash of a web/ source file, used as a ?v=
    cache-buster on the graph pages' script URLs. The graph pages are
    useless when their HTML, renderer and data come from different
    deploys (a stale graph.js against a new page fails silently), so
    every graph asset URL carries the hash of the bytes it serves:
    a new deploy is a new URL, and version skew cannot occur."""
    if rel not in _ASSET_V:
        path = os.path.join(WEB, rel)
        if os.path.exists(path):
            with open(path, "rb") as fh:
                _ASSET_V[rel] = hashlib.sha256(fh.read()).hexdigest()[:10]
        else:
            # Vendored libraries are optional at build time; a missing
            # one simply gets no cache-buster (and no library at all —
            # graph.js then surfaces the load note).
            _ASSET_V[rel] = ""
    return _ASSET_V[rel]


def _datasets_note(ov, sl, payload_en):
    """The datasets slice's honesty line, as HTML for under its intro.

    The slice ships only resources with a recorded link to a paper
    (scripts/graph_slices.py drops the rest), so the page says how
    many that is out of the library's totals and points at the
    datasets-and-benchmarks directory for everything else. Counts
    come from the (trimmed) slice itself, so the line cannot drift
    from what the graph actually shows.
    """
    types = Counter(n["t"] for n in sl["nodes"])
    note = esc(ov.ui("graphDatasetsNote", ""))
    note = note.replace("{d_shown}", str(types.get("dataset", 0)))
    note = note.replace("{d_total}", str(len(payload_en["datasets"])))
    note = note.replace("{b_shown}", str(types.get("benchmark", 0)))
    note = note.replace("{b_total}", str(len(payload_en["benchmarks"])))
    note = note.replace(
        "{ds}", '<a href="{{ROOT}}datasets/">%s</a>'
        % esc(ov.ui("graphDirDatasets", "datasets and benchmarks directory")))
    return note


def _backbone_note(ov):
    """The backbone slice's honesty line, as HTML for under its intro.

    The choosing-a-ct-reconstruction-dataset guide deliberately has
    no topics (option (b), user decision 2026-10-27), so the graph
    builder gives it no topic edges and the slice drops it as an
    isolate. The page says so explicitly instead of silently
    omitting it, mirroring _datasets_note's honesty line.
    """
    return esc(ov.ui("graphBackboneGuideNote", ""))


def render_graph_slice_body(ov, code, title, intro, sl, back="../",
                            data_v="", note_html=""):
    """The <main> of one category graph page: back link, controls,
    canvas, detail panel, and the no-JS fallback — this slice's own
    entries as a plain grouped list of links. `back` is the relative
    path back to the graph index (the homepage's Graph tab). `note_html` is an optional extra intro
    paragraph (the datasets slice's shown-vs-total line)."""
    strings = graph_strings(ov)
    bits = ['<p class="graph-back"><a href="%s">%s</a></p>'
            % (esc(back), esc(ov.ui("graphBackToIndex",
                                    "\u2190 All graph categories"))),
            '<h1>%s</h1>' % esc(title),
            '<p class="lede">%s</p>' % esc(intro),
            ('<p class="lede graph-note">%s</p>' % note_html)
            if note_html else '',
            '<div id="graph-bar" class="graph-bar" hidden>',
            '<input id="graph-search" type="search" list="graph-search-list" '
            'placeholder="%s" aria-label="%s">'
            % (esc(ov.ui("graphSearchPlaceholder", "Search\u2026")),
               esc(ov.ui("graphSearchPlaceholder", "Search\u2026"))),
            '<datalist id="graph-search-list"></datalist>',
            '<button type="button" id="graph-reset">%s</button>'
            % esc(ov.ui("graphReset", "Reset")),
            '<span id="graph-counts" class="g-counts"></span>',
            '</div>',
            '<div id="graph-stage" class="graph-cy"></div>',
            '<aside id="graph-panel" class="graph-panel" hidden>',
            '<button type="button" id="gp-close" class="gp-close" '
            'aria-label="%s">\u00d7</button>' % esc(ov.ui("graphClose", "Close")),
            '<span id="gp-type" class="gp-type"></span>',
            '<h2 id="gp-name"></h2>',
            '<dl id="gp-meta" class="gp-meta"></dl>',
            '<p class="gp-actions">'
            '<a id="gp-open" class="gp-open" href="#">%s</a></p>'
            % esc(ov.ui("graphOpen", "Open in the directory")),
            '<h3>%s</h3>' % esc(ov.ui("graphNeighbours", "Connections")),
            '<div id="gp-neighbours"></div>',
            '</aside>',
            '<p id="graph-load-note" class="g-note" hidden>%s</p>'
            % esc(ov.ui("graphLoadNote", "")),
            '<div id="graph-fallback" class="graph-fallback">',
            '<h2>%s</h2>' % esc(title)]
    groups = {}
    for n in sl["nodes"]:
        groups.setdefault(n["t"], []).append(n)
    for ty in ("team", "topic", "paper", "toolkit", "dataset", "benchmark",
               "author", "venue", "learning", "guide"):
        members = groups.get(ty)
        if not members:
            continue
        bits.append('<h3>%s</h3>' % esc(strings.get("type_" + ty, ty)))
        bits.append('<ul>')
        for n in sorted(members, key=lambda n: _slice_label(n, code).lower()):
            lab = esc(_slice_label(n, code))
            href = n.get("href")
            if href:
                if href.startswith(("http://", "https://")):
                    bits.append('<li><a href="%s" target="_blank" '
                                'rel="noopener">%s</a></li>' % (esc(href), lab))
                else:
                    bits.append('<li><a href="{{ROOT}}%s">%s</a></li>'
                                % (esc(href), lab))
            else:
                bits.append('<li>%s</li>' % lab)
        bits.append('</ul>')
    bits += ['</div>',
             '<script>window.GRAPH_STRINGS = %s;'
             'window.GRAPH_LANG = "%s";'
             'window.GRAPH_ROOT = "{{ROOT}}";'
             'window.GRAPH_DATA = "data.json?v=%s";</script>'
             % (safe_json(strings), esc(code), esc(data_v)),
             # One renderer: sigma (WebGL) over a graphology graph.
             # Missing vendor files leave window.Sigma undefined, and
             # graph.js then leaves the static fallback in charge.
             # The ?v= hashes keep HTML, renderer and data from the
             # same deploy (see _asset_version).
             '<script src="{{ROOT}}graphology.min.js?v=%s"></script>'
             % _asset_version(os.path.join("vendor", "graphology.min.js")),
             '<script src="{{ROOT}}sigma.min.js?v=%s"></script>'
             % _asset_version(os.path.join("vendor", "sigma.min.js")),
             '<script src="{{ROOT}}graph.js?v=%s"></script>'
             % _asset_version("graph.js")]
    return "\n".join(bits)


def head_extra_static(cfg, base, langs, entry, name, title, desc, site_title):
    """hreflang alternates + og for a standalone page (about/contact/privacy).

    These pages take their head from web/page.html, which carries no
    hreflang or og tags of its own — so without this they are the only
    pages search engines see without them.
    """
    default = i18n.default_language(langs)
    url = i18n.url_for(base, entry) + name + "/"
    bits = ['<link rel="alternate" hreflang="%s" href="%s">'
            % (esc(e["hreflang"]), esc(i18n.url_for(base, e) + name + "/"))
            for e in langs]
    bits.append('<link rel="alternate" hreflang="x-default" href="%s">'
                % esc(i18n.url_for(base, default) + name + "/"))
    bits += ['<meta property="og:type" content="website">',
             '<meta property="og:url" content="%s">' % esc(url),
             '<meta property="og:title" content="%s — %s">' % (esc(title), esc(site_title)),
             '<meta property="og:description" content="%s">' % esc(desc),
             '<meta property="og:locale" content="%s">' % esc(entry["og_locale"])]
    return "\n".join(bits)


def add_to_head(page, canonical, extra):
    """Insert extra <head> markup right after the canonical link."""
    tag = '<link rel="canonical" href="%s">' % esc(canonical)
    if tag not in page:
        sys.exit("canonical link %s not found while adding head markup" % canonical)
    return page.replace(tag, tag + "\n" + extra, 1)

# Sub-page nav section for the underline: first path segment -> the nav
# item that counts as "you are here". Pages with no entry (changelog,
# about, contact, privacy) get no underline, honestly.
_NAV_SECTION = {"graph": "graph", "datasets": "datasets",
                "benchmarks": "benchmarks", "guides": "learning",
                "topics": "papers"}


def mark_nav(html_, where):
    """Mark the current section's nav link in a page.html build.

    ``where`` is "<lang>/<rel path>" (or "<lang>/<rel path>" for the
    manual blocks); the first segment names the section. The nav links
    carry data-nav="<section>", and the marked one gets aria-current,
    which styles.css underlines exactly like a selected homepage tab.
    """
    rel = where.split("/", 1)[1] if "/" in where else ""
    sec = _NAV_SECTION.get(rel.split("/")[0])
    if not sec:
        return html_
    return html_.replace('class="nav-ext" data-nav="%s"' % sec,
                         'class="nav-ext" data-nav="%s" aria-current="page"' % sec, 1)


def fill_page(tpl, body, title, desc, url, root, subs, where, switch):
    """page.html filled for one standalone page; fails on a leftover {{X}}.

    ``switch`` is this page's own language-switcher HTML (see
    i18n.switch_links): it is per-page, so it cannot ride in ``subs``,
    which is built once per language."""
    html_ = (tpl.replace("{{BODY}}", body)
             .replace("{{PAGE_TITLE}}", esc(title))
             .replace("{{PAGE_DESC}}", esc(desc))
             .replace("{{PAGE_URL}}", esc(url))
             .replace("{{ROOT}}", root))
    for k, v in subs.items():
        html_ = html_.replace(k, v)
    html_ = html_.replace("{{LANG_SWITCH}}", switch)
    html_ = mark_nav(html_, where)
    left = re.findall(r"\{\{[A-Z_]+\}\}", html_)
    if left:
        sys.exit("%s: unreplaced placeholders: %s" % (where, ", ".join(sorted(set(left)))))
    return html_


def guide_topic_map(guides, rp_pages):
    """topic id -> [guide] for the topic pages. A guide names its topics; a
    guide whose table lists every dataset page is linked from every topic page
    that lists one of those datasets."""
    out = {}
    for g in guides:
        tids = list(g.get("topics") or [])
        if any(((b.get("table") or {}).get("all")) for b in g.get("blocks") or []):
            for pg in rp_pages:
                if pg["table"] == "datasets":
                    tids += pg["topics"]
        for t in tids:
            if g not in out.setdefault(t, []):
                out[t].append(g)
    return out


# ------------------------------------------------------------------- config
def load_config():
    if not os.path.exists(CONFIG):
        sys.exit("site.config.yml not found at the repository root")
    import yaml
    with io.open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        sys.exit("site.config.yml: expected a mapping at the top level")
    for key in ("title", "tagline", "description", "repo",
                "code_license", "content_license", "content_license_url"):
        if not cfg.get(key):
            sys.exit("site.config.yml: missing required key '%s'" % key)
    return cfg


def resolve_base(cfg, cli_url):
    url = (cli_url or cfg.get("url") or "").strip()
    if not url:
        repo = cfg.get("repo") or ""
        owner = repo.split("/")[0] if "/" in repo else ""
        name = repo.split("/")[-1]
        if not owner or not name:
            sys.exit("site.config.yml: set `url`, or set `repo` to 'owner/name'")
        url = "https://%s.github.io/%s/" % (owner, name)
        cfg["_url_from_repo"] = True
    if not re.match(r"^https?://", url):
        sys.exit("site.config.yml: `url` must start with http:// or https://")
    if not url.endswith("/"):
        url += "/"
    return url


def host_of(base):
    """'https://computedtomography.org/' -> 'computedtomography.org'."""
    return re.sub(r"^https?://", "", base).split("/")[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="override site.config.yml's `url`")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    cfg = load_config()

    # P0-3: CI never executed the site's own scripts, so a syntax error
    # in app.js / graph.js / lineage.js / chrome.js / lang.js / search.js
    # shipped green. Check them here, inside the build, so the failure
    # bites in BOTH workflows (validate and deploy both run build_site.py)
    # with no workflow-file change — the connector cannot edit .github/*.
    # This is parse-only: it catches syntax errors, not top-level runtime
    # throws; those are the DOM suite's job (tests/test_site_dom.js).
    import shutil
    import subprocess
    node = shutil.which("node")
    if not node:
        sys.exit("node is required to syntax-check web/*.js")
    for _js in ("search.js", "app.js", "chrome.js", "lang.js",
                "graph.js", "lineage.js"):
        _r = subprocess.run([node, "--check", os.path.join(WEB, _js)],
                            capture_output=True, text=True)
        if _r.returncode != 0:
            sys.exit("web/%s fails node --check:\n%s" % (_js, _r.stderr))

    base = resolve_base(cfg, args.url)
    cfg["repo_url"] = "https://github.com/" + cfg["repo"]

    # Counts are language-independent, so one build of the source-language
    # payload is enough to size the page tokens. The per-language loop below
    # rebuilds the payload so each language's data.json carries its own notes.
    payload = build_payload(i18n.SOURCE)
    c = payload["counts"]
    # The site is maintained from Asia/Shanghai (UTC+8, no DST); stamp its date, not the build server's UTC one.
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()

    # The coverage sentence now comes from ui.coverage per language, so it reads
    # in the page's own language; see `shared["coverage"]` below.

    out = args.out
    meta = yaml.safe_load(io.open(os.path.join(ROOT, "data", "meta.yaml"),
                                  encoding="utf-8"))
    langs = i18n.languages(meta)

    # Tokens available inside every ui.* and readme.* string. Only ever numbers
    # and known-safe config values — see the header comment in data/i18n/en.yaml.
    tokens = {
        "papers": c["papers"],
        "preprints": c["preprints"], "toolkits": c["toolkits"],
        "datasets": c["datasets"], "benchmarks": c["benchmarks"],
        "learning": c["learning"], "teams": c.get("teams", 0),
        "year_min": c["year_min"],
        "year_max": c["year_max"], "updated": str(meta["last_updated"]),
        "title": cfg["title"],
        "tagline": cfg["tagline"], "repo": cfg["repo"],
        "repo_url": cfg["repo_url"], "build_date": today,
        "code_license": cfg["code_license"],
        "code_license_url": cfg["repo_url"] + "/blob/main/LICENSE",
        "content_license": cfg["content_license"],
        "content_license_url": cfg["content_license_url"],
        "license_year": today[:4], "host": host_of(base),
    }

    # The page bodies live in data/i18n so a translation can replace a whole
    # page. web/pages/ is still the maintainers' copy of the English; say so
    # loudly if the two ever drift apart instead of silently serving one.
    src_en = i18n.load(i18n.SOURCE)
    for name in PAGES:
        disk = re.sub(r"<!-- (title|description): .*? -->\n", "",
                      read(os.path.join(WEB, "pages", name + ".html"))).strip("\n")
        if disk.strip() != (src_en.page(name) or "").strip():
            print("  note: web/pages/%s.html and data/i18n/en.yaml `pages.%s` "
                  "differ; the build uses the yaml copy" % (name, name))

    tpl = read(os.path.join(WEB, "page.html"))
    index_tpl = read(os.path.join(WEB, "index.html"))
    # The homepage intro, shared with /graph/ (the last item of the same nav
    # row), so the two open identically; filled from the homepage's subs.
    hero_tpl = read(os.path.join(WEB, "hero.html"))
    hero_tpl = hero_tpl[hero_tpl.index("-->") + 4:]
    sitemap_urls = []
    # Topic hub pages (data/topics.yaml). Validated once, against English.
    topic_doc = load_topic_pages(payload)
    topic_ids = ([t["id"] for t in payload["topics"]
                  if t["id"] not in TOPIC_SKIP and t["id"] in topic_doc["topics"]]
                 if topic_doc else [])
    faq_counts = {}
    # Dataset / benchmark pages and guides (scripts/resource_pages.py).
    res_cfg, guides_doc = RP.load_config()
    rp_pages, rp_skipped = RP.select(payload, topic_doc, topic_resources, res_cfg)
    rp_res = dict(((pg["kind"], pg["name"]), pg["rel"]) for pg in rp_pages)
    rp_table = dict(((pg["table"], pg["name"]), pg["rel"]) for pg in rp_pages)
    rp_guides = guides_doc.get("guides") or []
    rp_topic_guides = guide_topic_map(rp_guides, rp_pages)
    payload_en = payload
    new_pages = {}          # code -> [rel path] of every page added here
    graph_rels = {}         # code -> [rel path] of the graph category pages
    lineage_rels = {}       # code -> [rel path] of the lineage pages

    # ------------------------------------------------------------ graph data
    # The knowledge graph is projected once (scripts/graph.py) and cut
    # into per-category slices (scripts/graph_slices.py), each with
    # its own precomputed layout; the language loop below renders the
    # index + one page per category and writes each slice's data.json
    # at every language root (both editions carry both labels, so the
    # files are identical). The enrichment files under data/graph/ are
    # optional: absent, the graph is the P0 graph without authors or
    # citation edges.
    _enrichment = graph_mod.load_enrichment()
    g_authors, g_citations = _enrichment[0], _enrichment[1]
    # Tolerate a graph.py that predates the paper_datasets file (returns a
    # 2-tuple): the graph then simply has no verified usage edges yet.
    g_paper_datasets = _enrichment[2] if len(_enrichment) > 2 else None
    g_problems = graph_mod.validate_graph(
        payload_en["papers"], payload_en["teams"], g_authors, g_citations,
        g_paper_datasets,
        set(r["name"] for r in payload_en["datasets"]))
    if g_problems:
        print("GRAPH DATA INVALID:")
        for x in g_problems:
            print("  -", x)
        sys.exit(1)
    other = next((e["code"] for e in langs if e["code"] != i18n.SOURCE),
                 i18n.SOURCE)
    graph = graph_mod.build_graph(
        payload_en, build_payload(other), topic_doc, topic_resources,
        rp_pages, rp_guides, g_authors, g_citations, g_paper_datasets)
    g_problems = graph_mod.check_graph(graph)
    if g_problems:
        print("GRAPH BUILD INVALID:")
        for x in g_problems:
            print("  -", x)
        sys.exit(1)
    graph_slices = graph_slices_mod.build_slices(graph)
    graph_slice_json = {}
    for name, sl in graph_slices.items():
        graph_slice_json[name] = graph_slices_mod.slice_json(
            graph_slices_mod.slice_payload(sl, total=len(graph["nodes"])))
        print("  graph slice %-24s %3d nodes, %4d edges, %.0f KB"
              % (name, len(sl["nodes"]), len(sl["edges"]),
                 len(graph_slice_json[name].encode("utf-8")) / 1024.0))
    try:
        _, cl_entries = changelog.parse()
    except changelog.ChangelogError as e:
        sys.exit(str(e))

    # Curated lineages (data/lineages.yaml). Validated here as well as in
    # build.py --check, because the renderer dereferences every paper id
    # it names; the file is optional, like the graph enrichment files.
    lineages_doc = load("lineages.yaml")
    lineages = []
    if lineages_doc is not None:
        lin_problems = validate_lineages(payload["papers"], lineages_doc)
        if lin_problems:
            print("LINEAGE DATA INVALID:")
            for x in lin_problems:
                print("  -", x)
            sys.exit(1)
        lineages = lineages_doc.get("lineages") or []

    for entry in langs:
        code = entry["code"]
        ov = i18n.load(code)
        lang_base = i18n.url_for(base, entry)
        sub = os.path.join(out, entry.get("path") or "")

        # Rebuild per language rather than mutating one shared payload: the
        # notes (and the topic names below) differ by language, and the
        # previous iteration's edits would otherwise leak into this one.
        payload = build_payload(code)

        # `tokens` is built once, with the English tagline from site.config.yml.
        # Give each language its own copy so `{tagline}` in ui.* strings reads in
        # the page's language (the /zh/ hero used to open with the English one).
        tokens_lang = dict(tokens, tagline=top_for(ov, code, "tagline", cfg["tagline"]))
        shared = dict(tokens_lang)
        shared["coverage"] = fill(ov.ui("coverage"), tokens_lang)
        payload["ui"] = js_ui(ov)
        # Topic names/descs already arrive translated: build_payload()
        # applies the overlay to the topics list itself. (A previous
        # build translated them here only, which left the graph payload
        # English — P0-1. Do not re-add a second translation point.)

        # Homepage links to the detail pages and guides (web/app.js renders
        # them): a row's own page, relative to the language root, and the
        # Guides group at the top of the Learning tab.
        for table in ("datasets", "benchmarks"):
            for r in payload[table]:
                rel = rp_table.get((table, r["name"]))
                if rel:
                    r["page"] = rel
        rs_home = RP.strings(res_cfg, code)
        payload["guides"] = {
            "label": rs_home["guides"], "kind": rs_home["guideKicker"],
            "official": rs_home["homeOfficial"], "officialTitle": rs_home["official"],
            "index": RP.GUIDES_PATH, "indexLabel": rs_home["homeGuidesAll"],
            "items": [{"url": RP.GUIDES_PATH + g["slug"] + "/",
                       "title": ((g.get(code) or {}).get("title") or g["en"]["title"]).strip(),
                       "note": ((g.get(code) or {}).get("description")
                                or g["en"]["description"]).strip()}
                      for g in rp_guides],
        }

        # The homepage's own switcher: its twin is the other homepage.
        switch = i18n.switch_links(base, langs, code, "")

        subs = {
            "{{HEAD}}": render_head(cfg, payload, lang_base, base, entry, langs,
                                   ov, tokens_lang),
            "{{DATA}}": safe_json(page_payload(payload)),
            "{{PAPERS_STATIC}}": render_static_papers(payload, ov),
            "{{TEAMS_STATIC}}": render_static_teams(payload, ov),
            "{{GRAPH_PANEL}}": render_graph_index_body(payload, ov, code, graph_slices,
                                                       lineages, prefix="graph/", panel=True),
            "{{PAPERS_LEGEND}}": md_inline(ov.readme("legendPapers", PAPERS_LEGEND)),
            "{{TEAMS_LEGEND}}": md_inline(ov.readme("legendTeams", "")),
            "{{DATASET_LEGEND}}": md_inline(ov.readme("legendDatasets", DATASET_LEGEND)),
            "{{TITLE}}": esc(top_for(ov, code, "title", cfg["title"])),
            "{{TAGLINE}}": esc(top_for(ov, code, "tagline", cfg["tagline"])),
            "{{REPO_URL}}": esc(cfg["repo_url"]),
            "{{REPO_NAME}}": esc(cfg["repo"]),
            "{{CODE_LICENSE}}": esc(cfg["code_license"]),
            "{{CODE_LICENSE_URL}}": esc(cfg["repo_url"] + "/blob/main/LICENSE"),
            "{{CONTENT_LICENSE}}": esc(cfg["content_license"]),
            "{{CONTENT_LICENSE_URL}}": esc(cfg["content_license_url"]),
            "{{BUILD_DATE}}": today,
            "{{COVERAGE}}": esc(shared["coverage"]),
            "{{HTML_LANG}}": esc(entry["html"]),
            "{{N_PAPERS}}": str(c["papers"]),
            "{{N_TOOLKITS}}": str(c["toolkits"]),
            "{{N_DATASETS}}": str(c["datasets"]),
            "{{N_BENCHMARKS}}": str(c["benchmarks"]),
            "{{N_LEARNING}}": str(c["learning"]),
            "{{N_TEAMS}}": str(c.get("teams", 0)),
            "{{YEAR_MIN}}": str(c["year_min"]),
            "{{YEAR_MAX}}": str(c["year_max"]),
            "{{UPDATED}}": esc(str(meta["last_updated"])),
        }
        subs.update(ui_subs(ov, shared))

        page = index_tpl.replace("{{HERO}}", hero_tpl).replace("{{ROOT}}", "./")
        for k, v in subs.items():
            page = page.replace(k, v)
        page = page.replace("{{LANG_SWITCH}}", switch)
        left = re.findall(r"\{\{[A-Z_]+\}\}", page)
        if left:
            sys.exit("%s: unreplaced placeholders: %s"
                     % (code, ", ".join(sorted(set(left)))))
        if ('<link rel="canonical" href="%s">' % lang_base) not in page:
            sys.exit("%s: canonical URL missing or wrong" % code)
        if ('<meta property="og:url" content="%s">' % lang_base) not in page:
            sys.exit("%s: og:url missing or wrong" % code)

        write(os.path.join(sub, "index.html"), page)
        write(os.path.join(sub, "styles.css"), read(os.path.join(WEB, "styles.css")))
        write(os.path.join(sub, "search.js"), read(os.path.join(WEB, "search.js")))
        write(os.path.join(sub, "app.js"), read(os.path.join(WEB, "app.js")))
        write(os.path.join(sub, "chrome.js"), read(os.path.join(WEB, "chrome.js")))
        write(os.path.join(sub, "lang.js"), read(os.path.join(WEB, "lang.js")))
        write(os.path.join(sub, "graph.js"), read(os.path.join(WEB, "graph.js")))
        write(os.path.join(sub, "lineage.js"), read(os.path.join(WEB, "lineage.js")))
        # The vendored sigma + graphology are optional at build time:
        # without them the graph page still ships, with its static
        # fallback list visible (graph.js checks for the globals).
        # The release builds carry no licence text, and MIT requires the
        # notice in every copy, so the deployed copy opens with it
        # (web/vendor/<name>.LICENSE.txt, as shipped in the npm package).
        for vend in ("graphology.min.js", "sigma.min.js"):
            vendor = os.path.join(WEB, "vendor", vend)
            if os.path.exists(vendor):
                lic = read(os.path.join(WEB, "vendor",
                                        vend.split(".")[0] + ".LICENSE.txt"))
                assert "*/" not in lic
                write_bytes(os.path.join(sub, vend),
                            ("/*!\n%s\n*/\n" % lic.strip()).encode("utf-8")
                            + open(vendor, "rb").read())
            else:
                print("  note: web/vendor/%s is absent; "
                      "/graph/ will serve its static fallback" % vend)
        sitemap_urls.append((lang_base, "weekly", "1.0"))

        for name in PAGES:
            body = ov.page(name)
            if not body.strip():
                sys.exit("data/i18n/%s.yaml carries no `pages.%s`" % (code, name))
            # About carries the list of topic pages, so none is orphaned.
            body = body.replace("{{TOPIC_LINKS}}",
                                render_topic_links(payload, None, "{{ROOT}}")
                                if topic_doc else "")
            # About also lists the guides, so none is orphaned.
            rs_about = RP.strings(res_cfg, code)
            body = body.replace("{{GUIDE_LINKS}}", "<ul>\n%s\n</ul>" % "\n".join(
                ['<li><a href="{{ROOT}}datasets/">%s</a></li>' % esc(rs_about["indexTitle"]),
                 '<li><a href="{{ROOT}}guides/">%s</a></li>' % esc(rs_about["guidesTitle"])]
                + ['<li><a href="{{ROOT}}guides/%s/">%s</a></li>'
                   % (esc(g["slug"]), esc(((g.get(code) or {}).get("title") or g["en"]["title"])))
                   for g in rp_guides]))
            p_title = ov.ui("page%sTitle" % name.title(), name.title())
            p_desc = fill(ov.ui("page%sDesc" % name.title(), ""), shared)
            html_ = (tpl.replace("{{BODY}}", body)
                     .replace("{{PAGE_TITLE}}", esc(p_title))
                     .replace("{{PAGE_DESC}}", esc(p_desc))
                     .replace("{{PAGE_URL}}", esc(lang_base + name + "/"))
                     .replace("{{ROOT}}", "../"))
            for k, v in subs.items():
                html_ = html_.replace(k, v)
            html_ = html_.replace("{{LANG_SWITCH}}", i18n.switch_links(
                base, langs, code, name + "/"))
            html_ = mark_nav(html_, "%s/%s" % (code, name))
            left = re.findall(r"\{\{[A-Z_]+\}\}", html_)
            if left:
                sys.exit("%s/%s: unreplaced placeholders: %s"
                         % (code, name, ", ".join(sorted(set(left)))))
            # Every page carries the favicon + share image, even the
            # standalone pages whose head comes from page.html.
            html_ = add_to_head(html_, lang_base + name + "/",
                                brand_assets.head_brand(base))
            # ... and the standalone pages need hreflang + og too, for the
            # same reason: page.html carries neither.
            html_ = add_to_head(html_, lang_base + name + "/",
                                head_extra_static(
                                    cfg, base, langs, entry, name,
                                    p_title, p_desc,
                                    top_for(ov, code, "title", cfg["title"])))
            if name == "about":
                ld, nfaq = faq_jsonld(html_)
                faq_counts[code] = nfaq
                if ld:
                    html_ = add_to_head(html_, lang_base + name + "/", ld)
            write(os.path.join(sub, name, "index.html"), html_)
            sitemap_urls.append((lang_base + name + "/", "monthly", "0.3"))

        strings = topic_strings(topic_doc, code) if topic_doc else {}

        cl_url = lang_base + CHANGELOG_PATH
        cl_desc = re.sub(r"\s+", " ", fill(ov.ui("pageChangelogDesc"), shared)).strip()
        cl_lang, cl_untranslated = changelog_for(cl_entries, entry)
        html_ = (tpl.replace("{{BODY}}", render_changelog_body(
                     cl_lang, code, ov, strings, cfg, entry["html"], cl_untranslated,
                     None if code == i18n.SOURCE else entry["changelog"]))
                 .replace("{{PAGE_TITLE}}", esc(ov.ui("pageChangelogTitle", "Changelog")))
                 .replace("{{PAGE_DESC}}", esc(cl_desc))
                 .replace("{{PAGE_URL}}", esc(cl_url))
                 .replace("{{ROOT}}", "../"))
        for k, v in subs.items():
            html_ = html_.replace(k, v)
        html_ = html_.replace("{{LANG_SWITCH}}", i18n.switch_links(
            base, langs, code, CHANGELOG_PATH))
        html_ = mark_nav(html_, "%s/changelog" % code)
        left = re.findall(r"\{\{[A-Z_]+\}\}", html_)
        if left:
            sys.exit("%s/changelog: unreplaced placeholders: %s"
                     % (code, ", ".join(sorted(set(left)))))
        html_ = add_to_head(html_, cl_url, head_extra_changelog(
            cfg, base, langs, entry, ov, cl_desc))
        write(os.path.join(sub, "changelog", "index.html"), html_)
        sitemap_urls.append((cl_url, "weekly", "0.4"))

        g_url = lang_base + GRAPH_PATH
        g_desc = re.sub(r"\s+", " ", fill(ov.ui("pageGraphDesc"), shared)).strip()
        html_ = fill_page(tpl, hero_tpl + render_graph_index_body(payload, ov, code,
                                                                  graph_slices, lineages),
                          ov.ui("pageGraphTitle", "Knowledge Graph"), g_desc,
                          g_url, "../", subs, "%s/graph" % code,
                          i18n.switch_links(base, langs, code, GRAPH_PATH))
        # Laid out like a homepage tab (full width, panel heading), not like
        # a prose page.
        assert html_.count('<main class="wrap prose">') == 1
        html_ = html_.replace('<main class="wrap prose">', '<main class="wrap graph-home">')
        html_ = add_to_head(html_, g_url, head_extra_graph(
            cfg, base, langs, entry, ov, g_desc))
        write(os.path.join(sub, "graph", "index.html"), html_)
        sitemap_urls.append((g_url, "monthly", "0.5"))

        # One small graph page per category slice; each loads only its
        # own data.json (written beside data.json at the end of the
        # loop body), so no page ships another category's nodes.
        slice_pages = [
            ("backbone", ov.ui("graphBackboneTitle", "Team backbone"),
             ov.ui("graphBackboneIntro", ""), ov.ui("graphBackboneDesc", ""),
             _backbone_note(ov)),
            ("datasets",
             ov.ui("graphDatasetsTitle", "Datasets & the papers that use them"),
             ov.ui("graphDatasetsIntro", ""), ov.ui("graphDatasetsDesc", ""),
             _datasets_note(ov, graph_slices["datasets"], payload_en)),
        ]
        # Lead each topic page's meta description with the topic's name: the
        # shared sentence alone gave all 17 topic graphs one description.
        topic_sep = "：" if code == "zh" else ": "
        for t in payload["topics"]:
            slice_pages.append(("topic/" + t["id"], t["name"],
                                ov.ui("graphTopicIntro", ""),
                                t["name"] + topic_sep + ov.ui("graphTopicDesc", ""), ""))
        grels = graph_rels.setdefault(code, [])
        for name, title, intro, desc, note_html in slice_pages:
            rel = GRAPH_PATH + name + "/"
            url = lang_base + rel
            desc = re.sub(r"\s+", " ", fill(desc, shared)).strip()
            depth = rel.rstrip("/").count("/") + 1
            html_ = fill_page(
                tpl, render_graph_slice_body(
                    ov, code, title, intro, graph_slices[name],
                    # Back to the homepage's Graph tab, where the nav's
                    # Graph item goes (fill_page fills {{ROOT}}).
                    back="{{ROOT}}?tab=graph",
                    data_v=hashlib.sha256(
                        graph_slice_json[name].encode("utf-8")
                    ).hexdigest()[:10],
                    note_html=note_html),
                title, desc, url, "../" * depth,
                subs, "%s/%s" % (code, rel),
                i18n.switch_links(base, langs, code, rel))
            html_ = add_to_head(html_, url, head_extra_graph(
                cfg, base, langs, entry, ov, desc, rel=rel, title=title,
                parent=True))
            write(os.path.join(sub, "graph", *name.split("/"), "index.html"),
                  html_)
            sitemap_urls.append((url, "monthly", "0.5"))
            grels.append(rel)

        # One static page per curated lineage, under the graph index:
        # the tree canvas (render_lineage_body) — no slice, no
        # data.json, so none of the slice machinery applies to it.
        lin_rels = lineage_rels.setdefault(code, [])
        for lin in lineages:
            rel = GRAPH_PATH + "lineage/" + lin["id"] + "/"
            url = lang_base + rel
            l_title = lin_text(lin["title"], code)
            l_desc = re.sub(r"\s+", " ",
                            fill(lin_text(lin["description"], code),
                                 shared)).strip()
            depth = rel.rstrip("/").count("/") + 1
            html_ = fill_page(
                tpl, render_lineage_body(payload, ov, code, lin),
                l_title, l_desc, url, "../" * depth,
                subs, "%s/%s" % (code, rel),
                i18n.switch_links(base, langs, code, rel))
            html_ = add_to_head(html_, url, head_extra_graph(
                cfg, base, langs, entry, ov, l_desc, rel=rel, title=l_title,
                parent=True))
            write(os.path.join(sub, "graph", "lineage", lin["id"],
                               "index.html"), html_)
            sitemap_urls.append((url, "monthly", "0.5"))
            lin_rels.append(rel)

        for tid in topic_ids:
            tp = topic_doc["topics"][tid]
            t_title = topic_text(tp, code, "title")
            t_desc = re.sub(r"\s+", " ", topic_text(tp, code, "description"))
            t_url = topic_url(lang_base, tid)
            rs = RP.strings(res_cfg, code)
            body = render_topic_body(
                tid, tp, payload, code, strings, ov, res_pages=rp_res, rs=rs,
                guides=[(g["slug"], (g.get(code) or {}).get("title") or g["en"]["title"])
                        for g in rp_topic_guides.get(tid, [])])
            html_ = (tpl.replace("{{BODY}}", body)
                     .replace("{{PAGE_TITLE}}", esc(t_title))
                     .replace("{{PAGE_DESC}}", esc(t_desc))
                     .replace("{{PAGE_URL}}", esc(t_url))
                     .replace("{{ROOT}}", "../../"))
            for k, v in subs.items():
                html_ = html_.replace(k, v)
            html_ = html_.replace("{{LANG_SWITCH}}", i18n.switch_links(
                base, langs, code, "topics/" + tid + "/"))
            html_ = mark_nav(html_, "%s/topics/%s" % (code, tid))
            left = re.findall(r"\{\{[A-Z_]+\}\}", html_)
            if left:
                sys.exit("%s/topics/%s: unreplaced placeholders: %s"
                         % (code, tid, ", ".join(sorted(set(left)))))
            html_ = add_to_head(html_, t_url, head_extra_topic(
                cfg, base, langs, entry, tid,
                "%s \u2014 %s" % (t_title, top_for(ov, code, "title", cfg["title"])),
                t_desc, payload))
            write(os.path.join(sub, "topics", tid, "index.html"), html_)
            sitemap_urls.append((t_url, "weekly", "0.6"))

        # /topics/: the index of the hub pages above. It used to be a 404,
        # although /datasets/, /guides/ and /graph/ all had an index.
        if topic_ids:
            ti_rel = "topics/"
            ti_url = lang_base + ti_rel
            ti_title = strings.get("indexTitle", "Topics")
            ti_desc = re.sub(r"\s+", " ", strings.get("indexDesc", "")
                             .replace("{n}", str(len(topic_ids)))).strip()
            html_ = fill_page(tpl, render_topics_index(payload, topic_ids, strings),
                              ti_title, ti_desc, ti_url, "../", subs,
                              "%s/topics" % code,
                              i18n.switch_links(base, langs, code, ti_rel))
            html_ = add_to_head(html_, ti_url, head_extra_graph(
                cfg, base, langs, entry, ov, ti_desc, rel=ti_rel, title=ti_title))
            write(os.path.join(sub, "topics", "index.html"), html_)
            sitemap_urls.append((ti_url, "weekly", "0.6"))

        # ------------------------------------- datasets, benchmarks, guides
        site_t = top_for(ov, code, "title", cfg["title"])
        rsite = RP.Site(sys.modules[__name__], cfg, res_cfg, guides_doc, topic_doc or {},
                        rp_pages, payload, payload_en, entry, langs, base,
                        meta["last_updated"], topic_ids)
        rs = rsite.s
        added = new_pages.setdefault(code, [])
        guides_for = {}
        for g in rp_guides:
            for rel in rsite.guide_members(g):
                guides_for.setdefault(rel, []).append(g)

        def emit(rel, body, title, desc, head, depth):
            url = lang_base + rel
            html_ = fill_page(tpl, body, title, desc, url, "../" * depth, subs,
                              "%s/%s" % (code, rel),
                              i18n.switch_links(base, langs, code, rel))
            html_ = add_to_head(html_, url, head(
                "%s \u2014 %s" % (title, site_t), desc))
            if rel.startswith(RP.GUIDES_PATH) and rel != RP.GUIDES_PATH:
                ld, _ = faq_jsonld(html_)
                if ld:
                    html_ = add_to_head(html_, url, ld)
            write(os.path.join(sub, rel, "index.html"), html_)
            added.append(rel)

        t_ = rs["indexTitle"]
        d_ = rs["indexDesc"]
        # The datasets index also points at the graph's dataset slice
        # (which papers use which datasets): a reader cross-link, and
        # it keeps /graph/datasets/ from being an orphan page.
        emit(RP.DATASETS_PATH,
             rsite.index_body() +
             '<p><a href="../graph/datasets/">%s</a></p>'
             % esc(ov.ui("graphDatasetsTitle",
                         "Datasets & the papers that use them")),
             t_, d_, lambda t, d: rsite.index_head(t, d), 1)
        sitemap_urls.append((lang_base + RP.DATASETS_PATH, "weekly", "0.6"))
        for pg in rp_pages:
            t_ = rsite.resource_title(pg)
            d_ = rsite.resource_desc(pg)
            emit(pg["rel"], rsite.resource_body(pg, guides_for), t_, d_,
                 lambda t, d, pg=pg: rsite.resource_head(pg, t, d), 2)
            sitemap_urls.append((lang_base + pg["rel"], "monthly", "0.5"))
        emit(RP.GUIDES_PATH, rsite.guides_index_body(), rs["guidesTitle"], rs["guidesDesc"],
             lambda t, d: rsite.guides_index_head(t, d), 1)
        sitemap_urls.append((lang_base + RP.GUIDES_PATH, "monthly", "0.5"))
        for g in rp_guides:
            t_ = rsite.g_text(g, "title")
            d_ = rsite.g_text(g, "description")
            emit(RP.GUIDES_PATH + g["slug"] + "/", rsite.guide_body(g), t_, d_,
                 lambda t, d, g=g: rsite.guide_head(g, t, d), 2)
            sitemap_urls.append((lang_base + RP.GUIDES_PATH + g["slug"] + "/", "monthly", "0.6"))
        if rsite.problems:
            print("RESOURCE / GUIDE PAGES INVALID (%s):" % code)
            for x in rsite.problems:
                print("  -", x)
            sys.exit(1)

        write(os.path.join(sub, "data.json"),
              json.dumps(payload, ensure_ascii=False, indent=1) + "\n")

        # Each category page's own slice, beside its index.html; no
        # monolithic graph.json exists any more.
        for name, text in graph_slice_json.items():
            write(os.path.join(sub, "graph", *name.split("/"), "data.json"),
                  text)

    write(os.path.join(out, "robots.txt"), render_robots(base))
    en_payload = build_payload(i18n.SOURCE)
    write(os.path.join(out, "llms.txt"),
          render_llms(cfg, base, en_payload["counts"], en_payload["topics"],
                      set(topic_ids), rp_pages, rp_guides, payload_en,
                      lineages))
    # Brand files: the favicon, the iOS touch icon and the share image.
    # Generated from assets/logo.svg's geometry (brand_assets), so the repo
    # carries no binary blobs and the build stays stdlib-only.
    write(os.path.join(out, "favicon.svg"),
          read(os.path.join(ROOT, "assets", "logo.svg")))
    write_bytes(os.path.join(out, "favicon.ico"), brand_assets.favicon_ico())
    write_bytes(os.path.join(out, "apple-touch-icon.png"),
                brand_assets.apple_touch_icon())
    write_bytes(os.path.join(out, "og-image.png"), brand_assets.og_image())
    # IndexNow (Bing, Yandex, ...): the key file must be served at the site
    # root; the deploy workflow pings api.indexnow.org with the sitemap URLs.
    if cfg.get("indexnow_key"):
        write(os.path.join(out, "%s.txt" % cfg["indexnow_key"]),
              cfg["indexnow_key"] + "\n")
    # <lastmod> is the content date (data/meta.yaml last_updated), not the
    # build date: a rebuild that changes no data must not tell search engines
    # that every page changed today.
    write(os.path.join(out, "sitemap.xml"),
          render_sitemap(sitemap_urls, str(meta["last_updated"])))
    write(os.path.join(out, ".nojekyll"), "")

    # Version every page's core stylesheet and scripts, as the graph and
    # lineage pages already do (see _asset_version). GitHub Pages serves them
    # with max-age=600, so for ten minutes after a deploy a browser could pair
    # the new HTML (and its inline data) with the previous app.js or
    # styles.css. A content hash in the URL makes each deploy a new URL.
    core_re = re.compile(r'((?:href|src)="(?:[^"?#]*/)?)(%s)"'
                         % "|".join(re.escape(a) for a in CORE_ASSETS))
    for dirpath, _dirs, files in os.walk(out):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            html_text = read(fp)
            new_text = core_re.sub(
                lambda m: '%s%s?v=%s"' % (m.group(1), m.group(2),
                                          _asset_version(m.group(2))),
                html_text)
            if new_text != html_text:
                write(fp, new_text)

    # GitHub Pages reads CNAME from the deployed files. With the Actions source
    # the domain is also set in Settings -> Pages, but writing it here keeps the
    # site's own record of where it belongs beside the canonical URL it was
    # built with, so the two cannot drift apart.
    if not cfg.get("_url_from_repo"):
        write(os.path.join(out, "CNAME"), host_of(base) + "\n")

    # ------------------------------------------------------------ self-check
    # A deployment must expose exactly one origin, or search engines split the
    # ranking between the custom domain and the free github.io copy. This is the
    # guard Paper-Notes uses; keep it.
    #
    # Only *this repository's* Pages address counts as a leak. Third-party
    # project pages on *.github.io are ordinary links in a corpus of papers
    # (ooonesevennn.github.io/DiffNR/, open-pros.github.io, ...), so a bare
    # "github.io" substring test would fail the build on perfectly good data.
    # The canonical / og:url pair is checked per language above, where each
    # language's own URL is known; what is left here is origin-level.
    problems = []
    if "Sitemap: %ssitemap.xml" % base not in read(os.path.join(out, "robots.txt")):
        problems.append("robots.txt sitemap points elsewhere")
    if not cfg.get("_url_from_repo"):
        own_pages = "%s.github.io" % (cfg["repo"].split("/")[0] or "\x00")
        for fname in ("index.html", "robots.txt", "sitemap.xml"):
            if own_pages in read(os.path.join(out, fname)):
                problems.append("our own Pages address (%s) leaked into %s of a "
                                "custom-domain build" % (own_pages, fname))
        cname = os.path.join(out, "CNAME")
        if not os.path.exists(cname) or read(cname).strip() != host_of(base):
            problems.append("CNAME is missing or does not match the configured origin")
    # ------------------------------------------------------- note translation
    # A note lives in English in data/*.yaml and may be translated in
    # data/i18n/<code>.yaml. The overlay is merged at export time, so a
    # translated note has to appear in that language's data.json. This used to
    # silently fall back to English because export_site_data read the raw
    # field; asserting it here keeps that from coming back. Missing *entire*
    # translations are fine (that is a normal fallback), but a translation
    # that exists and gets dropped is a bug.
    for entry in langs:
        code = entry["code"]
        if code == i18n.SOURCE:
            continue
        ov = i18n.load(code)
        sub = os.path.join(out, entry.get("path") or "")
        data = json.load(io.open(os.path.join(sub, "data.json"), encoding="utf-8"))
        for table, key_field in (("papers", "id"), ("toolkits", "name"),
                                 ("datasets", "name"), ("benchmarks", "name"),
                                 ("learning", "name")):
            for rec in data.get(table) or []:
                want = ov.item(table, rec[key_field]).get("note")
                if want and rec.get("note") != want:
                    problems.append(
                        "%s/%s: %s %r has a translated note that did not reach "
                        "data.json" % (code, table, key_field, rec[key_field]))
        # Teams carry their long text in `intro` rather than `note`, keyed by
        # the team's id; the same dropped-translation guard applies.
        for rec in data.get("teams") or []:
            want = ov.item("teams", rec["id"]).get("intro")
            if want and rec.get("intro") != re.sub(r"\s+", " ", want).strip():
                problems.append(
                    "%s/teams: id %r has a translated intro that did not reach "
                    "data.json" % (code, rec["id"]))

    # ------------------------------------------------------------ topic pages
    # Every topic page must name itself as canonical and carry the full set of
    # hreflang alternates (each language plus x-default), or search engines
    # treat the two editions as duplicates instead of translations.
    default = i18n.default_language(langs)
    for entry in langs:
        sub = os.path.join(out, entry.get("path") or "")
        lang_base = i18n.url_for(base, entry)
        for tid in topic_ids:
            f = os.path.join(sub, "topics", tid, "index.html")
            if not os.path.exists(f):
                problems.append("%s: topic page %s was not written" % (entry["code"], tid))
                continue
            page = read(f)
            if ('<link rel="canonical" href="%s">' % esc(topic_url(lang_base, tid))) not in page:
                problems.append("%s/topics/%s: canonical missing or wrong" % (entry["code"], tid))
            want = [(e["hreflang"], topic_url(i18n.url_for(base, e), tid)) for e in langs]
            want.append(("x-default", topic_url(i18n.url_for(base, default), tid)))
            for hl, u in want:
                if ('<link rel="alternate" hreflang="%s" href="%s">' % (esc(hl), esc(u))) not in page:
                    problems.append("%s/topics/%s: hreflang %s missing or wrong"
                                    % (entry["code"], tid, hl))
            if '"BreadcrumbList"' not in page or '"CollectionPage"' not in page:
                problems.append("%s/topics/%s: JSON-LD missing" % (entry["code"], tid))
            if (topic_url(lang_base, tid)) not in read(os.path.join(out, "sitemap.xml")):
                problems.append("%s/topics/%s: not in sitemap.xml" % (entry["code"], tid))
        about = read(os.path.join(sub, "about", "index.html"))
        for tid in topic_ids:
            if 'href="../topics/%s/"' % tid not in about:
                problems.append("%s/about: no link to topic page %s" % (entry["code"], tid))
        if faq_counts.get(entry["code"], 0) and '"FAQPage"' not in about:
            problems.append("%s/about: FAQ present but FAQPage JSON-LD missing" % entry["code"])

    # ------------------------------------------------------------- brand
    # Every page must carry the favicon + share image, or a new page type
    # silently ships without them again. The files themselves must exist:
    # a head that points at a missing favicon.ico is worse than no favicon.
    for name in ("favicon.svg", "favicon.ico", "apple-touch-icon.png",
                 "og-image.png"):
        f = os.path.join(out, name)
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            problems.append("brand file %s was not written" % name)
    for dirpath, _, files in os.walk(out):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            f = os.path.join(dirpath, fn)
            page = read(f)
            if 'rel="icon"' not in page:
                problems.append("%s: favicon link missing"
                                % os.path.relpath(f, out))
            if 'property="og:image"' not in page:
                problems.append("%s: og:image missing"
                                % os.path.relpath(f, out))
            if page.count('name="twitter:card"') != 1:
                problems.append("%s: twitter:card must appear exactly once"
                                % os.path.relpath(f, out))
            # hreflang / og live in the head: the body also carries
            # hreflang on the language switcher, which must not count.
            head = page.split("</head>")[0]
            if "hreflang" not in head:
                problems.append("%s: hreflang missing from head"
                                % os.path.relpath(f, out))
            if 'property="og:' not in head:
                problems.append("%s: og: tags missing from head"
                                % os.path.relpath(f, out))

    # ------------------------------------------------- changelog + DataCatalog
    # The changelog page must be canonical, carry every hreflang alternate,
    # a BreadcrumbList, appear in sitemap.xml and be linked from About. The
    # homepage DataCatalog must agree with the live counts and the update date
    # the stat tiles show, or it would be saying something the page does not.
    sitemap = read(os.path.join(out, "sitemap.xml"))
    for entry in langs:
        code = entry["code"]
        sub = os.path.join(out, entry.get("path") or "")
        lang_base = i18n.url_for(base, entry)
        f = os.path.join(sub, "changelog", "index.html")
        if not os.path.exists(f):
            problems.append("%s: changelog page was not written" % code)
        else:
            page = read(f)
            cl_url = lang_base + CHANGELOG_PATH
            if ('<link rel="canonical" href="%s">' % esc(cl_url)) not in page:
                problems.append("%s/changelog: canonical missing or wrong" % code)
            want = [(e["hreflang"], i18n.url_for(base, e) + CHANGELOG_PATH) for e in langs]
            want.append(("x-default", i18n.url_for(base, default) + CHANGELOG_PATH))
            for hl, u in want:
                if ('<link rel="alternate" hreflang="%s" href="%s">' % (esc(hl), esc(u))) not in page:
                    problems.append("%s/changelog: hreflang %s missing or wrong" % (code, hl))
            if '"BreadcrumbList"' not in page:
                problems.append("%s/changelog: BreadcrumbList JSON-LD missing" % code)
            if page.count('class="cl-entry"') != len(cl_entries):
                problems.append("%s/changelog: %d entries rendered, CHANGELOG.md has %d"
                                % (code, page.count('class="cl-entry"'), len(cl_entries)))
            if "<loc>%s</loc>" % esc(cl_url) not in sitemap:
                problems.append("%s/changelog: not in sitemap.xml" % code)
        # Look inside <main> only: the shared footer links the changelog too,
        # and that must not satisfy the check for the About body.
        about = read(os.path.join(sub, "about", "index.html"))
        about_main = re.search(r"<main\b.*?</main>", about, re.S)
        if not about_main or 'href="../changelog/"' not in about_main.group(0):
            problems.append("%s/about: no link to the changelog" % code)

        home = read(os.path.join(sub, "index.html"))
        data = json.load(io.open(os.path.join(sub, "data.json"), encoding="utf-8"))
        cat = None
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', home, re.S):
            obj = json.loads(blob)
            if obj.get("@type") == "DataCatalog":
                cat = obj
        if not cat:
            problems.append("%s/index: DataCatalog JSON-LD missing" % code)
            continue
        dc = data["counts"]
        if cat.get("dateModified") != dc["updated"]:
            problems.append("%s/index: DataCatalog dateModified %r != last_updated %r"
                            % (code, cat.get("dateModified"), dc["updated"]))
        if cat.get("url") != lang_base:
            problems.append("%s/index: DataCatalog url is not the page URL" % code)
        names = dict((d["@id"].rsplit("-", 1)[-1], d) for d in cat.get("dataset") or [])
        for key in ("papers", "datasets", "benchmarks"):
            d = names.get(key)
            if not d or not d.get("description", "").startswith(str(dc[key])):
                problems.append("%s/index: DataCatalog dataset %s missing or its count "
                                "is not %d" % (code, key, dc[key]))

    # ------------------------------------- datasets, benchmarks and guides
    # Each new page must be canonical, carry every hreflang alternate and its
    # JSON-LD, be in sitemap.xml, and be linked from another page (no orphans):
    # the index pages from About, entry pages from /datasets/, guides from
    # /guides/ and About. Topic pages must link every entry page they list.
    for entry in langs:
        code = entry["code"]
        sub = os.path.join(out, entry.get("path") or "")
        lang_base = i18n.url_for(base, entry)
        pages_html = {}
        for rel in new_pages.get(code, []):
            f = os.path.join(sub, rel, "index.html")
            page = read(f)
            pages_html[rel] = page
            if ('<link rel="canonical" href="%s">' % esc(lang_base + rel)) not in page:
                problems.append("%s/%s: canonical missing or wrong" % (code, rel))
            want = [(e["hreflang"], i18n.url_for(base, e) + rel) for e in langs]
            want.append(("x-default", i18n.url_for(base, default) + rel))
            for hl, u in want:
                if ('<link rel="alternate" hreflang="%s" href="%s">' % (esc(hl), esc(u))) not in page:
                    problems.append("%s/%s: hreflang %s missing or wrong" % (code, rel, hl))
            if '"BreadcrumbList"' not in page:
                problems.append("%s/%s: BreadcrumbList missing" % (code, rel))
            if rel.startswith(("datasets/", "benchmarks/")) and rel != RP.DATASETS_PATH \
                    and '"@type":"Dataset"' not in page:
                problems.append("%s/%s: Dataset JSON-LD missing" % (code, rel))
            if rel.startswith(RP.GUIDES_PATH) and rel != RP.GUIDES_PATH:
                if '"FAQPage"' not in page or '<section class="faq">' not in page:
                    problems.append("%s/%s: FAQ or FAQPage JSON-LD missing" % (code, rel))
            if "<loc>%s</loc>" % esc(lang_base + rel) not in sitemap:
                problems.append("%s/%s: not in sitemap.xml" % (code, rel))
        about = read(os.path.join(sub, "about", "index.html"))
        idx = pages_html.get(RP.DATASETS_PATH, "")
        gidx = pages_html.get(RP.GUIDES_PATH, "")
        for rel in pages_html:
            if rel in (RP.DATASETS_PATH, RP.GUIDES_PATH):
                linked = ('href="../%s"' % rel) in about
            elif rel.startswith(RP.GUIDES_PATH):
                linked = ('href="../%s"' % rel) in gidx and ('href="../%s"' % rel) in about
            else:
                linked = ('href="../%s"' % rel) in idx
            if not linked:
                problems.append("%s/%s: orphan page (no link from its index or About)" % (code, rel))
        for tid in topic_ids:
            page = read(os.path.join(sub, "topics", tid, "index.html"))
            tp = topic_doc["topics"][tid]
            for kind, r in topic_resources(tp, payload_en):
                rel = rp_res.get((kind, r["name"]))
                if rel and ('href="../../%s"' % rel) not in page:
                    problems.append("%s/topics/%s: no link to %s" % (code, tid, rel))
            for g in rp_topic_guides.get(tid, []):
                if ('href="../../guides/%s/"' % g["slug"]) not in page:
                    problems.append("%s/topics/%s: no link to guide %s" % (code, tid, g["slug"]))

    # ------------------------------------------------------------- graph
    # The graph index must be canonical, carry every hreflang alternate
    # and a BreadcrumbList, appear in sitemap.xml, and link every
    # category page; each category page must meet the same bar, and its
    # data.json must parse, match the slice the build computed, and
    # reconcile with the payload it projects. The retired monolith
    # (graph.json at a language root, a full-graph mode) must not
    # reappear.
    _ov_by_code = {}
    for entry in langs:
        code = entry["code"]
        sub = os.path.join(out, entry.get("path") or "")
        lang_base = i18n.url_for(base, entry)
        f = os.path.join(sub, "graph", "index.html")
        if not os.path.exists(f):
            problems.append("%s: graph page was not written" % code)
            continue
        if os.path.exists(os.path.join(sub, "graph.json")):
            problems.append("%s: retired monolithic graph.json was written"
                            % code)
        page = read(f)
        g_url = lang_base + GRAPH_PATH
        if ('<link rel="canonical" href="%s">' % esc(g_url)) not in page:
            problems.append("%s/graph: canonical missing or wrong" % code)
        want = [(e["hreflang"], i18n.url_for(base, e) + GRAPH_PATH) for e in langs]
        want.append(("x-default", i18n.url_for(base, default) + GRAPH_PATH))
        for hl, u in want:
            if ('<link rel="alternate" hreflang="%s" href="%s">' % (esc(hl), esc(u))) not in page:
                problems.append("%s/graph: hreflang %s missing or wrong" % (code, hl))
        if '"BreadcrumbList"' not in page:
            problems.append("%s/graph: BreadcrumbList JSON-LD missing" % code)
        if "<loc>%s</loc>" % esc(g_url) not in sitemap:
            problems.append("%s/graph: not in sitemap.xml" % code)
        for rel in graph_rels.get(code, []):
            name = rel[len(GRAPH_PATH):].rstrip("/")
            if ('href="%s/"' % name) not in page:
                problems.append("%s/graph: index does not link %s" % (code, rel))
            pf = os.path.join(sub, rel, "index.html")
            if not os.path.exists(pf):
                problems.append("%s/%s: graph page was not written" % (code, rel))
                continue
            ppage = read(pf)
            p_url = lang_base + rel
            if ('<link rel="canonical" href="%s">' % esc(p_url)) not in ppage:
                problems.append("%s/%s: canonical missing or wrong" % (code, rel))
            want = [(e["hreflang"], i18n.url_for(base, e) + rel) for e in langs]
            want.append(("x-default", i18n.url_for(base, default) + rel))
            for hl, u in want:
                if ('<link rel="alternate" hreflang="%s" href="%s">' % (esc(hl), esc(u))) not in ppage:
                    problems.append("%s/%s: hreflang %s missing or wrong"
                                    % (code, rel, hl))
            if '"BreadcrumbList"' not in ppage:
                problems.append("%s/%s: BreadcrumbList JSON-LD missing" % (code, rel))
            if "<loc>%s</loc>" % esc(p_url) not in sitemap:
                problems.append("%s/%s: not in sitemap.xml" % (code, rel))
            if 'id="graph-full"' in ppage or "graph.json" in ppage:
                problems.append("%s/%s: retired full-graph machinery present"
                                % (code, rel))
            # HTML, renderer and slice data must be version-locked to
            # one deploy (see _asset_version); an unversioned URL here
            # means a future stale cache can pair them across deploys.
            for marker in ('graphology.min.js?v=', 'sigma.min.js?v=',
                           'graph.js?v=', 'data.json?v='):
                if marker not in ppage:
                    problems.append("%s/%s: graph asset URL lacks its "
                                    "cache-buster (%s)" % (code, rel, marker))
            if ('<p class="graph-back"><a href="%s?tab=graph">'
                    % ("../" * (rel.rstrip("/").count("/") + 1))) not in ppage:
                problems.append("%s/%s: back-to-index link wrong" % (code, rel))
            dj = os.path.join(sub, rel, "data.json")
            if not os.path.exists(dj):
                problems.append("%s/%s: data.json was not written" % (code, rel))
                continue
            sdata = json.load(io.open(dj, encoding="utf-8"))
            sl = graph_slices[name]
            if len(sdata["nodes"]) != len(sl["nodes"]) \
                    or len(sdata["edges"]) != len(sl["edges"]) \
                    or len(sdata["pos"]) != len(sl["nodes"]):
                problems.append("%s/%s: data.json does not match its slice "
                                "(%d nodes / %d edges)"
                                % (code, rel, len(sdata["nodes"]),
                                   len(sdata["edges"])))
            types = Counter(n["t"] for n in sdata["nodes"])
            # P0-1 regression: a translated slice's topic nodes must carry
            # the overlay label (lz). graph.node() drops lz when it equals
            # the English label, so only genuinely translated names are
            # asserted here.
            if code != i18n.SOURCE:
                if code not in _ov_by_code:
                    _ov_by_code[code] = i18n.load(code)
                ov_c = _ov_by_code[code]
                en_names = dict((t["id"], t["name"])
                                for t in payload_en["topics"])
                for n in sdata["nodes"]:
                    if n["t"] != "topic":
                        continue
                    tid = n["id"][len("topic:"):]
                    want = ov_c.topic(tid).get("name") or en_names.get(tid)
                    if (want and want != en_names.get(tid)
                            and n.get("lz") != want):
                        problems.append(
                            "%s/%s: topic node %s lacks label '%s' (has %r)"
                            % (code, rel, tid, want, n.get("lz")))
            # A slice ships only nodes with at least one edge inside
            # it; the isolates it dropped ride along on the slice
            # (sl["dropped"]), so completeness is slice + dropped.
            gtype = dict((n["id"], n["t"]) for n in graph["nodes"])
            dropped = Counter(gtype[i] for i in (sl.get("dropped") or [])
                              if i in gtype)
            sdeg = Counter()
            for e in sdata["edges"]:
                sdeg[sdata["nodes"][e[0]]["id"]] += 1
                sdeg[sdata["nodes"][e[1]]["id"]] += 1
            isolates = [n["id"] for n in sdata["nodes"]
                        if sdeg[n["id"]] == 0]
            if "dropped" in sl and isolates:
                problems.append("%s/%s: slice ships %d isolated nodes "
                                "(e.g. %s)"
                                % (code, rel, len(isolates), isolates[0]))
            if name == "backbone":
                for tname, want_n in (("team", len(payload_en["teams"])),
                                      ("topic", len(payload_en["topics"])),
                                      ("toolkit", len(payload_en["toolkits"])),
                                      ("guide", len(rp_guides))):
                    if types.get(tname, 0) + dropped.get(tname, 0) != want_n:
                        problems.append("%s/%s: %s nodes %d + %d dropped "
                                        "!= payload %d"
                                        % (code, rel, tname,
                                           types.get(tname, 0),
                                           dropped.get(tname, 0), want_n))
            if name == "datasets":
                for tname, key in (("dataset", "datasets"),
                                   ("benchmark", "benchmarks")):
                    if types.get(tname, 0) + dropped.get(tname, 0) \
                            != len(payload_en[key]):
                        problems.append("%s/%s: %s nodes %d + %d dropped "
                                        "!= payload %d"
                                        % (code, rel, tname,
                                           types.get(tname, 0),
                                           dropped.get(tname, 0),
                                           len(payload_en[key])))
            if name.startswith("topic/"):
                tid = name[len("topic/"):]
                if types.get("topic", 0) != 1 \
                        or ("topic:" + tid) not in set(n["id"] for n in sdata["nodes"]):
                    problems.append("%s/%s: its topic node is missing"
                                    % (code, rel))
                if len(sdata["nodes"]) > graph_slices_mod.CAP:
                    problems.append("%s/%s: %d nodes over the %d cap"
                                    % (code, rel, len(sdata["nodes"]),
                                       graph_slices_mod.CAP))

    # ------------------------------------------------------------- lineages
    # Each curated lineage page must be canonical, carry every hreflang
    # alternate and a BreadcrumbList, appear in sitemap.xml, and be
    # linked from its own language's graph index (no orphans) — the
    # same bar as the other graph pages, minus the slice data: a
    # lineage page ships no data.json; its canvas contract is the
    # inline layout JSON checked below.
    for entry in langs:
        code = entry["code"]
        sub = os.path.join(out, entry.get("path") or "")
        lang_base = i18n.url_for(base, entry)
        gindex = os.path.join(sub, "graph", "index.html")
        index_page = read(gindex) if os.path.exists(gindex) else ""
        for rel in lineage_rels.get(code, []):
            lid = rel[len(GRAPH_PATH + "lineage/"):].rstrip("/")
            pf = os.path.join(sub, rel, "index.html")
            if not os.path.exists(pf):
                problems.append("%s/%s: lineage page was not written"
                                % (code, rel))
                continue
            ppage = read(pf)
            p_url = lang_base + rel
            if ('<link rel="canonical" href="%s">' % esc(p_url)) not in ppage:
                problems.append("%s/%s: canonical missing or wrong"
                                % (code, rel))
            want = [(e["hreflang"], i18n.url_for(base, e) + rel)
                    for e in langs]
            want.append(("x-default",
                         i18n.url_for(base, default) + rel))
            for hl, u in want:
                if ('<link rel="alternate" hreflang="%s" href="%s">'
                        % (esc(hl), esc(u))) not in ppage:
                    problems.append("%s/%s: hreflang %s missing or wrong"
                                    % (code, rel, hl))
            if '"BreadcrumbList"' not in ppage:
                problems.append("%s/%s: BreadcrumbList JSON-LD missing"
                                % (code, rel))
            if "<loc>%s</loc>" % esc(p_url) not in sitemap:
                problems.append("%s/%s: not in sitemap.xml" % (code, rel))
            if ('href="lineage/%s/"' % lid) not in index_page:
                problems.append("%s/graph: index does not link lineage %s"
                                % (code, lid))
            # The tree canvas: the embedded layout JSON is the contract
            # the viewport script and tests/test_seo.js both read, so
            # the markup must agree with it (counts, bounds, no overlap).
            _m = re.search(r'<script type="application/json" class="tree-layout">(.*?)</script>', ppage, re.S)
            if not _m:
                problems.append("%s/%s: tree layout JSON missing" % (code, rel))
            else:
                _lay = json.loads(_m.group(1))
                _boxes = _lay["nodes"]
                _papers = sum(1 for b in _boxes if not b["group"])
                _svgm = re.search(r'<svg class="tree-edges".*?</svg>', ppage, re.S)
                _paths = _svgm.group(0).count("<path") if _svgm else -1
                for _what, _got, _want in (
                        ("tn-node cards", ppage.count('class="tn-node"'), _papers),
                        ("tn-group boxes", ppage.count('class="tn-group"'), len(_boxes) - _papers),
                        ("svg paths", _paths, len(_lay["edges"])),
                        ("edges vs nodes", len(_lay["edges"]), len(_boxes) - 1),
                        ("tn-label chips", ppage.count('class="tn-label"'), len(_lay["edges"])),
                        ("reading entries", ppage.count('class="lr-item"'), _papers)):
                    if _got != _want:
                        problems.append("%s/%s: %s = %d, layout JSON says %d"
                                        % (code, rel, _what, _got, _want))
                for _prob in lineage_tree.check_layout(_lay):
                    problems.append("%s/%s: %s" % (code, rel, _prob))

    if problems:
        print("SITE CHECK FAILED:")
        for x in problems:
            print("  -", x)
        sys.exit(1)

    total = sum(os.path.getsize(os.path.join(out, f))
                for f in os.listdir(out) if os.path.isfile(os.path.join(out, f)))
    # `--out` may point at another drive (H: project, C: scratch). relpath
    # raises ValueError across drives rather than returning a path, so fall
    # back to the absolute one. Same guard as export_site_data.py.
    try:
        out_label = os.path.relpath(out, ROOT)
    except ValueError:
        out_label = out
    print("built %s for %s" % (out_label, base))
    print("  index.html %.0f KB, data.json %.0f KB, whole site %.0f KB"
          % (os.path.getsize(os.path.join(out, "index.html")) / 1024.0,
             os.path.getsize(os.path.join(out, "data.json")) / 1024.0,
             total / 1024.0))
    print("  %d papers (%d peer-reviewed, %d preprints), %d toolkits, %d datasets, "
          "%d benchmarks, %d learning"
          % (c["papers"], c["peer_reviewed"], c["preprints"], c["toolkits"],
             c["datasets"], c["benchmarks"], c["learning"]))
    print("  changelog: %d entries per language, sitemap %d URLs"
          % (len(cl_entries), len(sitemap_urls)))
    if topic_ids:
        print("  %d topic pages per language (%d languages), FAQ entries on About: %s"
              % (len(topic_ids), len(langs),
                 ", ".join("%s %d" % kv for kv in sorted(faq_counts.items()))))
    print("  %d dataset and %d benchmark pages per language, %d entries skipped, %d guides"
          % (sum(1 for pg in rp_pages if pg["table"] == "datasets"),
             sum(1 for pg in rp_pages if pg["table"] == "benchmarks"),
             len(rp_skipped), len(rp_guides)))
    for table, name, why in rp_skipped:
        print("    skipped %s %r: %s" % (table, name, why))
    if cfg.get("_url_from_repo"):
        print("  note: `url` is empty in site.config.yml, so the GitHub Pages "
              "address was used. Set it once the domain is ready.")


if __name__ == "__main__":
    main()
