# -*- coding: utf-8 -*-
"""第二轮：DOI 反查 + 权威元数据回写。

对 papers_supp.yaml 里的每条 paper 链接：
  - doi.org  -> 拉 https://api.crossref.org/works/<doi>，拿权威 title / year / venue，
                 与期望标题比对；相似度 < 0.85 判定为错配，进入重解析。
  - arxiv    -> 拉 arXiv API，同样比对。
重解析用「年份加窗的 Crossref 检索 + arXiv 兜底」，仍失败则删掉 paper 字段。
最后把权威 year / venue 写回 yaml。
"""
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "papers_supp.yaml")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

PREPRINT = ("techrxiv", "researchsquare", "ssrn", "preprints.org", "biorxiv", "medrxiv")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def get(url, tries=4, timeout=35):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                return None
            time.sleep(2 + 2 * k)
        except Exception:
            time.sleep(2 + 2 * k)
    return None


def cr_work(doi):
    txt = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if not txt:
        return None
    try:
        it = json.loads(txt)["message"]
    except Exception:
        return None
    t = (it.get("title") or [""])[0]
    yr = None
    for k in ("published-print", "published-online", "issued", "created"):
        dp = (it.get(k) or {}).get("date-parts") or []
        if dp and dp[0] and dp[0][0]:
            yr = dp[0][0]
            break
    cont = (it.get("container-title") or [""])[0]
    return {"title": t, "year": yr, "container": cont,
            "doi": it.get("DOI"), "type": it.get("type")}


def cr_search(title, year):
    """年份加窗检索，返回按 (相似度, 年份接近度) 排序的候选。"""
    q = urllib.parse.quote(title)
    url = ("https://api.crossref.org/works?rows=8&select=DOI,title,type,container-title,"
           "published-print,published-online,issued&query.bibliographic=" + q)
    txt = get(url)
    if not txt:
        return []
    try:
        items = json.loads(txt)["message"]["items"]
    except Exception:
        return []
    out = []
    for it in items:
        ts = it.get("title") or []
        if not ts:
            continue
        s = similar(title, ts[0])
        yr = None
        for k in ("published-print", "published-online", "issued"):
            dp = (it.get(k) or {}).get("date-parts") or []
            if dp and dp[0] and dp[0][0]:
                yr = dp[0][0]
                break
        cont = (it.get("container-title") or [""])[0]
        low = cont.lower()
        pen = 0.15 if any(p in low for p in PREPRINT) else 0.0
        if it.get("type") == "posted-content":
            pen += 0.1
        dy = abs((yr or year) - year)
        out.append({"score": s - pen - 0.02 * min(dy, 5), "sim": s,
                    "doi": it["DOI"], "title": ts[0], "year": yr, "container": cont})
    out.sort(key=lambda x: -x["score"])
    return out


def ax_lookup(title):
    url = ("https://export.arxiv.org/api/query?search_query=all:%s&max_results=6"
           % urllib.parse.quote('"%s"' % title))
    txt = get(url)
    if txt is None:
        return None
    best, bs = None, 0.0
    for e in re.findall(r"<entry>(.*?)</entry>", txt, re.S):
        ids = re.findall(r"<id>(http://arxiv\.org/abs/[^<]+)</id>", e)
        ts = re.findall(r"<title>([^<]*)</title>", e)
        if not ids or not ts:
            continue
        got = re.sub(r"\s+", " ", ts[0]).strip()
        s = similar(title, got)
        if s > bs:
            bs, best = s, (ids[0].replace("http://", "https://"), got)
    if best and bs >= 0.75:
        return {"url": best[0], "title": best[1], "sim": bs}
    return None


def main():
    items = yaml.safe_load(io.open(SRC, encoding="utf-8"))
    fixed, bad, keep, nopaper = [], [], 0, []
    report = []

    for e in items:
        abbr = e.get("abbr") or e["id"]
        title = e["title"]
        year = int(e["year"])
        url = e.get("paper")

        real = None
        if url and "doi.org/" in url:
            doi = url.split("doi.org/", 1)[1]
            w = cr_work(doi)
            if w:
                s = similar(title, w["title"])
                if s >= 0.85:
                    real = {"url": "https://doi.org/" + w["doi"], "title": w["title"],
                            "year": w["year"], "venue": w["container"], "sim": s,
                            "via": "doi-check"}
                    keep += 1
                else:
                    report.append((abbr, "DOI MISMATCH %.2f" % s, url,
                                   (w["title"] or "")[:60]))
            else:
                report.append((abbr, "DOI UNRESOLVED", url, "-"))
        elif url and "arxiv.org/abs/" in url:
            aid = url.split("arxiv.org/abs/", 1)[1]
            txt = get("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid))
            got = None
            if txt:
                ts = re.findall(r"<title>([^<]*)</title>", txt)
                if len(ts) > 1:
                    got = re.sub(r"\s+", " ", ts[1]).strip()
            if got:
                s = similar(title, got)
                if s >= 0.85:
                    real = {"url": url, "title": got, "year": year,
                            "venue": e.get("venue"), "sim": s, "via": "arxiv-check"}
                    keep += 1
                else:
                    report.append((abbr, "ARXIV MISMATCH %.2f" % s, url, got[:60]))
            else:
                report.append((abbr, "ARXIV UNRESOLVED", url, "-"))

        if real is None:
            # ---- re-resolve with a year window
            cands = cr_search(title, year)
            pick = None
            for c in cands:
                if c["sim"] >= 0.90 and abs((c["year"] or year) - year) <= 3:
                    pick = c
                    break
            if pick:
                real = {"url": "https://doi.org/" + pick["doi"], "title": pick["title"],
                        "year": pick["year"], "venue": pick["container"],
                        "sim": pick["sim"], "via": "cr-re-resolve"}
                fixed.append(abbr)
            else:
                ax = ax_lookup(title)
                if ax:
                    real = {"url": ax["url"], "title": ax["title"], "year": year,
                            "venue": e.get("venue"), "sim": ax["sim"], "via": "arxiv-re-resolve"}
                    fixed.append(abbr)
                else:
                    real = None
                    nopaper.append(abbr)
            time.sleep(1.5)

        # ---- write back
        if real:
            e["paper"] = real["url"]
            e["_verified_title"] = real["title"]
            e["_sim"] = round(real["sim"], 2)
            e["_via"] = real["via"]
            if real.get("year"):
                e["year"] = int(real["year"])
            if real.get("venue"):
                v = real["venue"]
                v = re.sub(r"\s+", " ", v).strip()
                if v:
                    e["venue"] = v
        else:
            e.pop("paper", None)
            e["_via"] = "none"

        report.append((abbr, (real or {}).get("via", "none"),
                       (real or {}).get("url", "-"),
                       "%s | %s | %s" % ((real or {}).get("year", "-"),
                                         str((real or {}).get("venue", "-"))[:30],
                                         str((real or {}).get("title", "-"))[:46])))
        time.sleep(0.8)

    # 保留稳定字段顺序
    order = ["id", "abbr", "title", "year", "venue", "topics", "paper", "code", "project"]
    out = ["# Supplementary entries (gap-filling).",
           "# paper links: Crossref DOI first, arXiv fallback; year/venue written back",
           "# from the authoritative Crossref record. `_via` / `_sim` are audit trails.",
           ""]
    for e in items:
        for k in order:
            if e.get(k) is None:
                continue
            v = e[k]
            if k == "topics":
                out.append("  topics: [%s]" % ", ".join(v))
            elif k in ("year",):
                out.append("  %s: %d" % (k, v))
            else:
                out.append("  %s: %s" % (k, json.dumps(v, ensure_ascii=False)))
        for k in ("_via", "_sim", "_verified_title"):
            if e.get(k) is not None:
                out.append("  %s: %s" % (k, json.dumps(e[k], ensure_ascii=False)))
        out.append("")

    io.open(SRC, "w", encoding="utf-8", newline="\n").write("\n".join(out))

    print("%-14s %-16s %s" % ("abbr", "via", "resolved"))
    print("-" * 104)
    for a, v, u, extra in report:
        print("%-14s %-16s %s" % (a, v, u))
        print("%-31s %s" % ("", extra))
    print("\nDOI/arXiv 直接通过 : %d" % keep)
    print("重解析修正        : %d  %s" % (len(fixed), ", ".join(fixed)))
    print("无可用论文链接    : %d  %s" % (len(nopaper), ", ".join(nopaper)))


if __name__ == "__main__":
    main()
