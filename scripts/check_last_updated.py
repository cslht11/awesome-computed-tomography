# -*- coding: utf-8 -*-
"""Fail when data/ changed after the date in data/meta.yaml `last_updated`.

`last_updated` is the one hand-set date the whole site reads: the homepage
"Updated" stat, both READMEs, the meta description, llms.txt, the JSON-LD
dateModified and every sitemap <lastmod>. Nothing else moves it, so a data
commit that forgets to bump it leaves the whole site claiming an older date.

The check compares it with the date of the newest commit that touched data/.
That date is taken both in the committer's own timezone and in Asia/Shanghai
(UTC+8, the timezone the build stamps dates in), and either one passes — a
commit made late in the evening in one zone is already "tomorrow" in the other,
and that must not fail the push.

Usage:  python scripts/check_last_updated.py
Exits 0 when the date is current, or when there is no git history to read
(a tarball checkout); exits 1 when `last_updated` is older than the newest data
commit. Standard library only.
"""
import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHANGHAI = datetime.timezone(datetime.timedelta(hours=8))


def last_updated():
    with open(os.path.join(ROOT, "data", "meta.yaml"), encoding="utf-8") as fh:
        m = re.search(r"^last_updated:\s*[\"']?(\d{4}-\d{2}-\d{2})", fh.read(), re.M)
    if not m:
        sys.exit("data/meta.yaml: no `last_updated: YYYY-MM-DD` line")
    return datetime.date.fromisoformat(m.group(1))


def newest_data_commit():
    """(sha, committer datetime with its own offset) or None without git."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%h %cI", "--", "data/"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    if not out:
        return None
    sha, stamp = out.split(" ", 1)
    return sha, datetime.datetime.fromisoformat(stamp)


def main():
    stated = last_updated()
    newest = newest_data_commit()
    if newest is None:
        print("last_updated %s (no git history to compare against)" % stated)
        return 0
    sha, when = newest
    local_day = when.date()
    shanghai_day = when.astimezone(SHANGHAI).date()
    if stated >= min(local_day, shanghai_day):
        print("OK: last_updated %s covers the newest data commit %s (%s)"
              % (stated, sha, when.isoformat()))
        return 0
    print("::error::data/meta.yaml last_updated is %s, but data/ changed in %s on %s. "
          "Set `last_updated: %s` and rebuild the READMEs (python scripts/build.py)."
          % (stated, sha, when.isoformat(), shanghai_day))
    return 1


if __name__ == "__main__":
    sys.exit(main())
