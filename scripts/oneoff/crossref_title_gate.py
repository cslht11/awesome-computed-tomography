"""Last pass over the 11 venue-less pre-2025 entries: query Crossref by FULL
TITLE (not the loose `query.bibliographic`) and accept a hit only when the
returned title matches at >= 0.90 after normalisation.

Rationale: `query.bibliographic` at low similarity returns a different paper
(it "matched" casredscan's DOI 10.1109/tmi.2021.3066318 for the limited-view
entry, which is a different work). A strict title gate removes those.
"""
import io
import json
import os
import re
import time
import urllib.parse
import urllib.request
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
UA = "ct-awesome venue check (mailto:noreply@example.com)"
THRESH = 0.90


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def sim(a, b):
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def search(title):
    url = ("https://api.crossref.org/works?rows=5&select=DOI,title,container-title,issued,type"
           "&query.title=" + urllib.parse.quote(title))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))["message"]["items"]


def main():
    d = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    todo = [e for e in d
            if not e.get("venue") and not e.get("code") and int(e.get("year") or 0) < 2025]
    print("checking %d entries\n" % len(todo))
    results = []
    for e in todo:
        title = e["title"]
        try:
            items = search(title)
        except Exception as ex:  # noqa: BLE001
            print("!! %s : %s" % (e["id"], ex))
            time.sleep(2)
            continue
        best = None
        for it in items:
            t = (it.get("title") or [""])[0]
            s = sim(title, t)
            if best is None or s > best[0]:
                parts = (it.get("issued", {}) or {}).get("date-parts", [[None]])
                best = (s, t, it.get("DOI"), (parts[0][0] if parts and parts[0] else None),
                        (it.get("container-title") or [""])[0], it.get("type"))
        print("%-4s %-58s" % (e.get("year"), e["id"][:58]))
        print("     local : %s" % title[:88])
        if best:
            mark = "ACCEPT" if best[0] >= THRESH else "reject"
            print("     %s %.2f  %s" % (mark, best[0], best[2]))
            print("            %s | %s | %s" % (best[1][:70], best[4][:40], best[3]))
        results.append({"id": e["id"], "year": e.get("year"), "local_title": title,
                        "best": ({"sim": round(best[0], 3), "title": best[1], "doi": best[2],
                                  "year": best[3], "container": best[4], "type": best[5]}
                                 if best else None)})
        time.sleep(1.2)
    io.open(os.path.join(HERE, "weak-tail-crossref.json"), "w", encoding="utf-8").write(
        json.dumps(results, ensure_ascii=False, indent=2))
    acc = [r for r in results if r["best"] and r["best"]["sim"] >= THRESH]
    print("\n=== accepted (sim >= %.2f): %d ===" % (THRESH, len(acc)))
    for r in acc:
        print("  %-46s %-34s %s" % (r["id"][:46], r["best"]["doi"], r["best"]["container"][:40]))


if __name__ == "__main__":
    main()
