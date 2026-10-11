# -*- coding: utf-8 -*-
"""Full-repo arXiv audit, keyed by id.

Why this exists: earlier link checks polled arXiv faster than its documented
limit (>= 3 s per request), so throttled responses came back with no <entry>
and were reported as "arxiv id not found". That produced 79 false alarms. A
later point-check script tried to triage them but compared the entry title to
the *position* of the id inside a batched response, which can mis-pair.

This script avoids both traps:
  * one id_list per batch, mapped back to the entry by the <id> inside the XML
    itself, never by position;
  * a 4 s gap between requests and retries on empty/incomplete feeds.

For every arXiv link in data/papers.yaml it reports the title-match score
(word-set overlap) so a real title drift is visible instead of being mistaken
for a dead link.

Usage:
    python scripts/oneoff/audit_arxiv.py            # full audit
    python scripts/oneoff/audit_arxiv.py --min 0.6  # flag only scores below .6
"""
import argparse
import io
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
OUT = os.path.join(HERE, "arxiv-audit.txt")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

GAP = 4.0          # arXiv asks for >= 3 s between requests; leave headroom
BATCH = 20
TRIES = 4


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    return len(wa & wb) / max(len(wa), len(wb)) if wa and wb else 0.0


def load_entries(path):
    """Return [(entry_id, title, arxiv_id)] for every arXiv link in the file."""
    out, eid, title = [], None, None
    for line in io.open(path, encoding="utf-8"):
        m = re.match(r"^- id: \"?([^\"\n]+)\"?\s*$", line)
        if m:
            eid = m.group(1)
            continue
        m = re.match(r'^\s+title: "?(.+?)"?\s*$', line)
        if m:
            title = m.group(1)
            continue
        m = re.match(r'^\s+paper: "?https?://arxiv\.org/abs/([^"\s]+)"?\s*$', line)
        if m and eid:
            aid = re.sub(r"v\d+$", "", m.group(1))
            out.append((eid, title, aid))
            eid, title = None, None
    return out


def parse_entries(xml):
    """Map arxiv id -> title, read from inside each <entry> block."""
    got = {}
    for m in re.finditer(r"<entry>(.*?)</entry>", xml, re.S):
        b = m.group(1)
        i = re.search(r"<id>\s*https?://arxiv\.org/abs/([^<\s]+)\s*</id>", b)
        t = re.search(r"<title>(.*?)</title>", b, re.S)
        if not i or not t:
            continue
        aid = re.sub(r"v\d+$", "", i.group(1).strip())
        got[aid] = re.sub(r"\s+", " ", t.group(1)).strip()
    return got


def fetch(ids, tries=TRIES):
    """Fetch one batch. Retries when the feed comes back short."""
    for k in range(tries):
        url = ("https://export.arxiv.org/api/query?id_list=%s&max_results=%d"
               % (urllib.parse.quote(",".join(ids)), len(ids)))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                xml = r.read().decode("utf-8", "replace")
            got = parse_entries(xml)
            # a throttled feed answers 200 but carries few/no entries
            if len(got) >= max(1, len(ids) // 2):
                return got, None
            err = "short feed (%d/%d)" % (len(got), len(ids))
        except urllib.error.HTTPError as e:
            err = "HTTP %s" % e.code
        except Exception as e:
            err = type(e).__name__
        time.sleep(GAP * (k + 2))
    return {}, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=float, default=0.0,
                    help="only report entries scoring below this")
    args = ap.parse_args()

    entries = load_entries(PAPERS)
    ids = sorted({a for _, _, a in entries})
    if args.min == 0.0:
        print("arXiv links in papers.yaml : %d  (%d unique ids)"
              % (len(entries), len(ids)))
    log = []
    resolved, missing = {}, {}
    batches = [ids[i:i + BATCH] for i in range(0, len(ids), BATCH)]
    for n, batch in enumerate(batches, 1):
        got, err = fetch(batch)
        resolved.update(got)
        for a in batch:
            if a not in got:
                missing[a] = err or "absent"
        if args.min == 0.0:
            print("  batch %2d/%d  %2d/%2d resolved%s"
                  % (n, len(batches), len(got), len(batch),
                     ("  [%s]" % err) if err else ""))
        time.sleep(GAP)

    rows = []
    for eid, title, aid in entries:
        if aid in resolved:
            rows.append((similar(title, resolved[aid]), eid, title, aid,
                         resolved[aid]))
        else:
            rows.append((-1.0, eid, title, aid, "<not resolved: %s>"
                         % missing.get(aid, "?")))
    rows.sort(key=lambda r: r[0])

    log.append("arXiv audit -- %d links, %d ids" % (len(entries), len(ids)))
    log.append("resolved: %d   unresolved: %d" % (len(resolved), len(missing)))
    log.append("")
    for s, eid, title, aid, got in rows:
        if s < 0 or s < args.min:
            log.append("[%.2f] %s" % (s, eid))
            log.append("        ours : %s" % title)
            log.append("        arxiv: %s  (%s)" % (got, aid))
    if not any(s < 0 or s < args.min for s, *_ in rows):
        log.append("(nothing below threshold)")

    io.open(OUT, "w", encoding="utf-8").write("\n".join(log) + "\n")

    bad = [r for r in rows if r[0] < 0 or r[0] < args.min]
    print("")
    print("=" * 74)
    print("resolved          : %d / %d" % (len(resolved), len(ids)))
    print("below threshold   : %d  (min=%.2f)" % (len(bad), args.min))
    if rows and rows[0][0] >= 0:
        print("lowest match score: %.2f  (%s)" % (rows[0][0], rows[0][1]))
    print("report -> %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
