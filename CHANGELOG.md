# Changelog

All notable changes to this list are recorded here, newest first, **dated rather than
versioned**.

This project does **not** tag releases. The list is a curated dataset that is refined
continuously — entries added, venues corrected, links repaired — so there is no point
at which it is "finished" and no boundary a version number could mark. To cite a fixed
snapshot, use a commit hash or `main` as of a date.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) in spirit,
with dates in place of version numbers. The stable public contract is the pair of `id`
fields — topic ids in `data/meta.yaml` and entry ids in `data/*.yaml`. Anything else
may be reformatted at any time.

## 2026-10-12 — Search, sorting and language-switch fixes

### Fixed

- **An arXiv id typed into the search box no longer jumps to the wrong page.**
  Toolkit, dataset, benchmark and learning records indexed their whole URL, so
  every number inside it became a searchable token and an id matched an
  unrelated record. They now index the host only, which is what the code always
  said it did. The bare arXiv id is indexed separately — 151 of the papers link
  to one — so searching `2607.14415` finds `$K$-NeAS`, the paper it belongs to,
  instead of a dataset whose URL happens to contain `2607`.
- **Enter needs a real hit before it navigates.** With no paper match, Enter
  opened the top-ranked result however weak it was. It now opens only at a
  score of 2 or more, which is what a name or metadata hit earns; a lone weak
  body hit (~0.7) filters the list instead, so a stray keystroke cannot send
  someone off-site.
- **Title sort no longer files `$K$-NeAS` first.** The sort used the raw title,
  and `$` sorts ahead of every digit and letter; it now sorts on the title as
  displayed, with the inline TeX delimiters stripped. The comparator also
  returns 0 for equal keys, which a `-1/1`-only comparator never did.
- **The year filter's "and later" label is translated.** It was built as a
  hardcoded English string; it now reads the existing `yearAndLater` key, which
  the Chinese overlay already provides.
- **Switching language keeps the filters.** The switch links are written at
  build time and carry no query string, so `/zh/?tab=datasets&q=…` lost every
  filter on switching. `web/lang.js` appends the current query once at load;
  both templates load it.

### Docs

- `SITE.md` still described the search as "filters as you type … multiple words
  are AND-ed", which stopped being true when ranking replaced the strict AND.
  It now describes the dropdown-then-Enter behaviour and why Enter has a
  threshold.

## 2026-10-12 — Corrected two challenge descriptions and two dataset records

### Fixed

- **AAPM DL-Sparse-View CT Challenge** (and its dataset entry): the challenge is
  the 2021 one, not 2022, and it asks for recovery of simulated 2D breast-CT
  phantoms from ideal noiseless **128-view** fan-beam data (4,000 training pairs,
  100 test cases). The earlier text described a 2/4/8/16/32/64-view re-projection
  of the 2016 clinical cohort, which is not what the challenge provides. Dataset
  modality and licence now follow the AAPM page and the Zenodo record
  (CC BY 4.0).
- **Helsinki Tomography Challenge 2022**: the winner was a purely learned
  network trained on synthetic data; the only model-based entry (CIL) placed
  third. The note had this the wrong way round.
- **LDCT-and-Projection-data** licence: TCIA version 7 opened the chest and
  abdomen scans under CC BY 4.0; the head scans stay under NIH controlled access.
  It was recorded as CC BY-NC 4.0.

## 2026-10-12 — Three CT foundation models, and the CT-RATE dataset

### Added

- **TAMP**, **DeepSparse** and **LCTfound.** Each was resolved against Crossref
  before being written down — title match 1.000 for all three — rather than
  taken from the PDF it was harvested from, because the markdown those PDFs
  produce carries the arXiv ids of the *references*, not of the paper itself.
  TAMP (Nat Commun 2026) covers low-dose, sparse-view and limited-angle in one
  backbone; DeepSparse (TMI 2026) is the sparse-view CBCT one; LCTfound
  (Nat Commun 2025) spans eight tasks of which CT enhancement and sparse-view
  reconstruction are the reconstruction-relevant ones.
- **CT-RATE**, in the image-domain half of the datasets: 50,188 reconstructed
  3D chest CT volumes with a paired radiology report each. It gets no
  projection marker — there are no raw sinograms — which is worth knowing before
  reaching for it to test a forward model. Its landing page does not state a
  licence, so it is recorded as `see source` rather than guessed at.
- `scripts/oneoff/verify_foundation_papers.py` and its output, so the batch's
  provenance sits in the repository beside the entries it produced.

### Fixed

- **HorusEye had no code link.** Its repository is now recorded.

### Deliberately left out

Three papers came out of the same batch and were **not** added: CT-RATE's own
paper (CT-CLIP / CT-CHAT), Merlin and TAP-CT. All three are CT foundation
models, but what they contribute is vision-language retrieval, report
generation and frozen-feature classification — not reconstruction. The bar in
`MAINTENANCE.md` is a paper *on CT reconstruction*, and a reader who came here
for reconstruction methods would find them noise. Recorded here rather than
quietly dropped.

## 2026-10-12 — The contributor graph is cslht11-only again

### Fixed (attribution)

- **A merged Dependabot pull request put `dependabot[bot]` in the contributor
  graph.** Squash-merging attributes the new commit to the pull request's author,
  so `main` picked up a commit authored by `dependabot[bot]` — ranked second, with
  one commit, next to cslht11's fourteen. The commit is rewritten as a cslht11
  commit; the change it carried (the PyYAML floor) is kept exactly as it was.
- **`.github/dependabot.yml` is deleted.** A `refs/pull/N/head` ref cannot be
  removed — the API answers `refs/pull/* is read-only` (HTTP 422) — so from the
  moment Dependabot opens a pull request its author is in that graph for good,
  whether the pull request is merged, closed or left open. There is no setting
  that scopes the graph to one author. Version bumps are applied by hand as
  cslht11 commits from here on. Dependabot **security alerts** are a separate
  setting that needs no configuration file, and stay on.

### Added (authorship guards)

- **`hooks/` and `scripts/install-hooks.sh`.** The two guards that keep this from
  happening again lived only in one clone's `.git/hooks/`, which is to say they were
  one recloning away from not existing. Both are now in the repository and installed
  by one command, which the repository map now says to run after a clone.
  - `hooks/pre-commit` — refuses a commit whose `user.email` is not cslht11's.
  - `hooks/pre-push` — refuses any push containing a commit not authored by cslht11.
    This is the one that would have stopped `dependabot[bot]`: squash-merging signs
    with the pull request author's identity, which local `git config` never sees, so
    no `pre-commit` hook can catch it.

## 2026-10-12 — Licences made precise, structure written down, payload 16% smaller

### Fixed (licensing)

- **The content/code boundary was wrong in two places.** `LICENSE-content` listed
  `site/` as content, but the build copies `web/*.js` and `web/*.css` into it
  verbatim — so the same bytes were claimed under both licences. It also missed
  `data/i18n/*.yaml` entirely (`data/*.yaml` does not match a subdirectory), which is
  where all the translated prose lives. Both files now list their paths explicitly,
  including the `site/*.js` and `site/*.css` carve-out.
- `MAINTENANCE.md` explains **why the code is not under the same licence as the
  content** — CC advises against its licences for software: they say nothing about
  patents or about source versus object form, NonCommercial is not an open-source
  licence (the OSI and the DFSG both reject it), and ShareAlike is viral over code.
  The consequence of NC is stated plainly too, rather than left implied.

### Added (structure)

- **A repository map in `MAINTENANCE.md`** — every directory and file, plus a
  "to change X, edit Y, then run Z" table. Written for someone arriving with no
  context, which is what the file is for.
- **`tests/`, in the repository.** The search tests lived in a private ops
  directory; a test that is not next to the code it tests is a test that rots.
  `tests/test_search.js` needs no packages and now runs in `validate.yml` after the
  site build; `tests/test_site_dom.js` drives the real pages in jsdom and stays a
  local pre-push check on purpose — a workflow that can go red because a registry
  was unreachable teaches people to ignore red, which is the argument `SITE.md`
  already makes for keeping the deploy workflow off pull requests.

### Changed (maintenance)

- **GitHub Actions brought up to current majors**: `checkout` v4 → v7,
  `setup-python` v5 → v7, `upload-pages-artifact` v3 → v5, `deploy-pages` v4 → v5.
  The deploy log had been warning that `deploy-pages@v4` still targets Node 20.
- `requirements.txt` pins PyYAML to `>=6.0.3,<7`. The floor is the first 6.x with
  the patched loader; the ceiling keeps a major bump a deliberate change with the
  tests run, not something CI picks up overnight.

### Changed (payload)

- **The `_q` search blob is gone** (payload schema 1 → 2). It was a lower-cased
  concatenation of title, abbreviation, venue, topic names, note and link hosts,
  shipped so the client could substring-match one string. `web/search.js` builds a
  weighted index in the browser from the structured fields instead, so the blob was
  duplicated content with no remaining reader — ~68,000 characters of it.
  `index.html` 541 KB → **472 KB**, `data.json` 263 KB → **192 KB**, the whole site
  868 KB → **727 KB**, and one less derived field to keep in sync.

## 2026-10-12 — The site's search actually works now, and stops throwing

Two name collisions were breaking the site's JavaScript. Both were pre-existing, both were
invisible in the served HTML (which is server-rendered), and together they explain why the
search box did nothing.

- **`renderPapers` declared `var t = titleParts(p)`**, shadowing the i18n helper `t()` used
  a few lines below it. The resulting `TypeError` fired on every render, which aborted
  `init()` before it wired the search box — so typing in the filter never did anything.
- **`renderToolkits` used `function (t)` as its `map` callback**, the same collision, and it
  threw for the 14 toolkits that carry a `homepage`.
- **The top-bar box declared `var t` for its debounce timer**, shadowing its own `t()`: the
  first keystroke turned `t` into a timer id, and the next render threw. The dropdown now
  survives more than one keypress.
- `debounce` and the `/`-to-focus handler had the same shadowing shape without calling
  `t()`, so they worked by luck; both were renamed while fixing the others.

### Added: a real search core (`web/search.js`)

The old search was a case-insensitive substring test over one flat blob, with strict AND
semantics and no ranking — so a query had to be an exact substring, one extra word emptied
the list, and results kept whatever order the data was in.

- **CJK tokenising.** Chinese is not space-separated, so a run of ideographs is indexed as
  both its characters and its adjacent pairs: 「稀疏视角」 becomes 稀 疏 视 角 + 稀疏 疏视
  视角. 「稀疏重建」 now finds a record titled 「稀疏视角 … 重建」 even though the user's two
  words never sit next to each other.
- **Field weighting.** One weighted token map per record (title 5, abbreviation 4, metadata
  2, everything else 1), keeping the highest weight per token, so a title hit outranks the
  same word buried in a note.
- **Ranking.** Token weights scaled by query coverage, plus a bonus for the query appearing
  verbatim. Records matching nothing are dropped, but a partial match is no longer thrown
  away: ranking is a stable sort applied after the user's own sort, so ties keep the order
  they chose.
- **Substring fallback for Latin tokens.** Exact token equality would lose "mamba" →
  DenoMamba and "splat" → Splatting, which the old substring search did find, so a query
  token with no exact key falls back to index keys containing it, at a discount.
- **Highlighting everywhere it matters** — results, the dropdown, and the topic line of each
  paper row (a Chinese query usually matches the topic, not the English title, so without
  that the results would look like nothing had matched).
- **The top-bar box searches all five sections**, not just papers, and Enter now filters the
  paper list only when the query actually found papers; otherwise it opens the best match.
- Verified by two test suites (54 assertions on the core, 23 driving the built pages in
  jsdom), including that a render throws nowhere — the check that would have caught the
  collisions above.

### Changed

- **No web font, and said so.** The system UI face plus the platform's own CJK family is
  faster and better-looking here, and it keeps the page free of third-party requests and of
  any font-licence question. The stack gained `system-ui` and a fuller CJK fallback chain so
  macOS, Windows and Linux agree; the decision is documented where it is made.
- The LoDoPaB-CT paper title no longer repeats "(Scientific Data)" — its venue already says it.

## 2026-10-12 — Three external audits worked through, and the contributor list cleaned up

Three independent audits of the repository — data, i18n, links, CI, docs — were checked
finding by finding rather than applied wholesale. Every repair was re-derived from
Crossref, the publisher's record or the project's own primary source before it was made;
several audit claims turned out to be wrong and were dropped or narrowed (see below).

### Fixed (paper and dataset records)

- **Four wrong years or venues**, each confirmed against the record at the DOI:
  LoDoPaB-CT 2017 → **2021** (Scientific Data), MAP-NN 2021 → **2019** (Nat Mach Intell),
  DL-PICCS 2019 → **2021** (Med Phys), DREAM-Net TMI 2022 → **JBHI 2023** — a mistake the
  DOI's own prefix, `10.1109/jbhi...`, already contradicted. DenoMamba 2025 → **2026**,
  following the volume/issue convention the other IEEE entries use.
- **LoDoPaB-CT's title carried leftover markdown** (`(**Scientific Data**) -->`) from a
  link removed by hand, and `FSTensor`'s title was missing its separator
  ("FSTensorFull-spectrum…", now "FSTensor: Full-spectrum…").
- **Two duplicate pairs removed**, keeping the peer-reviewed record in each case:
  CasRedSCAN's 2020 preprint against its TMI 2021 paper, and the CAIP 2025 registration
  paper against its earlier workshop-titled arXiv posting. Papers 391 → 389.
- **Dataset facts corrected against the primary sources.** LDCT-and-Projection-data
  claimed "four dose levels (full / quarter / 10% / 5%)"; the challenge released routine
  dose plus *one* simulated reduction, and TCIA states 25% for head/abdomen and 10% for
  chest. VerSe claimed "3,741 CT/CBCT spine scans" — it is **374 CT scans from 355
  patients**, with no CBCT. Medical Segmentation Decathlon has **six** CT tasks, not four.
  KiTS23 has **599** scans (489 train + 110 test), not 489 across "three editions".
  RibFrac's two numbers were **swapped**: 660 scans carrying ~5,000 annotations. STOIC 2021
  is **10,735 French first-wave** scans, not "23,000+ multi-centre". LUNGx is a diagnostic
  classification task, not nodule detection. CHAOS's CT is portal-venous contrast, not
  low-dose. AutoPET ran **four** editions by 2025, not three.
- **`sigpy` ships no Radon primitives** and **RadIO is not a Radon/FBP package** — both
  notes now describe what the code actually contains. **LEAP**'s expansion was invented
  (it is LivermorE AI Projector for Computed Tomography). **libcbct** is CC BY-NC-SA 4.0,
  which GitHub's API reports as "Other". **CBCT Scatter Correction Tool** has no source in
  its repository — it ships a Windows executable — so it no longer claims a language.
- **Two splat-based CBCT metal-artifact papers were kept, not merged.** Both exist and
  both are peer-reviewed (CVPR 2026 and Computer Graphics Forum 45(2) 2026, same group);
  each now carries a note saying so, so the near-identical titles read as a pair rather
  than as a duplication error.
- **`generative-modeling-in-sinogram-domain`** now links its published TRPMS DOI
  (10.1109/trpms.2023.3309474) instead of the arXiv posting, and two Transformer papers
  and two purely-learned papers lost topic tags that did not describe them.
- **Chinese strings**: the typo 高斯泼澅 fixed and the three competing renderings of
  "Gaussian splatting" unified.

### Fixed (build and rendering)

- **`paper_head()` treated any title that merely *started* with the abbreviation as a
  prefix match**, so an abbreviation like "A" would have mangled "A benchmark …". It now
  requires the abbreviation to *be* the first token, and drops an abbreviation repeated in
  trailing parentheses. `web/app.js` mirrors both rules and the two implementations
  cross-reference each other so they cannot drift.
- **The dataset marker stripper only recognised the English full stop**, so the Chinese
  ToothFairy2 note — which had translated the marker itself — printed the sentence in both
  the Data and the Description column. The marker stays English now, as everywhere else.
- **A row can be renamed by an overlay**, not only have its note translated. That is what
  `learning."CT Principles and Algorithms".name` was for, and the key had been silently
  dead; the site payload keeps the English name as its stable key and carries the
  translation as `label`.
- **`tableDescription` sat in the `readme:` section but is read through `ov.ui()`**, so it
  could never be found and the Chinese README printed the English header "Description".
  Moved into `ui:` in both language files, together with ten `readme:` keys that reach
  neither README nor site — two of which were actively misleading: `licenseBody1` stated
  CC BY 4.0 with commercial reuse (the licence is CC BY-NC-SA 4.0) and `contributing*`
  linked to CONTRIBUTING.md, deleted on 2026-10-10.
- **The README's site URL is no longer hardcoded.** `build.py` reads the origin from
  `site.config.yml`, the single place the docs promise it lives, so a domain change can
  no longer leave the README badge pointing at the old address.
- **`new entry` label created.** The issue form referenced it, but it did not exist —
  GitHub drops an unknown label silently, so suggestions arrived unlabelled.

### Changed

- **Journal venue strings unified**: the `IEEE ` prefix dropped from TNS, TIT, TSP, SPM
  and JSAIT to match the bare abbreviations used everywhere else (IEEE Access keeps it,
  being the journal's actual name), and `MedIA` → `Med Image Anal`.
- **Chinese terminology unified** (同行评审, 工具包, 出版方), plus wording corrections:
  "on-board imaging" is 机载成像 rather than 在轨成像, "beam hardening" is 射束硬化
  throughout, and `topics.diffusion` is described as covering generative priors generally
  — which its own name ("Diffusion & Generative Priors") already claimed.
- Three Chinese-language books and the XDesign entry now link or describe what the source
  actually is: two books gained their publisher's page, the 1992 one is documented as
  having no publisher page (so it links a title search), the Kak & Slaney note says
  "chapter PDFs" rather than "Free PDF", and XDesign is described as the phantom and
  acquisition-simulation package its README documents, not as "Differentiable".
- `validate.yml` gained `permissions: contents: read`; `check_links.py`'s disabled
  certificate check is now documented and justified rather than silent.
- Corrected **SITE.md**'s description of what CI does: the README-freshness guard lives in
  `validate.yml` and runs on pull requests too, while `deploy.yml` runs only on pushes to
  `main`. The two same-day `2026-10-10` entries were given distinct titles.

### Not changed, deliberately

- **The workshop venues** ("SC Workshops", "NeurIPS Workshop", "Off-Grid Workshop") are
  three different workshops, not three spellings of one; forcing a single string would
  lose information.
- **The 17 truncated `id`s** (e.g. `…-for-low-`) stay as they are: `id` is the permanent
  `/p/<id>` key, so the generator was fixed instead of the data.
- **`oneoff/`'s 2.2 MB of harvested JSON** stays: it is the provenance record that lets
  every entry be traced back to how it was found, and `check_links.py` still writes into
  it.

## 2026-10-11 — 102 more papers, the whole list in Chinese, and a new home

The largest single addition so far. The list moves to a repository of its own and
becomes bilingual end to end.

### Content

- **391 papers** (was 289), spanning **1917–2026** (was 1976) across 17 topics, plus
  **44 toolkits** (was 43), **40 datasets** (was 34), 19 benchmarks/challenges and
  29 learning resources. **328 of 391 (84%)** carry a peer-reviewed venue.
- **Radon 1917** added: the paper that introduces the transform every analytic
  method here inverts, published 54 years before the first CT scanner. No DOI
  exists for the original, so the entry links P. C. Parks's English translation
  in IEEE TMI (1986) and records the original Leipzig imprint as its venue.
- 57 papers added from a Web of Science export, kept only where Crossref confirmed a
  journal article and the work is a reconstruction method rather than an application
  that merely uses CT. A further 44 came from cross-checking a review manuscript's
  bibliography.

### Language

- The list, the site chrome, the static pages and both READMEs now exist in English
  and Chinese. Interface strings live in `data/i18n/`; English is the source of truth
  and every other language is an overlay that falls back to it.
- `/zh/` serves the Chinese site, with its own canonical URL, `hreflang` pair and
  sitemap entries.

### Site

- **`description` is now filled in at build time.** It used to spell out "289 papers",
  which went stale the moment a paper was added — and this is the text search engines
  show.
- Fixed the light/dark toggle: it had one listener in `app.js` and another in
  `chrome.js`, so a click switched the theme twice. It now lives in one inline script
  in `<head>`, applies the saved choice before first paint, and the button shows the
  icon for the theme it will switch to.
- The EN / 中文 switch moves from the footer to the header, next to the theme toggle.
- The site is served from `computedtomography.org`, now published from this repository.
- **Entry notes now translate.** The 132 notes (and the Radon entry's) were rendered
  in English on the Chinese site even where a translation existed, because the site
  export read the English field directly and never consulted the overlay. Each
  language now builds its own payload, and `build_site.py` fails if a translated
  note does not reach that language's `data.json`.

## 2026-10-10 — Static pages, a non-commercial content licence, and no more pull requests

### Added (About, Contact and Privacy pages)

- New static pages at `/about/`, `/contact/` and `/privacy/` (scope and verification method, how to suggest or correct an entry, what the site does and doesn't collect).
- Compact footer on every page linking to them; licence line kept.
- `build_site.py` renders the pages from `web/pages/` and adds them to the sitemap.

### Changed (maintenance)

- The list is maintained by its authors only and no longer takes pull requests.
  `CONTRIBUTING.md` and the pull-request template are gone. The entry schemas and
  verification rules now live in `MAINTENANCE.md#adding-entries`. Suggestions come
  in as issues or by email.

### Changed (licence)

- **Content is now CC BY-NC-SA 4.0** (was CC BY 4.0); code stays MIT. The
  maintainers want the list credited, kept non-commercial, and adaptations shared
  alike. `LICENSE-content` holds the full, unmodified legal code. Not retroactive:
  copies received earlier under CC BY 4.0 keep that licence.
- Contact address added to the README and the site footer: heitieya@163.com.

**The list is now online at <https://computedtomography.org/>**, and the site
republishes on every push to `main`.

## 2026-10-10 — First public release

First public state. The list is stable enough to cite.

### Contents

- **289 papers** spanning **1976–2026** across **17 topics**, plus **43 toolkits**,
  **34 datasets**, **19 benchmarks/challenges** and **29 learning resources**.
- Every paper link was resolved against Crossref, arXiv or the publisher's own record,
  and every URL was checked.
- **226 of 289 papers (78%)** carry a peer-reviewed venue. Entries without one render
  as `preprint year` in italics, so the reviewed/unreviewed split is visible in the
  README itself rather than left for the reader to guess.

### Added

- **The foundational papers of the three thinnest sections.** Spectral, scatter and
  dynamic/4D held 6, 6 and 9 entries while other sections held 45–62, because they
  were missing the works the sub-fields are built on rather than because little
  exists. 17 papers recovered, taking them to 12, 11 and 15: Alvarez & Macovski 1976
  (the founding spectral-CT paper), Roessl & Proksa 2007 and Schlomka 2008
  (photon-counting K-edge imaging), Elbakri & Fessler 2002 and De Man 2001
  (polyenergetic statistical reconstruction), Siewerdsen & Jaffray 2001 and
  Zhu 2006 (the CBCT scatter references), Sonke 2005 (the founding 4D-CBCT paper),
  Chen 2008 (PICCS), Leng 2008, Rit 2009, Bergner 2010 and Gao 2012.
- The 2025–2026 frontier: 94 entries, weighted towards diffusion priors, Gaussian
  splatting, implicit neural representations and dynamic/4D CBCT.
- `MAINTENANCE.md`, this changelog, an `.editorconfig`, and issue/PR templates.
- **The website source, which renders this same corpus as a searchable single page.**
  `web/` (template, stylesheet, client script), `site.config.yml` (title and the single
  `url` that every absolute address is derived from) and `scripts/build_site.py` produce
  a `site/` directory; `scripts/export_site_data.py` produces the JSON payload on its own
  for anything that wants the data programmatically. The build reads `data/*.yaml` and
  calls `build.py`'s own validator, so the page and the README cannot disagree, and it
  adds no dependencies. `site/` is git-ignored and regenerated.

  It is **deployed**: <https://computedtomography.org/>, published by
  `.github/workflows/deploy.yml` on every push to `main`. That workflow deliberately began
  as manual-only — `actions/deploy-pages` fails while Pages is switched off, and a
  workflow that goes red for reasons unrelated to the change under review teaches people
  to ignore red — and the push trigger was added once Pages was enabled. `SITE.md`
  documents the file map, the four Settings-side steps to reproduce the setup, the DNS
  records, the one-line domain switch, and the failure modes seen while writing it.
  `CONTRIBUTING.md` and `MAINTENANCE.md` pointed at it when it was written;
  `CONTRIBUTING.md` was dropped the same day and the README does not link it, so in
  practice `MAINTENANCE.md` is the surviving entry point.

- **The page itself: a hero, six stat tiles and a framed finder panel.** The stat tiles
  read from the same counts as the README coverage line (`{{N_PAPERS}}`, `{{PEER_PCT}}`,
  …) rather than hardcoding numbers, so they cannot drift from `data/`. `data-goto` links
  on the tiles and the hero buttons switch to the matching tab; with JavaScript off they
  degrade to plain `#tabs` / `#q` anchors.
- **A second harvest pass: 32 papers recovered from a cross-check against two private
  papernotes collections.** The two files held 43 works between them (39 ∪ 34, 30 in
  common); 10 were already on the list and 33 were new. 32 are added — the 33rd, a pure
  learning-theory paper that carries no paper link, was left out as out of scope. The
  additions are weighted to the newest venues (CVPR / ICCV / ECCV / ICLR / ICML /
  NeurIPS / AAAI / ICASSP 2024–2026, plus one journal) because that is where the
  collections were densest.
- **Four entries carry a `paper` link that is neither an arXiv id nor a DOI** — the
  first in the list to do so. Three CVPR 2026 papers (`CryoDeRec`, `Exact-GS`,
  `GH-NAF`) have no arXiv posting and no registered DOI, so they link to their CVF
  OpenAccess page; `MedGMAE` (ICLR 2026) links to its OpenReview forum. Each was
  verified against the page's own `citation_title` metadata or the conference's own
  listing, and the coverage line in the README now says so rather than claiming every
  link came from Crossref or arXiv.

### Fixed

- **`scatter-rev` pointed at the wrong half of a pair.** The entry carried Part 1's
  title but Part 2's DOI (`10.1118/1.3589140`), so the link led to a different paper
  than the title promised. Both parts are now present and each points at its own DOI;
  the two subtitles ("Scatter compensation approaches" / "Scatter estimation
  approaches") are in the titles so the pair can be told apart.
- **Removed 88 duplicate entries.** A harvesting pass had appended papers that were
  already on the list, under a different `id`: existing entries use short abbreviation
  ids (`lpd`, `dip`, `super`), harvested ones use title slugs, so the two never
  collided and duplicate detection — which compared `id` — saw nothing wrong. Detection
  now uses a canonical identity (arXiv id, DOI, or normalised title plus year), and
  `build.py` fails CI when the same work appears twice.
- **Normalised venue strings**: 85 distinct spellings collapsed to 70. This repaired
  strings truncated at their source (`the Journal of Machine Learning for Biomedical
  Imaging (MELB` → `MELBA`), an unescaped HTML entity (`Physics in Medicine &amp` →
  `PMB`), synonym splits (`IEEE Transactions on Medical Imaging` vs `TMI`), years
  duplicated inside the venue (which the generated README printed twice), and six
  entries that carried a preprint server (`arXiv`, `TechRxiv`) where a venue belongs.
- **Corrected years** that had recorded the arXiv posting year instead of the year at
  the venue, and one entry whose year and venue had been inherited from an unrelated
  paper that happened to share its short id.
- Recovered 14 missing venues: 11 from the source records, and 3 more — `Epi-NAF` →
  ISBI 2025, `Generative Modeling in Sinogram Domain` → TRPMS 2024, `CoCoDiff` →
  SPIE 2022 — by checking candidate DOIs one at a time in Crossref. Two of those also
  exposed a wrong year that no title-based check would have caught.
- Fixed 8 dead table-of-contents links and a broken badge.
- **Two wrong venues and one imprecise one, all inherited from the source notes.**
  `Regularizing INR with Diffusion Prior … Neutron CT` was recorded as CVPR 2025 — it
  is **ICASSP 2026** (`10.1109/ICASSP55912.2026.11464479`, pp. 21947–21951, Barcelona);
  `Variational Garrote for Sparse Inverse Problems` was recorded as CVPR 2025 — it is
  **Journal of Computational Science** 2026, vol. 100, art. 102980
  (`10.1016/j.jocs.2026.102980`). `Modeling X-ray Photon Pile-up with a Normalizing
  Flow` was recorded as NeurIPS 2025, which is not wrong — it is the **NeurIPS 2025
  ML4PS workshop**, so only the precision needed fixing.

  The two CVPR claims were not simply overruled by a better source; the "a conference
  version came first, a journal version later" reading was ruled out explicitly, since
  that would have made the notes right rather than wrong. No CVPR record exists for
  either paper anywhere: not in the CVPR 2025 main proceedings (2,871 papers), not in
  any of that year's 52 CVF workshop volumes, and likewise nothing in CVPR 2026
  (4,042 papers / 86 workshop volumes) or ICCV 2025 (2,701 / 76) — and OpenAlex, which
  indexes journals, conferences *and* workshops, lists exactly two works for the first
  paper (ICASSP 2026 + arXiv) and exactly three for the second (J. Comput. Sci. + SNU
  repository + arXiv), with no preprint–proceedings relation registered in Crossref.
  The "CVPR 2025" label traces to the note sites themselves, which carry it
  inconsistently next to a March-2026 arXiv id, and is mirrored verbatim across at
  least three of them.

  No venue claim was carried over unchecked: each was re-derived from the arXiv
  `comment` field and re-confirmed against Crossref, OpenAlex or dblp. Every arXiv id
  was also read back through the arXiv API instead of being trusted as printed: 25 of
  26 matched their entry's title at similarity 1.000, the last differing only in
  wording ("neutron computed tomography data" vs "neutron CT data").
- **`MedGMAE` was listed with no paper link.** It is an accepted **ICLR 2026 poster**;
  the OpenReview record and the conference listing were both located.
- **One of the new links was dead on arrival, and the link sweep caught it.**
  `Efficient Unrolled Networks` pointed at `github.com/romainvo/efficientunrolling`
  (404); the repository is `romainvo/efficient-unrolling`. This is the argument for
  running the sweep after any import rather than trusting the source's URL.

### Changed

- **Content is now licensed CC BY 4.0; code stays MIT.** The repository carried a
  single MIT licence over everything, which is the wrong licence for the content half:
  the awesome standard is explicit that code licences are not acceptable for list
  content (*"We strongly recommend the CC0 license, but any Creative Commons license
  will work. Code licenses like MIT, BSD, Apache, GPL, etc, are not acceptable."*).
  `LICENSE-content` now holds the full, unmodified CC BY 4.0 legal code and covers
  `data/`, `README.md` and the generated site; `LICENSE` continues to cover
  `scripts/`, `web/` and `.github/`. The split is stated in the README, the site
  footer, the JSON-LD `license` field, a `<link rel="license">` tag and
  CONTRIBUTING.md.

  Chosen over CC0 because the list wants to be credited, and over CC BY-NC-SA —
  which a comparable project uses — because NC would exclude the industrial-CT and
  medical-device readers who most need this list, and ShareAlike would stop anyone
  merging these entries into a permissively licensed project. The change is not
  retroactive: what was already published under MIT stays MIT for whoever received it.

- Clarified that the `License` column in the toolkit and dataset tables describes
  **those projects**, not this list. `data/` was also checked for text derived from
  another list's notes — there is none; the only non-ASCII prose in it is nine Chinese
  author names (庄天戈, 张朝宗), and paper records carry no `authors`, no abstract and
  no field over 300 characters.
- `README.md` is now generated from `data/*.yaml`. CI fails if the committed copy
  differs from a fresh build, so the README can no longer drift from the data.
- Entries without a venue render as `preprint 2025` in italics instead of a bare year, and
  the coverage line reports the reviewed/preprint split. (The wording was later shortened
  to the bare year inside the italics; see the 2026-10-11 entry.)
- Renamed the repository to `awesome-computed-tomography`, and reworked the description,
  topics and the README scope paragraph so the project is findable by the vocabulary of
  the field rather than by the project name alone.
- **The GitHub topic set is now chosen from measured repository counts**, not by keyword
  guesswork. With one star, only topics holding well under ~100 repositories can put the
  repository on page 1, so six niche tags the list documents were added
  (`spectral-ct`, `dual-energy-ct`, `limited-angle`, `4d-ct`, `scatter-correction`,
  `ct-imaging`) and six unreachable or redundant ones dropped, notably
  `medical-image-processing` (931 repos, saying what `medical-imaging` already said) and
  `awesome` (11,730, redundant with `awesome-list`). Two spellings were rejected for
  matching *zero* repositories: `limited-angle-tomography` and `dynamic-ct`.
