# -*- coding: utf-8 -*-
"""One-off audit: where does every `paper` DOI actually land?

The link checker only reports a status code. A 200 is not enough: a DOI can
resolve happily to a paywalled per-paper store while the paper is open access
elsewhere. This resolves each doi.org link and records the final host, so that
aggregators and resellers stand out from real publisher domains.

Writes scripts/oneoff/doi-hosts.txt
"""
import io
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "doi-hosts.txt")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Hosts that are resellers / aggregators rather than the venue itself.
SUSPECT = ("proceedings.com", "bookstore", "eurekaselect", "bentham",
           "sci-hub", "researchgate", "semanticscholar", "ouci.dntb.gov.ua")


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def do_link(e):
    for k in ("paper", "link"):
        v = e.get(k)
        if v and str(v).startswith("https://doi.org/"):
            return str(v)
    return None


def final_host(url, tries=3):
    for i in range(tries):
        try:
            p = subprocess.run(
                ["curl", "-s", "-o", os.devnull, "-A", UA, "--max-time", "30",
                 "-L", "-w", "%{http_code} %{url_effective}", url],
                capture_output=True, text=True, timeout=60)
            out = (p.stdout or "").strip()
            parts = out.split(" ", 1)
            if len(parts) == 2 and parts[0].startswith(("2", "3")):
                m = re.match(r"https?://([^/]+)", parts[1])
                return parts[0], (m.group(1) if m else parts[1])
            if len(parts) == 2 and parts[0] not in ("000",):
                return parts[0], parts[1]
        except Exception:
            pass
        time.sleep(2 + 2 * i)
    return "ERR", ""


def main():
    papers = read(os.path.join(ROOT, "data", "papers.yaml"))
    # Minimal extraction: id / abbr / paper link, in document order.
    entries = []
    cur = {}
    for line in papers.split("\n"):
        m = re.match(r'^- id:\s*"?([^"]+)"?\s*$', line)
        if m:
            if cur:
                entries.append(cur)
            cur = {"id": m.group(1)}
            continue
        m = re.match(r'^\s+abbr:\s*"?([^"]+)"?\s*$', line)
        if m and cur is not None:
            cur["abbr"] = m.group(1)
            continue
        m = re.match(r'^\s+paper:\s*"?([^"]+)"?\s*$', line)
        if m and cur is not None:
            cur["paper"] = m.group(1)
    if cur:
        entries.append(cur)

    dois = [e for e in entries if do_link(e)]
    print("resolving %d DOI links ..." % len(dois))

    lines = []
    hosts = Counter()
    suspects = []
    for i, e in enumerate(dois, 1):
        url = do_link(e)
        code, host = final_host(url)
        hosts[host] += 1
        name = e.get("abbr") or e["id"]
        lines.append("%-28s %-4s %s\n    %s" % (name, code, host, url))
        if any(s in host.lower() for s in SUSPECT):
            suspects.append((name, url, code, host))
            lines[-1] = "SUSPECT " + lines[-1]
        if i % 20 == 0:
            print("  %d/%d" % (i, len(dois)))

    body = "final hosts for %d DOI links\n" % len(dois)
    body += "=" * 78 + "\n"
    body += "\n".join(lines) + "\n\n"
    body += "--- host histogram ---\n"
    for h, c in hosts.most_common():
        body += "%4d  %s\n" % (c, h)
    body += "\n--- suspects (resellers / aggregators) ---\n"
    if suspects:
        for n, u, c, h in suspects:
            body += "  %-28s %s -> %s  (%s)\n" % (n, u, c, h)
    else:
        body += "  none\n"

    with io.open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(body)
        f.flush()
        os.fsync(f.fileno())

    print("\n--- host histogram ---")
    for h, c in hosts.most_common():
        print("%4d  %s" % (c, h))
    print("\nsuspects: %d" % len(suspects))
    for n, u, c, h in suspects:
        print("  %-28s -> %s (%s)" % (n, c, h))
    print("\nwrote %s" % OUT)


if __name__ == "__main__":
    main()
