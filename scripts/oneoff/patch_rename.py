# -*- coding: utf-8 -*-
"""One-off: rename the project from `awesome-ct-reconstruction` to
`awesome-computed-tomography`.

Reason: `LoraLinH/Awesome-CT-Reconstruction` (241 stars) already occupies that
exact name — GitHub repo names are case-insensitive, so it is a literal
collision, not just a similar one. The new name is unoccupied.

Deliberately NOT touched:
  - `data/learning.yaml` and the README line it generates, which reference
    LoraLinH's list as a *related* resource. That is someone else's repo.

Idempotent (probe-based).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OLD = "awesome-ct-reconstruction"
NEW = "awesome-computed-tomography"

# Files where the old slug must be rewritten. Excludes data/learning.yaml.
FILES = [
    os.path.join(ROOT, "scripts", "build.py"),
    os.path.join(ROOT, "CONTRIBUTING.md"),
    os.path.join(ROOT, "scripts", "oneoff", "build_supp.py"),
    os.path.join(ROOT, "scripts", "oneoff", "normalize_links.py"),
    os.path.join(ROOT, "scripts", "oneoff", "verify_paper_dois.py"),
    os.path.join(ROOT, "scripts", "oneoff", "verify_supp.py"),
]


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
total = 0

for p in FILES:
    s = read(p)
    n = s.count(OLD)
    if n == 0:
        print("SKIP  %-46s (nothing to do)" % os.path.relpath(p, ROOT))
        continue
    out = s.replace(OLD, NEW)
    assert OLD not in out
    write(p, out)
    total += n
    print("OK    %-46s %d occurrence(s)" % (os.path.relpath(p, ROOT), n))

# The README title becomes the umbrella name; the subtitle keeps "CT
# reconstruction" as the first thing a reader (and a search index) sees.
OLD_H1 = "# Awesome CT Reconstruction [![Awesome]"
NEW_H1 = "# Awesome Computed Tomography [![Awesome]"
p = os.path.join(ROOT, "scripts", "build.py")
s = read(p)
if "Awesome Computed Tomography" in s:
    print("SKIP  %-46s (already applied)" % "README H1")
elif s.count(OLD_H1) == 1:
    write(p, s.replace(OLD_H1, NEW_H1))
    print("OK    %-46s" % "README H1 -> Awesome Computed Tomography")
else:
    print("FAIL  %-46s (count=%d)" % ("README H1", s.count(OLD_H1)))
    ok = False

print("\nrewrote %d slug occurrence(s)" % total)
if not ok:
    sys.exit(1)
