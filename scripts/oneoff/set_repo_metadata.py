# -*- coding: utf-8 -*-
"""One-off: set the repository description and topics for discoverability.

GitHub matches repository search against the name, description, topics and
README. The name is deliberately unique (`awesome-computed-tomography`), so the
other three channels have to carry the vocabulary the name cannot: "CT",
"reconstruction", "CBCT", "low-dose", ...

Topic selection is driven by *where we can actually be seen*, not by keyword
count. Browsing a topic page lists repositories by stars, so:

  - huge topics are useless to us: `awesome-list` has 15,383 repos and
    `awesome` 11,730 — we would sit dozens of pages in;
  - niche, on-target topics put us on page 1 immediately: `sparse-view-ct`
    (3 repos), `spectral-ct` (3), `dual-energy-ct` (2),
    `metal-artifact-reduction` (6), `scatter-correction` (6), `low-dose-ct` (8),
    `cone-beam-ct` (15), `tomographic-reconstruction` (23), `ct-imaging` (30),
    `ct-reconstruction` (38), `radon-transform` (40), `cbct` (44).

The set below is therefore weighted towards niche/on-target topics, plus the
broad ones that matter for search matching (`computed-tomography` 235,
`ct` 222, `tomography` 313 — `ct` is what the comparable 241-star list uses and
we lacked).

Repo counts were measured on 2026-10-10 via
`gh api "search/repositories?q=topic:<t>&per_page=1" --jq .total_count`.
As of that date the repo has 1 star, so "page 1" means a topic with well under
~100 repositories; anything in the thousands is unreachable by browsing.

Four decisions follow from that data, and are worth keeping:

  - **One topic per acquisition regime**, at the exact spelling people type.
    The list documents seven regimes and each is a niche tag, so each earns a
    slot: `sparse-view-ct`, `limited-angle`, `low-dose-ct`,
    `metal-artifact-reduction`, `cone-beam-ct`/`cbct`, `spectral-ct`, `4d-ct`.
  - **Two spellings were rejected** because they match *zero* repositories:
    `limited-angle-tomography` and `dynamic-ct`. A tag nobody else uses reaches
    nobody; the list's work is filed under `limited-angle` and `4d-ct`.
  - **A near-duplicate was traded for a niche tag.** `medical-image-processing`
    (931 repos, unreachable) sat beside the umbrella `medical-imaging`
    (6,199) saying almost the same thing; that slot now carries `spectral-ct`.
    `ct-scan` (89) went the same way in favour of `ct-imaging` (30), which is
    the more on-target spelling.
  - **`awesome` was dropped, `awesome-list` kept.** The pair used to be
    justified as a requirement of sindresorhus/awesome, which this list no
    longer targets; one ecosystem tag is enough, and `awesome-list` is the one
    people actually browse.

GitHub allows at most 20 topics per repository.

Idempotent: re-running sets the same values and reports whether anything
changed.
"""
import json
import os
import subprocess
import sys

REPO = "cslht11/awesome-computed-tomography"

DESCRIPTION = (
    "A curated list of CT (computed tomography) reconstruction: papers, toolkits, "
    "datasets and benchmarks for sparse-view, limited-angle, low-dose, "
    "metal-artifact, cone-beam (CBCT), spectral and 4D/dynamic CT."
)

TOPICS = [
    # core identity — what the list *is*
    "computed-tomography",            # 235 repos
    "ct",                             # 222
    "tomography",                     # 313
    "ct-reconstruction",              # 38
    "ct-imaging",                     # 30
    # acquisition regimes — one per section of the list, exact spelling, all
    # niche enough that we land on page 1
    "cbct",                           # 44
    "cone-beam-ct",                   # 15
    "sparse-view-ct",                 # 3
    "limited-angle",                  # 1
    "low-dose-ct",                    # 8
    "metal-artifact-reduction",       # 6
    "spectral-ct",                    # 3
    "dual-energy-ct",                 # 2
    "4d-ct",                          # 1
    "scatter-correction",             # 6
    "tomographic-reconstruction",     # 23
    "radon-transform",                # 40
    # method families
    "implicit-neural-representation", # 146
    # audience. Only the umbrella survives: `medical-image-processing` (931)
    # was traded for `spectral-ct`, and `x-ray` (405) is subsumed by the
    # modality tags above.
    "medical-imaging",                # 6,199
    # list discovery. `awesome-list` is the one people browse; the paired
    # `awesome` tag (11,730) was dropped when sindresorhus/awesome stopped
    # being a target.
    "awesome-list",                   # 15,383
]

assert len(TOPICS) <= 20, "GitHub allows at most 20 topics, got %d" % len(TOPICS)
assert len(DESCRIPTION) <= 350, "description too long: %d" % len(DESCRIPTION)


def gh(*args):
    p = subprocess.run(["gh"] + list(args), capture_output=True, text=True)
    if p.returncode != 0:
        print("gh failed:", " ".join(args))
        print(p.stdout.strip())
        print(p.stderr.strip())
        sys.exit(1)
    return p.stdout


def main():
    print("repo       : %s" % REPO)
    print("description: %d chars" % len(DESCRIPTION))
    print("topics     : %d" % len(TOPICS))

    cur = json.loads(gh("api", "repos/" + REPO))
    old_desc = cur.get("description") or ""
    old_topics = cur.get("topics") or []

    changed = False

    if old_desc.strip() == DESCRIPTION:
        print("\ndescription: SKIP (already set)")
    else:
        gh("api", "-X", "PATCH", "repos/" + REPO, "-f", "description=" + DESCRIPTION)
        print("\ndescription: UPDATED")
        changed = True

    if sorted(old_topics) == sorted(TOPICS):
        print("topics     : SKIP (already set)")
    else:
        added = sorted(set(TOPICS) - set(old_topics))
        removed = sorted(set(old_topics) - set(TOPICS))
        args = ["api", "-X", "PUT", "repos/" + REPO + "/topics"]
        for t in TOPICS:
            args += ["-f", "names[]=" + t]
        gh(*args)
        print("topics     : UPDATED")
        if added:
            print("  + %s" % ", ".join(added))
        if removed:
            print("  - %s" % ", ".join(removed))
        changed = True

    # Verify by reading back.
    now = json.loads(gh("api", "repos/" + REPO))
    got = now.get("topics") or []
    print("\n--- read back ---")
    print("description: %s" % (now.get("description") or ""))
    print("topics (%d): %s" % (len(got), ", ".join(sorted(got))))
    assert sorted(got) == sorted(TOPICS), "topic read-back mismatch"
    assert (now.get("description") or "").strip() == DESCRIPTION, "description read-back mismatch"
    print("\nverified OK%s" % (" (changed)" if changed else " (no change needed)"))


if __name__ == "__main__":
    main()
