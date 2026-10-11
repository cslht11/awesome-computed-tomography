# -*- coding: utf-8 -*-
"""把 data/papers.yaml 里的 paper 链接统一成 doi.org / arxiv.org/abs 两种规范形式。

- 先做确定性修复（老式 arXiv FTP 链接、带跟踪参数的链接、临时签名链接、ResearchGate）
- 其余非规范链接按标题去 Crossref 查 DOI，相似度 >= 0.90 才替换
- 结果写成 scripts/oneoff/link_map.json，由 merge_papers.py 幂等套用
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
MAP = os.path.join(HERE, "link_map.json")

UA = "awesome-computed-tomography/1.0 (mailto:ct-awesome@example.com)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
PREPRINT = ("techrxiv", "researchsquare", "ssrn", "preprints.org", "biorxiv", "medrxiv")

# 已人工核验的确定性替换
HARD = {
    "https://www.researchgate.net/profile/Hongming-Shan-2/publication/364550369_CoCoDiff_a_contextual_conditional_diffusion_model_for_low-dose_CT_image_denoising/links/6363d9b4431b1f5300689d48/CoCoDiff-a-contextual-conditional-diffusion-model-for-low-dose-CT-image-denoising.pdf":
        "https://doi.org/10.1117/12.2634939",
    "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9852485":
        "https://doi.org/10.1109/tmi.2022.3197400",
    "https://www.sciencedirect.com/science/article/abs/pii/S1746809422006589":
        "https://doi.org/10.1016/j.bspc.2022.104204",
    "https://www.sciencedirect.com/science/article/abs/pii/S0031320319301086":
        "https://doi.org/10.1016/j.patcog.2019.03.009",
    # CVF open-access page -> publisher DOI; Nature landing page -> DOI
    "https://openaccess.thecvf.com/content/ICCV2021/html/Reed_Dynamic_CT_Reconstruction_From_Limited_Views_With_Implicit_Neural_Representations_ICCV_2021_paper.html":
        "https://doi.org/10.1109/iccv48922.2021.00226",
    "https://www.nature.com/articles/s41597-021-00893-z":
        "https://doi.org/10.1038/s41597-021-00893-z",
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def sim(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def get(url, tries=4, timeout=40):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return None
            time.sleep(2 + 2 * k)
        except Exception:
            time.sleep(2 + 2 * k)
    return None


def clean(url):
    """确定性清理：去掉跟踪参数、还原 arXiv 链接、去掉视图后缀。"""
    m = re.match(r"https?://arxiv\.org/ftp/arxiv/papers/(\d{4})/(\d{4}\.\d+)\.pdf$", url)
    if m:
        return "https://arxiv.org/abs/%s" % m.group(2)
    m = re.match(r"https?://arxiv\.org/(?:pdf|abs)/(\d{4}\.\d+)(?:v\d+)?(?:\.pdf)?$", url)
    if m:
        return "https://arxiv.org/abs/%s" % m.group(1)
    if url in HARD:
        return HARD[url]
    # 去掉查询串里的跟踪参数（sciencedirect / ieee 等）
    if "?" in url:
        base, qs = url.split("?", 1)
        keep = [p for p in qs.split("&")
                if not re.match(r"(ref|fr|rr|utm_|fbclid|gclid|attachauth|attredirects)",
                                p, re.I)]
        url = base + ("?" + "&".join(keep) if keep else "")
    # 去掉尾部的 /meta、/pdf、/abs 等视图后缀（iopscience 等）
    url = re.sub(r"/(meta|abstract|full|pdf)/?$", "/", url)
    url = re.sub(r"\.pdf$", "", url)
    return url


def is_canonical(u):
    return u.startswith("https://doi.org/") or u.startswith("https://arxiv.org/abs/")


def cr_doi(title, year):
    url = ("https://api.crossref.org/works?rows=6&select=DOI,title,type,container-title,"
           "published-print,published-online,issued&query.bibliographic="
           + urllib.parse.quote(title))
    txt = get(url)
    if not txt:
        return None
    try:
        items = json.loads(txt)["message"]["items"]
    except Exception:
        return None
    best, bs = None, 0.0
    for it in items:
        ts = it.get("title") or []
        if not ts:
            continue
        s = sim(title, ts[0])
        yr = None
        for k in ("published-print", "published-online", "issued"):
            dp = (it.get(k) or {}).get("date-parts") or []
            if dp and dp[0] and dp[0][0]:
                yr = dp[0][0]
                break
        cont = (it.get("container-title") or [""])[0].lower()
        pen = 0.12 if any(p in cont for p in PREPRINT) else 0.0
        if it.get("type") == "posted-content":
            pen += 0.08
        if yr and abs(yr - year) > 3:
            pen += 0.05
        sc = s - pen
        if sc > bs:
            bs, best = sc, ("https://doi.org/" + it["DOI"], s, ts[0])
    if best and bs >= 0.90:
        return best
    return None


def main():
    items = yaml.safe_load(io.open(PAPERS, encoding="utf-8"))
    mapping = {}
    stats = {"already": 0, "hard": 0, "crossref": 0, "keep": 0, "nochange": 0}
    report = []

    for e in items:
        u = e.get("paper")
        if not u:
            continue
        if is_canonical(u):
            stats["already"] += 1
            continue
        c = clean(u)
        if is_canonical(c):
            mapping[u] = c
            stats["hard"] += 1
            report.append(("HARD", e.get("abbr") or e["title"][:24], u, c))
            continue
        if c != u:
            mapping[u] = c
            stats["hard"] += 1
            report.append(("CLEAN", e.get("abbr") or e["title"][:24], u, c))
            u = c
        r = cr_doi(e["title"], int(e["year"]))
        if r:
            mapping[u] = r[0]
            stats["crossref"] += 1
            report.append(("DOI", e.get("abbr") or e["title"][:24], u, r[0]))
        else:
            stats["keep"] += 1
            report.append(("KEEP", e.get("abbr") or e["title"][:24], u, ""))
        time.sleep(0.9)

    io.open(MAP, "w", encoding="utf-8", newline="\n").write(
        json.dumps(mapping, indent=1, ensure_ascii=False, sort_keys=True) + "\n")

    for kind, ab, old, new in report:
        print("%-5s %-26s %s" % (kind, ab[:26], (new or old)[:104]))
    print("\n已是规范形式 %d | 确定性修复 %d | Crossref 换 DOI %d | 保留原链接 %d"
          % (stats["already"], stats["hard"], stats["crossref"], stats["keep"]))
    print("写入", MAP, "（%d 条映射）" % len(mapping))


if __name__ == "__main__":
    main()
