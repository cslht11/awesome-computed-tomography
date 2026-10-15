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
import html
import io
import json
import os
import re
import sys
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import load, validate, fill  # noqa: E402
from export_site_data import build_payload  # noqa: E402
import i18n  # noqa: E402

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


def esc(s):
    return html.escape(str(s), quote=True)


def md_inline(text):
    """The legends in build.py are Markdown; the site needs HTML. Same words,
    so the README and the page cannot drift apart."""
    out = esc(text)
    out = out.replace("`", "\x00")
    out = re.sub(r"\x00([^\x00]+)\x00", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


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
            head += ('<span class="p-titletext has-blurb" tabindex="0"'
                     ' role="button" aria-label="What this paper is about"'
                     ' title="%s">%s</span>' % (esc(blurb), esc(title)))
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
    ld_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "CT reconstruction papers",
        "numberOfItems": len(payload["papers"]),
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": p["title"],
                "url": (p["links"].get("paper") or p["links"].get("project")
                        or p["links"].get("code") or base),
            }
            for i, p in enumerate(payload["papers"])
        ],
    }

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
        '<meta name="twitter:card" content="summary">',
        '<meta name="twitter:title" content="%s \u2014 %s">' % (esc(title), esc(top_for(ov, entry["code"], "tagline", cfg["tagline"]))),
        '<meta name="twitter:description" content="%s">' % esc(desc),
        '<link rel="license" href="%s">' % esc(cfg["content_license_url"]),
        '<link rel="alternate" type="application/json" href="./data.json" title="Machine-readable dataset">',
        '<script type="application/ld+json">%s</script>' % safe_json(ld_org),
        '<script type="application/ld+json">%s</script>' % safe_json(ld_site),
        '<script type="application/ld+json">%s</script>' % safe_json(ld_list),
    ]

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


def render_llms(cfg, base, c, topics):
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
        "- [论文目录（中文）](%szh/): Chinese edition of the same directory" % base,
        "- [About](%sabout/): scope, sourcing, verification and how to cite" % base,
        "- [Contact](%scontact/): how to suggest or correct an entry" % base,
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
        lines.append("- %s (%d papers): %s" % (t["name"], t["count"], t["desc"]))
    return "\n".join(lines) + "\n"


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

    base = resolve_base(cfg, args.url)
    cfg["repo_url"] = "https://github.com/" + cfg["repo"]

    # Counts are language-independent, so one build of the source-language
    # payload is enough to size the page tokens. The per-language loop below
    # rebuilds the payload so each language's data.json carries its own notes.
    payload = build_payload(i18n.SOURCE)
    c = payload["counts"]
    today = datetime.date.today().isoformat()

    peer_pct = round(100.0 * c["peer_reviewed"] / c["papers"]) if c["papers"] else 0
    # The coverage sentence now comes from ui.coverage per language, so it reads
    # in the page's own language; see `shared["coverage"]` below.

    out = args.out
    meta = yaml.safe_load(io.open(os.path.join(ROOT, "data", "meta.yaml"),
                                  encoding="utf-8"))
    langs = i18n.languages(meta)

    # Tokens available inside every ui.* and readme.* string. Only ever numbers
    # and known-safe config values — see the header comment in data/i18n/en.yaml.
    tokens = {
        "papers": c["papers"], "peer": c["peer_reviewed"], "peer_pct": peer_pct,
        "preprints": c["preprints"], "toolkits": c["toolkits"],
        "datasets": c["datasets"], "benchmarks": c["benchmarks"],
        "learning": c["learning"], "year_min": c["year_min"],
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
    sitemap_urls = []

    for entry in langs:
        code = entry["code"]
        ov = i18n.load(code)
        lang_base = i18n.url_for(base, entry)
        sub = os.path.join(out, entry.get("path") or "")

        # Rebuild per language rather than mutating one shared payload: the
        # notes (and the topic names below) differ by language, and the
        # previous iteration's edits would otherwise leak into this one.
        payload = build_payload(code)

        shared = dict(tokens)
        shared["coverage"] = fill(ov.ui("coverage"), tokens)
        payload["ui"] = js_ui(ov)
        # Topic names and blurbs are display text too, and live in data/meta.yaml
        # in English; the overlay is what makes them read in this language.
        for t in payload["topics"]:
            tr = ov.topic(t["id"])
            t["name"] = tr.get("name") or t["name"]
            t["desc"] = tr.get("desc") or t["desc"]

        # Absolute, so the same string works from any directory depth.
        switch = "".join(
            '<a href="%s" hreflang="%s" lang="%s">%s</a>'
            % (esc(i18n.url_for(base, e)), esc(e["hreflang"]),
               esc(e["html"]), esc(e["label"]))
            for e in langs if e["code"] != code)

        subs = {
            "{{HEAD}}": render_head(cfg, payload, lang_base, base, entry, langs,
                                   ov, tokens),
            "{{DATA}}": safe_json(payload),
            "{{PAPERS_STATIC}}": render_static_papers(payload, ov),
            "{{PAPERS_LEGEND}}": md_inline(ov.readme("legendPapers", PAPERS_LEGEND)),
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
            "{{LANG_SWITCH}}": switch,
            "{{N_PAPERS}}": str(c["papers"]),
            "{{N_PEER}}": str(c["peer_reviewed"]),
            "{{PEER_PCT}}": str(peer_pct),
            "{{N_PREPRINT}}": str(c["preprints"]),
            "{{N_TOOLKITS}}": str(c["toolkits"]),
            "{{N_DATASETS}}": str(c["datasets"]),
            "{{N_BENCHMARKS}}": str(c["benchmarks"]),
            "{{N_LEARNING}}": str(c["learning"]),
            "{{YEAR_MIN}}": str(c["year_min"]),
            "{{YEAR_MAX}}": str(c["year_max"]),
            "{{UPDATED}}": esc(str(meta["last_updated"])),
        }
        subs.update(ui_subs(ov, shared))

        page = index_tpl.replace("{{ROOT}}", "./")
        for k, v in subs.items():
            page = page.replace(k, v)
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
        sitemap_urls.append((lang_base, "weekly", "1.0"))

        for name in PAGES:
            body = ov.page(name)
            if not body.strip():
                sys.exit("data/i18n/%s.yaml carries no `pages.%s`" % (code, name))
            html_ = (tpl.replace("{{BODY}}", body)
                     .replace("{{PAGE_TITLE}}",
                              esc(ov.ui("page%sTitle" % name.title(), name.title())))
                     .replace("{{PAGE_DESC}}",
                              esc(fill(ov.ui("page%sDesc" % name.title(), ""), shared)))
                     .replace("{{PAGE_URL}}", esc(lang_base + name + "/"))
                     .replace("{{ROOT}}", "../"))
            for k, v in subs.items():
                html_ = html_.replace(k, v)
            left = re.findall(r"\{\{[A-Z_]+\}\}", html_)
            if left:
                sys.exit("%s/%s: unreplaced placeholders: %s"
                         % (code, name, ", ".join(sorted(set(left)))))
            write(os.path.join(sub, name, "index.html"), html_)
            sitemap_urls.append((lang_base + name + "/", "monthly", "0.3"))

        write(os.path.join(sub, "data.json"),
              json.dumps(payload, ensure_ascii=False, indent=1) + "\n")

    write(os.path.join(out, "robots.txt"), render_robots(base))
    en_payload = build_payload(i18n.SOURCE)
    write(os.path.join(out, "llms.txt"),
          render_llms(cfg, base, en_payload["counts"], en_payload["topics"]))
    # IndexNow (Bing, Yandex, ...): the key file must be served at the site
    # root; the deploy workflow pings api.indexnow.org with the sitemap URLs.
    if cfg.get("indexnow_key"):
        write(os.path.join(out, "%s.txt" % cfg["indexnow_key"]),
              cfg["indexnow_key"] + "\n")
    write(os.path.join(out, "sitemap.xml"), render_sitemap(sitemap_urls, today))
    write(os.path.join(out, ".nojekyll"), "")

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
    if cfg.get("_url_from_repo"):
        print("  note: `url` is empty in site.config.yml, so the GitHub Pages "
              "address was used. Set it once the domain is ready.")


if __name__ == "__main__":
    main()
