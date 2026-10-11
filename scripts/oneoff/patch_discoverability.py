# -*- coding: utf-8 -*-
"""One-off: make the list discoverable.

The repo name `awesome-computed-tomography` is deliberately unique, but it
contains neither "CT" nor "reconstruction" — the words people actually search
for. GitHub matches repository search against the name, description, topics and
README, so those channels have to carry the vocabulary the name cannot.

This rewrites the README intro so the scope terms appear naturally (they are
genuinely what the list covers — scope, not keyword stuffing).

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
        print("SKIP  %-44s (already applied)" % label)
        return
    n = s.count(old)
    if n != 1:
        print("FAIL  %-44s (count=%d)" % (label, n))
        ok = False
        return
    out = s.replace(old, new)
    if probe:
        assert probe in out, "probe missing after splice: " + label
    write(BUILD, out)
    print("OK    %-44s" % label)


OLD = (
    '    parts.append("> A curated list of papers, toolkits, datasets and benchmarks for "\n'
    '                 "**CT reconstruction** \u2014 analytical, iterative, model-based and "\n'
    '                 "deep-learning methods, spanning the whole computed-tomography "\n'
    '                 "chain from projection data to reconstructed volume.\\n")\n'
    '    parts.append("Coverage: %d papers (%d\u2013%d), %d toolkits, %d datasets, "\n'
    '                 "%d benchmarks/challenges, %d learning resources.\\n"\n'
    '                 % (n, min(years), max(years), ntk, nds, nbm, nlr))\n'
)

NEW = (
    '    parts.append("> A curated list of **CT reconstruction** resources for **computed "\n'
    '                 "tomography** (CT / CBCT / micro-CT) \u2014 papers, toolkits, datasets "\n'
    '                 "and benchmarks.\\n"\n'
    '                 ">\\n"\n'
    '                 "> Covers sparse-view, limited-angle, low-dose, metal-artifact, "\n'
    '                 "spectral, cone-beam and 4D/dynamic CT, from analytical FBP and "\n'
    '                 "iterative solvers through deep unrolling, diffusion priors, "\n'
    '                 "implicit neural representations and Gaussian splatting.\\n")\n'
    '    parts.append("Coverage: %d papers (%d\u2013%d), %d toolkits, %d datasets, "\n'
    '                 "%d benchmarks/challenges, %d learning resources. Every paper link "\n'
    '                 "was resolved against Crossref or arXiv, and every URL was checked.\\n"\n'
    '                 % (n, min(years), max(years), ntk, nds, nbm, nlr))\n'
)

splice(OLD, NEW, "build.py README intro", probe="CT / CBCT / micro-CT")

if not ok:
    sys.exit(1)
print("\napplied")
