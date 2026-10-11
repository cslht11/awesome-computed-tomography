# -*- coding: utf-8 -*-
"""One-off: add a legend for the projection-domain markers in the Datasets section,
and drop the lone `**Image domain.**` marker so the convention stays binary.

Idempotent: re-running is a no-op (probe checks).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "scripts", "build.py")
DSETS = os.path.join(ROOT, "data", "datasets.yaml")


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, s, nl="\n"):
    if nl == "\r\n":
        s = s.replace("\r\n", "\n").replace("\n", "\r\n")
    assert "\r" not in s.replace("\r\n", ""), "stray CR before write: " + p
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)
        f.flush()
        os.fsync(f.fileno())


ok = True


def splice(path, old, new, label, probe=None):
    global ok
    s = read(path)
    if probe and probe in s:
        print("SKIP  %-34s (already applied)" % label)
        return
    n = s.count(old)
    if n != 1:
        print("FAIL  %-34s (count=%d)" % (label, n))
        ok = False
        return
    out = s.replace(old, new)
    if probe:
        assert probe in out, "probe missing after splice: " + label
    write(path, out)
    print("OK    %-34s" % label)


OLD_DATASETS = '''def render_datasets(items):
    if not items:
        return ""
    rows = []
    for e in items:
        nm = "[%s](%s)" % (e["name"], e.get("url") or e["repo"])
        rows.append([nm, esc(e.get("modality", "-")),
                     esc(", ".join(e.get("tasks") or []) or "-"),
                     esc(e.get("license", "-")), esc(e.get("note", ""))])
    return render_table(["Dataset", "Modality", "Tasks", "License", "Notes"], rows)
'''

NEW_DATASETS = '''DATASET_LEGEND = (
    "Legend: **Projection + image.** \\u2014 raw projections and a reference volume are both "
    "available, so a forward model can be fitted and the reconstruction scored end to end. "
    "**Projection only.** \\u2014 raw projections with no reference volume; evaluation is "
    "usually task-based (material identification, geometry recovery, downstream segmentation) "
    "rather than image-based. No marker means the release is image-domain only: still useful, "
    "but it cannot be used to test a projection model.\\n"
)


def render_datasets(items):
    if not items:
        return ""
    rows = []
    for e in items:
        nm = "[%s](%s)" % (e["name"], url_of(e, "url", "repo"))
        rows.append([nm, esc(e.get("modality", "-")),
                     esc(", ".join(e.get("tasks") or []) or "-"),
                     esc(e.get("license", "-")), esc(e.get("note", ""))])
    return DATASET_LEGEND + "\\n" + render_table(
        ["Dataset", "Modality", "Tasks", "License", "Notes"], rows)
'''

splice(BUILD, OLD_DATASETS, NEW_DATASETS, "build.py render_datasets + legend",
       probe="DATASET_LEGEND")

splice(DSETS, 'note: "**Image domain.** 480 dental CBCT scans',
       'note: "480 dental CBCT scans', "datasets.yaml drop Image-domain marker",
       probe='note: "480 dental CBCT scans')

if not ok:
    sys.exit(1)
print("\nall patches applied")
