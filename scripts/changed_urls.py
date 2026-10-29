#!/usr/bin/env python3
"""Which sitemap URLs changed since the live deploy (for IndexNow).

    python scripts/changed_urls.py site https://computedtomography.org/

Hashes every page listed in site/sitemap.xml, writes the hashes to
site/page-hashes.json (deployed with the site), fetches the same file from
the live site, and prints a JSON list of the URLs whose page is new or
differs from what is live. IndexNow asks for changed URLs only; the deploy
used to submit the whole sitemap on every push.

What is compared is the page with its build-day noise removed: the payload's
"generated" date and the ?v= asset hashes (a stylesheet change alters every
page but none of their content). If the live file cannot be read (first run,
network error) every URL counts as changed, which is what the deploy did
before. Standard library only.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request

HASHES = "page-hashes.json"
NOISE = (re.compile(r'"generated":\s*"\d{4}-\d{2}-\d{2}"'),
         re.compile(r"\?v=[0-9a-f]{10}"))


def page_file(site, base, url):
    rel = url[len(base):]
    if not rel or rel.endswith("/"):
        rel += "index.html"
    return os.path.join(site, *rel.split("/"))


def digest(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for pat in NOISE:
        text = pat.sub("", text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main(site, base):
    with open(os.path.join(site, "sitemap.xml"), encoding="utf-8") as f:
        urls = re.findall(r"<loc>([^<]+)</loc>", f.read())
    now = {}
    for u in urls:
        if not u.startswith(base):
            sys.exit("%s is not under %s" % (u, base))
        now[u] = digest(page_file(site, base, u))
    with open(os.path.join(site, HASHES), "w", encoding="utf-8") as f:
        json.dump(now, f, indent=0, sort_keys=True)
        f.write("\n")

    try:
        with urllib.request.urlopen(base + HASHES, timeout=20) as r:
            live = json.load(r)
    except Exception as e:  # first deploy, 404, network: submit everything
        print("no live %s (%s); every URL counts as changed" % (HASHES, e),
              file=sys.stderr)
        live = {}
    changed = [u for u in urls if live.get(u) != now[u]]
    print("%d of %d URLs changed" % (len(changed), len(urls)), file=sys.stderr)
    print(json.dumps(changed))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
