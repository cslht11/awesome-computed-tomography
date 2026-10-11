# -*- coding: utf-8 -*-
"""One-off: fix two real defects that `awesome-lint` surfaced.

1. Eight of the twenty-four table-of-contents links were dead.

   `slug()` collapsed runs of whitespace into a single hyphen, but GitHub turns
   *each* space into its own hyphen. The anchor for `Surveys & Reviews` is
   `surveys--reviews`; we were emitting `surveys-reviews`, which matches
   nothing. Every heading containing "&" was affected.

2. The Awesome badge pointed at `cdn.rawgit.com`, the RawGit CDN that shut down
   in 2018. It still answers today, but the canonical source is
   `https://awesome.re/badge.svg` linking to `https://awesome.re`.

Both are fixed in `scripts/build.py` so they survive regeneration.

Idempotent (probe-based).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "scripts", "build.py")


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, s):
    assert "\r" not in s, "stray CR before write: " + p
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)
        f.flush()
        os.fsync(f.fileno())


ok = True


def splice(old, new, label, probe=None):
    global ok
    s = read(BUILD)
    if probe and probe in s:
        print("SKIP  %-40s (already applied)" % label)
        return
    n = s.count(old)
    if n != 1:
        print("FAIL  %-40s (count=%d)" % (label, n))
        ok = False
        return
    out = s.replace(old, new)
    if probe:
        assert probe in out, "probe missing after splice: " + label
    write(BUILD, out)
    print("OK    %-40s" % label)


OLD_SLUG = (
    'def slug(text):\n'
    '    s = re.sub(r"[^\\w\\s-]", "", text.lower())\n'
    '    return re.sub(r"[\\s_]+", "-", s).strip("-")\n'
)

NEW_SLUG = (
    'def slug(text):\n'
    '    """GitHub-compatible heading anchor.\n'
    '\n'
    '    GitHub lowercases, drops punctuation, then turns *each* space into its\n'
    '    own hyphen. Runs of spaces therefore yield consecutive hyphens: the\n'
    '    anchor for "Surveys & Reviews" is `surveys--reviews`, not\n'
    '    `surveys-reviews`. Collapsing the run breaks the link.\n'
    '    """\n'
    '    s = re.sub(r"[^\\w\\- ]", "", text.lower(), flags=re.UNICODE)\n'
    '    return s.replace(" ", "-")\n'
)

splice(OLD_SLUG, NEW_SLUG, "build.py slug()", probe="GitHub-compatible heading anchor")


def read_badge():
    s = read(BUILD)
    i = s.find('BADGE = (')
    if i < 0:
        return None
    j = s.find(')\n', i)
    return s[i:j + 2]


OLD_BADGE = read_badge()
if OLD_BADGE is None:
    print("FAIL  %-40s (BADGE not found)" % "build.py BADGE")
    ok = False
else:
    NEW_BADGE = (
        'BADGE = "https://awesome.re/badge.svg"\n'
    )
    splice(OLD_BADGE, NEW_BADGE, "build.py BADGE -> awesome.re")

# The badge link target: the badge should point at awesome.re.
OLD_LINK = 'parts.append("# Awesome Computed Tomography [![Awesome](%s)](https://github.com/sindresorhus/awesome)\\n" % BADGE)'
NEW_LINK = 'parts.append("# Awesome Computed Tomography [![Awesome](%s)](https://awesome.re)\\n" % BADGE)'
splice(OLD_LINK, NEW_LINK, "build.py badge link -> awesome.re",
       probe="](https://awesome.re)\\n\" % BADGE")

if not ok:
    sys.exit(1)
print("\napplied")
