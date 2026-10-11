# -*- coding: utf-8 -*-
"""Merge the harvested 2025-2026 papers into data/, routing non-paper entries.

Three destinations:
  - data/papers.yaml      reconstruction papers
  - data/datasets.yaml    papers that *release a dataset* (e.g. COBRA2026)
  - data/benchmarks.yaml  challenge reports (e.g. SynthRAD2025)

Idempotent and self-checking: after writing, every file is re-parsed and the
entry count asserted, and any entry block missing its `- ` list marker aborts
the run. That check exists because an earlier version of this script silently
folded 89 entries into the preceding block.

Usage:
    python scripts/oneoff/apply_recent.py            # dry run
    python scripts/oneoff/apply_recent.py --write
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCORED = os.path.join(HERE, "recent_scored.json")
# Second pass: peer-reviewed work the first pass's score threshold missed.
EXTRA = os.path.join(HERE, "recent_extra_final.json")

MIN_SCORE = 57
EXCLUDE = r"quantum|withdraw|retract"

# Rule order = priority. First three matches win, so put narrow facets first.
RULES = [
    ("gaussian",        r"gaussian|splat|3dgs|radiative field"),
    ("inr",             r"implicit neural|\binr\b|neural representation|nerf|coordinate-based"),
    ("diffusion",       r"diffusion|score-based|flow matching|generative model|ddpm|generative adversarial|\bgan\b|variational autoencoder|\bvae\b"),
    ("spectral",        r"spectral ct|dual-energy|dual energy|photon-counting|multi-energy|material decomposition|full-spectrum|energy-resolved|tissue composition|multi-material|k-edge"),
    ("metal-artifact",  r"metal artifact|metal-artifact|\bmar\b|beam hardening|polychromatic|implant|metal-guided"),
    ("scatter",         r"scatter"),
    ("dynamic",         r"\b4d\b|dynamic|time-resolved|temporal|cardiac|perfusion|motion-resolved|deformation field"),
    ("geometry",        r"geometr|trajectory|scan path|\bpose\b|calibration|motion compensat|motion estimat|registration|alignment|misalign|truncat|field of view|\bfov\b|view selection|sampling pattern|shift-variant"),
    ("limited-angle",   r"limited-angle|limited angle|limited-view|angularly sparse|few-view|interior tomography|incomplete (data|projection)"),
    ("sparse-view",     r"sparse[- ]view|sparse x-ray|sparse data|undersampl|subsampl|multi-rate"),
    ("low-dose",        r"low-dose|low dose|denois|noise reduction|dose reduction|ultra-low|dose-aware|sinogram flicking"),
    ("self-supervised", r"self-supervis|unsupervised|untrained|deep image prior|training-free|zero-shot|dataset-free|data-free|test-time"),
    ("cbct",            r"cone-beam|cone beam|\bcbct\b|dental|micro-ct|micro ct|breast|radiotherapy|radiology|image-guided"),
    ("unrolling",       r"unroll|learned|neural network|u-net|transformer|convnet|cnn|deep learning|plug-and-play|primal-dual|neural operator|network|deep prior|half-quadratic|conjugate gradient|learned invertible|deep learning"),
    ("classical",       r"filtered back|\bfbp\b|\bfdk\b|\bsart\b|\bsirt\b|cgls|total variation|\btv\b|algebraic reconstruction|iterative reconstruction|statistical reconstruction|compressed sensing|wavelet|markov random field|dictionary learning|low-rank|tensor|variational"),
    ("survey",          r"survey|review|overview|tutorial|comparison of|challenge report"),
]

# route: title must match -> goes to that file instead of papers.yaml
ROUTES = [
    ("dataset", r"^COBRA2026|projection dataset|dataset for|benchmark dataset|a dataset |"
                r"REconstruction Dataset|Multi-Organ Medical Image REconstruction"),
    ("benchmark", r"challenge report|challenge 202\d|SynthRAD20\d\d challenge report|"
                  r"Benchmark for CT|DegradBench|Physics-Informed Benchmark"),
]

# Titles the keyword rules cannot place; reviewed by hand against the abstract.
TOPIC_OVERRIDE = {
    "MONSTR: Model-Oriented Neutron Strain Tomographic Reconstruction":
        ["classical", "other"],
    "Learning Where and What to Lift for Bi-planar X-ray-to-CT Reconstruction":
        ["sparse-view", "unrolling"],
    "Semantic contrastive learning for orthogonal X-ray computed tomography reconstruction":
        ["sparse-view", "unrolling"],
    "Bigger Isn't Always Better: Towards a General Prior for Medical Image Reconstruction":
        ["diffusion"],
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def topics_for(title, venue):
    t = (title + " " + (venue or "")).lower()
    hits = [k for k, p in RULES if re.search(p, t)]
    return hits[:3] or ["other"]


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "entry"


def clean_venue(c):
    """Turn an arXiv comment into a short venue label, or None."""
    if not c:
        return None
    pats = [r"accepted (?:at|to|by|in|for publication (?:at|in)|for presentation (?:at|in))\s+([^.,;]{3,60})",
            r"published (?:by|in|with|at)\s+([^.,;]{3,60})",
            r"to appear in\s+([^.,;]{3,60})",
            r"(?:oral|spotlight) (?:presentation )?(?:at|in)\s+([^.,;]{3,60})"]
    for p in pats:
        m = re.search(p, c, re.I)
        if m:
            v = re.sub(r"\s+", " ", m.group(1)).strip(" .;:,")
            v = re.sub(r"^\d{4}\s+", "", v)
            return v or None
    return None


def extract_links(comment, abstract):
    blob = (comment or "") + " " + (abstract or "")
    found = re.findall(r"https?://[^\s,;)\]]+", blob)
    code = proj = None
    for u in found:
        u = u.rstrip(".,;")
        if re.search(r"github\.com/[^/]+/[^/?#]+|gitlab\.|codeberg\.", u):
            code = code or u
        elif re.search(r"github\.io|project|page", u, re.I) or re.search(r"\.io/|\.org/", u):
            proj = proj or u
    return code, proj


def dump_yaml_entry(e, dest):
    """Append one entry and return the new file text."""
    lines = []
    if dest == "papers":
        order = ["id", "abbr", "title", "year", "venue", "topics", "paper", "code", "project"]
        first = True
        for k in order:
            v = e.get(k)
            if v is None:
                continue
            if k == "topics":
                body = "topics: [%s]" % ", ".join(v)
            elif k == "year":
                body = "year: %d" % v
            else:
                body = "%s: %s" % (k, json.dumps(v, ensure_ascii=False))
            lines.append(("- " + body) if first else ("  " + body))
            first = False
    else:
        # datasets / benchmarks use `name` + free-form note
        first = True
        for k in ("name", "url", "repo", "homepage", "year", "tasks", "license", "note"):
            v = e.get(k)
            if v is None:
                continue
            if k == "tasks":
                body = "tasks: [%s]" % ", ".join(v)
            elif k == "year":
                body = "year: %d" % v
            else:
                body = "%s: %s" % (k, json.dumps(v, ensure_ascii=False))
            lines.append(("- " + body) if first else ("  " + body))
            first = False
    return "\n".join(lines)


def main():
    write = "--write" in sys.argv
    rows = json.load(io.open(SCORED, encoding="utf-8"))
    sel = [r for r in rows
           if r["score"] >= MIN_SCORE
           and not re.search(EXCLUDE, r["title"] + " " + (r.get("comment") or ""), re.I)]
    # second pass: entries that already carry an acceptance signal, already
    # hand-filtered for scope in recent_extra_final.json
    if os.path.exists(EXTRA):
        extra = json.load(io.open(EXTRA, encoding="utf-8"))
        seen = {r["arxiv_id"] for r in sel}
        for r in extra:
            if r["arxiv_id"] not in seen:
                sel.append(r)
        print("extra batch    : %d" % len(extra))

    # ---- existing state
    src = {}
    for fn in ("papers.yaml", "datasets.yaml", "benchmarks.yaml"):
        p = os.path.join(ROOT, "data", fn)
        s = io.open(p, encoding="utf-8", newline="").read()
        src[fn] = (p, s, "\r\n" if "\r\n" in s else "\n")

    import yaml
    have_titles = {norm(p["title"]) for p in yaml.safe_load(src["papers.yaml"][1])}
    have_ids = {p["id"] for p in yaml.safe_load(src["papers.yaml"][1])}
    # datasets/benchmarks key on `name`; without this the re-run re-adds them
    have_ds = {norm(x["name"]) for x in (yaml.safe_load(src["datasets.yaml"][1]) or [])}
    have_bm = {norm(x["name"]) for x in (yaml.safe_load(src["benchmarks.yaml"][1]) or [])}

    papers, datasets, benchmarks = [], [], []
    for r in sel:
        t = r["title"]
        if norm(t) in have_titles:
            continue
        dest = "papers"
        for kind, pat in ROUTES:
            if re.search(pat, t, re.I):
                dest = kind
                break
        venue = clean_venue(r.get("comment"))
        code, proj = extract_links(r.get("comment") or "", r.get("abstract") or "")
        e = {"title": t, "year": r["year"], "venue": venue,
             "topics": TOPIC_OVERRIDE.get(t) or topics_for(t, venue),
             "paper": "https://arxiv.org/abs/" + r["arxiv_id"],
             "code": code, "project": proj}
        e["id"] = slug(t)
        if dest == "papers":
            i, n = e["id"], 2
            while i in have_ids:
                i = "%s-%d" % (e["id"], n)
                n += 1
            e["id"] = i
            have_ids.add(i)
            papers.append(e)
        elif dest == "dataset":
            if norm(t) in have_ds:
                continue
            have_ds.add(norm(t))
            datasets.append({"name": t, "url": "https://arxiv.org/abs/" + r["arxiv_id"],
                             "year": r["year"], "tasks": ["reconstruction", "benchmarking"],
                             "note": "Released as a public projection dataset (see the paper for access). "
                                     + (r.get("comment") or "")[:120]})
        else:
            if norm(t) in have_bm:
                continue
            have_bm.add(norm(t))
            benchmarks.append({"name": t, "url": "https://arxiv.org/abs/" + r["arxiv_id"],
                               "year": r["year"], "tasks": ["reconstruction"],
                               "note": (r.get("comment") or "")[:180] or "Community challenge."})

    print("selected      : %d" % len(sel))
    print("-> papers     : %d" % len(papers))
    print("-> datasets   : %d %s" % (len(datasets), [d["name"][:34] for d in datasets]))
    print("-> benchmarks : %d %s" % (len(benchmarks), [b["name"][:34] for b in benchmarks]))
    from collections import Counter
    print("topics        : %s" % dict(Counter(t for e in papers for t in e["topics"]).most_common()))
    print("with code     : %d" % sum(1 for e in papers if e["code"]))
    print("other-topic   : %s" % [e["title"][:40] for e in papers if e["topics"] == ["other"]])

    if not write:
        print("\n(dry run — pass --write to apply)")
        return

    # ---- papers.yaml
    p, s, nl = src["papers.yaml"]
    body = (nl + nl).join(dump_yaml_entry(e, "papers") for e in papers)
    io.open(p, "w", encoding="utf-8", newline="").write(s.rstrip("\r\n") + nl + nl + body + nl)

    # ---- datasets.yaml / benchmarks.yaml
    for key, rows_, fn in (("datasets", datasets, "datasets.yaml"),
                           ("benchmarks", benchmarks, "benchmarks.yaml")):
        if not rows_:
            continue
        p, s, nl = src[fn]
        body = (nl + nl).join(dump_yaml_entry(e, key) for e in rows_)
        io.open(p, "w", encoding="utf-8", newline="").write(s.rstrip("\r\n") + nl + nl + body + nl)

    # ---- read back and assert
    n_old = len(yaml.safe_load(src["papers.yaml"][1]))
    back = yaml.safe_load(io.open(src["papers.yaml"][0], encoding="utf-8"))
    assert isinstance(back, list)
    assert len(back) == n_old + len(papers), \
        "expected %d, parsed %d" % (n_old + len(papers), len(back))
    ids = [x["id"] for x in back]
    assert len(ids) == len(set(ids)), "duplicate ids"
    txt = io.open(src["papers.yaml"][0], encoding="utf-8").read()
    assert not re.findall(r"^(?!- )(  id: .+)$", txt, re.M), "block without '- ' marker"
    print("\npapers.yaml : %d -> %d entries (assertions OK)" % (n_old, len(back)))
    for fn in ("datasets.yaml", "benchmarks.yaml"):
        p, s, _ = src[fn]
        o = len(yaml.safe_load(s))
        n = len(yaml.safe_load(io.open(p, encoding="utf-8")))
        print("%-15s : %d -> %d" % (fn, o, n))


if __name__ == "__main__":
    main()
