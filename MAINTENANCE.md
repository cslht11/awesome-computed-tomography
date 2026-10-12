# Maintaining this list

Maintainer notes. This list is curated and maintained by its authors only; it does
not take outside pull requests. Suggestions come in as issues or by email
(heitieya@163.com), and a maintainer verifies and adds them.

## Repository map

```
awesome-computed-tomography/
├── data/                        the only hand-edited content
│   ├── papers.yaml              papers
│   ├── toolkits.yaml            toolkits and libraries
│   ├── datasets.yaml            datasets
│   ├── benchmarks.yaml          benchmarks and challenges
│   ├── learning.yaml            books, courses, tutorials
│   ├── meta.yaml                the topic taxonomy + the language registry
│   └── i18n/
│       ├── en.yaml              every user-visible string, English (source of truth)
│       └── zh.yaml              Chinese overlay; a missing key falls back to English
├── scripts/                     the build pipeline, all of it
│   ├── build.py                 data/*.yaml -> both READMEs, and the validator
│   ├── build_site.py            templates + payload + origin -> site/<lang>/
│   ├── export_site_data.py      the JSON payload on its own (build_site uses it too)
│   ├── i18n.py                  overlay lookup and the orphan-key checker
│   ├── check_links.py           link-health sweep; writes into scripts/oneoff/
│   ├── install-hooks.sh         copies hooks/ into .git/hooks/ (see below)
│   └── oneoff/                  the harvest history — how each entry was found
├── hooks/                       authorship guards — MUST be installed after a clone
│   ├── pre-commit              rejects any commit whose user.email is not cslht11's
│   └── pre-push                rejects pushing any commit not authored by cslht11
├── web/                         the site's source; no framework, no bundler
│   ├── index.html               the one page: tabs, filters, the top-bar search
│   ├── page.html, pages/        About / Contact / Privacy
│   ├── styles.css               all styling; light and dark from one token set
│   ├── search.js                the search core: tokenise, index, rank, highlight
│   ├── app.js                   filtering and rendering; uses search.js
│   └── chrome.js                the phone drawer on the standalone pages
├── tests/                       the search tests (pure ones run in CI)
├── assets/logo.svg              the mark
├── site.config.yml              title, origin, licence — the site's single config
├── requirements.txt             PyYAML, and nothing else
├── README.md, README.zh-CN.md   GENERATED — never edit by hand
├── CHANGELOG.md                 what changed, dated; no version numbers
├── MAINTENANCE.md, SITE.md      this file, and how the site is put together
├── LICENSE (MIT)                code
└── LICENSE-content (CC)         the records and the prose
```

To change something, edit the left column and rerun the right one:

| Change | Edit | Then run |
| --- | --- | --- |
| a paper, toolkit, dataset, benchmark or learning resource | the matching `data/*.yaml` | `python scripts/build.py` |
| a user-visible string, in either language | `data/i18n/<lang>.yaml` | `python scripts/build.py` |
| a topic's name, description or order | `data/meta.yaml` and the overlays | `python scripts/build.py` |
| anything about the website | `web/` | `python scripts/build_site.py` |
| the site's title, origin or licence | `site.config.yml` | `python scripts/build_site.py` |
| how the build behaves | `scripts/` | run it; if it is the search, run `tests/` too |

**After cloning, run `sh scripts/install-hooks.sh` once.** Git deliberately never
enables a repository's own `hooks/` directory, so the authorship guards are inert
until they are copied into `.git/hooks/`.

**Generated, never hand-edited:** `README.md`, `README.zh-CN.md` and `site/`.
Editing them by hand produces a change the next build erases, and CI fails the
push that contains it.

## The list is data-driven

`README.md` is a **build artefact**, not a source file. It is generated from `data/*.yaml`
by `scripts/build.py`. Editing it by hand produces a change that the next build erases,
and CI fails the push that contains it.

Every change is therefore the same four steps:

```bash
git pull
# edit data/*.yaml
python scripts/build.py          # regenerate README.md and README.zh-CN.md
python scripts/build.py --check  # validate (this is also CI's first step)
```

then commit the data change **and** every regenerated README together. Running
`build.py` with no arguments renders **all** languages at once, so one command
writes both `README.md` and `README.zh-CN.md`; committing only the English one
leaves the Chinese file stale, and CI now fails on that.

CI (`.github/workflows/validate.yml`) does exactly three things:

1. `python scripts/build.py --check`
2. rebuild and fail if **any** generated README (`README.md`, `README.zh-CN.md`) is not
   byte-identical to the committed copy — the loop covers every language, so a stale
   translation fails the push just like a stale English file
3. `python scripts/build_site.py` — build the website too, so a change that breaks it
   fails here rather than at deploy time

So if `--check` passes locally, `git status` is clean after a rebuild, and
`build_site.py` exits 0, CI will pass.

## What `build.py` validates

- required fields per entry: `id`, `title`, `year`, `topics`
- at least one link (`paper` / `code` / `project`)
- no duplicate `id`
- no `topics` value that is missing from `data/meta.yaml`
- **no duplicate work**: the same arXiv id, DOI, or normalised title appearing twice

That last check is the one worth understanding. Duplicate detection compares a
*canonical identity*, never the `id` field. Entry ids here are short abbreviations
(`lpd`, `dip`, `super`) while newly harvested entries get title-derived slugs, so the
two id schemes never collide — which is exactly how 88 duplicates once accumulated
without anything complaining. If you add an entry, check the arXiv id and DOI against
the rest of the file first.

## The topic taxonomy

Sections in the README are the `topics` list in `data/meta.yaml`, **in the order they
appear there** — not alphabetically, and not by entry count. To move a section, move it
in `meta.yaml`. To add a topic, add it to `meta.yaml` and drop a broader one if the
taxonomy is getting long.

A paper may carry several topics and will then appear in several sections. That is
intended: the sections are lenses on the literature, not a partition of it.

## Verify venues by DOI, not by search

When you fill in a `venue`, confirm it against the DOI in Crossref and read back the
title that DOI actually has. Crossref's loose bibliographic search returns
plausible-looking hits for the wrong paper — it once "matched" a limited-view
reconstruction entry to a completely different 2021 TMI paper — and at low similarity
the response is not trustworthy. Only accept a hit whose title matches; then fill in
the venue and the year from that record.

`year` means the year **at the venue**. When a work appeared on arXiv first, the value
belongs to the publication, not the posting. For an entry with no venue, `year` is the
first public posting and the README prints `_preprint <year>_`.

`arXiv` and `TechRxiv` are not venues. If an entry has no venue, leave the field out —
do not fill it with the preprint server.

## Keeping the frontier current

Roughly half the value of a list like this is recency. The practical pattern is to sweep
arXiv for the topics in scope every few months, then verify each candidate before adding
it. The harvesting scripts and their reports are kept under `scripts/oneoff/`;
`scripts/oneoff/README.md` records what each one does, in what order to run them, and
what went wrong when they were first written.

Two things to be careful about when harvesting:

- **Match on canonical identity, not on titles or ids.** See the duplicate note above.
- **Rate-limit politely.** The arXiv API asks for at least three seconds between
  requests. Exceeding it returns an empty response rather than an error, which a naive
  script reads as "not found" — a false negative that looks like a missing paper.

## The website

`web/` + `site.config.yml` + `scripts/build_site.py` render the same corpus as a
searchable single page:

```bash
python scripts/build_site.py       # data/*.yaml -> site/  (git-ignored, regenerated)
python -m http.server 8899 -d site # then open http://127.0.0.1:8899/
```

It reads `data/*.yaml` and calls `build.py`'s own `validate()`, so the site and the
README cannot disagree and there is no second validator to keep in sync. It adds no
dependencies — `requirements.txt` is still just PyYAML.

The origin lives in exactly **one** place: `url:` in `site.config.yml`. Every absolute
address is derived from it (canonical, `og:url`, JSON-LD, `sitemap.xml`, the `Sitemap:`
line in `robots.txt`), and the build refuses to emit output that would be reachable at
two origins. Leaving it empty falls back to the GitHub Pages address, which is the right
behaviour before a domain exists.

Website process — the file map, the deploy workflow and its trigger, switching the domain,
the two constraints that look arbitrary and are not, and its own failure modes — lives in
[SITE.md](SITE.md). The site is live at <https://computedtomography.org/> and republishes
on every push to `main`; `site/` is rebuilt by CI and never committed.

## Licensing

Two licences, split along the code/content line:

| Path | Licence | File |
| --- | --- | --- |
| `scripts/`, `web/`, `.github/`, `assets/`, `site.config.yml` | MIT | `LICENSE` |
| `data/*.yaml`, `data/i18n/*.yaml`, the READMEs, these docs, the rendered site | CC BY-NC-SA 4.0 | `LICENSE-content` |

`web/*.js` and `web/*.css` are copied into `site/` verbatim, so those generated
copies stay MIT — they are code. Everything else under `site/` is generated from
`data/` and is content. `LICENSE-content` lists both halves explicitly; if a path
is added, add it there too.

### Why the content is CC — and the code is not

The awesome standard is explicit that a code licence is the wrong instrument for
list content ("We strongly recommend the CC0 license … Code licenses like MIT,
BSD, Apache, GPL, etc, are not acceptable"), so the content is CC.

The reverse matters just as much, and it is the mistake worth naming: **Creative
Commons advises against using its licences for software**, and a repository that
puts one licence over code *and* content inherits three concrete problems.

- CC licences say nothing about **patents**, and nothing about **source versus
  object form** — the two things a software licence exists to settle.
- **NonCommercial is not an open-source licence.** Neither the OSI nor the Debian
  Free Software Guidelines accept an NC restriction, so CC BY-NC-SA code is
  source-available, not open source, however the repository describes itself.
- **ShareAlike is viral over code.** Copying any part of it forces an entire
  downstream project onto the same licence, which rules out reuse inside an MIT
  or Apache project — the normal way infrastructure code travels.

So this repository keeps MIT for the code and CC for the records and prose. If you
want to reuse the build pipeline, take `scripts/` and `web/` under MIT and leave
the records behind.

### What NC means here, plainly

NC is a real restriction rather than a formality: the records cannot be merged into
a permissively licensed collection, and the content would not count as "open" under
the Open Knowledge Definition. That is the maintainers' deliberate choice (since
2026-10-10), made to keep commercial re-publication of the list under control, and
it is written down here so the trade-off is not rediscovered later.

Five places state the licence and must stay in agreement: the `## License` section of
**both** `README.md` and `README.zh-CN.md` (both generated by `build.py`), the
`LICENSE` / `LICENSE-content` files themselves, and — for the site — the footer, the
JSON-LD `license` field and the `<link rel="license">` in the `<head>`, all driven from
`code_license` / `content_license` in `site.config.yml`. Changing a licence means
changing those, not just the file.

A licence change is not retroactive: what shipped under the old licence stays under it.
The `License` **columns** in the toolkit and dataset tables are a different thing —
they describe the linked projects.

## Citing a snapshot

This list is deliberately **not versioned** — no tags, no releases. It is refined
continuously (entries added, venues corrected, links repaired) and has no point at which
it is "finished", so a version number would be a promise with nothing behind it. In
place of a release page, `CHANGELOG.md` records what changed when, by date.

A reader who needs a fixed point to cite should use a commit hash, or `main` as of a
date. If a tag is ever reintroduced, this is the wrong decision to make quietly — it
imposes a compatibility contract on the `id` fields that nothing currently promises.

**Do not tag or release, for a second reason too** (learned the hard way,
2026-10-11): a tag is a *ref* to a commit, and a tag that outlives a history rewrite
keeps the rewritten-away commits reachable. GitHub counts contributors over every
reachable commit, so a stale tag made a deleted author reappear in Insights long
after the branch itself was clean. Tags are not free bookkeeping here; they are
anchors into history. See `HANDOFF.md` §5.9b.

## Sole authorship: one author, no bots, no pull requests

This repository is authored by **cslht11 and nobody else**. That is a property of the
commit graph, not just of the prose, and it is easy to break without noticing — GitHub
never warns you, and the damage cannot be undone:

- **Squash-merging or merge-committing a pull request attributes the commit to the
  pull request's author.** Merge Dependabot's pull request and `main` gains a commit
  authored by `dependabot[bot]`, which then appears in Insights → Contributors as a
  second author. This happened once; it took a history rewrite to undo.
- **`refs/pull/N/head` cannot be deleted.** `DELETE /repos/{o}/{r}/git/refs/pull/1/head`
  answers `refs/pull/* is read-only` (HTTP 422). Closing or never merging the pull
  request does not help — the ref, and the author behind it, stay.

So the rule is: **do not let a pull request come into existence on this repository.**

| Do | Don't |
| --- | --- |
| Commit directly to `main` as cslht11 | Enable Dependabot version updates (`.github/dependabot.yml` is deliberately absent) |
| Apply a dependency bump by hand, as a cslht11 commit, then close the bot's PR unmerged | Merge a bot's pull request "just this once" |
| Keep Dependabot **security alerts** on — they are a separate setting, need no config file, and create no commits | Assume closing an unmerged pull request keeps the graph clean |

Three guards are in place. The first two ship in `hooks/` and are installed by
`sh scripts/install-hooks.sh` — Git never enables a repository's own `hooks/`
directory on its own, so a fresh clone has no protection until that is run:

1. **`hooks/pre-commit`** refuses any commit whose `user.email` is not
   `cslht11@users.noreply.github.com`. This catches the account-mix-up case:
   this machine holds two GitHub accounts, and only cslht11 may sign here.
2. **`hooks/pre-push`** walks every commit about to be pushed and refuses if any
   author is not `cslht11`. This is the one that actually matters — squash-merging
   signs with *the pull request author's* identity, which has nothing to do with
   local `git config`, so `pre-commit` cannot see it coming. It is what would have
   stopped `dependabot[bot]` at the door.
3. **Verify after pushing**, because no hook can see what GitHub computed:
   ```
   curl -s https://github.com/cslht11/awesome-computed-tomography/graphs/contributors-data \
     | grep -o '"login":"[^"]*"'
   ```
   It must print `"login":"cslht11"` and nothing else. A `202` response means
   GitHub is still recalculating — wait a minute and retry. This is the same
   endpoint the Insights page reads, so it is the page's own answer, not a proxy
   for it. (`gh api repos/.../graphs/contributors-data` will 404: the endpoint has
   no `/repos/` prefix and is not part of the REST API.)

One thing worth knowing, because it is counter-intuitive and it changes what is
worth doing about it: **the contributor graph counts commits on the default branch
and anything a tag can still reach — it does not read `refs/pull/*`.** After the
`dependabot[bot]` commit was rewritten, `refs/pull/1/head` still pointed at the bot's
commit and still could not be deleted, and the graph was clean anyway. So a leftover
pull request ref is untidy but harmless; recreating the repository to get rid of one
is not worth the custom-domain certificate reissue.

## Failure modes seen so far

Worth knowing, because each of these was silent:

| Symptom | Cause |
| --- | --- |
| Counts higher than reality, no errors | Duplicates added under a different `id` scheme. Detection compared `id`, not identity. |
| A venue printed with a stray year, e.g. `(AAAI 2026, 2026)` | The year was left inside the venue string, and the renderer prints venue and year separately. |
| An entry whose year and venue belong to an unrelated paper | Both were inherited from a paper that shared its short id. |
| `(2017)` on a paper posted in 2020 | The `YYMM` of an arXiv id (`2008.02839`) read as a year. |
| A plausible venue that is entirely the wrong paper | Crossref bibliographic search at low similarity. Verify by DOI. |
| A venue-less entry indistinguishable from a published one | Both printed as a bare year. Now `_preprint year_`, against `_venue year_` for the rest. |

## Adding entries

### What we accept

| Category | File | Bar |
| --- | --- | --- |
| Papers | `data/papers.yaml` | Peer-reviewed, arXiv preprint, or a well-documented technical report on CT reconstruction. |
| Toolkits & libraries | `data/toolkits.yaml` | Publicly available, actively usable code (reconstruction, simulation, geometry, denoising). |
| Datasets | `data/datasets.yaml` | Publicly downloadable CT datasets with a stable landing page. |
| Benchmarks & challenges | `data/benchmarks.yaml` | Community benchmarks and challenge campaigns with published results. |
| Learning resources | `data/learning.yaml` | Books, courses, tutorials, teaching tools and related curated lists. |

We are deliberately **topic-first**: a paper is filed under every topic it
belongs to (a sparse-view diffusion paper goes under both `sparse-view` and
`diffusion`). Use the topic ids defined in `data/meta.yaml`.

### Entry schemas

#### `data/papers.yaml`

```yaml
- id: fbpconvnet                 # required, unique, lowercase slug
  abbr: FBPConvNet               # optional short name used in the list
  title: Deep Convolutional Neural Network for Inverse Problems in Imaging
  authors: Kyong Hwan Jin, Michael T. McCann, Emmanuel Froustey, Michael Unser  # optional
  year: 2017                     # required, 4-digit
  venue: IEEE TIP                # optional; journal or conference
  topics: [low-dose, unrolling]  # required, >=1 id from data/meta.yaml
  paper: https://arxiv.org/abs/1611.03679   # at least one link is required
  code: https://github.com/...              # optional
  project: https://...                      # optional
  data: https://...                         # optional
  note: optional one-liner                  # optional
```

**How `venue` and `year` are rendered.** A paper with a `venue` prints as
`_venue year_` in italics, and the year is the year **at that venue** — for a work that
first appeared on arXiv and was later published, put the publication year, not
the posting year. A paper with **no** `venue` prints as `_preprint year_`, where
the year is the first public posting. The distinction is deliberate: it lets a
reader tell a peer-reviewed entry from an unrefereed preprint at a glance, and
the list reports the split in its coverage line. If you know the venue of a
`preprint` entry, adding it is the single most useful contribution you can
make — verify it against the DOI in Crossref first, because a title search at low
similarity will happily return a different paper.

#### `data/toolkits.yaml`

```yaml
- name: TIGRE
  repo: CERN/TIGRE          # or use `url:` for a non-GitHub project
  homepage: https://...     # optional
  language: MATLAB / Python
  license: BSD-3-Clause
  stars: 812                # refreshed manually; approximate is fine
  tags: [CBCT, GPU, iterative]
  note: GPU-accelerated iterative reconstruction toolbox.
```

#### `data/datasets.yaml`

```yaml
- name: LoDoPaB-CT
  url: https://...          # stable landing page, not a direct download
  modality: CT
  tasks: [low-dose]
  license: CC-BY-4.0
  note: "**Projection + image.** 40k+ slice pairs from the LIDC/IDRI collection."
```

Start the `note` with one of two markers when raw projections are available:

| Marker | Meaning |
| --- | --- |
| `**Projection + image.**` | Raw projections **and** a reference volume are released. |
| `**Projection only.**` | Raw projections with no reference volume. |

No marker means the release is image-domain only — still useful, but it cannot
be used to test a forward model. The README renders this convention as a legend,
so keep the wording exactly as above.

#### `data/benchmarks.yaml`

```yaml
- name: AAPM Low Dose CT Grand Challenge
  year: 2016
  url: https://...
  tasks: [low-dose]
  note: 25 patients, quarter-dose reference data.
```

#### `data/learning.yaml`

```yaml
- name: Computed Tomography: Principles, Design, Artifacts and Recent Advances
  type: book                # book | course | tutorial | tool | list
  url: https://...
  note: Jiang Hsieh. The standard practitioner reference.
```

Survey papers are **not** listed here — file them under `data/papers.yaml` with
the `survey` topic, so they appear in the Papers section instead of being
duplicated.

### How entries are verified

Every link in this list was opened before being added, and papers were resolved
against a bibliographic database rather than typed by hand:

- A paper's `paper` link is either a publisher DOI (`https://doi.org/...`) or an
  arXiv abstract page, obtained by title lookup against **Crossref** first and
  the **arXiv API** as a fallback. The returned title is compared with the entry
  title, and a mismatch above a similarity threshold is rejected rather than
  silently accepted.
- Every link was then normalised to one of those two forms, and each DOI was
  fetched back from Crossref a second time to confirm that the title behind it
  really is the paper in the entry. Two wrong DOIs were caught this way.
- `year` and `venue` are written back from the authoritative Crossref record, so
  they reflect the version of record (e.g. a MICCAI paper is dated to the
  proceedings year, not the arXiv preprint year). Manual corrections take
  precedence where Crossref reports an online-first date instead.
- Toolkit `stars` are a snapshot and are refreshed by hand; `license` comes from
  the repository's declared SPDX identifier.
- `scripts/check_links.py` requests every URL in `data/` and writes a report to
  `scripts/oneoff/link-report.txt`. Status handling follows what the sites
  actually do to automated clients: `200`/`202`/`30x` count as **OK** (`202` is
  what IEEE's DOI resolver returns to a non-browser client, so it is not a
  failure), `403`/`405`/`429` are reported as **BLOCKED** — reachable but
  refusing bots — and anything else is a **PROBLEM**. A transport error is not
  treated as proof that a site is down.
- `scripts/oneoff/audit_doi_hosts.py` resolves every DOI and records the host it
  actually ends on, because a `200` is not by itself evidence that a link is
  *useful*. Two findings from that audit are worth knowing: the NeurIPS
  Foundation's own prefix (`10.52202/...`) resolves to `www.proceedings.com`, a
  commercial per-paper store, for papers that are free on arXiv — those entries
  link the arXiv page instead; and four Springer/IEEE DOIs pass through
  `validate.perfdrive.com`, which is a bot check in front of the real publisher
  page, not a redirect somewhere else.

If you are adding a paper, please include the DOI or arXiv id — that is the
fastest thing to check.

### Where entries come from

Two kinds of pass feed the list, and both leave an audit trail under
`scripts/oneoff/`:

- **Mining comparable lists.** The community CT lists are parsed and subtracted
  against what we already have, and each surviving candidate is resolved through
  Crossref and then arXiv. A source list quoting a *journal* title for an
  arXiv preprint will not resolve this way — `arXiv:2203.15725` is listed
  elsewhere as *"Synergizing Physics/Model-based and Data-driven Methods for
  Low-Dose CT"* while its actual arXiv title is *"Physics-/Model-Based and
  Data-Driven Methods for Low-Dose CT"* — so a human has to read the abstract
  page when the machine comes back empty.
- **Harvesting the recent frontier.** `scripts/oneoff/harvest_recent.py` queries
  the arXiv API across 20 facets of CT reconstruction with a `submittedDate`
  window, because the community lists stop being updated well before the current
  year. Ranking the harvest by keyword density is not enough on its own: it
  favours long abstracts and will quietly drop well-published work, so anything
  carrying an acceptance signal in its arXiv comment (`Accepted to ECCV 2026`)
  is pulled in by a second pass regardless of score.

**Scope.** The list is about *reconstruction* from projection data. Papers whose
subject is CT *segmentation*, CT-based *classification* or *risk prediction*,
MRI synthesis *from* CT, US-CT *registration*, or CBCT *record retrieval* are out
of scope even when CT is the input — several such papers were removed by hand.
Synthetic-CT generation from CBCT is in scope, since it is an image-quality
problem defined against reconstructed volumes. The test is not "does CT appear
in the title" but "would this entry help someone recovering a volume from
projections".

**Recency.** There is no cutoff, but a 2025-2026 paper that a reader could not
find elsewhere is worth more here than another well-known 2018 one. If a recent
preprint is later published, update `year` and `venue` — the preprint link can
stay, since the arXiv page carries the journal reference.

### Repository metadata

The name is descriptive rather than unique: `awesome-computed-tomography` was
already taken by an inactive two-star repository when this one was created, and
that was judged not worth churning the URL over. A descriptive name is what a
field search matches on, and GitHub orders repository search by name match
before stars. What the name does *not* carry is the vocabulary of the sub-fields
— sparse-view, cone-beam, spectral, low-dose — so matching for those has to come
from the other channels, kept in sync by
`scripts/oneoff/set_repo_metadata.py`:

- **description** — leads with "CT (computed tomography) reconstruction" and
  names the acquisition regimes.
- **topics** — capped at 20 by GitHub, and chosen by *where we can be seen*, not
  by keyword count. Browsing a topic page lists repositories by stars, so a
  topic with thousands of repositories buries us while a topic with a handful
  puts us on page one. The rule that follows from that: **one topic per
  acquisition regime the list documents, at the exact spelling people type**
  (`sparse-view-ct`, `limited-angle`, `low-dose-ct`, `metal-artifact-reduction`,
  `cone-beam-ct`, `cbct`, `spectral-ct`, `dual-energy-ct`, `4d-ct`,
  `scatter-correction`), topped up with the identity tags a searcher types
  (`computed-tomography`, `ct`, `tomography`, `ct-reconstruction`) and a small
  number of method/audience tags.
  Two traps are worth knowing, because both look right and reach nobody:
  a spelling nobody else uses is invisible (`limited-angle-tomography` and
  `dynamic-ct` match **zero** repositories), and a near-duplicate wastes a slot
  (`medical-image-processing` said the same thing as `medical-imaging` while
  being 931 repositories deep). Verify counts before swapping a topic:
  `gh api "search/repositories?q=topic:<t>&per_page=1" --jq .total_count`.
  The full reasoning and the measured counts are in the docstring of
  `scripts/oneoff/set_repo_metadata.py`.
- **README intro** — the first two paragraphs name the scope in the vocabulary of
  the field. This is scope, not keyword stuffing: every term listed is covered by
  a section below.

When adding a topic, drop a broader one. Do not add `deep-learning` or similar —
with ~100k repositories behind it, it cannot send anyone here.

### Style rules

- **English only** for entries and descriptions.
- Link to the **canonical** source: the publisher or arXiv page for papers,
  the upstream repository for code.
- Prefer `https://` and avoid link shorteners or tracking parameters.
- Prefer the **open-access** destination when the DOI leads to a reseller or a
  per-paper paywall. The venue of record still goes in `venue`, so nothing is
  lost by pointing `paper` at the arXiv page.
- Do not add an entry you have not opened. Broken links get removed.
- One entry per logical artifact — do not add the same paper twice.
