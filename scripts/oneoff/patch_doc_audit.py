# -*- coding: utf-8 -*-
"""One-off: document the DOI-host audit and the open-access preference rule.

Idempotent (probe-based).
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(ROOT, "CONTRIBUTING.md")
ONE = os.path.join(ROOT, "scripts", "oneoff", "README.md")


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


def splice(path, old, new, label, probe=None):
    global ok
    s = read(path)
    if probe and probe in s:
        print("SKIP  %-46s (already applied)" % label)
        return
    n = s.count(old)
    if n != 1:
        print("FAIL  %-46s (count=%d)" % (label, n))
        ok = False
        return
    out = s.replace(old, new)
    if probe:
        assert probe in out, "probe missing after splice: " + label
    write(path, out)
    print("OK    %-46s" % label)


# ---------------------------------------------------------------- CONTRIBUTING
OLD = """- `scripts/check_links.py` requests every URL in `data/` and writes a report to
  `scripts/oneoff/link-report.txt`. Status handling follows what the sites
  actually do to automated clients: `200`/`202`/`30x` count as **OK** (`202` is
  what IEEE's DOI resolver returns to a non-browser client, so it is not a
  failure), `403`/`405`/`429` are reported as **BLOCKED** — reachable but
  refusing bots — and anything else is a **PROBLEM**. A transport error is not
  treated as proof that a site is down.
"""

NEW = """- `scripts/check_links.py` requests every URL in `data/` and writes a report to
  `scripts/oneoff/link-report.txt`. Status handling follows what the sites
  actually do to automated clients: `200`/`202`/`30x` count as **OK** (`202` is
  what IEEE's DOI resolver returns to a non-browser client, so it is not a
  failure), `403`/`405`/`429` are reported as **BLOCKED** — reachable but
  refusing bots — and anything else is a **PROBLEM**. A transport error is not
  treated as proof that a site is down.
- `scripts/oneoff/audit_doi_hosts.py` resolves every DOI and records the host it
  actually ends on, because a `200` is not by itself evidence that a link is
  *useful*. Two findings from that audit are worth knowing: the NeurIPS
  Foundation's own prefix (`10.52202/...`) resolves to `www.proceedings.com`, a
  commercial per-paper store, for papers that are free on arXiv — those entries
  link the arXiv page instead; and four Springer/IEEE DOIs pass through
  `validate.perfdrive.com`, which is a bot check in front of the real publisher
  page, not a redirect somewhere else.
"""

splice(DOC, OLD, NEW, "CONTRIBUTING DOI-host audit", probe="audit_doi_hosts.py")

OLD_STYLE = """- Prefer `https://` and avoid link shorteners or tracking parameters.
"""

NEW_STYLE = """- Prefer `https://` and avoid link shorteners or tracking parameters.
- Prefer the **open-access** destination when the DOI leads to a reseller or a
  per-paper paywall. The venue of record still goes in `venue`, so nothing is
  lost by pointing `paper` at the arXiv page.
"""

splice(DOC, OLD_STYLE, NEW_STYLE, "CONTRIBUTING open-access rule", probe="per-paper paywall")

# ---------------------------------------------------------------- oneoff README
OLD_TBL = """| `patch_contributing.py` | Documented the projection-domain markers and the `202`-is-OK link-check semantics in `CONTRIBUTING.md` |
"""

NEW_TBL = """| `patch_contributing.py` | Documented the projection-domain markers and the `202`-is-OK link-check semantics in `CONTRIBUTING.md` |
| `audit_doi_hosts.py` | Resolved all 112 DOI links and recorded the host each one ends on — this is what caught two NeurIPS entries whose DOI led to a commercial per-paper store instead of the open-access paper |
| `patch_neurips_links.py` | Repointed those two entries (Polyner, R2-Gaussian) at their arXiv records, confirmed by id |
"""

splice(ONE, OLD_TBL, NEW_TBL, "oneoff README audit rows", probe="patch_neurips_links.py")

OLD_FILES = """- `link-report.txt` — output of `scripts/check_links.py` over the whole dataset.
"""

NEW_FILES = """- `link-report.txt` — output of `scripts/check_links.py` over the whole dataset.
- `doi-hosts.txt` — output of `scripts/oneoff/audit_doi_hosts.py`: the final host
  behind every DOI link, plus a histogram, so publisher domains can be told apart
  from resellers and bot-check interstitials.
"""

splice(ONE, OLD_FILES, NEW_FILES, "oneoff README doi-hosts.txt", probe="doi-hosts.txt` — output")

if not ok:
    sys.exit(1)
print("\nall patches applied")
