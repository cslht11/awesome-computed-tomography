"""Independently re-verify three candidate DOIs before writing them into data/papers.yaml.

For each DOI we print the authoritative Crossref record (container-title, title,
issued year) and a local title-similarity score, so the decision is auditable.
"""
import io
import json
import re
import time
import urllib.request

LOCAL = {
    "10.1109/isbi60581.2025.10981301":
        "Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency",
    "10.1109/trpms.2023.3309474":
        "Generative Modeling in Sinogram Domain for Sparse-view CT Reconstruction",
    "10.1117/12.2634939":
        "CoCoDiff: A Contextual Conditional Diffusion Model for Low-dose CT Image Denoising",
}

UA = "Mozilla/5.0 (compatible; ct-awesome venue verification; mailto:noreply@example.com)"


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def tokens(s):
    return set(norm(s).split())


def jaccard(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["message"]


def main():
    print("%-34s %-8s %-6s %-6s %s" % ("DOI", "sim", "title", "year", "container"))
    print("-" * 110)
    rows = []
    for doi, local_title in LOCAL.items():
        try:
            m = crossref(doi)
        except Exception as e:  # noqa: BLE001
            print("%-34s  ERROR %s" % (doi, e))
            continue
        title = (m.get("title") or [""])[0]
        ctitle = (m.get("container-title") or [""])[0]
        parts = (m.get("issued", {}) or {}).get("date-parts", [[None]])
        year = parts[0][0] if parts and parts[0] else None
        sim = jaccard(local_title, title)
        flag = "OK " if sim >= 0.7 else "?? "
        print("%-34s %s%.2f  %-6s %-6s %s" % (doi, flag, sim, "yes" if sim >= 0.7 else "NO", year, ctitle))
        print("      crossref title: %s" % title)
        print("      local    title: %s" % local_title)
        rows.append({"doi": doi, "sim": round(sim, 3), "year": year,
                     "container": ctitle, "crossref_title": title,
                     "local_title": local_title, "type": m.get("type")})
        time.sleep(1.0)
    io.open("scripts/oneoff/venue3-verify.json", "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=2))
    print("\nwrote scripts/oneoff/venue3-verify.json")


if __name__ == "__main__":
    main()
