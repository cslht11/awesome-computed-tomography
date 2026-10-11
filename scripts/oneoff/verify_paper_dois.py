# -*- coding: utf-8 -*-
"""对 data/papers.yaml 里每个 doi.org 链接做元数据核验。

- 拉 Crossref 权威记录，比对标题（相似度 < 0.85 判为错配并报警）
- 把权威 year / container-title 写进 scripts/oneoff/doi_meta.json
  （由 merge_papers.py 幂等套用；venue 只在能映射成短标签时覆盖）
"""
import io
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(ROOT, "data", "papers.yaml")
OUT = os.path.join(HERE, "doi_meta.json")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def sim(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return None
            time.sleep(2 + 2 * k)
        except Exception:
            time.sleep(2 + 2 * k)
    return None


def main():
    items = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    meta, mismatch, n = {}, [], 0
    for e in items:
        u = str(e.get("paper") or "")
        if "doi.org/" not in u:
            continue
        doi = u.split("doi.org/", 1)[1]
        x = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        n += 1
        if not x:
            mismatch.append((e.get("abbr") or e["title"][:26], doi, "FETCH FAILED", 0.0))
            continue
        try:
            d = json.loads(x)["message"]
        except Exception:
            mismatch.append((e.get("abbr") or e["title"][:26], doi, "BAD JSON", 0.0))
            continue
        got = (d.get("title") or [""])[0]
        s = sim(e["title"], got)
        yr = None
        for k in ("published-print", "published-online", "issued"):
            dp = (d.get(k) or {}).get("date-parts") or []
            if dp and dp[0] and dp[0][0]:
                yr = dp[0][0]
                break
        cont = (d.get("container-title") or [""])[0]
        if s >= 0.85:
            meta[doi] = {"year": yr, "container": cont}
        else:
            mismatch.append((e.get("abbr") or e["title"][:26], doi, got[:52], s))
        if n % 25 == 0:
            print("  ... %d" % n)
        time.sleep(0.55)

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(meta, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    print("\n核验 %d 个 DOI，写入 %d 条元数据 -> %s" % (n, len(meta), OUT))
    if mismatch:
        print("\n!! 标题不匹配（需人工确认）%d 条：" % len(mismatch))
        for a, doi, got, s in mismatch:
            print("  %-28s %-34s %.2f  %s" % (a, doi, s, got))
    else:
        print("全部 DOI 的标题与条目一致。")


if __name__ == "__main__":
    main()
