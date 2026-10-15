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

    python scripts/changelog.py          # print the parsed entry list
"""

import datetime
import html
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")

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


def _inline_rest(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
    return t


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
        out.append("<p>%s</p>" % inline(" ".join(para), repo_url))
    return "\n".join(out)


def slug(date, used):
    s = date
    k = 2
    while s in used:
        s = "%s-%d" % (date, k)
        k += 1
    used.add(s)
    return s


def parse(path=CHANGELOG, today=None):
    """Return (preamble_lines, entries). Each entry is a dict with date
    (datetime.date), title, body (list of lines) and id. Entries come back
    newest first; equal dates keep file order. Raises ChangelogError on a
    top-level heading that is not dated, a date that does not exist, or a
    date in the future."""
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
                raise ChangelogError("CHANGELOG.md:%d: entry heading must read "
                                     "'## YYYY-MM-DD — Title': %r" % (no, line))
            try:
                d = datetime.date.fromisoformat(m.group(1))
            except ValueError:
                raise ChangelogError("CHANGELOG.md:%d: %s is not a real date"
                                     % (no, m.group(1)))
            cur = {"date": d, "title": m.group(2), "body": [], "line": no}
            entries.append(cur)
            continue
        (cur["body"] if cur else preamble).append(line)
    if not entries:
        raise ChangelogError("CHANGELOG.md has no dated entries")
    # One day of slack: an entry written in UTC+8 can be dated "tomorrow" for a
    # build running in UTC. Anything further ahead is a typo, not a timezone.
    today = today or datetime.date.today()
    for e in entries:
        if e["date"] > today + datetime.timedelta(days=1):
            raise ChangelogError("CHANGELOG.md:%d: entry dated %s is in the future"
                                 % (e["line"], e["date"]))
    order = sorted(range(len(entries)), key=lambda k: (-entries[k]["date"].toordinal(), k))
    entries = [entries[k] for k in order]
    used = set()
    for e in entries:
        e["id"] = slug(e["date"].isoformat(), used)
    return preamble, entries


def render_entries(entries, repo_url=None):
    out = []
    for e in entries:
        d = e["date"].isoformat()
        out.append('<article class="cl-entry" id="%s">\n'
                   '<h2><a href="#%s"><time datetime="%s">%s</time></a> \u2014 %s</h2>\n'
                   '%s\n</article>'
                   % (esc(e["id"]), esc(e["id"]), d, d, inline(e["title"], repo_url),
                      render_blocks(e["body"], repo_url, h_level=3)))
    return "\n".join(out)


def render_preamble(preamble, repo_url=None):
    return render_blocks(preamble, repo_url, h_level=3)


if __name__ == "__main__":
    try:
        pre, ents = parse()
    except ChangelogError as e:
        sys.exit(str(e))
    for e in ents:
        print("%s  %-14s %s" % (e["date"], e["id"], e["title"]))
    print("%d entries" % len(ents))
