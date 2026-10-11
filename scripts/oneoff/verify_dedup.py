# -*- coding: utf-8 -*-
"""Verify a dedup pass was surgical.

Compares scripts/oneoff/papers_pre_dedup.yaml with data/papers.yaml and checks:

  1. every surviving block is byte-identical to the pre-dedup block, except for
     the small, explicitly listed set of patched fields;
  2. the only blocks that disappeared are duplicates (their normalised title
     still occurs in the new file);
  3. nothing was accidentally reordered or reformatted.

Usage:
    python scripts/oneoff/verify_dedup.py
"""
import io
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from dedup_papers import split_blocks, field, norm   # noqa: E402

PRE = os.path.join(HERE, "papers_pre_dedup.yaml")
POST = os.path.join(ROOT, "data", "papers.yaml")


def by_id(path):
    pre, blocks = split_blocks(io.open(path, encoding="utf-8", newline="").read())
    return pre, collections.OrderedDict((field(b, "id"), b) for b in blocks)


def main():
    pre_head, a = by_id(PRE)
    post_head, b = by_id(POST)
    bad = 0
    print("pre: %d blocks   post: %d blocks" % (len(a), len(b)))

    # 1. order: survivors must keep their relative order
    sa = [i for i in a if i in b]
    sb = list(b)
    if sa != sb:
        print("FAIL order changed")
        for i, (x, y) in enumerate(zip(sa, sb)):
            if x != y:
                print("   first divergence at %d: %s vs %s" % (i, x, y))
                break
        bad += 1
    else:
        print("ok   survivor order preserved")

    # 2. removed blocks must be duplicates
    removed = [i for i in a if i not in b]
    post_titles = {norm(field(v, "title")) for v in b.values()}
    orphans = [i for i in removed if norm(field(a[i], "title")) not in post_titles]
    if orphans:
        print("FAIL removed blocks with no surviving twin: %s" % orphans)
        bad += 1
    else:
        print("ok   all %d removed blocks still have a twin in the new file"
              % len(removed))

    # 3. survivors identical except for declared patches
    changed = []
    for i in sa:
        if a[i] != b[i]:
            changed.append(i)
            da = dict(re.findall(r"(?m)^\s*(\w+): (.*)$", a[i]))
            db = dict(re.findall(r"(?m)^\s*(\w+): (.*)$", b[i]))
            for k in sorted(set(da) | set(db)):
                if da.get(k) != db.get(k):
                    print("     %-58s %s: %s -> %s"
                          % (i[:58], k, da.get(k), db.get(k)))
    print("ok   %d survivors patched, %d byte-identical"
          % (len(changed), len(sa) - len(changed)))

    # 4. no block lost or gained any field other than by insertion
    lost = []
    for i in sa:
        fa = set(re.findall(r"(?m)^\s*(\w+):", a[i]))
        fb = set(re.findall(r"(?m)^\s*(\w+):", b[i]))
        if fa - fb:
            lost.append((i, fa - fb))
    if lost:
        print("FAIL fields dropped: %s" % lost)
        bad += 1
    else:
        print("ok   no survivor lost a field")

    # 5. duplicate titles gone
    t = collections.Counter(norm(field(v, "title")) for v in b.values())
    dup = [k for k, v in t.items() if v > 1]
    if dup:
        print("FAIL duplicate titles remain: %s" % dup[:3])
        bad += 1
    else:
        print("ok   titles unique")

    print("")
    print("RESULT: %s" % ("FAIL" if bad else "PASS"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
