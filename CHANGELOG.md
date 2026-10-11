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

## 2026-10-11 — 101 more papers, the whole list in Chinese, and a new home

The largest single addition so far. The list moves to a repository of its own and
becomes bilingual end to end.

### Content

- **390 papers** (was 289), spanning **1971–2026** (was 1976) across 17 topics, plus
  **44 toolkits** (was 43), **40 datasets** (was 34), 19 benchmarks/challenges and
  29 learning resources. **327 of 390 (84%)** carry a peer-reviewed venue.
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

## 2026-10-10 — About, Contact and Privacy pages

- New static pages at `/about/`, `/contact/` and `/privacy/` (scope and verification method, how to suggest or correct an entry, what the site does and doesn't collect).
- Compact footer on every page linking to them; licence line kept.
- `build_site.py` renders the pages from `web/pages/` and adds them to the sitemap.

## 2026-10-10

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

First public state. The list is stable enough to cite.

### Contents

- **289 papers** spanning **1976–2026** across **17 topics**, plus **43 toolkits**,
  **34 datasets**, **19 benchmarks/challenges** and **29 learning resources**.
- Every paper link was resolved against Crossref, arXiv or the publisher's own record,
  and every URL was checked.
- **226 of 289 papers (78%)** carry a peer-reviewed venue. Entries without one render
  as `(preprint, year)`, so the reviewed/unreviewed split is visible in the README
  itself rather than left for the reader to guess.

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
  `README.md`, `CONTRIBUTING.md` and `MAINTENANCE.md` now point at it.

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
- Entries without a venue render as `(preprint, 2025)` instead of a bare year, and the
  coverage line reports the reviewed/preprint split.
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
