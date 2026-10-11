#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language overlays for the generated README and the generated site.

English is the source of truth and lives in ``data/i18n/en.yaml`` (interface
strings and README prose) and ``data/*.yaml`` (content). Every other language
is an *overlay* in ``data/i18n/<code>.yaml`` that replaces individual strings.
A key the overlay does not carry falls back to English, so a half-finished
translation still produces a whole, working page instead of a broken one.

Overlay shape — every section is optional::

    lang: zh-Hans                # BCP 47; used for <html lang> and hreflang
    title: ...                   # optional override of the site/README title
    tagline: ...
    description: ...
    ui:                          # interface strings, see data/i18n/en.yaml
      searchPlaceholder: ...
    readme:                      # prose that scripts/build.py writes
      blurb: ...
    pages:                       # bodies of the static site pages, as HTML
      about: ...
    topics:                      # keyed by topic id from data/meta.yaml
      sparse-view:
        name: ...
        desc: ...
    toolkits:                    # keyed by the row's `name`
      TIGRE:
        note: ...
    datasets: {}
    benchmarks: {}
    learning: {}

Two failure modes are treated very differently on purpose:

* **A missing translation is not an error.** It falls back to English — the
  page stays whole, and ``build.py`` prints how many strings each language
  still lacks so the gap is visible rather than silent.
* **An orphan is an error.** An orphan is a key in an overlay that names
  something the English source does not have — a topic id that was renamed, a
  dataset that was dropped. Those are always bugs: the translation is dead
  weight that silently stops applying, and only the checker will ever notice.
  See :func:`check`.
"""

import io
import os

try:
    import yaml
except ImportError:  # pragma: no cover - reported by the callers
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, "data", "i18n")

#: The language everything else is written in and falls back to.
SOURCE = "en"

_SECTIONS = ("topics", "toolkits", "datasets", "benchmarks", "learning")

#: ``ui.*`` keys handed to ``web/app.js`` through ``payload.ui``. These must
#: stay unfilled: ``noMatch`` / ``showAll`` carry ``{q}`` / ``{n}`` that the
#: script substitutes itself. Kept here rather than in build_site.py so the
#: site build and the standalone data export publish an identical key set.
JS_UI = {
    "kindPaper", "kindToolkit", "kindDataset", "kindBenchmark", "kindLearning",
    "noMatch", "showAll", "copyLink", "copied", "copyLinkTitle",
    "homepageTitle", "venuePreprint", "yearAndLater", "labelShare", "reset",
    "tableToolkit", "tableLanguage", "tableLicense", "tableStars", "tableNotes",
    "tableDataset", "tableModality", "tableTasks", "tableBenchmark",
    "tableYear", "tableResource", "tableType",
}


def path_of(code):
    return os.path.join(I18N_DIR, "%s.yaml" % code)


def _read(code):
    p = path_of(code)
    if not os.path.exists(p):
        return {}
    with io.open(p, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    if d is None:
        return {}
    if not isinstance(d, dict):
        raise ValueError("data/i18n/%s.yaml: expected a mapping at the top level" % code)
    return d


class Overlay(object):
    """One language's strings, layered over English.

    Lookups walk the overlay first and English second, so ``zh`` only has to
    carry what has actually been translated.
    """

    def __init__(self, code, data=None):
        self.code = code
        self.data = _read(code) if data is None else data
        self._source = None if code == SOURCE else Overlay(SOURCE)

    # ------------------------------------------------------------------ core
    def _stack(self):
        return [self.data] + ([self._source.data] if self._source else [])

    def _text(self, section, key, default=""):
        for d in self._stack():
            v = (d.get(section) or {}).get(key)
            if isinstance(v, str) and v.strip():
                return v
        return default

    def _mapping(self, section, key):
        """Merge ``section.key`` across the stack; the overlay wins outright.

        Returning a merged dict rather than the overlay's alone means a
        translation may override only ``note`` and keep the English ``name``.
        """
        out = {}
        for d in self._stack():
            for k, v in ((d.get(section) or {}).get(key) or {}).items():
                if k not in out and isinstance(v, str) and v.strip():
                    out[k] = v
        return out

    # --------------------------------------------------------------- lookups
    def text(self, section, key, default=""):
        return self._text(section, key, default)

    def ui(self, key, default=""):
        return self._text("ui", key, default)

    def readme(self, key, default=""):
        return self._text("readme", key, default)

    def page(self, name, default=""):
        """Body HTML of one static page (about / contact / privacy)."""
        return self._text("pages", name, default)

    def top(self, key, default=""):
        """A key at the top level of the file: title, tagline, description."""
        for d in self._stack():
            v = d.get(key)
            if isinstance(v, str) and v.strip():
                return v
        return default

    def topic(self, tid):
        """``{name:, desc:}`` for a topic id, filled in from English."""
        return self._mapping("topics", tid)

    def item(self, table, name):
        """Per-row overrides for toolkits/datasets/benchmarks/learning."""
        return self._mapping(table, name)

    # ------------------------------------------------------------ reporting
    def untranslated(self, expected):
        """Keys this language does not carry yet. ``expected`` maps
        ``(section, key) -> <count>``; the return value is the list of pairs
        the overlay is missing, for the build to report.

        Deliberately reads ``self.data`` rather than going through ``_text``:
        ``_text`` falls back to English, so it would report every key as
        translated and hide exactly the gap this is meant to surface.
        """
        missing = []
        for (section, key), n in sorted(expected.items()):
            v = (self.data.get(section) or {}).get(key)
            if not (isinstance(v, str) and v.strip()):
                missing.append((section, key, n))
        return missing


def load(code):
    return Overlay(code)


def js_ui(overlay):
    """``payload.ui``: the strings ``web/app.js`` renders at run time."""
    return dict((k, overlay.ui(k)) for k in sorted(JS_UI))


def available():
    """Language codes that have an overlay file, English first."""
    if not os.path.isdir(I18N_DIR):
        return [SOURCE]
    codes = [os.path.splitext(f)[0] for f in sorted(os.listdir(I18N_DIR))
             if f.endswith(".yaml")]
    if SOURCE in codes:
        codes.remove(SOURCE)
        codes.insert(0, SOURCE)
    return codes


# ------------------------------------------------------------------ registry
def languages(meta):
    """The language registry declared in ``data/meta.yaml``.

    Falls back to English-only when no ``languages:`` block is present, so the
    builders keep working on a checkout that predates the bilingual work.
    """
    langs = (meta or {}).get("languages")
    if not langs:
        langs = [{"code": SOURCE, "default": True}]
    out = []
    for e in langs:
        if not isinstance(e, dict) or not e.get("code"):
            continue
        e = dict(e)
        code = e["code"]
        e.setdefault("label", code.upper())
        e.setdefault("html", code)
        e.setdefault("hreflang", code)
        e.setdefault("og_locale", code)
        # `path` is the URL prefix under the site root: "" for the default
        # language, "<code>/" for the others.
        e.setdefault("path", "" if code == SOURCE else "%s/" % code)
        e.setdefault("readme", "README.md" if code == SOURCE else "README.%s.md" % code)
        out.append(e)
    if out and not any(e.get("default") for e in out):
        out[0]["default"] = True
    return out


def default_language(langs):
    for e in langs:
        if e.get("default"):
            return e
    return langs[0]


def url_for(base, entry):
    """``https://x.org/`` + ``zh/`` -> ``https://x.org/zh/``."""
    return base + (entry.get("path") or "")


# ------------------------------------------------------------------ checking
def check(overlay, topic_ids, names):
    """Orphan keys: things an overlay translates that no longer exist.

    ``names`` maps table -> set of row names. Returns a list of problem
    strings; empty means the overlay is consistent with English. English
    itself is the reference, so it is never checked.
    """
    problems = []
    if overlay.code == SOURCE:
        return problems
    where = "data/i18n/%s.yaml" % overlay.code

    valid = {"topics": set(topic_ids)}
    for t in _SECTIONS:
        if t != "topics":
            valid[t] = set(names.get(t, ()))

    for section in _SECTIONS:
        for k in (overlay.data.get(section) or {}):
            if k not in valid[section]:
                problems.append("%s: %s '%s' does not exist in the English source"
                                % (where, section, k))

    ref = overlay._source.data
    for section in ("ui", "readme", "pages"):
        known = set(ref.get(section) or {})
        for k in (overlay.data.get(section) or {}):
            if k not in known:
                problems.append("%s: %s '%s' is not a known key" % (where, section, k))
    return problems
