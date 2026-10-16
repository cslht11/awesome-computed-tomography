#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset, benchmark and guide pages for the static site.

    /datasets/                 index of every dataset and benchmark page
    /datasets/<slug>/          one page per dataset with real content
    /benchmarks/<slug>/        one page per benchmark with real content
    /guides/                   index of the guides
    /guides/<slug>/            evergreen guides (data/guides.yaml)

and the same under /zh/. build_site.py calls into this module; nothing here
writes files. Every fact on these pages is read from the directory's own data
(data/datasets.yaml, data/benchmarks.yaml, data/toolkits.yaml,
data/papers.yaml, data/topics.yaml); data/resources.yaml only decides which
rows get a page and how they are named, and data/guides.yaml carries the
guides' editorial prose. Which rows get a page is explained at the top of
data/resources.yaml.
"""

import html
import io
import json
import os
import re
import sys

import yaml

import brand_assets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_FILE = os.path.join(ROOT, "data", "resources.yaml")
GUIDES_FILE = os.path.join(ROOT, "data", "guides.yaml")

KINDS = (("datasets", "datasets/", "kindDataset"),
         ("benchmarks", "benchmarks/", "kindBenchmark"))
DATASETS_PATH = "datasets/"
GUIDES_PATH = "guides/"

# Exact SPDX-style licence strings in the data that have a canonical URL. Any
# other licence text is published as text, never guessed into a URL.
LICENSE_URLS = {
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "CC BY-NC 4.0": "https://creativecommons.org/licenses/by-nc/4.0/",
    "CC BY-NC 3.0": "https://creativecommons.org/licenses/by-nc/3.0/",
    "CC BY-NC-SA 4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "CC BY-NC-ND 3.0": "https://creativecommons.org/licenses/by-nc-nd/3.0/",
}
UNKNOWN_LICENSE = ("", "see source", "unknown")


def esc(s):
    return html.escape(str(s), quote=True)


def safe_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def plain(md):
    """Inline Markdown note -> plain text (for meta and JSON-LD)."""
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", md or "")
    t = re.sub(r"`([^`]+)`", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


DOMAIN_RE = re.compile(r"^\s*\*\*(Projection \+ image|Projection only)\.\*\*\s*", re.I)


def domain_of(note_en):
    """What a dataset ships, as the directory's English note states it.

    Notes on projection-domain data open with **Projection + image.** or
    **Projection only.**; an image-only collection says "image domain only" or
    "only image domain" in its note. Anything else is "not stated"."""
    m = DOMAIN_RE.match(note_en or "")
    if m:
        return "both" if "image" in m.group(1).lower() else "projection"
    low = (note_en or "").lower()
    if "image domain only" in low or "only image domain" in low or "image-domain only" in low:
        return "image"
    return "unknown"


def body_note(note):
    """The note without its leading **Projection ...** marker (shown as a fact
    instead)."""
    return DOMAIN_RE.sub("", note or "", count=1).strip()


def license_known(lic):
    return (lic or "").strip().lower() not in UNKNOWN_LICENSE


def license_url(lic):
    return LICENSE_URLS.get((lic or "").strip())


def free_access(lic):
    """True only for a plain Creative Commons licence with no access caveat."""
    lic = (lic or "").strip()
    return lic in LICENSE_URLS


def doi_of(url):
    m = re.match(r"^https?://(?:dx\.)?doi\.org/(10\.\S+)$", url or "")
    return m.group(1) if m else None


def note_dois(note):
    return re.findall(r"\bdoi:(10\.\d{4,9}/[^\s);,]+[^\s);,.])", note or "")


def norm_url(u):
    return re.sub(r"/+$", "", re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower()))


def fmt(template, **kw):
    out = template
    for k, v in kw.items():
        out = out.replace("{%s}" % k, str(v))
    return out


# ----------------------------------------------------------------- loading
def load_config():
    with io.open(RESOURCES_FILE, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    with io.open(GUIDES_FILE, encoding="utf-8") as f:
        guides = yaml.safe_load(f) or {}
    return cfg, guides


def strings(cfg, code, source="en"):
    s = dict((cfg.get("strings") or {}).get(source) or {})
    s.update((cfg.get("strings") or {}).get(code) or {})
    return s


# --------------------------------------------------------------- selection
def select(payload, topic_doc, topic_resources, cfg):
    """Decide which dataset/benchmark rows get a page.

    Returns (pages, skipped). ``pages`` is a list of dicts in directory order
    (datasets first); ``skipped`` a list of (table, name, reason)."""
    problems = []
    min_note = int(cfg.get("min_note") or 80)
    papers = payload["papers"]
    by_id = dict((p["id"], p) for p in papers)
    text = dict((p["id"], " ".join([p["title"], p.get("note") or "", p.get("blurb") or ""]))
                for p in papers)

    # Which topic pages list each row.
    on_topics = {}
    if topic_doc:
        for t in payload["topics"]:
            tp = (topic_doc.get("topics") or {}).get(t["id"])
            if not tp:
                continue
            for kind, r in topic_resources(tp, payload):
                on_topics.setdefault((kind, r["name"]), []).append(t["id"])

    pages, skipped, slugs = [], [], {}
    for table, path, kind in KINDS:
        conf = cfg.get(table) or {}
        names = set(r["name"] for r in payload[table])
        for n in conf:
            if n not in names:
                problems.append("data/resources.yaml: %s '%s' is not in data/%s.yaml"
                                % (table, n, table))
        for r in payload[table]:
            c = conf.get(r["name"]) or {}
            for pid in c.get("cite") or []:
                if pid not in by_id:
                    problems.append("data/resources.yaml: %s '%s' cites unknown paper '%s'"
                                    % (table, r["name"], pid))
            if c.get("skip"):
                skipped.append((table, r["name"], c["skip"]))
                continue
            note = body_note(r.get("note") or "")
            if len(plain(note)) < min_note:
                skipped.append((table, r["name"], "description too short"))
                continue
            if not r.get("url"):
                skipped.append((table, r["name"], "no official link"))
                continue
            # Papers that use or describe it: named (full name or a curated
            # alias) in a paper's title / note / abstract blurb, linked from
            # one of the paper's links, or listed as its citation.
            pats = [r["name"]] + list(c.get("aliases") or [])
            rx = re.compile("|".join(r"(?<![\w-])%s(?![\w])" % re.escape(a) for a in pats), re.I)
            own = set(norm_url(u) for u in (r.get("url"), r.get("homepage")) if u)
            used = []
            for p in papers:
                links = set(norm_url(u) for u in p["links"].values() if u)
                if rx.search(text[p["id"]]) or (links & own) or p["id"] in (c.get("cite") or []):
                    used.append(p["id"])
            topics = on_topics.get((kind, r["name"]), [])
            if not topics and not used:
                skipped.append((table, r["name"],
                                "no topic page lists it and no paper in the directory names or links it"))
                continue
            slug = c.get("slug") or slugify(r["name"])
            if (path, slug) in slugs:
                problems.append("data/resources.yaml: slug %s%s is used by both '%s' and '%s'"
                                % (path, slug, slugs[(path, slug)], r["name"]))
            slugs[(path, slug)] = r["name"]
            pages.append({
                "table": table, "path": path, "kind": kind, "name": r["name"],
                "slug": slug, "short": c.get("short") or r["name"],
                "rel": "%s%s/" % (path, slug),
                "topics": topics, "papers": used, "cite": list(c.get("cite") or []),
                "aliases": pats, "domain": domain_of(r.get("note")) if table == "datasets" else None,
            })
    if problems:
        print("RESOURCE PAGE DATA INVALID:")
        for x in problems:
            print("  -", x)
        sys.exit(1)

    # Related entries: rows (with or without a page) that share an official
    # link with this one, or whose name one of the two notes mentions.
    rows = [(t, r) for t, _, _ in KINDS for r in payload[t]]
    page_of = dict(((pg["table"], pg["name"]), pg) for pg in pages)
    for pg in pages:
        me = next(r for t, r in rows if t == pg["table"] and r["name"] == pg["name"])
        mine = set(norm_url(u) for u in (me.get("url"), me.get("homepage")) if u)
        rel = []
        for t, r in rows:
            if (t, r["name"]) == (pg["table"], pg["name"]):
                continue
            theirs = set(norm_url(u) for u in (r.get("url"), r.get("homepage")) if u)
            short_other = (page_of.get((t, r["name"])) or {}).get("short") or r["name"]
            named = (_mentions(me.get("note"), r["name"]) or _mentions(r.get("note"), pg["name"])
                     or (short_other != r["name"] and _mentions(me.get("note"), short_other)))
            if (mine & theirs) or named:
                rel.append((t, r["name"]))
        pg["related"] = rel
    return pages, skipped


def _mentions(note, name):
    if not note or len(name) < 4:
        return False
    return re.search(r"(?<![\w-])%s(?![\w])" % re.escape(name), note) is not None


# -------------------------------------------------------------- formatting
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def rich(text, root, known_paths, where, problems, anchors=None):
    """Escaped text with **bold** and [links](...). A link starting with '/'
    is a page of this site in the same language; it must be generated."""
    out = esc(re.sub(r"\s+", " ", text).strip())
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)

    def link(m):
        label, target = m.group(1), html.unescape(m.group(2))
        if target.startswith("/"):
            page, _, frag = target[1:].partition("#")
            pth = page.split("?")[0]
            if pth and pth not in known_paths:
                problems.append("%s: link to /%s, which is not a generated page" % (where, pth))
            return '<a href="%s%s">%s</a>' % (root, esc(page) + ("#" + esc(frag) if frag else ""), label)
        if target.startswith("#"):
            if anchors is not None and target[1:] not in anchors:
                problems.append("%s: in-page link %s has no target" % (where, target))
            return '<a href="%s">%s</a>' % (esc(target), label)
        if re.match(r"^https?://", target):
            return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(target), label)
        problems.append("%s: unsupported link target %s" % (where, target))
        return label
    return LINK_RE.sub(link, out)


def paras(text):
    return [x.strip() for x in re.split(r"\n\s*\n", (text or "").strip()) if x.strip()]


def head_bits(urls, entry, langs_default, url, title, desc, blocks, origin):
    """hreflang alternates, Open Graph and JSON-LD blocks for one page.
    ``urls`` is [(hreflang, url)] for every language. ``origin`` is the
    site root the favicon and share image live under."""
    bits = ['<link rel="alternate" hreflang="%s" href="%s">' % (esc(hl), esc(u)) for hl, u in urls]
    bits.append('<link rel="alternate" hreflang="x-default" href="%s">' % esc(langs_default))
    bits += ['<meta property="og:type" content="website">',
             '<meta property="og:url" content="%s">' % esc(url),
             '<meta property="og:title" content="%s">' % esc(title),
             '<meta property="og:description" content="%s">' % esc(desc),
             '<meta property="og:locale" content="%s">' % esc(entry["og_locale"])]
    bits.append(brand_assets.head_brand(origin))
    for b in blocks:
        bits.append('<script type="application/ld+json">%s</script>' % safe_json(b))
    return "\n".join(bits)


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                for i, (n, u) in enumerate(items)]}


def short_text(text, limit):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    out = ""
    for sent in re.split(r"(?<=[.!?;])\s+|(?<=[\u3002\uff1b\uff01\uff1f])", text):
        if not sent:
            continue
        if out and len(out) + len(sent) + 1 > limit:
            break
        out = (out + (" " if out and not re.search(r"[\u3000-\u9fff]$", out) else "") + sent).strip()
    if len(out) > limit or len(out) < limit // 2:
        cut = text[:limit - 1]
        if " " in cut[limit // 2:]:  # never split a word; CJK text has no spaces
            cut = cut.rsplit(" ", 1)[0]
        out = cut.rstrip(",;:—- ") + "\u2026"
    return out


# ---------------------------------------------------------------- rendering
DOMAIN_KEYS = {"both": "domainBoth", "projection": "domainProjection",
               "image": "domainImage", "unknown": "domainUnknown"}
DOMAIN_ORDER = {"both": 0, "projection": 1, "image": 2, "unknown": 3}


class Site(object):
    """Everything the pages of one language need. ``h`` is build_site (for
    paper_url / paper_label / md_inline), passed in to avoid a circular
    import."""

    def __init__(self, h, cfg_site, res_cfg, guides_doc, topic_doc, pages, payload,
                 payload_en, entry, langs, base, updated, topic_ids):
        self.h, self.cfg, self.res_cfg, self.gdoc = h, cfg_site, res_cfg, guides_doc
        self.topic_doc, self.pages = topic_doc, pages
        self.payload, self.en = payload, payload_en
        self.entry, self.langs, self.base = entry, langs, base
        self.code = entry["code"]
        self.lang_base = base + (entry.get("path") or "")
        self.updated = str(updated)
        self.s = strings(res_cfg, self.code)
        self.topic_ids = topic_ids
        self.topics = dict((t["id"], t) for t in payload["topics"])
        self.papers = dict((p["id"], p) for p in payload["papers"])
        self.rows = dict(((t, r["name"]), r) for t, _, _ in KINDS for r in payload[t])
        self.rows_en = dict(((t, r["name"]), r) for t, _, _ in KINDS for r in payload_en[t])
        self.page_of = dict(((pg["table"], pg["name"]), pg) for pg in pages)
        self.problems = []
        self.known = set(["", DATASETS_PATH, GUIDES_PATH, "about/", "contact/",
                          "privacy/", "changelog/"])
        self.known.update("topics/%s/" % t for t in topic_ids)
        self.known.update(pg["rel"] for pg in pages)
        self.known.update(GUIDES_PATH + g["slug"] + "/" for g in self.guides())
        self.home_name = (self.h.top_for(i18n_overlay(self.code), self.code, "title", cfg_site["title"]))

    # ------------------------------------------------------------ helpers
    def guides(self):
        return self.gdoc.get("guides") or []

    def g_text(self, g, key):
        return ((g.get(self.code) or {}).get(key) or (g.get("en") or {}).get(key) or "").strip()

    def lang_urls(self, rel):
        default = [e for e in self.langs if e.get("default")] or self.langs
        urls = [(e["hreflang"], self.base + (e.get("path") or "") + rel) for e in self.langs]
        return urls, self.base + (default[0].get("path") or "") + rel

    def kind_word(self, pg):
        return self.s[pg["kind"]]

    def ext(self, url, text):
        if not url:
            return esc(text)
        return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(text))

    def venue(self, p):
        return esc(p["venue"]) if p["venue"] else "<em>%s</em>" % esc(self.s["preprint"])

    def paper_links(self, p):
        return " \u00b7 ".join(
            '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(p["links"][k]), k)
            for k in self.h.PAPER_LINK_LABELS if p["links"].get(k))

    def note(self, pg):
        return body_note(self.rows[(pg["table"], pg["name"])].get("note") or "")

    def tokens(self):
        """{tokens} for guide prose, filled from the live data."""
        t = {}
        for tid in self.topics:
            ps = [p for p in self.payload["papers"] if tid in p["topics"]]
            k = tid.replace("-", "_")
            t["n_papers_" + k] = len(ps)
            t["n_code_" + k] = sum(1 for p in ps if p["links"].get("code"))
        ds = [pg for pg in self.pages if pg["table"] == "datasets"]
        t["n_dataset_pages"] = len(ds)
        t["n_benchmark_pages"] = len(self.pages) - len(ds)
        t["n_proj_both"] = sum(1 for pg in ds if pg["domain"] == "both")
        t["n_proj_only"] = sum(1 for pg in ds if pg["domain"] == "projection")
        t["n_proj"] = t["n_proj_both"] + t["n_proj_only"]
        t["n_image_only"] = sum(1 for pg in ds if pg["domain"] == "image")
        mod = lambda pg: (self.rows_en[(pg["table"], pg["name"])].get("modality") or "").lower()
        t["n_fan2d"] = sum(1 for pg in ds if "2d fan-beam" in mod(pg))
        t["n_cone"] = sum(1 for pg in ds if "cone-beam" in mod(pg))
        t["n_nc"] = sum(1 for pg in ds if re.search(
            r"\bNC\b", self.rows_en[(pg["table"], pg["name"])].get("license") or ""))
        sep = "\u3001" if self.code == "zh" else ", "
        proj = [pg for pg in ds if pg["domain"] in ("both", "projection")]
        t["proj_names"] = sep.join("[%s](/%s)" % (pg["short"], pg["rel"]) for pg in proj)
        t["proj_low_dose"] = sep.join("[%s](/%s)" % (pg["short"], pg["rel"])
                                      for pg in proj if "low-dose" in pg["topics"])
        return t

    def fill(self, text, where):
        tok = self.tokens()

        def sub(m):
            k = m.group(1)
            if k not in tok:
                self.problems.append("%s: unknown token {%s}" % (where, k))
                return m.group(0)
            return str(tok[k])
        return re.sub(r"\{([a-z0-9_]+)\}", sub, text)

    def rich(self, text, root, where, anchors=None):
        return rich(self.fill(text, where), root, self.known, where, self.problems, anchors)

    # ------------------------------------------------------- resource page
    def resource_title(self, pg):
        r = self.rows_en[(pg["table"], pg["name"])]
        if pg["table"] == "benchmarks":
            return fmt(self.s["titleBenchmark"], short=pg["short"], year=r.get("year") or "")
        modality = (r.get("modality") or "").strip()
        modality_ct = modality if re.search(r"\bCT\b", modality) else (modality + " CT").strip()
        lic = re.split(r"\s+\(", (r.get("license") or "").strip())[0]
        key = "titleDataset" if license_known(lic) else "titleDatasetNoLicense"
        return fmt(self.s[key], short=pg["short"], modality_ct=modality_ct, license=lic)

    def resource_desc(self, pg):
        return short_text(plain(self.note(pg)), 90 if self.code == "zh" else 158)

    def resource_body(self, pg, guides_for):
        s, root = self.s, "{{ROOT}}"
        r = self.rows[(pg["table"], pg["name"])]
        out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
               '<a href="%s">%s</a> / <a href="%s%s">%s</a> / %s</p></nav>'
               % (root, esc(s["home"]), root, DATASETS_PATH, esc(s["indexCrumb"]),
                  esc(self.kind_word(pg))),
               "<h1>%s</h1>" % esc(pg["name"]),
               '<p class="lede">%s</p>' % self.h.md_inline(self.note(pg))]
        facts = [(s["factType"], esc(self.kind_word(pg)))]
        if pg["table"] == "datasets":
            facts.append((s["factData"], esc(s[DOMAIN_KEYS[pg["domain"]]])))
            if r.get("modality"):
                facts.append((s["factModality"], esc(r["modality"])))
        if r.get("tasks"):
            facts.append((s["factTasks"], esc(", ".join(str(x) for x in r["tasks"]))))
        if pg["table"] == "datasets" and license_known(r.get("license")):
            lu = license_url(r["license"])
            facts.append((s["factLicense"], self.ext(lu, r["license"]) if lu else esc(r["license"])))
        if r.get("year"):
            facts.append((s["factYear"], esc(r["year"])))
        facts.append((s["factLink"], self.ext(r["url"], r["url"])))
        if r.get("homepage"):
            facts.append((s["factHomepage"], self.ext(r["homepage"], r["homepage"])))
        dois = self.dois(pg)
        if dois:
            facts.append((s["factDoi"], ", ".join(self.ext("https://doi.org/" + d, d) for d in dois)))
        out.append('<table class="facts"><tbody>%s</tbody></table>'
                   % "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (esc(k), v)
                             for k, v in facts))

        if pg["cite"]:
            out += ['<h2 id="cite">%s</h2>' % esc(s["cite"]), "<p>%s</p>" % esc(s["citeLede"]), "<ul>"]
            for pid in pg["cite"]:
                p = self.papers[pid]
                out.append("<li>%s <span class=\"sep\">(%s, %d)</span></li>"
                           % (self.ext(self.h.paper_url(p), self.h.paper_label(p)), self.venue(p), p["year"]))
            out.append("</ul>")

        if pg["papers"]:
            ps = sorted((self.papers[i] for i in pg["papers"]), key=lambda p: -p["year"])
            out += ['<h2 id="papers">%s</h2>' % esc(s["papers"]), "<p>%s</p>" % esc(s["papersLede"]),
                    '<table class="grid"><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>'
                    % (esc(s["colPaper"]), esc(s["colVenue"]), esc(s["colYear"]), esc(s["colLinks"]))]
            for p in ps:
                out.append('<tr><td>%s</td><td data-label="%s">%s</td><td class="n" data-label="%s">%d</td>'
                           '<td data-label="%s">%s</td></tr>'
                           % (self.ext(self.h.paper_url(p), self.h.paper_label(p)), esc(s["colVenue"]),
                              self.venue(p), esc(s["colYear"]), p["year"], esc(s["colLinks"]),
                              self.paper_links(p)))
            out.append("</tbody></table>")

        if pg["topics"]:
            out += ['<h2 id="topics">%s</h2>' % esc(s["topics"]), "<p>%s</p>" % esc(s["topicsLede"]), "<ul>"]
            for tid in pg["topics"]:
                t = self.topics[tid]
                out.append('<li><a href="%stopics/%s/">%s</a> <span class="sep">(%d)</span></li>'
                           % (root, esc(tid), esc(t["name"]), t["count"]))
            out.append("</ul>")

        if pg["related"]:
            out += ['<h2 id="related">%s</h2>' % esc(s["related"]), "<p>%s</p>" % esc(s["relatedLede"]), "<ul>"]
            for t, n in pg["related"]:
                other = self.page_of.get((t, n))
                rr = self.rows[(t, n)]
                kind = s["kindDataset"] if t == "datasets" else s["kindBenchmark"]
                link = ('<a href="%s%s">%s</a>' % (root, other["rel"], esc(n)) if other
                        else self.ext(rr.get("url"), n))
                out.append('<li>%s <span class="sep">\u00b7 %s</span></li>' % (link, esc(kind)))
            out.append("</ul>")

        gl = guides_for.get(pg["rel"]) or []
        if gl:
            out += ['<h2 id="guides">%s</h2>' % esc(s["guides"]), "<p>%s</p>" % esc(s["entryGuidesLede"]), "<ul>"]
            for g in gl:
                out.append('<li><a href="%s%s%s/">%s</a></li>'
                           % (root, GUIDES_PATH, esc(g["slug"]), esc(self.g_text(g, "title"))))
            out.append("</ul>")

        out.append('<p><a href="%s%s">%s</a></p>' % (root, DATASETS_PATH, esc(s["backIndex"])))
        out.append('<p class="src-note">%s</p>' % esc(fmt(s["source"], updated=self.updated)))
        return "\n".join(out)

    def dois(self, pg):
        r = self.rows_en[(pg["table"], pg["name"])]
        out = []
        d = doi_of(r.get("url"))
        if d:
            out.append(d)
        for d in note_dois(r.get("note")):
            if d not in out:
                out.append(d)
        return out

    def resource_head(self, pg, title, desc):
        url = self.lang_base + pg["rel"]
        r = self.rows[(pg["table"], pg["name"])]
        r_en = self.rows_en[(pg["table"], pg["name"])]
        home = self.lang_base
        ds = {
            "@context": "https://schema.org", "@type": "Dataset", "@id": url + "#dataset",
            "name": pg["name"], "description": plain(self.note(pg)), "url": url,
            "sameAs": [u for u in (r.get("url"), r.get("homepage")) if u],
            "keywords": [str(x) for x in (r.get("tasks") or [])]
                        + ([r_en["modality"]] if r_en.get("modality") else []),
            "includedInDataCatalog": {"@id": home + "#datacatalog"},
        }
        if pg["short"] != pg["name"]:
            ds["alternateName"] = pg["short"]
        if pg["table"] == "datasets" and license_known(r_en.get("license")):
            ds["license"] = license_url(r_en["license"]) or r_en["license"]
            if free_access(r_en["license"]):
                ds["isAccessibleForFree"] = True
        dois = self.dois(pg)
        if dois:
            ds["identifier"] = ["https://doi.org/" + d for d in dois] if len(dois) > 1 else "https://doi.org/" + dois[0]
        if pg["cite"]:
            ds["citation"] = [{"@type": "ScholarlyArticle",
                               "name": re.sub(r"\$([^$]+)\$", r"\1", self.papers[i]["title"]),
                               "url": self.h.paper_url(self.papers[i]),
                               "datePublished": str(self.papers[i]["year"])} for i in pg["cite"]]
        crumbs = crumbs_ld([(self.home_name, home), (self.s["indexCrumb"], home + DATASETS_PATH),
                            (pg["name"], url)])
        urls, xdef = self.lang_urls(pg["rel"])
        return head_bits(urls, self.entry, xdef, url, title, desc, [crumbs, ds],
                         self.base)

    # ---------------------------------------------------------- index page
    def resource_table(self, pgs, root, kind, show_note=False, tid=None):
        s = self.s
        if kind == "datasets":
            head = (s["colName"], s["colData"], s["colModality"], s["colLicense"])
        else:
            head = (s["colName"], s["colYear"], s["colEvaluates"] if show_note else s["colTasks"])
        out = ['<table class="grid"%s><thead><tr>%s</tr></thead><tbody>'
               % (' id="%s"' % tid if tid else "", "".join("<th>%s</th>" % esc(x) for x in head))]
        for pg in pgs:
            r = self.rows[(pg["table"], pg["name"])]
            name = '<a href="%s%s">%s</a>' % (root, pg["rel"], esc(pg["short"]))
            if kind == "datasets":
                cells = [esc(s[DOMAIN_KEYS[pg["domain"]]]), esc(r.get("modality") or ""),
                         esc(r.get("license") or "")]
            else:
                third = (self.h.md_inline(short_text(r.get("note") or "", 200)) if show_note
                         else esc(", ".join(str(x) for x in r.get("tasks") or [])))
                cells = [esc(r.get("year") or ""), third]
            out.append("<tr><td>%s</td>%s</tr>" % (name, "".join(
                '<td data-label="%s"%s>%s</td>' % (esc(h), ' class="note"' if (show_note and i == 1) else "", c)
                for i, (h, c) in enumerate(zip(head[1:], cells)))))
        out.append("</tbody></table>")
        return "\n".join(out)

    def index_counts(self):
        n_ds = sum(1 for pg in self.pages if pg["table"] == "datasets")
        n_bm = len(self.pages) - n_ds
        n_rest = len(self.payload["datasets"]) + len(self.payload["benchmarks"]) - len(self.pages)
        return n_ds, n_bm, n_rest

    def index_body(self):
        s, root = self.s, "{{ROOT}}"
        n_ds, n_bm, n_rest = self.index_counts()
        kw = dict(n_ds=n_ds, n_bm=n_bm, n_rest=n_rest)
        out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
               '<a href="%s">%s</a> / %s</p></nav>' % (root, esc(s["home"]), esc(s["indexCrumb"])),
               "<h1>%s</h1>" % esc(s["indexTitle"]),
               '<p class="lede">%s</p>' % esc(fmt(s["indexLede"], **kw)),
               "<p>%s</p>" % self.rich(fmt(s["indexRest"], **kw), root, "datasets index"),
               "<p>%s</p>" % self.rich(s["indexGuide"], root, "datasets index")]
        ds = [pg for pg in self.pages if pg["table"] == "datasets"]
        bm = [pg for pg in self.pages if pg["table"] == "benchmarks"]
        out += ['<h2 id="datasets">%s <span class="sep">(%d)</span></h2>' % (esc(s["datasets"]), len(ds)),
                self.resource_table(ds, root, "datasets"),
                '<h2 id="benchmarks">%s <span class="sep">(%d)</span></h2>' % (esc(s["benchmarks"]), len(bm)),
                self.resource_table(bm, root, "benchmarks")]
        out.append('<p class="src-note">%s</p>' % esc(fmt(s["source"], updated=self.updated)))
        return "\n".join(out)

    def collection_ld(self, url, title, desc, items):
        return {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url,
                "url": url, "name": title, "description": desc, "inLanguage": self.entry["hreflang"],
                "isPartOf": {"@type": "WebSite", "name": self.cfg["title"], "url": self.lang_base},
                "license": self.cfg["content_license_url"],
                "mainEntity": {"@type": "ItemList", "numberOfItems": len(items),
                               "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                                    "name": n, "url": u}
                                                   for i, (n, u) in enumerate(items)]}}

    def index_head(self, title, desc):
        url = self.lang_base + DATASETS_PATH
        items = [(pg["name"], self.lang_base + pg["rel"]) for pg in self.pages]
        crumbs = crumbs_ld([(self.home_name, self.lang_base), (self.s["indexCrumb"], url)])
        urls, xdef = self.lang_urls(DATASETS_PATH)
        return head_bits(urls, self.entry, xdef, url, title, desc,
                         [crumbs, self.collection_ld(url, title, desc, items)],
                         self.base)

    # -------------------------------------------------------------- guides
    def guide_members(self, g):
        """rel paths of the dataset/benchmark pages a guide's tables list."""
        out = []
        for b in g.get("blocks") or []:
            t = b.get("table") or {}
            if t.get("type") == "resources":
                out += [pg["rel"] for pg in self.table_pages(t)]
        return out

    def table_pages(self, t):
        pgs = [pg for pg in self.pages if pg["table"] == t["kind"]]
        if not t.get("all"):
            pgs = [pg for pg in pgs if t.get("topic") in pg["topics"]]
        if t["kind"] == "datasets":
            pgs = sorted(pgs, key=lambda pg: DOMAIN_ORDER[pg["domain"]])
        return pgs

    def guide_table(self, t, root, where, tid):
        s = self.s
        typ = t.get("type")
        if typ == "families":
            main = t["topic"]
            head = (s["colFamily"], s["colWhat"], s["colPapers"], s["colWithCode"], s["colRecent"])
            rows = []
            for f in t["families"]:
                if f not in self.topics:
                    self.problems.append("%s: unknown family topic %s" % (where, f))
                    continue
                ps = [p for p in self.payload["papers"] if main in p["topics"] and f in p["topics"]]
                withc = [p for p in ps if p["links"].get("code")]
                recent = withc[0] if withc else None
                rec = ("%s <span class=\"sep\">(%s, %d)</span>"
                       % (self.ext(self.h.paper_url(recent), self.h.paper_label(recent)),
                          self.venue(recent), recent["year"]) if recent else "\u2014")
                rows.append(['<a href="%stopics/%s/">%s</a>' % (root, esc(f), esc(self.topics[f]["name"])),
                             esc(self.topics[f]["desc"]), str(len(ps)), str(len(withc)), rec])
        elif typ == "resources":
            pgs = self.table_pages(t)
            if not pgs:
                self.problems.append("%s: resources table %s is empty" % (where, t))
            return self.resource_table(pgs, root, t["kind"], show_note=(t["kind"] == "benchmarks"), tid=tid)
        elif typ == "toolkits":
            tk = dict((r["name"], r) for r in self.payload["toolkits"])
            head = (s["colName"], s["colLanguage"], s["colLicense"], s["colProvides"])
            rows = []
            for n in t["names"]:
                if n not in tk:
                    self.problems.append("%s: unknown toolkit %s" % (where, n))
                    continue
                r = tk[n]
                url = r.get("url") or ("https://github.com/" + r["repo"] if r.get("repo") else None)
                rows.append([self.ext(url, n), esc(r.get("language") or ""), esc(r.get("license") or ""),
                             self.h.md_inline(short_text(r.get("note") or "", 200))])
        elif typ == "start":
            tp = (self.topic_doc.get("topics") or {}).get(t["topic"]) or {}
            head = (s["colPaper"], s["colVenue"], s["colYear"], s["colWhy"])
            rows = []
            for item in tp.get("start") or []:
                p = self.papers[item["id"]]
                why = (item.get(self.code) or item.get("en") or "").strip()
                code = (' \u00b7 <a href="%s" target="_blank" rel="noopener">code</a>' % esc(p["links"]["code"])
                        if p["links"].get("code") else "")
                rows.append([self.ext(self.h.paper_url(p), self.h.paper_label(p)) + code,
                             self.venue(p), str(p["year"]), esc(why)])
        else:
            self.problems.append("%s: unknown table type %s" % (where, typ))
            return ""
        out = ['<table class="grid" id="%s"><thead><tr>%s</tr></thead><tbody>'
               % (tid, "".join("<th>%s</th>" % esc(x) for x in head))]
        for row in rows:
            cells = ["<td>%s</td>" % row[0]] + [
                '<td data-label="%s"%s>%s</td>' % (esc(h), ' class="n"' if c.isdigit() else "", c)
                for h, c in zip(head[1:], row[1:])]
            out.append("<tr>%s</tr>" % "".join(cells))
        out.append("</tbody></table>")
        return "\n".join(out)

    def guide_body(self, g):
        s, root = self.s, "{{ROOT}}"
        where = "data/guides.yaml: %s (%s)" % (g["slug"], self.code)
        upd = str(g.get("updated") or self.gdoc.get("updated"))
        # Table ids first, so in-page links in the FAQ can be checked.
        tids, seen = [], {}
        for b in g.get("blocks") or []:
            t = b.get("table")
            if not t:
                tids.append(None)
                continue
            base_id = "guide-table-" + (t.get("kind") or t.get("type"))
            seen[base_id] = seen.get(base_id, 0) + 1
            tids.append(base_id if seen[base_id] == 1 else "%s-%d" % (base_id, seen[base_id]))
        anchors = set(x for x in tids if x)
        out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
               '<a href="%s">%s</a> / <a href="%s%s">%s</a></p></nav>'
               % (root, esc(s["home"]), root, GUIDES_PATH, esc(s["guidesCrumb"])),
               "<h1>%s</h1>" % esc(self.g_text(g, "title")),
               '<p class="updated">%s</p>' % esc(s["updated"]).replace(
                   "{date}", '<time datetime="%s">%s</time>' % (upd, upd))]
        for i, para in enumerate(paras(self.g_text(g, "answer"))):
            out.append('<p%s>%s</p>' % (' class="lede"' if i == 0 else "",
                                        self.rich(para, root, where, anchors)))
        for b, tid in zip(g.get("blocks") or [], tids):
            h2 = (b.get("h2") or {})
            if h2:
                h2t = h2.get(self.code) or h2.get("en")
                out.append('<h2 id="%s">%s</h2>' % (slugify(h2.get("en")), esc(h2t)))
            txt = b.get("text") or {}
            for para in paras(txt.get(self.code) or txt.get("en") or ""):
                out.append("<p>%s</p>" % self.rich(para, root, where, anchors))
            if b.get("table"):
                out.append(self.guide_table(b["table"], root, where, tid))
        # Related pages: the guide's topics, the family topics, the index and
        # the other guides.
        rel_topics = list(g.get("topics") or [])
        for b in g.get("blocks") or []:
            t = b.get("table") or {}
            for f in ([t.get("topic")] if t.get("topic") else []) + list(t.get("families") or []):
                if f and f not in rel_topics:
                    rel_topics.append(f)
        out += ['<h2 id="related">%s</h2>' % esc(s["relatedPages"]), "<ul>"]
        for tid in rel_topics:
            if tid in self.topic_ids:
                out.append('<li><a href="%stopics/%s/">%s</a></li>' % (root, esc(tid), esc(self.topics[tid]["name"])))
        out.append('<li><a href="%s%s">%s</a></li>' % (root, DATASETS_PATH, esc(s["indexTitle"])))
        for other in self.guides():
            if other["slug"] != g["slug"]:
                out.append('<li><a href="%s%s%s/">%s</a></li>'
                           % (root, GUIDES_PATH, esc(other["slug"]), esc(self.g_text(other, "title"))))
        out.append("</ul>")
        faq = g.get("faq") or []
        if faq:
            out += ['<h2 id="faq">%s</h2>' % esc(s["faq"]), '<section class="faq">']
            for qa in faq:
                x = qa.get(self.code) or qa.get("en")
                out.append("<h3>%s</h3>" % esc(x["q"]))
                out.append("<p>%s</p>" % self.rich(x["a"], root, where, anchors))
            out.append("</section>")
        return "\n".join(out)

    def guide_head(self, g, title, desc):
        rel = GUIDES_PATH + g["slug"] + "/"
        url = self.lang_base + rel
        org = {"@type": "Organization", "name": self.cfg["title"], "url": self.base}
        art = {"@context": "https://schema.org", "@type": "Article", "@id": url + "#article",
               "headline": self.g_text(g, "title"), "description": desc, "url": url,
               "mainEntityOfPage": url, "inLanguage": self.entry["hreflang"],
               "datePublished": str(g.get("published") or self.gdoc.get("published")),
               "dateModified": str(g.get("updated") or self.gdoc.get("updated")),
               "author": org, "publisher": org, "license": self.cfg["content_license_url"]}
        crumbs = crumbs_ld([(self.home_name, self.lang_base), (self.s["guidesCrumb"], self.lang_base + GUIDES_PATH),
                            (self.g_text(g, "title"), url)])
        urls, xdef = self.lang_urls(rel)
        return head_bits(urls, self.entry, xdef, url, title, desc, [crumbs, art],
                         self.base)

    def guides_index_body(self):
        s, root = self.s, "{{ROOT}}"
        out = ['<nav class="crumbs" aria-label="breadcrumb"><p class="kicker">'
               '<a href="%s">%s</a> / %s</p></nav>' % (root, esc(s["home"]), esc(s["guidesCrumb"])),
               "<h1>%s</h1>" % esc(s["guidesTitle"]),
               '<p class="lede">%s</p>' % esc(s["guidesLede"]), "<ul>"]
        for g in self.guides():
            out.append('<li><a href="%s%s%s/"><strong>%s</strong></a><br>%s</li>'
                       % (root, GUIDES_PATH, esc(g["slug"]), esc(self.g_text(g, "title")),
                          esc(self.g_text(g, "description"))))
        out.append("</ul>")
        out.append('<p><a href="%s%s">%s</a></p>' % (root, DATASETS_PATH, esc(s["indexTitle"])))
        return "\n".join(out)

    def guides_index_head(self, title, desc):
        url = self.lang_base + GUIDES_PATH
        items = [(self.g_text(g, "title"), url + g["slug"] + "/") for g in self.guides()]
        crumbs = crumbs_ld([(self.home_name, self.lang_base), (self.s["guidesCrumb"], url)])
        urls, xdef = self.lang_urls(GUIDES_PATH)
        return head_bits(urls, self.entry, xdef, url, title, desc,
                         [crumbs, self.collection_ld(url, title, desc, items)],
                         self.base)


def i18n_overlay(code):
    import i18n
    return i18n.load(code)
