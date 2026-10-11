# One-off scripts

These are the scripts that built the **first version** of the list. They are kept
for provenance — so that any entry in `data/*.yaml` can be traced back to how it
was discovered and verified — but they are not part of the normal contribution
workflow. Day-to-day changes only need `scripts/build.py`.

| Script | What it did |
| --- | --- |
| `collect.sh` | Batch GitHub code search for candidate toolkits → `toolkits_raw.txt` |
| `verify_core.sh` | Targeted metadata check for the hand-picked core toolkits → `toolkits_core.tsv` |
| `verify.sh` | Same, for every candidate in `toolkits_raw.txt` → `toolkits_meta.tsv` (438 repos) |
| `import_existing.py` | Parsed the pre-existing community CT list into `papers_draft.yaml` and tagged topics by keyword rules |
| `build_supp.py` | Curated the gap-filling entries (metal artifact, 3DGS, INR, CBCT, 4D, diffusion) and resolved each paper link via Crossref, then arXiv |
| `verify_supp.py` | Re-fetched every resolved DOI/arXiv id, compared the returned title with the entry title, and wrote the authoritative `year` / `venue` back |
| `merge_papers.py` | Applied the manual corrections, normalised venues to short labels, de-duplicated draft against supplementary entries, and emitted `data/papers.yaml` |
| `normalize_links.py` | Normalised every paper link to `https://doi.org/...` or `https://arxiv.org/abs/...` — deterministic fixes first (old arXiv FTP URLs, tracking parameters, signed URLs, ResearchGate), then a title-matched Crossref DOI lookup → `link_map.json` |
| `verify_paper_dois.py` | Fetched the authoritative Crossref record behind every DOI, compared the returned title with the entry title (8 flagged, 1 was a genuinely wrong DOI and was fixed), and wrote `year` / `container-title` → `doi_meta.json` |

Two further one-offs patch the generated documentation rather than the data. Both
are probe-guarded and safe to re-run (a second run prints `SKIP`):

| Script | What it did |
| --- | --- |
| `patch_legend.py` | Moved the datasets `note` markers into a rendered legend in `scripts/build.py`, and dropped a lone `**Image domain.**` marker so the convention stays binary |
| `patch_contributing.py` | Documented the projection-domain markers and the `202`-is-OK link-check semantics in `CONTRIBUTING.md` |
| `audit_doi_hosts.py` | Resolved all 112 DOI links and recorded the host each one ends on — this is what caught two NeurIPS entries whose DOI led to a commercial per-paper store instead of the open-access paper |
| `patch_neurips_links.py` | Repointed those two entries (Polyner, R2-Gaussian) at their arXiv records, confirmed by id |
| `patch_rename.py` | Renamed the project to `awesome-computed-tomography` after finding that the original slug was a literal collision with a 241-star list |
| `patch_discoverability.py` | Rewrote the README intro so the scope vocabulary the repo name cannot carry (CT, CBCT, sparse-view, low-dose, …) appears up front |
| `set_repo_metadata.py` | Sets and verifies the repository description and the 20 topics; the topic set is chosen by where we can actually be *seen*, not by keyword count |

## Data files here

- `papers_draft.yaml` — raw parse of the community list (103 entries), before verification.
- `papers_supp.yaml` — supplementary entries with a `_via` / `_sim` audit trail
  recording which source each paper link came from and the title-match score.
- `link_map.json` — old paper URL → canonical DOI/arXiv URL, applied transitively by
  `merge_papers.py`.
- `doi_meta.json` — DOI → authoritative `year` and journal/conference, written back into
  `data/papers.yaml`.
- `link-report.txt` — output of `scripts/check_links.py` over the whole dataset.
- `doi-hosts.txt` — output of `scripts/oneoff/audit_doi_hosts.py`: the final host
  behind every DOI link, plus a histogram, so publisher domains can be told apart
  from resellers and bot-check interstitials.
- `toolkits_raw.txt`, `toolkits_meta.tsv`, `toolkits_core.tsv` — raw GitHub search
  output and the metadata snapshot (stars / language / license / last push) taken
  on 2026-10-09.

## Expansion round (2026-10-10)

A second pass widened the list from 146 to 235 papers by mining the two
comparable CT lists rather than reading the web again. Same rule as the first
pass: **nothing enters `data/` before it has been resolved against Crossref or
arXiv and its title compared.**

| Script | What it does |
| --- | --- |
| `diff_existing.py` | Parses the community list and subtracts our 146 curated titles, leaving a candidate pool (96 rows; 92 unique after de-duplication). Read-only. |
| `verify_candidate_papers.py` | Resolves every candidate through Crossref first (title search) and arXiv second (phrase search, then a keyword fallback). Writes `candidates_papers.json` with a `_via` / `_sim` audit trail per row. 88/92 resolved at ≥ 0.92 similarity; the remaining 4 were resolved by hand. |
| `verify_candidates.py` | The non-paper half: HTTP-checks each candidate toolkit / learning resource, recording the final URL and page title. This is what rejected *Ettention* (last commit 2018). |
| `apply_candidates.py` | Merges `candidates_merged.json` into `data/papers.yaml`. Idempotent, and it **reads back and asserts** the entry count and id uniqueness — without that check a missing `- ` list marker silently folds 89 entries into the preceding block. |

Two corrections are worth recording, because both were found by verification
rather than by reading:

- **A source title can be a journal title, not the arXiv title.** The community
  list calls `arXiv:2203.15725` *"Synergizing Physics/Model-based and Data-driven
  Methods for Low-Dose CT"*, but the paper's actual arXiv title is
  *"Physics-/Model-Based and Data-Driven Methods for Low-Dose CT"*. The API
  lookup fails and the entry looks unresolvable until you read the abstract page.
- **`LoDoPaB-CT` is a dataset paper, not a reconstruction paper.** Its DOI points
  at *Scientific Data*, so it was filed under `data/datasets.yaml` next to the
  dataset it describes.

### Data files from this round

- `candidates.json` — the HTTP check for toolkit / learning candidates.
- `candidates_papers.json` — every candidate with `_via` (crossref / arxiv) and
  `_sim` (title-match score).
- `candidates_merged.json` — the final, topic-tagged blocks that were merged.

## Recent-work round (2026-10-10, second pass)

The first pass left a visible hole: almost nothing in the list was from
2025-2026, because the two community lists it mined had largely stopped being
updated around 2024. For a list whose readers are doing research *now*, that is
the part that matters most, so the second pass goes straight to the source.

| Script | What it does |
| --- | --- |
| `harvest_recent.py` | Queries the arXiv API across 20 facets of CT reconstruction, restricted to `submittedDate:[2025… TO 2026…]` and to `eess.IV` / `cs.CV` / `physics.med-ph`. 349 unique papers. |
| `apply_recent.py` | Relevance-scores the harvest, drops anything already present, routes non-paper entries to `datasets.yaml` / `benchmarks.yaml`, tags topics, and merges with the same read-back assertions. |

**Why arXiv and not a web search:** the arXiv API *is* the source, so the id it
returns can be re-verified later; and `submittedDate` is the only reliable way
to window "the last two years" without scraping date strings off publisher
pages.

### Two scoring traps worth remembering

1. **Abstract-keyword scoring silently discards well-published work.** Ranking
   by keyword density favours long abstracts, so `TG-Field` (AAAI 2026),
   `FaCT-GS` (ECCV 2026), `DIGS` (MICCAI 2025) and `FIND-Net` (MICCAI 2025) all
   fell below a top-64 cut. The fix is a second pass keyed on the *acceptance
   signal* in the arXiv comment (`Accepted to X`), not on the score. 32 further
   papers came from that pass.
2. **A keyword filter is not a scope filter.** The same pass swept up
   `ReBrain` (synthesises **MRI** from CT), `Unsupervised Adaptation of 3D CT
   Foundation Models for 3D CBCT *Segmentation*`, `GEPAR3D` / `SemiTooth`
   (tooth segmentation) and `Top-K MIP Priors for 3D Liver Vessel
   *Segmentation*`. All four are about CT *inputs* but not about
   reconstruction, and were removed by hand. Conversely `GLFC` and the
   CBCT→sCT systematic review were dropped by the filter but belong in.

### Data files from this round

- `recent_candidates.json` — raw arXiv harvest (349 papers).
- `recent_scored.json` — every candidate with its relevance score.
- `recent_extra.json` / `recent_extra_keep.json` / `recent_extra_final.json` —
  the acceptance-signal pass, before and after the hand scope filter.

## Duplicate cleanup (2026-10-10, third pass)

Round 1 did not add a single new paper. It added 88 duplicates, and every count
reported about the list in between was inflated by that much (328 → 240).

**How it happened.** Two independent mistakes lined up:

1. `diff_existing.py` built its "already present" set from `papers_supp.yaml`,
   the hand-curated supplement, instead of `data/papers.yaml`. The 146 entries
   that actually ship were therefore invisible, and ~96 candidates that were
   already in the list were reported as new.
2. `apply_candidates.py` then deduplicated by `id` alone. The existing entries
   use short acronym ids (`lpd`, `dip`, `super`) while candidates were assigned
   slug ids, so almost nothing collided and the duplicates were appended.

Every pair is the same work carrying two link forms — an arXiv preprint and the
journal DOI — so the pairs are invisible to an id check but obvious to a title,
arXiv-id or DOI check.

**Repair and guards.**

| Script | Role |
| --- | --- |
| `find_duplicates.py` | Clusters entries by canonical identity — shared arXiv id, shared DOI, one entry's DOI equal to the other's `<arxiv:doi>`, or identical title *and* year. Read-only. |
| `dedup_papers.py` | Applies the plan: keeps the entry that exists in `git HEAD` so ids and curated wording survive, folds `code` / `project` / `venue` from the dropped copy when the keeper lacks them, and asserts read-back uniqueness. |
| `verify_dedup.py` | Proves the pass was surgical: survivor order preserved, all 88 removals have a surviving twin, 230 of 241 blocks byte-identical. |
| `audit_arxiv.py` | Re-checks every arXiv id at 4 s intervals and pairs the answer to the query by `<id>`, not by position. |
| `audit_years.py` | Compares every `year` against arXiv's `<published>` and `<arxiv:journal_ref>`. |

Two guardrails were added so this cannot return:

- `build.py` now fails on a duplicate title, arXiv id or DOI, so CI catches it.
  Run against the pre-fix file it reports 165 problems; on the current file, none.
- `diff_existing.py` reads `data/papers.yaml`, and `apply_candidates.py` rejects
  a candidate whose title, arXiv id or DOI is already present.

**What the audits turned up beyond the duplication.** Five years were earlier
than the preprint they cite, which is impossible. Four came from reading the
`YYMM` of an arXiv id as a year (`2008.02839` → "2008", true year 2020;
`2012.04743` → "2012", true year 2020). The fifth, `dgr-2`, had inherited both
its year (2025) and its venue (ICCV) from the unrelated ICCV-2025 paper whose
short id it collided with; `<arxiv:journal_ref>` identifies it correctly as
*Biomedical Signal Processing and Control* 75 (2022). The JORSC review was
likewise 2020, not 2017. All five are corrected.

### Data files from this round

- `papers_pre_dedup.yaml` — snapshot before the pass, kept for `verify_dedup.py`.
- `duplicates-report.txt` / `dedup-plan.txt` / `year-audit.txt` / `arxiv-audit.txt`.
- `arxiv-meta.json` — cached arXiv metadata (title, doi, journal_ref, year) for
  all 130 linked ids, so re-runs cost nothing.

## Venue normalisation (2026-10-10, fourth pass)

The list had been accumulating venue strings free-form, so the same venue appeared
under several spellings and a few entries carried a *preprint server* in the venue
field. `normalize_venues.py` collapses this: `85 distinct strings -> 70`, and
entries with a venue `170 -> 174`.

What it does, in order:

1. **Repair truncations.** Several strings had been cut at the source's length
   limit: `the Journal of Machine Learning for Biomedical Imaging (MELB` → `MELBA`,
   `the 2025 IEEE International Conference on Image Processing (` → `ICIP`,
   `the IEEE Transactions on Radiation and Plasma Medical Scienc` → `TRPMS`.
2. **Undo HTML entities.** `Physics in Medicine &amp` → `PMB`.
3. **Merge synonyms.** `IEEE Transactions on Medical Imaging` (1 entry) folded into
   `TMI` (37); three SPIE *Medical Imaging* entries and `wavresnet` (whose source
   scraped a SPIE proceedings as its venue) folded into `SPIE MI`.
4. **Drop redundant years inside the venue.** `AAAI 2026 (**AAAI 2026**, 2026)` →
   `AAAI` — `build.py` renders `(venue, year)` and the year is a separate field, so
   repeating it printed twice.
5. **Remove preprint servers.** `arXiv` ×5 and `TechRxiv` ×1 are not venues; the
   field was deleted rather than faked.
6. **Fill 11 missing venues** where the source carried one that had been lost
   (CGF, CVPR ×2, PMB ×2, TRPMS, TCI, `J. Phys. Soc. Jpn.`, Digital, IEEE SPM).

`set_venue()` had to be able to **insert** a `venue:` line, not just rewrite one —
the first version only did the latter and silently wrote the file back unchanged
for the 11 entries that needed an insert (the assert fired only *after* the write,
so the file had already been clobbered). It is now backed by
`papers_pre_venue.yaml`, which is why that snapshot exists.

### Three venues recovered by DOI, not by search

The 14 weakest entries (pre-2025, no venue, no code) were checked against Crossref
one DOI at a time via `query.bibliographic`. That endpoint is **not** trustworthy
at low similarity — 0.68 "matched" a completely different paper — so every hit was
re-read by DOI. Only three survived, and they are the three whose local title
matched the DOI's real title at ≥0.93:

| entry | DOI | venue | year |
|---|---|---|---|
| `epi-naf` | `10.1109/isbi60581.2025.10981301` | ISBI | 2025 |
| `generative-modeling-in-sinogram-domain-for-sparse-view-ct-` | `10.1109/trpms.2023.3309474` | TRPMS | 2024 |
| `cocodiff-a-contextual-conditional-diffusion-model-for-low-` | `10.1117/12.2634939` | SPIE DXRT | 2022 |

Two of them also carried a **wrong year** that only the DOI check exposed:
`cocodiff` was listed as 2024 but the SPIE proceedings is 2022 (the arXiv search
confirms no CT paper named CoCoDiff exists, so the local entry is that SPIE paper),
and `generative-modeling-in-sinogram` was listed as 2022 (its arXiv posting) when
the TRPMS issue is 2024.

Three candidates were **rejected** after reading the DOI's real title: `diffmed`,
`learned-convex-regularizers-for-inverse-problems` and `baggagect` all "matched" a
different work. They stay venue-less and are recorded in `VERIFIED_LATER` /
`NOT_A_MATCH` at the top of `normalize_venues.py` so nobody re-investigates them.

### Data files from this round

- `papers_pre_venue.yaml` (md5 `a328e67f7421a0e7c92c7fb27f22bf47`) — before pass 4.
- `papers_pre_venue3.yaml` (md5 `9146e1be85812b4a181cdadb309c9168`) — after pass 4,
  before the three DOI-backed fills.
- `venue-plan.txt` / `year-audit.txt` / `venue3-verify.json`.

## Re-running

These scripts hit the network (GitHub API, Crossref, arXiv) and are rate-limited
by design. If you re-run them, expect minutes, not seconds.

```bash
pip install -r requirements.txt
python scripts/oneoff/import_existing.py
python scripts/oneoff/build_supp.py
python scripts/oneoff/verify_supp.py
python scripts/oneoff/merge_papers.py        # writes data/papers.yaml
python scripts/oneoff/normalize_links.py     # writes link_map.json
python scripts/oneoff/verify_paper_dois.py   # writes doi_meta.json
python scripts/oneoff/merge_papers.py        # re-apply link_map + doi_meta
python scripts/build.py
python scripts/check_links.py                # writes link-report.txt
```

Expansion rounds only (safe to re-run; already-applied entries are skipped):

```bash
# round 1 — mine the comparable community lists
python scripts/oneoff/diff_existing.py                # dry run, prints candidates
python scripts/oneoff/verify_candidate_papers.py      # -> candidates_papers.json
python scripts/oneoff/verify_candidates.py            # -> candidates.json
python scripts/oneoff/apply_candidates.py             # dry run
python scripts/oneoff/apply_candidates.py --write     # merges + asserts

# round 2 — harvest the 2025-2026 frontier from arXiv
python scripts/oneoff/harvest_recent.py               # -> recent_candidates.json
python scripts/oneoff/apply_recent.py                 # dry run
python scripts/oneoff/apply_recent.py --write         # merges + asserts

# integrity passes (read-only unless noted)
python scripts/oneoff/audit_arxiv.py --min 0.60       # every arXiv id re-resolved
python scripts/oneoff/audit_years.py                  # years vs arXiv metadata
python scripts/oneoff/find_duplicates.py              # -> duplicates-report.txt
python scripts/oneoff/dedup_papers.py --write         # apply; then verify:
python scripts/oneoff/verify_dedup.py

# round 4 — venue normalisation + DOI-backed venue recovery
python scripts/oneoff/normalize_venues.py             # dry run -> venue-plan.txt
python scripts/oneoff/normalize_venues.py --write     # apply
python scripts/oneoff/verify_venue3.py                # re-check the 3 DOIs at Crossref
python scripts/oneoff/apply_venue3.py                 # apply the 3 verified venues

python scripts/build.py
```
