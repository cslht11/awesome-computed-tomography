# -*- coding: utf-8 -*-
"""One-off: repoint two NeurIPS entries at their open-access version.

`10.52202/*` is the NeurIPS Foundation's own DOI prefix, but the resolver sends
it to `www.proceedings.com` — Curran Associates' per-paper store, with an
"Add to Cart" button — even though both papers are free on arXiv and on the
NeurIPS proceedings site. For a reading list that is the wrong destination.

Both arXiv records were confirmed by id (titles match the entries exactly):
  Polyner      -> arXiv:2306.15203
  R2-Gaussian  -> arXiv:2405.20693

Idempotent (probe-based).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MP = os.path.join(ROOT, "scripts", "oneoff", "merge_papers.py")


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
    s = read(MP)
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
    write(MP, out)
    print("OK    %-44s" % label)


splice(
    '    "R2-Gaussian": {\n'
    '        "title": "R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction",\n'
    '        "venue": "NeurIPS", "year": 2024,\n'
    '        "paper": "https://doi.org/10.52202/079017-1427"},',

    '    "R2-Gaussian": {\n'
    '        "title": "R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction",\n'
    '        "venue": "NeurIPS", "year": 2024,\n'
    '        # The NeurIPS Foundation DOI (10.52202/079017-1427) resolves to a\n'
    '        # paywalled per-paper store; the arXiv record is the same paper and\n'
    '        # is open access.\n'
    '        "paper": "https://arxiv.org/abs/2405.20693"},',
    "R2-Gaussian -> arXiv abs",
    probe="2405.20693")

splice(
    '    "Polyner": {"venue": "NeurIPS", "year": 2023},',
    '    # 10.52202/075280-3048 resolves to the same paywalled store.\n'
    '    "Polyner": {"venue": "NeurIPS", "year": 2023,\n'
    '                "paper": "https://arxiv.org/abs/2306.15203"},',
    "Polyner -> arXiv abs",
    probe="2306.15203")

if not ok:
    sys.exit(1)
print("\nall patches applied")
