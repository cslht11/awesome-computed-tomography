# -*- coding: utf-8 -*-
"""Re-check the arXiv ids that `check_links.py` flagged, at a polite rate.

Why this exists: `check_links.py` polls arXiv every 1.2 s, but the API asks for
one request per 3 s. When it gets throttled the response comes back without a
<entry>, the helper returns None, and the caller reports "arxiv id not found" —
a false negative. This script re-queries each flagged id individually with
retries and a 3.5 s gap, so "not found" is only reported when it is real.

Usage:
    python scripts/oneoff/recheck_arxiv.py
"""
import io
import os
import re
import ssl
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REPORT = os.path.join(HERE, "link-report.txt")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

GAP = 3.5          # arXiv asks for >= 3 s between requests


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    return len(wa & wb) / max(len(wa), len(wb)) if wa and wb else 0.0


def entry_title(xml):
    ts = re.findall(r"<title>([^<]*)</title>", xml)
    if len(ts) < 2:
        return None
    return re.sub(r"\s+", " ", ts[1]).strip()


def lookup(aid, tries=3):
    for k in range(tries):
        url = "https://export.arxiv.org/api/query?id_list=%s" % aid
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                xml = r.read().decode("utf-8", "replace")
            t = entry_title(xml)
            if t:
                return t, None
            err = "empty entry"
        except urllib.error.HTTPError as e:
            err = "HTTP %s" % e.code
        except Exception as e:
            err = type(e).__name__
        time.sleep(GAP * (k + 2))        # back off harder on each failure
    return None, err


def main():
    txt = io.open(REPORT, encoding="utf-8").read()
    # blocks look like:  papers.yaml[20] <entry title>\n      <url>\n      -> why
    blocks = re.findall(r"^  (\S+)\[(\d+)\] (.+)\n      (\S+)\n      -> (.+)$",
                        txt, re.M)
    targets = []
    for fn, idx, title, url, why in blocks:
        m = re.match(r"https?://arxiv\.org/abs/(.+)$", url)
        if m:
            targets.append((fn, idx, title, m.group(1), why))

    print("flagged arXiv ids to re-check: %d\n" % len(targets))
    real, false_alarm = [], []
    for i, (fn, idx, title, aid, why) in enumerate(targets, 1):
        got, err = lookup(aid)
        if got is None:
            real.append((fn, idx, title, aid, err))
            print("%3d/%d  %-16s %-28s STILL FAILING (%s)"
                  % (i, len(targets), aid, title[:28], err))
        else:
            s = similar(title, got)
            if s < 0.5:
                real.append((fn, idx, title, aid, "title mismatch %.2f: %s" % (s, got[:50])))
                print("%3d/%d  %-16s %-28s MISMATCH %.2f -> %s"
                      % (i, len(targets), aid, title[:28], s, got[:44]))
            else:
                false_alarm.append((fn, idx, title, aid, s))
                print("%3d/%d  %-16s %-28s OK (%.2f)"
                      % (i, len(targets), aid, title[:28], s))
        time.sleep(GAP)

    print("\n" + "=" * 74)
    print("false alarms (id is valid) : %d" % len(false_alarm))
    print("genuine problems          : %d" % len(real))
    for fn, idx, title, aid, why in real:
        print("   %s[%s] %s  %s  -> %s" % (fn, idx, str(title)[:40], aid, why))
    if false_alarm:
        lo = min(s for *_, s in false_alarm)
        print("lowest title-match score among the valid ids: %.2f" % lo)


if __name__ == "__main__":
    main()
