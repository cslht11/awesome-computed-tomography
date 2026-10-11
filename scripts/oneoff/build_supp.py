# -*- coding: utf-8 -*-
"""补充条目：金属伪影 / 3DGS / INR / CBCT / 4D / 扩散 / 2025-2026 新工作。

论文链接用双通道检索，逐条核验：
  1) Crossref（query.bibliographic）—— 拿 DOI，覆盖 TMI / PMB / MICCAI / CVPR / IJCAI 等
  2) arXiv（all: 全文检索）—— 兜底 NeurIPS / ICLR / ICML 等无 DOI 的会议
两者都按标题相似度打分，低于阈值就不写 paper 字段（宁缺毋滥，只保留 code 链接）。
"""
import io
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

OUT = r"C:\Users\86722\WorkBuddy AI\2026-10-09-15-24-19\ct-awesome\scripts\papers_supp.yaml"

# (repo, abbr, true title, year, venue, topics)
ITEMS = [
    # ---- 3D Gaussian splatting for tomography
    ("Ruyi-Zha/r2_gaussian", "R2-Gaussian",
     "Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction",
     2024, "NeurIPS", ["gaussian", "sparse-view"]),
    ("caiyuanhao1998/SAX-NeRF", "SAX-NeRF",
     "Structure-Aware Sparse-View X-Ray 3D Reconstruction",
     2024, "CVPR", ["inr", "sparse-view"]),
    ("xmed-lab/DIF-Gaussian", "DIF-Gaussian",
     "Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction",
     2024, "MICCAI", ["gaussian", "sparse-view", "cbct"]),
    ("yuyouxixi/x2-gaussian", "X2-Gaussian",
     "X2-Gaussian: 4D Radiative Gaussian Splatting for Continuous-Time Tomographic Reconstruction",
     2025, "ICCV", ["gaussian", "dynamic"]),
    ("wskingdom/DGR", "DGR",
     "Discretized Gaussian Representation for Tomographic Reconstruction",
     2025, "ICCV", ["gaussian"]),
    ("fuyabo/4DGS_for_4DCBCT", "4DGS-4DCBCT",
     "Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections",
     2025, None, ["gaussian", "dynamic", "cbct"]),
    ("Ruyi-Zha/naf_cbct", "NAF",
     "Neural Attenuation Fields for Sparse-View Cone-Beam CT Reconstruction",
     2022, "MICCAI", ["inr", "cbct", "sparse-view"]),

    # ---- implicit neural representations
    ("efzero/PINER", "PINER",
     "PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction",
     2023, "WACV", ["inr", "sparse-view", "self-supervised"]),
    ("jiayangshi/INR4JointCTRecon", "INR-Joint",
     "Implicit Neural Representations for Robust Joint Sparse-View CT Reconstruction",
     2024, "TMLR", ["inr", "sparse-view"]),
    ("MeijiTian/Spener", "Spener",
     "Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction",
     2025, "AAAI", ["inr", "sparse-view", "self-supervised"]),
    ("xmindflow/INCODE", "INCODE",
     "INCODE: Implicit Neural Conditioning with Prior Knowledge Embeddings",
     2024, "WACV", ["inr"]),

    # ---- metal artifact reduction
    ("hongwang01/InDuDoNet", "InDuDoNet",
     "An Interpretable Dual Domain Network for CT Metal Artifact Reduction",
     2021, "MICCAI", ["metal-artifact", "unrolling"]),
    ("hongwang01/ACDNet", "ACDNet",
     "Adaptive Convolutional Dictionary Network for CT Metal Artifact Reduction",
     2022, "IJCAI", ["metal-artifact", "unrolling"]),
    ("iwuqing/Polyner", "Polyner",
     "Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction",
     2023, "NeurIPS", ["metal-artifact", "inr", "self-supervised"]),
    ("zjk1988/DAN-Net", "DAN-Net",
     "Dual-Domain Adaptive-Scaling Non-Local Network for CT Metal Artifact Reduction",
     2023, "Physics in Medicine & Biology", ["metal-artifact", "unrolling"]),
    ("zjk1988/IDOL-Net", "IDOL-Net",
     "IDOL-Net: An Interactive Dual-Domain Parallel Network for CT Metal Artifact Reduction",
     2024, "TMI", ["metal-artifact", "unrolling"]),
    ("zjk1988/SemiMAR", "SemiMAR",
     "SemiMAR: Semi-Supervised Learning for CT Metal Artifact Reduction",
     2024, None, ["metal-artifact", "self-supervised"]),
    ("DeepXuan/DuDoDp-MAR", "DuDoDp-MAR",
     "Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains",
     2024, "TMI", ["metal-artifact", "diffusion", "self-supervised"]),

    # ---- sparse-view / dual domain / unrolling
    ("cewang-sysu/DuDoTrans", "DuDoTrans",
     "DuDoTrans: Dual-Domain Transformer for Sparse-View CT Reconstruction",
     2022, "MLMIR", ["sparse-view", "unrolling"]),
    ("weiwenwu12/DRONE", "DRONE",
     "DRONE: Dual-Domain Residual-Based Optimization Network for Sparse-View CT Reconstruction",
     2021, "TMI", ["sparse-view", "unrolling"]),
    ("haimiaozh/MetaInv-Net", "MetaInv-Net",
     "MetaInv-Net: Meta Inversion Network for Sparse View CT Image Reconstruction",
     2021, "TMI", ["sparse-view", "unrolling"]),
    ("Masaaki-75/freeseed", "FreeSeed",
     "FreeSeed: Frequency-Band-Aware and Self-Guided Network for Sparse-View CT Reconstruction",
     2024, None, ["sparse-view", "unrolling"]),
    ("YC-Markus/code-for-DDDM", "DDDM",
     "Dual-Domain Diffusion Model for Sparse-View CT Reconstruction",
     2023, None, ["sparse-view", "diffusion"]),
    ("yqx7150/SWORD", "SWORD",
     "Stage-by-Stage Wavelet Optimization Refinement Diffusion Model for Sparse-View CT Reconstruction",
     2023, None, ["sparse-view", "diffusion"]),
    ("xmed-lab/CvG-Diff", "CvG-Diff",
     "Cross-View Generalized Diffusion Model for Sparse-View CT Reconstruction",
     2025, "MICCAI", ["sparse-view", "diffusion"]),
    ("zzc623/DD_Net", "DD-Net",
     "A Sparse-View CT Reconstruction Method Based on Dual-Domain Network",
     2021, "TMI", ["sparse-view", "unrolling"]),

    # ---- low-dose denoising
    ("SSinyu/RED-CNN", "RED-CNN",
     "Low-Dose CT with a Residual Encoder-Decoder Convolutional Neural Network",
     2017, "TMI", ["low-dose"]),
    ("workingcoder/EDCNN", "EDCNN",
     "EDCNN: Edge Enhancement-Based Densely Connected Network with Compound Loss for Low-Dose CT Denoising",
     2020, "ICIP", ["low-dose"]),
    ("SSinyu/WGAN-VGG", "WGAN-VGG",
     "Low Dose CT Image Denoising Using a Generative Adversarial Network with Wasserstein Distance and Perceptual Loss",
     2018, "TMI", ["low-dose"]),
    ("xinario/SAGAN", "SAGAN",
     "Sharpness-Aware Low Dose CT Denoising Using Conditional Generative Adversarial Network",
     2018, "Journal of Digital Imaging", ["low-dose"]),
    ("Hzzone/DU-GAN", "DU-GAN",
     "DU-GAN: Generative Adversarial Networks with Dual-Domain U-Net Based Discriminators for Low-Dose CT Denoising",
     2021, "IEEE Transactions on Instrumentation and Measurement", ["low-dose"]),
    ("wdayang/CTformer", "CTformer",
     "CTformer: Convolution-Free Token2Token Dilated Vision Transformer for Low-Dose CT Denoising",
     2023, "Physics in Medicine & Biology", ["low-dose"]),
    ("icon-lab/DenoMamba", "DenoMamba",
     "DenoMamba: A Fused State-Space Model for Low-Dose CT Denoising",
     2024, "MICCAI", ["low-dose"]),
    ("hao1635/ASCON", "ASCON",
     "ASCON: Anatomy-Aware Supervised Contrastive Learning Framework for Low-Dose CT Denoising",
     2023, "MICCAI", ["low-dose"]),

    # ---- spectral / geometry / motion
    ("scuchenxiang/SOUL-Net", "SOUL-Net",
     "SOUL-Net: A Sparse and Low-Rank Unrolling Network for Spectral CT Image Reconstruction",
     2022, "TMI", ["spectral", "unrolling"]),
    ("mareikethies/geometry_gradients_CT", "Motion-Grad",
     "A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT",
     2024, "TMI", ["geometry", "cbct", "dynamic"]),
    ("hejipro/DSigNet", "DSigNet",
     "Downsampled Imaging Geometric Modeling for Accurate CT Reconstruction via Deep Learning",
     2021, "TMI", ["geometry", "unrolling"]),

    # ---- 2025-2026 new work
    ("qic999/Foundation-VAE", "Foundation-VAE",
     "Foundation VAE for CT Reconstruction, Augmentation and Beyond",
     2026, "ICML", ["low-dose", "diffusion"]),
    ("DM4CT/DM4CT", "DM4CT",
     "DM4CT: Benchmarking Diffusion Models for CT Reconstruction",
     2026, "ICLR", ["diffusion", "survey"]),
]

UA = "awesome-computed-tomography/1.0 (https://github.com/cslht11/awesome-computed-tomography)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def similar(a, b):
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def get(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if k == tries - 1:
                return None
            time.sleep(2)
    return None


def crossref(title):
    """返回 (doi_url, got_title, score)。"""
    url = ("https://api.crossref.org/works?rows=5&select=DOI,title,type"
           "&query.bibliographic=" + urllib.parse.quote(title))
    txt = get(url)
    if not txt:
        return None, None, 0.0
    try:
        items = json.loads(txt)["message"]["items"]
    except Exception:
        return None, None, 0.0
    best, bs = None, 0.0
    for it in items:
        ts = it.get("title") or []
        if not ts:
            continue
        s = similar(title, ts[0])
        if s > bs:
            bs, best = s, (it["DOI"], ts[0])
    if not best:
        return None, None, 0.0
    return "https://doi.org/%s" % best[0], best[1], bs


def arxiv(title):
    """返回 (abs_url, got_title, score)。"""
    url = ("https://export.arxiv.org/api/query?search_query=all:%s"
           "&max_results=5" % urllib.parse.quote('"%s"' % title))
    txt = get(url)
    if txt is None:
        return None, None, 0.0
    entries = re.findall(r"<entry>(.*?)</entry>", txt, re.S)
    best, bs = None, 0.0
    for e in entries:
        ids = re.findall(r"<id>(http://arxiv\.org/abs/[^<]+)</id>", e)
        ts = re.findall(r"<title>([^<]*)</title>", e)
        if not ids or not ts:
            continue
        got = re.sub(r"\s+", " ", ts[0]).strip()
        s = similar(title, got)
        if s > bs:
            bs, best = s, (ids[0].replace("http://", "https://"), got)
    if not best:
        return None, None, 0.0
    return best[0], best[1], bs


def q(s):
    """YAML 安全标量（JSON 双引号字符串是合法 YAML）。"""
    return json.dumps(s, ensure_ascii=False)


def main():
    out = ["# Supplementary entries (gap-filling).",
           "# paper links resolved via Crossref (DOI) then arXiv, title-matched.",
           ""]
    rep = []
    for repo, abbr, title, year, venue, topics in ITEMS:
        doi, dt, ds = crossref(title)
        src, url, got, score = None, None, None, 0.0
        if doi and ds >= 0.80:
            src, url, got, score = "crossref", doi, dt, ds
        else:
            au, at, as_ = arxiv(title)
            if au and as_ >= 0.60 and as_ > ds:
                src, url, got, score = "arxiv", au, at, as_
            elif doi and ds >= 0.60:
                src, url, got, score = "crossref?", doi, dt, ds
        if not src:
            url = None
        out.append("- id: %s" % abbr.lower().replace(" ", "-"))
        out.append("  title: %s" % q(title))
        out.append("  abbr: %s" % q(abbr))
        out.append("  year: %d" % year)
        if venue:
            out.append("  venue: %s" % q(venue))
        out.append("  topics: [%s]" % ", ".join(topics))
        if url:
            out.append("  paper: %s" % url)
        out.append("  code: https://github.com/%s" % repo)
        out.append("")
        rep.append((abbr, src or "-", score, url or "-", (got or "-")[:56]))
        time.sleep(1.0)

    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("%-14s %-10s %5s  %s" % ("abbr", "source", "sim", "resolved"))
    print("-" * 100)
    for a, s, sc, u, g in rep:
        print("%-14s %-10s %5.2f  %s" % (a, s, sc, u))
    miss = [r for r in rep if r[1] == "-"]
    print("\n%d/%d 条解析到论文链接；未解析：%s"
          % (len(rep) - len(miss), len(rep), ", ".join(r[0] for r in miss) or "无"))


if __name__ == "__main__":
    main()
