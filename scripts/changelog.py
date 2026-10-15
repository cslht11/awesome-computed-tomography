#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read CHANGELOG.md into dated entries and render them as HTML for the site's
/changelog/ page.

CHANGELOG.md is the only source: the page is generated from it on every
build, so the two cannot disagree. Every top-level entry heading must read

    ## YYYY-MM-DD — Title

and the page lists entries by that date, newest first. Entries that share a
date keep the order they have in the file. The file itself is not reordered.

Only the Markdown subset CHANGELOG.md actually uses is supported: ``###``
headings, paragraphs, ``-`` lists (nested by two-space indentation, with
indented continuation lines and paragraphs), ``code``, **bold**, *italics*,
[links](url) and <https://autolinks>. No dependencies beyond the standard
library.

Translations
------------
A translated edition of the page reads ``CHANGELOG.<suffix>.md`` (the suffix
of that language's README, e.g. ``CHANGELOG.zh-CN.md``). It has the same
``## YYYY-MM-DD — Title`` headings, in the target language, and the first
line under each heading names the English entry it translates:

    ## 2026-10-12 — 搜索、排序与语言切换的修复
    <!-- en: Search, sorting and language-switch fixes -->

An entry is matched by its date plus that English title, so reordering
either file, or adding several entries on one day, never mismatches them.
An English entry with no translation is shown in English (and marked
``lang="en"``); a translation whose English entry no longer exists - because
the English title was edited, say - fails the build, so a stale translation
cannot linger unnoticed.

    python scripts/changelog.py          # print the parsed entry list
    python scripts/changelog.py --status CHANGELOG.zh-CN.md
                                         # which entries still lack a translation
"""

import datetime
import html
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")

EN_REF_RE = re.compile(r"^<!--\s*en:\s*(.+?)\s*-->\s*$")
HEAD_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s+[\u2014\u2013-]+\s+(.+?)\s*$")


class ChangelogError(ValueError):
    pass


def esc(s):
    return html.escape(str(s), quote=True)


def _safe_url(url):
    url = url.strip()
    if re.match(r"^(https?:|mailto:|#|/|\./|\.\./)", url) or not re.match(r"^[a-z]+:", url, re.I):
        return url
    return "#"


def inline(text, repo_url=None):
    """Inline Markdown -> HTML. Code spans are cut out first so nothing inside
    them is interpreted; everything else is escaped before markup is added."""
    stash = []

    def keep(fragment):
        stash.append(fragment)
        return "\x00%d\x00" % (len(stash) - 1)

    def code(m):
        return keep("<code>%s</code>" % esc(m.group(1)))

    def autolink(m):
        u = m.group(1)
        return keep('<a href="%s">%s</a>' % (esc(_safe_url(u)), esc(u)))

    def link(m):
        label, url = m.group(1), m.group(2)
        url = _safe_url(url)
        # Relative repository paths (e.g. LICENSE-content) mean nothing on the
        # website; point them at the file on GitHub instead.
        if repo_url and not re.match(r"^([a-z]+:|#|/)", url, re.I):
            url = "%s/blob/main/%s" % (repo_url.rstrip("/"), url)
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return keep('<a href="%s"%s>%s</a>' % (esc(url), ext, _inline_rest(esc(label))))

    t = re.sub(r"`([^`]+)`", code, text)
    t = re.sub(r"<(https?://[^>\s]+)>", autolink, t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
    t = _inline_rest(esc(t))
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], t)


_WORD = r"(?![\u3400-\u4dbf\u4e00-\u9fff])\w"


def _inline_rest(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    # *italics* may not touch a letter or digit (so a*b stays literal), but
    # may touch a Chinese character, which has no spaces to set it apart.
    t = re.sub(r"(?<!\*)(?<!%s)\*(?!\s)(.+?)(?<!\s)\*(?!\*)(?!%s)" % (_WORD, _WORD),
               r"<em>\1</em>", t)
    return t


# A line break inside a paragraph is normally a space. Chinese text is not
# space-separated, so a break between two ideographs, or next to full-width
# punctuation, takes none; a break between Chinese and Latin text keeps its
# space, which is how the Chinese prose in this repository spaces mixed text.
_IDEO = "\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
_PUNCT = "\u3000-\u303f\uff00-\uffef"


def join_lines(lines):
    """Join the wrapped lines of one paragraph (see the note above)."""
    out = ""
    for ln in lines:
        if out:
            a, b = out[-1], ln[:1]
            ideo = re.match("[%s]" % _IDEO, a) and re.match("[%s]" % _IDEO, b)
            punct = re.match("[%s]" % _PUNCT, a) or re.match("[%s]" % _PUNCT, b)
            if not (ideo or punct):
                out += " "
        out += ln
    return out


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def render_blocks(lines, repo_url=None, h_level=3):
    """Render a run of Markdown lines (already dedented) to HTML blocks."""
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{3,6})\s+(.*)$", line)
        if m:
            level = min(6, h_level + len(m.group(1)) - 3)
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2), repo_url), level))
            i += 1
            continue
        if re.match(r"^[-*] ", line):
            items = []
            while i < n and re.match(r"^[-*] ", lines[i]):
                item = [lines[i][2:]]
                i += 1
                while i < n:
                    nxt = lines[i]
                    if not nxt.strip():
                        # A blank line ends the item unless indented text follows.
                        j = i
                        while j < n and not lines[j].strip():
                            j += 1
                        if j < n and _indent(lines[j]) >= 2:
                            item.extend([""] * (j - i))
                            i = j
                            continue
                        break
                    if _indent(nxt) >= 2:
                        item.append(nxt[2:])
                        i += 1
                        continue
                    break
                items.append(item)
                # Skip blank lines between items of the same list.
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and re.match(r"^[-*] ", lines[j]):
                    i = j
            lis = []
            for item in items:
                body = render_blocks(item, repo_url, h_level)
                # A single plain paragraph renders inline, without <p>.
                m1 = re.match(r"^<p>(.*)</p>$", body, re.S)
                if m1 and "<p>" not in m1.group(1):
                    body = m1.group(1)
                lis.append("<li>%s</li>" % body)
            out.append("<ul>\n%s\n</ul>" % "\n".join(lis))
            continue
        para = []
        while i < n and lines[i].strip() and not re.match(r"^(#{3,6}\s|[-*] )", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(join_lines(para), repo_url))
    return "\n".join(out)


def slug(date, used):
    s = date
    k = 2
    while s in used:
        s = "%s-%d" % (date, k)
        k += 1
    used.add(s)
    return s


def parse(path=CHANGELOG, today=None, sort=True):
    """Return (preamble_lines, entries). Each entry is a dict with date
    (datetime.date), title, body (list of lines) and id. Entries come back
    newest first; equal dates keep file order. Raises ChangelogError on a
    top-level heading that is not dated, a date that does not exist, or a
    date in the future."""
    name = os.path.basename(path)
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    preamble, entries, cur = [], [], None
    for no, line in enumerate(lines, 1):
        if line.startswith("# ") and cur is None and not entries:
            continue                      # the "# Changelog" title
        if line.startswith("## "):
            m = HEAD_RE.match(line)
            if not m:
                raise ChangelogError("%s:%d: entry heading must read "
                                     "'## YYYY-MM-DD — Title': %r" % (name, no, line))
            try:
                d = datetime.date.fromisoformat(m.group(1))
            except ValueError:
                raise ChangelogError("%s:%d: %s is not a real date"
                                     % (name, no, m.group(1)))
            cur = {"date": d, "title": m.group(2), "body": [], "line": no}
            entries.append(cur)
            continue
        (cur["body"] if cur else preamble).append(line)
    if not entries:
        raise ChangelogError("%s has no dated entries" % name)
    # One day of slack: an entry written in UTC+8 can be dated "tomorrow" for a
    # build running in UTC. Anything further ahead is a typo, not a timezone.
    today = today or datetime.date.today()
    for e in entries:
        if e["date"] > today + datetime.timedelta(days=1):
            raise ChangelogError("%s:%d: entry dated %s is in the future"
                                 % (name, e["line"], e["date"]))
    if not sort:
        return preamble, entries
    order = sorted(range(len(entries)), key=lambda k: (-entries[k]["date"].toordinal(), k))
    entries = [entries[k] for k in order]
    used = set()
    for e in entries:
        e["id"] = slug(e["date"].isoformat(), used)
    return preamble, entries


def load_translations(path, today=None):
    """Read a translated changelog into {(date, english title): entry}.
    Returns {} when the file does not exist: a language without one simply
    shows every entry in English."""
    if not path or not os.path.exists(path):
        return {}
    name = os.path.basename(path)
    _, entries = parse(path, today=today, sort=False)
    out = {}
    for e in entries:
        body = list(e["body"])
        while body and not body[0].strip():
            body.pop(0)
        m = EN_REF_RE.match(body[0]) if body else None
        if not m:
            raise ChangelogError("%s:%d: the first line under the heading must be "
                                 "'<!-- en: English title -->' naming the entry "
                                 "it translates" % (name, e["line"]))
        key = (e["date"], m.group(1))
        if key in out:
            raise ChangelogError("%s:%d: %s — %s is translated twice"
                                 % (name, e["line"], key[0], key[1]))
        out[key] = {"title": e["title"], "body": body[1:], "line": e["line"]}
    return out


def translate(entries, translations, lang, path=None):
    """Swap in the translation of each entry that has one. Returns
    (entries, missing): the new list (same order and ids; untranslated
    entries are kept in English and marked lang="en") and the English
    entries that had no translation. Raises ChangelogError when a
    translation matches no English entry."""
    name = os.path.basename(path) if path else "translation"
    seen, out, missing = set(), [], []
    for e in entries:
        key = (e["date"], e["title"])
        t = translations.get(key)
        if t is None:
            out.append(dict(e, lang="en"))
            missing.append(e)
            continue
        seen.add(key)
        out.append(dict(e, title=t["title"], body=t["body"], lang=lang))
    for key, t in translations.items():
        if key not in seen:
            raise ChangelogError("%s:%d: translates '%s — %s', which is not an "
                                 "entry in CHANGELOG.md (was its English title or date "
                                 "changed?)" % (name, t["line"], key[0], key[1]))
    return out, missing


def render_entries(entries, repo_url=None, page_lang=None):
    """page_lang: the page's own language. An entry whose `lang` differs
    from it (an untranslated fallback) carries its own lang attribute."""
    out = []
    for e in entries:
        d = e["date"].isoformat()
        lang = e.get("lang")
        lang_attr = (' lang="%s"' % esc(lang)) if lang and lang != page_lang else ""
        out.append('<article class="cl-entry" id="%s"%s>\n'
                   '<h2><a href="#%s"><time datetime="%s">%s</time></a> \u2014 %s</h2>\n'
                   '%s\n</article>'
                   % (esc(e["id"]), lang_attr, esc(e["id"]), d, d, inline(e["title"], repo_url),
                      render_blocks(e["body"], repo_url, h_level=3)))
    return "\n".join(out)


def render_preamble(preamble, repo_url=None):
    return render_blocks(preamble, repo_url, h_level=3)


if __name__ == "__main__":
    try:
        pre, ents = parse()
        if len(sys.argv) == 3 and sys.argv[1] == "--status":
            tpath = os.path.join(ROOT, sys.argv[2]) if not os.path.isabs(sys.argv[2]) else sys.argv[2]
            _, missing = translate(ents, load_translations(tpath), "xx", tpath)
            for e in missing:
                print("untranslated: %s — %s" % (e["date"], e["title"]))
            print("%d of %d entries translated" % (len(ents) - len(missing), len(ents)))
            sys.exit(0)
    except ChangelogError as e:
        sys.exit(str(e))
    for e in ents:
        print("%s  %-14s %s" % (e["date"], e["id"], e["title"]))
    print("%d entries" % len(ents))
