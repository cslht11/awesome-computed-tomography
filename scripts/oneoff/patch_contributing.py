# -*- coding: utf-8 -*-
"""One-off: document two conventions added during the verification round.

1. The projection-domain markers in `data/datasets.yaml` notes.
2. HTTP 202 semantics in the link checker.

Idempotent (probe-based).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(ROOT, "CONTRIBUTING.md")


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
    s = read(DOC)
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
    write(DOC, out)
    print("OK    %-40s" % label)


OLD_DS = """- name: LoDoPaB-CT
  url: https://...          # stable landing page, not a direct download
  modality: CT
  tasks: [low-dose]
  license: CC-BY-4.0
  note: 40k+ slice pairs from the LIDC/IDRI collection.
```
"""

NEW_DS = """- name: LoDoPaB-CT
  url: https://...          # stable landing page, not a direct download
  modality: CT
  tasks: [low-dose]
  license: CC-BY-4.0
  note: "**Projection + image.** 40k+ slice pairs from the LIDC/IDRI collection."
```

Start the `note` with one of two markers when raw projections are available:

| Marker | Meaning |
| --- | --- |
| `**Projection + image.**` | Raw projections **and** a reference volume are released. |
| `**Projection only.**` | Raw projections with no reference volume. |

No marker means the release is image-domain only — still useful, but it cannot
be used to test a forward model. The README renders this convention as a legend,
so keep the wording exactly as above.
"""

splice(OLD_DS, NEW_DS, "CONTRIBUTING datasets markers",
       probe="so keep the wording exactly as above.")

OLD_LINK = """- `scripts/check_links.py` requests every URL in `data/` and writes a report.
  `403`/`429` responses are reported as *blocked* rather than *dead*, because
  publishers refuse non-browser clients.
"""

NEW_LINK = """- `scripts/check_links.py` requests every URL in `data/` and writes a report to
  `scripts/oneoff/link-report.txt`. Status handling follows what the sites
  actually do to automated clients: `200`/`202`/`30x` count as **OK** (`202` is
  what IEEE's DOI resolver returns to a non-browser client, so it is not a
  failure), `403`/`405`/`429` are reported as **BLOCKED** — reachable but
  refusing bots — and anything else is a **PROBLEM**. A transport error is not
  treated as proof that a site is down.
"""

splice(OLD_LINK, NEW_LINK, "CONTRIBUTING link-check semantics", probe="**BLOCKED** — reachable but")

if not ok:
    sys.exit(1)
print("\nall patches applied")
