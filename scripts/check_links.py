# -*- coding: utf-8 -*-
"""Verify every URL in data/*.yaml.

- arXiv abs URLs are checked against the arXiv API *and* their title is compared
  with the entry title (catches wrong-ID / right-ID-wrong-paper mistakes).
- All other URLs get an HTTP request with a browser user-agent.
  403 / 405 / 429 are reported as BLOCKED (reachable, but refuses bots) rather
  than DEAD, because publisher sites routinely do this.

Usage:  python scripts/check_links.py
"""
import io
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FILES = ["papers.yaml", "toolkits.yaml", "datasets.yaml", "benchmarks.yaml", "learning.yaml"]
URL_FIELDS = ("url", "repo", "homepage", "paper", "code", "project", "data")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
# Certificate verification is off on purpose. This checker only ever fetches
# public URLs listed in data/*.yaml, sends no credentials and stores no
# response body — only the status code — so there is nothing for a
# man-in-the-middle to steal, while verification would produce false "dead
# link" reports for hosts whose certificates are simply mismatched or expired
# (medicaldecathlon.com is a known case: its certificate does not cover the
# hostname). Liveness is what this script measures, not trust.
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


# arXiv's API guidelines ask for at least 3 seconds between requests. Going
# faster gets a *silently empty* feed rather than an error, which this script
# used to read as "id not found" — that produced 70+ phantom dead links in
# scripts/oneoff/link-report.txt. The delay below is deliberately above the
# documented floor, and arxiv_title() now distinguishes the two cases so a
# throttle can never be reported as a missing paper.
ARXIV_DELAY = 3.1


def arxiv_title(aid):
    """Title for an arXiv id, or None when the id genuinely has none.

    Returns a ``(title, unreachable)`` pair: on a throttle or transport error
    ``unreachable`` is True and the caller must NOT treat the entry as broken.
    A well-formed feed with no entry for the id is a real miss (True is False).
    """
    url = "https://export.arxiv.org/api/query?id_list=%s" % aid
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            xml = r.read().decode("utf-8", "replace")
    except Exception:
        return None, True
    if "<entry>" not in xml:
        # The feed came back without an entry. That is either a genuinely
        # absent id or an empty throttle response; the two are indistinguishable
        # by body alone, so confirm with one slower retry before calling it gone.
        time.sleep(ARXIV_DELAY)
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                xml = r.read().decode("utf-8", "replace")
        except Exception:
            return None, True
        if "<entry>" not in xml:
            return None, False
    ts = re.findall(r"<title>([^<]*)</title>", xml)
    if len(ts) < 2:
        return None, False
    return re.sub(r"\s+", " ", ts[1]).strip(), False


def http_status(url, tries=3):
    last = None
    for k in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception as e:
            last = type(e).__name__
            time.sleep(1.5 + 1.5 * k)
    return "ERR:%s" % last


def main():
    rows = []
    for fn in FILES:
        p = os.path.join(DATA, fn)
        if not os.path.exists(p):
            continue
        with io.open(p, encoding="utf-8") as f:
            items = yaml.safe_load(f) or []
        for i, e in enumerate(items):
            if not isinstance(e, dict):
                continue
            title = e.get("title") or e.get("name") or e.get("id")
            for k in URL_FIELDS:
                v = e.get(k)
                if not v or not str(v).startswith("http"):
                    continue
                rows.append((fn, i, title, k, str(v)))

    out = []
    out.append("checking %d URLs ..." % len(rows))
    print(out[-1] + "\n")
    bad, blocked, ok, warn = [], [], 0, []
    for fn, i, title, k, url in rows:
        m = re.match(r"https?://arxiv\.org/abs/(.+)$", url)
        if m:
            aid = m.group(1)
            try:
                got, unreachable = arxiv_title(aid)
            except Exception as e:
                got, unreachable = None, True
                warn.append((fn, i, title, url, "arxiv api %s" % type(e).__name__))
            if unreachable:
                # Throttled or unreachable: say so instead of inventing a dead
                # link, and keep it out of the PROBLEM list entirely.
                warn.append((fn, i, title, url, "arxiv api unreachable (not a dead link)"))
            elif got is None:
                bad.append((fn, i, title, url, "arxiv id not found"))
            else:
                s = similar(title, got)
                if s < 0.5:
                    bad.append((fn, i, title, url, "title mismatch (%.2f): %s" % (s, got[:60])))
                else:
                    ok += 1
            time.sleep(ARXIV_DELAY)
            continue

        st = http_status(url)
        if st in (200, 202, 301, 302, 307, 308):
            # 202 is what IEEE's DOI resolver returns to non-browser clients;
            # the DOI itself is valid (verified separately against Crossref).
            ok += 1
        elif st in (403, 405, 429):
            blocked.append((fn, i, title, url, st))
        else:
            bad.append((fn, i, title, url, st))
        time.sleep(0.4)

    out.append("=" * 78)
    out.append("OK      : %d" % ok)
    out.append("BLOCKED : %d  (reachable, refuses bots)" % len(blocked))
    out.append("PROBLEM : %d" % len(bad))
    if bad:
        out.append("\n--- PROBLEM ---")
        for fn, i, title, url, why in bad:
            out.append("  %s[%d] %s" % (fn, i, str(title)[:44]))
            out.append("      %s\n      -> %s" % (url, why))
    if blocked:
        out.append("\n--- BLOCKED (spot-check by hand) ---")
        for fn, i, title, url, st in blocked:
            out.append("  %-16s %-5s %s" % (fn, st, url))
    if warn:
        out.append("\n--- WARN ---")
        for w in warn:
            out.append("   %s" % (w,))

    text = "\n".join(out)
    print(text)
    with io.open(os.path.join(ROOT, "scripts", "oneoff", "link-report.txt"),
                 "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    print("\n报告已写入 scripts/oneoff/link-report.txt")


if __name__ == "__main__":
    main()
