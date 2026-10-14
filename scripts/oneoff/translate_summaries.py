"""Maintain `data/summaries.<lang>.yaml` — the translated blurbs.

Why a separate file per language
--------------------------------
The blurbs for the English site are generated (`data/summaries.yaml`); the
translations are written by hand and belong in their own file rather than
inside `data/i18n/zh.yaml`, which is a curated overlay full of comments that a
few hundred machine-length entries would swamp.

Usage
-----
Apply a batch of translations from a JSON file of `{paper id: text}`:

    python scripts/oneoff/translate_summaries.py batch.json --lang zh

Report what is still untranslated:

    python scripts/oneoff/translate_summaries.py --status

A missing translation is not an error: `scripts/export_site_data.py` falls back
to the English blurb, so the gap shows up as English text on the translated
site rather than as an empty card.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
EN = os.path.join(DATA, "summaries.yaml")

HEADER = (
    "# 中文一句话简介（覆盖层）。\n"
    "# 英文原文在 data/summaries.yaml；这里的条目按论文 id 覆盖它。\n"
    "# 没有列在这里的论文会回落显示英文原文——缺口是可见的，不是静默的。\n"
    "# 由 scripts/oneoff/translate_summaries.py 写入，也欢迎手工增补。\n\n"
)


def path_for(lang):
    return os.path.join(DATA, "summaries.%s.yaml" % lang)


def load(path):
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write(path, entries):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        for k in sorted(entries):
            f.write("%s: >-\n  %s\n" % (k, entries[k]))


def status(lang):
    en = load(EN)
    tr = load(path_for(lang))
    missing = [k for k in en if k not in tr]
    extra = [k for k in tr if k not in en]
    print("%s: %d / %d translated" % (lang, len(tr), len(en)))
    if missing:
        print("  untranslated (%d): %s%s"
              % (len(missing), ", ".join(sorted(missing)[:12]),
                 " …" if len(missing) > 12 else ""))
    if extra:
        print("  ⚠ keys with no English blurb (%d): %s"
              % (len(extra), ", ".join(sorted(extra)[:12])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch", nargs="?", help="JSON file of {paper id: text}")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status or not args.batch:
        status(args.lang)
        return

    with io.open(args.batch, encoding="utf-8") as f:
        batch = json.load(f)
    en = load(EN)
    unknown = [k for k in batch if k not in en]
    if unknown:
        print("⚠ not in summaries.yaml: %s" % ", ".join(unknown[:10]))
    p = path_for(args.lang)
    cur = load(p)
    cur.update(batch)
    write(p, cur)
    print("added %d; %s now holds %d of %d" % (len(batch), os.path.basename(p),
                                               len(cur), len(en)))


if __name__ == "__main__":
    main()
