# -*- coding: utf-8 -*-
"""合并 papers_draft.yaml + papers_supp.yaml -> data/papers.yaml

步骤：
  1. 修复 papers_supp.yaml 丢失的 YAML `- ` 列表前缀（上一轮写回 bug）
  2. 应用人工核验得到的修正表 CORRECTIONS（补 6 条缺失链接、纠正错配）
  3. venue 统一成短标签（Crossref 的长 container 名 -> TMI / MICCAI / CVPR ...）
  4. 与 draft 按标题相似度 + GitHub 仓库路径去重，supp 版本优先（已核验）
  5. 输出 data/papers.yaml，id / abbr 全局唯一
"""
import io
import json
import os
import re
import sys
from collections import Counter

import yaml

# scripts/oneoff/ -> project root is three levels up
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
LINK_MAP = os.path.join(HERE, "link_map.json")


def canonical_paper(u):
    """把 paper 链接归一化：老式 arXiv FTP / PDF -> abs；其余查 link_map。"""
    if not u:
        return u
    u = str(u)
    m = re.match(r"https?://arxiv\.org/ftp/arxiv/papers/(\d{4})/(\d{4}\.\d+)\.pdf$", u)
    if m:
        return "https://arxiv.org/abs/%s" % m.group(2)
    m = re.match(r"https?://arxiv\.org/(?:pdf|abs)/(\d{4}\.\d+)(?:v\d+)?(?:\.pdf)?$", u)
    if m:
        return "https://arxiv.org/abs/%s" % m.group(1)
    for _ in range(4):  # 传递闭包：原始 -> 清理 -> DOI
        nxt = _LINK_MAP.get(u)
        if not nxt or nxt == u:
            break
        u = nxt
    return u


# link_map.json 由 normalize_links.py 生成（确定性修复 + Crossref 换 DOI）
_LINK_MAP = {}
if os.path.exists(LINK_MAP):
    _LINK_MAP = json.load(io.open(LINK_MAP, encoding="utf-8"))

# doi_meta.json 由 verify_paper_dois.py 生成（DOI -> 权威 year / container）
DOI_META = os.path.join(HERE, "doi_meta.json")
_DOI_META = {}
if os.path.exists(DOI_META):
    _DOI_META = json.load(io.open(DOI_META, encoding="utf-8"))
SUPP = os.path.join(HERE, "papers_supp.yaml")
DRAFT = os.path.join(HERE, "papers_draft.yaml")
OUT = os.path.join(ROOT, "data", "papers.yaml")

# ---------------------------------------------------------------- 1. corrections
# abbr -> 覆盖字段。全部经过 Crossref / arXiv / 仓库 README 三方核对。
CORRECTIONS = {
    "R2-Gaussian": {
        "title": "R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction",
        "venue": "NeurIPS", "year": 2024,
        # The NeurIPS Foundation DOI (10.52202/079017-1427) resolves to a
        # paywalled per-paper store; the arXiv record is the same paper and
        # is open access.
        "paper": "https://arxiv.org/abs/2405.20693"},
    "X2-Gaussian": {
        "venue": "ICCV", "year": 2025,
        "paper": "https://doi.org/10.1109/iccv51701.2025.02293"},
    "4DGS-4DCBCT": {"paper": "https://arxiv.org/abs/2501.04140"},
    "NAF": {
        "title": "NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction",
        "venue": "MICCAI", "year": 2022,
        "paper": "https://arxiv.org/abs/2209.14540"},
    "DD-Net": {
        "title": "A Sparse-View CT Reconstruction Method Based on Combination of DenseNet and Deconvolution",
        "venue": "TMI", "year": 2018,
        "paper": "https://doi.org/10.1109/tmi.2018.2823338"},
    "DM4CT": {"paper": "https://arxiv.org/abs/2602.18589", "venue": "ICLR"},
    "Foundation-VAE": {
        # arXiv 2605.30893; comment field reads "ICML 2026 Accepted".
        "title": "Foundation VAEs for 3D CT Reconstruction, Augmentation, and Generation",
        "venue": "ICML", "year": 2026,
        "paper": "https://arxiv.org/abs/2605.30893"},
    "CvG-Diff": {"venue": "MICCAI", "year": 2025},
    "DenoMamba": {"venue": "JBHI", "year": 2025},
    "Motion-Grad": {"venue": "TMI", "year": 2025},
    "SOUL-Net": {"venue": "TNNLS", "year": 2024},
    "IDOL-Net": {"venue": "TRPMS", "year": 2022},
    "SemiMAR": {"venue": "JBHI", "year": 2023},
    "DAN-Net": {"venue": "MICCAI", "year": 2021},
    "FreeSeed": {"venue": "MICCAI", "year": 2023},
    "DuDoTrans": {"venue": "MLMIR", "year": 2022},
    "ASCON": {"venue": "MICCAI", "year": 2023},
    "DIF-Gaussian": {"venue": "MICCAI", "year": 2024},
    "DDDM": {"venue": "TechRxiv", "year": 2023},
    "INCODE": {"venue": "WACV", "year": 2024},
    "PINER": {"venue": "WACV", "year": 2023},
    "Spener": {"venue": "AAAI", "year": 2025},
    "INR-Joint": {"venue": "TMLR", "year": 2024},
    "SAX-NeRF": {"venue": "CVPR", "year": 2024},
    "DGR": {"venue": "ICCV", "year": 2025},
    "DU-GAN": {"venue": "TIM", "year": 2022},
    "MetaInv-Net": {"venue": "TMI", "year": 2021},
    # 10.52202/075280-3048 resolves to the same paywalled store.
    "Polyner": {"venue": "NeurIPS", "year": 2023,
                "paper": "https://arxiv.org/abs/2306.15203"},
    "ACDNet": {"venue": "IJCAI", "year": 2022},
    "InDuDoNet": {"venue": "MICCAI", "year": 2021},
    "DuDoDp-MAR": {"venue": "TMI", "year": 2024},
    "SWORD": {"venue": "TMI", "year": 2024},
    "DRONE": {"venue": "TMI", "year": 2021},
    "DSigNet": {"venue": "TMI", "year": 2021},
    "EDCNN": {"venue": "ICSP", "year": 2020},
    "RED-CNN": {"venue": "TMI", "year": 2017},
    "WGAN-VGG": {"venue": "TMI", "year": 2018},
    "SAGAN": {"venue": "JDI", "year": 2018},
    "CTformer": {"venue": "PMB", "year": 2023},
    "Spener-dup": {},
}

# ---------------------------------------------------------------- 1b. 手工核验的补充条目
# 每条都用 Crossref / arXiv 单独查过，link 与标题一致才写进来。
# 用于填补关键词自动归类覆盖不到的 topic：survey / scatter / 2025-2026 新工作。
EXTRA = [
    # ---- surveys
    {"abbr": "DL-CT-Rev", "title": "Deep Learning for Tomographic Image Reconstruction",
     "year": 2020, "venue": "Nat Mach Intell",
     "paper": "https://doi.org/10.1038/s42256-020-00273-z", "topics": ["survey"]},
    {"abbr": "DataDriven", "title": "Solving Inverse Problems Using Data-Driven Models",
     "year": 2019, "venue": "Acta Numerica",
     "paper": "https://doi.org/10.1017/S0962492919000059", "topics": ["survey", "classical"]},
    {"abbr": "Sparsity2DL",
     "title": "Image Reconstruction: From Sparsity to Data-Adaptive Methods and Machine Learning",
     "year": 2020, "venue": "Proc. IEEE",
     "paper": "https://doi.org/10.1109/JPROC.2019.2936204", "topics": ["survey", "classical"]},
    {"abbr": "DL-InvProb", "title": "Deep Learning Techniques for Inverse Problems in Imaging",
     "year": 2020, "venue": "IEEE JSAIT",
     "paper": "https://arxiv.org/abs/2005.06001", "topics": ["survey", "unrolling"]},
    {"abbr": "CNN-InvRev",
     "title": "Convolutional Neural Networks for Inverse Problems in Imaging: A Review",
     "year": 2017, "venue": "IEEE SPM",
     "paper": "https://doi.org/10.1109/MSP.2017.2739299", "topics": ["survey"]},
    {"abbr": "CT-Evolution",
     "title": "The Evolution of Image Reconstruction for CT: From Filtered Back Projection to Artificial Intelligence",
     "year": 2019, "venue": "Eur Radiol",
     "paper": "https://doi.org/10.1007/s00330-018-5810-7", "topics": ["survey", "classical"]},
    {"abbr": "MAR-4Dec", "title": "Metal Artifact Reduction in CT: Where Are We After Four Decades?",
     "year": 2016, "venue": "IEEE Access",
     "paper": "https://doi.org/10.1109/ACCESS.2016.2608621", "topics": ["survey", "metal-artifact"]},
    {"abbr": "DiffRecon", "title": "Diffusion Models for Medical Image Reconstruction",
     "year": 2024, "venue": "BJR|AI",
     "paper": "https://doi.org/10.1093/bjrai/ubae013", "topics": ["survey", "diffusion"]},
    {"abbr": "DiffMed",
     "title": "Diffusion Models for Medical Image Analysis: A Comprehensive Survey",
     "year": 2022, "venue": "arXiv",
     "paper": "https://arxiv.org/abs/2211.07804", "topics": ["survey", "diffusion"]},

    # ---- scatter
    {"abbr": "Scatter-Rev",
     "title": "A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1",
     "year": 2011, "venue": "Med Phys",
     "paper": "https://doi.org/10.1118/1.3589140", "topics": ["scatter", "survey", "cbct"]},
    {"abbr": "DSE",
     "title": "Deep Scatter Estimation (DSE): Feasibility of Using a Deep Convolutional Neural Network for Scatter Estimation in X-Ray Computed Tomography",
     "year": 2018, "venue": "SPIE MI",
     "paper": "https://doi.org/10.1117/12.2292919", "topics": ["scatter", "unrolling"]},
    {"abbr": "Scatter-DL",
     "title": "Scatter Correction Using Deep Learning for Cone-Beam Computed Tomography",
     "year": 2024, "venue": "DL4X-ray",
     "paper": "https://doi.org/10.1007/978-3-031-75653-5_6", "topics": ["scatter", "cbct"]},

    # ---- 2025-2026 recent work
    {"abbr": "GR-Gaussian",
     "title": "GR-Gaussian: Graph-Based Radiative Gaussian Splatting for Sparse-View Tomography",
     "year": 2026, "venue": "TCI",
     "paper": "https://doi.org/10.1109/TCI.2026.3701585", "topics": ["gaussian", "sparse-view"]},
    {"abbr": "SNAF", "title": "SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields",
     "year": 2022, "venue": "arXiv",
     "paper": "https://arxiv.org/abs/2211.17048", "topics": ["inr", "cbct", "sparse-view"]},
    {"abbr": "Epi-NAF",
     "title": "Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency",
     "year": 2024, "venue": "arXiv",
     "paper": "https://arxiv.org/abs/2411.06181", "topics": ["inr", "limited-angle", "geometry"]},
    {"abbr": "DiffNAF",
     "title": "Iterative Diffusion-Refined Neural Attenuation Fields for Multi-Source Stationary Tomography",
     "year": 2025, "venue": "arXiv",
     "paper": "https://arxiv.org/abs/2511.14310", "topics": ["inr", "diffusion"]},
    {"abbr": "BaggageCT",
     "title": "Fan-Beam CT Reconstruction for Unaligned Sparse-View X-Ray Baggage Data",
     "year": 2024, "venue": "arXiv",
     "paper": "https://arxiv.org/abs/2412.03036", "topics": ["sparse-view", "geometry"]},
]

# ---------------------------------------------------------------- 1c. 主题人工重标
# 关键词规则漏掉的条目（title 里没有显式关键词），按标题人工补 topic。
TOPIC_FIX = [
    ("Mixed Poisson-Gaussian Noise Model", ["classical", "low-dose"]),
    ("Stabilizing deep tomographic reconstruction - Part A", ["unrolling", "self-supervised"]),
    ("Stabilizing deep tomographic reconstruction - Part B", ["unrolling", "self-supervised"]),
    ("FISTA-Net", ["unrolling", "classical"]),
    ("Parameter-Dependent Framework for Data From Multiple Geometries", ["geometry", "unrolling"]),
    ("Learning to Reconstruct CT Images From the VVBP-Tensor", ["unrolling", "classical"]),
    ("Noise and spatial resolution properties of a commercially available", ["low-dose", "other"]),
    ("An End-to-End Deep Network for Reconstructing CT Images Directly", ["sparse-view", "unrolling"]),
    ("Radon Inversion via Deep Learning", ["unrolling", "classical"]),
    ("Momentum-Net", ["unrolling", "classical"]),
    ("regional adaptive variational PDE model", ["classical"]),
    ("Patient-specific reconstruction of volumetric computed tomography", ["sparse-view", "classical"]),
    ("Learning to Reconstruct Computed Tomography Images Directly From Sinogram", ["unrolling", "other"]),
    ("AUTOMAP", ["unrolling", "other"]),
    ("Intelligent Parameter Tuning in Optimization-Based Iterative", ["classical", "unrolling"]),
    ("Regularization analysis and design for prior-image-based", ["classical"]),
    ("spatially encoded nonlocal penalty", ["classical", "low-dose"]),
    ("Learned convex regularizers for inverse problems", ["classical", "unrolling"]),
    ("EAGLE", ["other"]),
    ("review on deep learning in medical image reconstruction", ["survey", "unrolling"]),
]

# ---------------------------------------------------------------- 2. venue 归一
VENUE_MAP = [
    (r"computer vision and pattern recognition", "CVPR"),
    (r"international conference on computer vision", "ICCV"),
    (r"winter conference on applications of computer vision", "WACV"),
    (r"international joint conference on artificial intelligence", "IJCAI"),
    (r"neural information processing systems", "NeurIPS"),
    (r"aaai conference on artificial intelligence", "AAAI"),
    (r"international conference on signal processing", "ICSP"),
    (r"^ieee transactions on medical imaging$", "TMI"),
    (r"^ieee transactions on radiation and plasma medical sciences$", "TRPMS"),
    (r"^ieee journal of biomedical and health informatics$", "JBHI"),
    (r"^ieee transactions on neural networks and learning systems$", "TNNLS"),
    (r"^ieee transactions on instrumentation and measurement$", "TIM"),
    (r"^ieee transactions on computational imaging$", "TCI"),
    (r"^physics in medicine", "PMB"),
    (r"^journal of digital imaging$", "JDI"),
    (r"^medical physics$", "Med Phys"),
    (r"^inverse problems$", "Inverse Problems"),
    (r"^tomography$", "Tomography"),
    (r"^biomedical signal processing and control$", "BSPC"),
    (r"^computers in biology and medicine$", "CBM"),
    (r"^computer methods and programs in biomedicine$", "CMPB"),
    (r"^patterns$", "Patterns"),
    (r"^ieee journal of biomedical", "JBHI"),
    (r"^ieee transactions on biomedical engineering$", "TBME"),
    (r"^nature machine intelligence$", "Nat Mach Intell"),
    (r"^acta numerica$", "Acta Numerica"),
    (r"^proceedings of the ieee$", "Proc. IEEE"),
    (r"^ieee journal on selected areas in information theory$", "IEEE JSAIT"),
    (r"^ieee signal processing magazine$", "IEEE SPM"),
    (r"^european radiology$", "Eur Radiol"),
    (r"^ieee access$", "IEEE Access"),
    (r"^bjr", "BJR|AI"),
    (r"^spie medical imaging", "SPIE MI"),
    (r"^deep learning for advanced x-ray", "DL4X-ray"),
    (r"^arxiv$", "arXiv"),
]
SHORT_VENUES = {"TMI", "MICCAI", "CVPR", "ICCV", "ECCV", "NeurIPS", "ICLR", "ICML",
                "AAAI", "WACV", "IJCAI", "MLMIR", "ICSP", "JBHI", "TIM", "TNNLS",
                "TRPMS", "TCI", "PMB", "JDI", "SSVM", "ACM MM", "CMPB", "CBM",
                "BSPC", "Patterns", "Tomography", "Inverse Problems", "Med Phys",
                "JBHI", "TechRxiv", "TMLR", "TRPMS", "ICIFXCT", "ISBI"}


def fix_venue(v):
    if not v:
        return None
    v = str(v).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()
    v = re.sub(r"\s+", " ", v)
    # LNCS 系列统一按会议名写死（Crossref 只给 "Lecture Notes in Computer Science"）
    if v.lower().startswith("lecture notes in computer science"):
        return None  # 由 CORRECTIONS 里的人工值兜底
    low = v.lower()
    for pat, short in VENUE_MAP:
        if re.search(pat, low):
            return short
    # 去掉尾部年份
    v2 = re.sub(r"[\s,]*\(?(?:19|20)\d{2}\)?$", "", v).strip(" ,")
    if v2 in SHORT_VENUES:
        return v2
    if len(v2) <= 22:
        return v2
    return None  # 太长的 container 名不显示，避免表格被撑爆


def fix_title(t):
    t = str(t).replace("&amp;", "&")
    t = re.sub(r"\s+", " ", t).strip()
    # draft 里把冒号换成了 " - "，第一个出现的还原成 ": "
    if ": " not in t:
        m = re.match(r"^(.{1,42}?) - (.+)$", t)
        if m:
            t = "%s: %s" % (m.group(1), m.group(2))
    return t


def norm_words(s):
    return set(re.sub(r"[^a-z0-9]+", " ", str(s).lower()).split())


def sim(a, b):
    wa, wb = norm_words(a), norm_words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def repo_key(u):
    if not u:
        return None
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)", str(u))
    if not m:
        return None
    return (m.group(1) + "/" + m.group(2)).lower().rstrip(".git")


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return (s[:58] or "entry")


# ---------------------------------------------------------------- 3. repair supp
def load_supp():
    raw = io.open(SUPP, encoding="utf-8").read()
    fixed = []
    for ln in raw.split("\n"):
        if re.match(r"^  id: ", ln):
            ln = "- " + ln.strip()
        fixed.append(ln)
    data = yaml.safe_load("\n".join(fixed))
    if not isinstance(data, list):
        sys.exit("supp 修复失败：顶层不是 list（得到 %s）" % type(data).__name__)
    return data


def main():
    supp = load_supp()
    draft = yaml.safe_load(io.open(DRAFT, encoding="utf-8"))
    for x in EXTRA:
        e = dict(x)
        e["topics"] = list(x["topics"])
        supp.append(e)

    for e in supp + draft:
        e["title"] = fix_title(e["title"])
        e["year"] = int(e["year"])

    # 先把 venue 归一成短标签；LNCS 之类无法判断的置空，
    # 后面由 doi_meta.json / CORRECTIONS 补上（CORRECTIONS 优先级最高）
    for e in supp + draft:
        e["venue"] = fix_venue(e.get("venue"))

    # ---------------------------------------------------------------- 4. 去重合并
    merged = list(supp)
    supp_repos = {repo_key(e.get("code")) for e in supp if repo_key(e.get("code"))}
    supp_titles = [e["title"] for e in supp]

    added, dup = 0, []
    for e in draft:
        rk = repo_key(e.get("code"))
        hit = None
        if rk and rk in supp_repos:
            hit = "repo:" + rk
        else:
            for s in supp_titles:
                if sim(e["title"], s) >= 0.90:
                    hit = "title:" + s[:40]
                    break
        if hit:
            dup.append((e["title"][:56], hit))
            continue
        merged.append(e)
        supp_titles.append(e["title"])
        if rk:
            supp_repos.add(rk)
        added += 1

    # ------------------------------------------------ 4b. DOI 权威元数据回写
    # doi_meta.json 由 verify_paper_dois.py 生成（每条 DOI 的标题都与条目比对过）
    nmeta = 0
    for e in merged:
        u = str(e.get("paper") or "")
        if "doi.org/" not in u:
            continue
        m = _DOI_META.get(u.split("doi.org/", 1)[1])
        if not m:
            continue
        if m.get("year") and int(m["year"]) != e["year"]:
            e["year"] = int(m["year"])
            nmeta += 1
        v = fix_venue(m.get("container"))
        if v and v != e.get("venue"):
            e["venue"] = v
            nmeta += 1
    print("DOI 元数据回写 %d 处" % nmeta)

    # ------------------------------------------------ 4c. 人工修正（优先级最高）
    ncorr = 0
    for e in merged:
        c = CORRECTIONS.get(e.get("abbr") or "")
        if not c:
            continue
        for k, v in c.items():
            if e.get(k) != v:
                e[k] = v
                ncorr += 1
    print("人工修正 %d 处" % ncorr)

    print("draft: %d 条，其中 %d 条与 supp 重复已合并，新增 %d 条"
          % (len(draft), len(dup), added))
    for t, h in dup:
        print("   dup  %-58s <- %s" % (t, h))

    # ---------------------------------------------------------------- 5. 收尾
    nfix = 0
    for e in merged:
        t = re.sub(r"[^a-z0-9]+", " ", e["title"].lower())
        for needle, topics in TOPIC_FIX:
            if re.sub(r"[^a-z0-9]+", " ", needle.lower()) in t:
                e["topics"] = topics
                nfix += 1
                break
    print("主题人工重标 %d 条" % nfix)

    ncan = 0
    for e in merged:
        old = e.get("paper")
        new = canonical_paper(old)
        if new != old:
            e["paper"] = new
            ncan += 1
    print("paper 链接归一化 %d 条" % ncan)

    seen_id, seen_ab = {}, {}
    for e in merged:
        base = slug(e.get("abbr") or e.get("id") or e["title"])
        n = seen_id.get(base, 0)
        seen_id[base] = n + 1
        e["id"] = base if not n else "%s-%d" % (base, n + 1)

    for e in merged:
        ab = e.get("abbr")
        if not ab:
            continue
        ab = re.sub(r"\s+", "", str(ab))
        n = seen_ab.get(ab.lower(), 0)
        seen_ab[ab.lower()] = n + 1
        e["abbr"] = ab if not n else "%s-%d" % (ab, n + 1)

    merged.sort(key=lambda e: (-int(e["year"]), (e.get("abbr") or e["title"]).lower()))

    order = ["id", "abbr", "title", "year", "venue", "topics", "paper", "code", "project"]
    out = ["# CT reconstruction papers.",
           "# Generated by scripts/merge_papers.py from community sources + verified",
           "# supplementary entries. Fields: id, abbr, title, year, venue, topics,",
           "# paper, code, project.",
           ""]
    for e in merged:
        first = True
        for k in order:
            v = e.get(k)
            if v in (None, ""):
                continue
            pre = "- " if first else "  "
            first = False
            if k == "topics":
                out.append("%stopics: [%s]" % (pre, ", ".join(v)))
            elif k == "year":
                out.append("%syear: %d" % (pre, int(v)))
            else:
                out.append("%s%s: %s" % (pre, k, json.dumps(str(v), ensure_ascii=False)))
        if first:
            continue
        out.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out))

    tc = Counter(t for e in merged for t in e["topics"])
    print("\ndata/papers.yaml: %d 条" % len(merged))
    print("  有 paper 链接: %d   有 code 链接: %d   无 venue: %d"
          % (sum(1 for e in merged if e.get("paper")),
             sum(1 for e in merged if e.get("code")),
             sum(1 for e in merged if not e.get("venue"))))
    for t, c in tc.most_common():
        print("    %-16s %3d" % (t, c))


if __name__ == "__main__":
    main()
