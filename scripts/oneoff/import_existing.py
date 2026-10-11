# -*- coding: utf-8 -*-
"""把已有榜单的引用解析成 papers.yaml 草稿，并按关键词做主题归类。"""
import io
import os
import re
import sys

SRC = r"C:\Users\86722\WorkBuddy AI\2026-10-09-15-24-19\awesome-lists\existing-ct-README.md"
OUT = r"C:\Users\86722\WorkBuddy AI\2026-10-09-15-24-19\ct-awesome\scripts\papers_draft.yaml"

TOPICS = ["survey", "classical", "sparse-view", "limited-angle", "low-dose",
          "metal-artifact", "spectral", "cbct", "dynamic", "scatter", "geometry",
          "unrolling", "self-supervised", "diffusion", "inr", "gaussian", "other"]

# 按优先级排列：先匹配到的主题一定入选；每篇最多保留 3 个主题
RULES = [
    ("survey",          r"survey|review|overview|tutorial|comparison of"),
    ("gaussian",        r"gaussian splatting|3dgs|gaussian primitives|splatting"),
    ("inr",             r"implicit neural|neural representation|nerf|coordinate-based|inr\b"),
    ("diffusion",       r"diffusion model|score-based|denoising diffusion|ddpm|generative model"),
    ("metal-artifact",  r"metal artifact|metal-artifact|\bmar\b|polychromatic|beam hardening|implant"),
    ("spectral",        r"spectral ct|dual-energy|dual energy|photon-counting|multi-energy|material decomposition"),
    ("scatter",         r"scatter"),
    ("geometry",        r"geometry|geometric calibration|motion compensat|head motion|marker-free|misalign"),
    ("dynamic",         r"\b4d\b|dynamic|temporal|cardiac|perfusion|time-resolved"),
    ("limited-angle",   r"limited-angle|limited angle|limited view|limited-view"),
    ("sparse-view",     r"sparse-view|sparse view|few-view|few view|sparse data|undersampl|subsampl|incomplete projection"),
    ("low-dose",        r"low-dose|low dose|denois|noise reduction|noise suppression|dose reduction|ultra-low"),
    ("self-supervised", r"unsupervised|self-supervised|untrained|deep image prior|data-free|dataset-free|test-time|without (paired|labeled)"),
    ("unrolling",       r"unroll|learned primal|learned gradient|model-based deep|deep (residual|unfold)|"
                        r"dual-domain|dual domain|cascaded|iterative network|reconstruction network|"
                        r"transformer|convolutional neural network|cnn|recurrent"),
    ("cbct",            r"cone-beam|cone beam|\bcbct\b"),
    ("classical",       r"filtered backprojection|\bfbp\b|\bfdk\b|sart|sirt|cgls|total variation|\btv\b|"
                        r"algebraic reconstruction|iterative reconstruction|statistical reconstruction|"
                        r"compressed sensing|prior image"),
]


def topics_for(title, venue):
    text = (title + " " + (venue or "")).lower()
    hits = [t for t, pat in RULES if re.search(pat, text)]
    return hits[:3] or ["other"]


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "entry"


def main():
    lines = io.open(SRC, encoding="utf-8", errors="replace").read().split("\n")
    year = None
    entries = []
    seen_titles = set()

    for ln in lines:
        h = re.match(r"^###\s+(\d{4})\s*$", ln)
        if h:
            year = int(h.group(1))
            continue
        if not ln.strip().startswith("- "):
            continue
        body = ln.strip()[2:]

        paper = re.search(r"\[\[(?:paper|Paper|pdf|PDF|Pdf)\]\((https?://[^)]+)\)\]", body)
        code = re.search(r"\[\[(?:code|Code|CODE)\]\((https?://[^)]+)\)\]", body)
        proj = re.search(r"\[\[(?:project|Project|website|Website)\]\((https?://[^)]+)\)\]", body)
        if not paper and not code:
            continue

        abbr = re.search(r"\*\*\[([^\]]{1,40})\]\*\*", body)
        # 去掉链接、锚点、加粗标记后剩下的才是标题
        t = re.sub(r"<a name=\"[^\"]*\"></a>", "", body)
        t = re.sub(r"\[\[[^\]]*\]\([^)]*\)\]", "", t)
        t = re.sub(r"\*\*\[[^\]]*\]\*\*", "", t)
        t = re.sub(r"\((?:\*\*)?[^()]*?(?:\*\*)?\)\s*$", "", t)
        title = t.strip().strip("*").strip()
        title = re.sub(r"\s+", " ", title)
        if len(title) < 12:
            continue
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        venue = None
        vm = re.findall(r"\((?:\*\*)?([A-Za-z][^()]{0,40}?)(?:\*\*)?\)\s*(?:\[\[|$)", body)
        if vm:
            venue = vm[-1].strip()

        y = year
        if y is None:
            ym = re.search(r"\b(20\d{2})\b", body)
            y = int(ym.group(1)) if ym else 2024

        entries.append({
            "id": slug((abbr.group(1) if abbr else title)),
            "abbr": abbr.group(1) if abbr else None,
            "title": title,
            "year": y,
            "venue": venue,
            "topics": topics_for(title, venue),
            "paper": paper.group(1) if paper else None,
            "code": code.group(1) if code else None,
            "project": proj.group(1) if proj else None,
        })

    # 去重 id
    used = {}
    for e in entries:
        base = e["id"]
        n = used.get(base, 0)
        used[base] = n + 1
        if n:
            e["id"] = "%s-%d" % (base, n + 1)

    out = ["# Draft generated from community sources — review before publishing.",
           "# Fields: id, abbr, title, year, venue, topics, paper, code, project", ""]
    for e in sorted(entries, key=lambda x: (-x["year"], x["id"])):
        out.append("- id: %s" % e["id"])
        if e["abbr"]:
            out.append("  abbr: %s" % e["abbr"])
        out.append("  title: %s" % e["title"].replace(":", " -"))
        out.append("  year: %d" % e["year"])
        if e["venue"]:
            out.append("  venue: %s" % e["venue"].replace(":", " -"))
        out.append("  topics: [%s]" % ", ".join(e["topics"]))
        for k in ("paper", "code", "project"):
            if e[k]:
                out.append("  %s: %s" % (k, e[k]))
        out.append("")

    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out))

    from collections import Counter
    tc = Counter(t for e in entries for t in e["topics"])
    print("解析出 %d 条" % len(entries))
    for t in TOPICS:
        print("  %-18s %3d" % (t, tc.get(t, 0)))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
