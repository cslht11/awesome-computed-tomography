# The website

Who this is for: anyone with commit access who has to build, deploy or change the
website. If you only want to *add an entry*, read [MAINTENANCE.md](MAINTENANCE.md#adding-entries) —
you never need to touch anything described here.

The site is the full rendering of the corpus; `README.md` is a landing page
whose sections point at the site. Both read `data/*.yaml`, so they cannot
disagree.

```bash
python scripts/build.py       # data/*.yaml -> README.md
python scripts/build_site.py  # data/*.yaml -> site/
```

Nothing else is needed. **No new dependencies** — `requirements.txt` is still just
PyYAML.

## Files

| Path | Committed? | What it is |
| --- | --- | --- |
| `site.config.yml` | yes | Title, tagline, description, repository, and the one `url` that drives every absolute address. **This is where the domain goes.** |
| `web/index.html` | yes | Home-page template with `{{PLACEHOLDER}}` markers. Not served directly. |
| `web/page.html` | yes | Template for the standalone pages (About / Contact / Privacy). |
| `web/pages/{about,contact,privacy}.html` | yes | Body content for those three pages. |
| `web/styles.css` | yes | All styling. Light and dark token sets. Deliberately ships **no web font** — the reasoning is in the comment at the top of the file. |
| `web/search.js` | yes | The search core: CJK-aware tokenising, a per-record weighted index, ranking and highlight ranges. Loaded before `app.js`; its pure functions have no DOM dependency, so they run under Node for tests. |
| `web/app.js` | yes | Client-side filtering and rendering. Delegates matching, ranking and highlighting to `search.js`. |
| `web/chrome.js` | yes | Phone drawer for the standalone pages. (The colour theme is wired in an inline `<head>` script instead, so it still works if a script fails to load.) |
| `data/i18n/en.yaml` | yes | English strings — the source of truth for every user-visible string. |
| `data/i18n/zh.yaml` | yes | Chinese overlay. Looked up first for `zh`; missing keys fall back to English. |
| `scripts/export_site_data.py` | yes | `data/*.yaml` -> the JSON payload. Also usable on its own. |
| `scripts/build_site.py` | yes | Assembles templates + payload + origin into `site/`, once per language. |
| `scripts/changelog.py` | yes | Parses `CHANGELOG.md` into dated entries (newest first) and renders them for `/changelog/` and `/zh/changelog/`. Fails the build on an undated `##` heading or a date more than a day in the future. The Chinese edition reads each entry's translation from `CHANGELOG.zh-CN.md`, matched by date and the `<!-- en: … -->` title line; an untranslated entry falls back to English (marked `lang="en"`, with a note on the page), and a translation whose English entry no longer exists fails the build. |
| `data/resources.yaml` | yes | Which dataset/benchmark rows get a page at `/datasets/<slug>/` or `/benchmarks/<slug>/`, their slugs, short names, paper-matching aliases and descriptor papers, plus the page strings (en/zh). The rule for which rows qualify is documented at the top of the file; every fact on the pages comes from `data/datasets.yaml` / `data/benchmarks.yaml` / `data/papers/`. |
| `data/guides.yaml` | yes | The evergreen guides at `/guides/<slug>/`: editorial prose (en/zh) with `{tokens}` filled from live data, the generated comparison tables they show, and their FAQ. |
| `scripts/resource_pages.py` | yes | Selects and renders the dataset, benchmark and guide pages and their two indexes; called by `build_site.py`. |
| `site/` | **no** | Build output. Git-ignored. Delete it freely; it is regenerated. |

The licence in the page footer, the JSON-LD `license` field and the
`<link rel="license">` tag all come from `code_license` / `content_license` /
`content_license_url` in `site.config.yml`. Content and code are licensed
separately — the reasoning is in [MAINTENANCE.md](MAINTENANCE.md).

## Languages

The site is bilingual, English at `/` and Chinese at `/zh/`. Both are rendered by
the same `build_site.py` run; each language builds its own payload so the
per-entry notes (and topic names) read in that language.

- `data/i18n/en.yaml` is the **source of truth** for every user-visible string.
- `data/i18n/zh.yaml` is an **overlay**. For `zh` a key is looked up in the overlay
  first and falls back to English when it is missing — so a partial translation is
  valid and degrades gracefully.
- The one error case is an **orphan key**: a key in `zh.yaml` that does not exist in
  `en.yaml`. That fails `build.py --check` (exit 1). A *missing* translation is not
  an error.

An entry's `note` follows the same rule. It lives in English in `data/*.yaml`, and
`data/i18n/zh.yaml` carries a per-table override — `papers.<id>.note`,
`toolkits.<name>.note`, and so on — which the site export merges in. A translated
note that exists but does not reach `site/<lang>/data.json` **fails**
`build_site.py` (it used to fall back to English silently; the assertion keeps that
from coming back).

Each language gets its own `<html lang>`, canonical URL and og:url, and the two are
wired together with `hreflang` alternates plus an `x-default` pointing at the
English page. `sitemap.xml` lists every page in both languages. The language
switcher lives in the header, after the colour-theme button.

> **The source-language trap.** English values come from `site.config.yml`, *not*
> from `en.yaml` — the overlay is only consulted for non-source languages. So when
> a value gets templated (a description, a count), editing `en.yaml` alone changes
> only the Chinese page and leaves English on the old text. Change both, or change
> `site.config.yml` and let the overlay inherit.

## Build and preview

```bash
python scripts/build_site.py            # writes site/, all languages
python scripts/build_site.py --url https://example.org/   # one-off origin override
python scripts/build_site.py --lang zh  # just one language
python -m http.server 8899 -d site      # then open http://127.0.0.1:8899/
```

**Stop the preview server when you are done with it.** `http.server` holds the
directory it was started in, and on Windows that alone is enough to make the folder
impossible to rename or move until the process is killed. (This actually bit us once.)

`site/index.html` also opens correctly by **double-clicking** it — see the two design
constraints below, which exist specifically to keep that working.

The build prints the size summary and, if `url` is empty, a note that the GitHub Pages
address was used.

## Sections: homepage tabs and section pages

The site has seven sections, Papers, Toolkits, Datasets, Benchmarks, Learning, Teams and
Knowledge Graph, and each exists in two forms built from the same code:

- **a homepage tab** (`/?tab=toolkits` …; Papers is the default tab at `/`). This is what
  the navigation switches: one page, so switching is instant. `?tab=` is applied before
  first paint (an inline script sets `html[data-tab]` and marks the nav), and the language
  switch carries the current tab, filters and `#anchor` (`web/lang.js`).
- **a standalone section page** (`/toolkits/`, `/datasets/`, `/benchmarks/`, `/learning/`,
  `/teams/`, `/graph/`, plus `/topics/` and `/guides/`), for search engines and links: a
  `?tab=` URL is the homepage to a crawler, so without these a section had no address of
  its own. They open with the same intro (`web/hero.html`), render their tables at build
  time (`render_section_tables`, mirroring `web/app.js` column for column), are linked from
  every page's footer, and are in the sitemap and `llms.txt`.

Detail pages (one dataset, one benchmark, one graph, one topic) are separate pages under
those paths; their "back" links and the nav lead to the homepage tab. Moves between
separate pages cross-fade (`@view-transition`) where the browser supports it.

To add a column or change a table, change both `web/app.js` and `render_section_tables`;
`tests/test_seo.js` checks every section page carries every row.

## Deploying

**Live at <https://computedtomography.org/>**, and published automatically: after
`validate` passes on a push to `main`, `.github/workflows/deploy.yml` rebuilds `site/`
from `data/` for that exact commit and publishes it. Nothing generated is committed.

Deploy is chained to validation with `workflow_run` (since 2026-10-29). Before that both
workflows triggered on `push` in parallel, so a push that failed `validate` — a stale
README, a commit by another account, the DOM suite, a stale `last_updated` — still went
live. Now a red `validate` means no deploy, and the deploy builds `workflow_run.head_sha`,
the commit validate actually checked. `workflow_dispatch` (Actions tab) still deploys by
hand, without waiting for validate.

It started as a manual-only workflow, deliberately: `actions/deploy-pages` fails while
Pages is switched off, so a push trigger added before then would turn every push red for
a reason that has nothing to do with the change under review — worse than no workflow,
because people learn to ignore red. Pages is now on, so the push trigger is on.

The state as of writing (all four are already done — this is the checklist to repeat if
the site is ever moved to a new repository or the domain changes):

1. Repository **Settings -> Pages -> Build and deployment -> Source: ``GitHub Actions``**.
   (`build_type` is `workflow`, not a branch.)
2. **Settings -> Pages -> Custom domain** set to the apex — `site.config.yml` names
   `computedtomography.org`, so the artifact ships a matching `CNAME`. See the DNS table
   below. `www` is configured too and 301s to the apex.
3. **Enforce HTTPS** ticked, once the certificate reads *approved*. It is issued after the
   domain resolves, so ticking it earlier only produces a warning.
4. Repository **homepage** field set to the live URL
   (`gh api -X PATCH repos/cslht11/awesome-computed-tomography -f homepage=<url>`), so the
   link appears at the top of the repository page.

Check the current state with:

```bash
gh api repos/cslht11/awesome-computed-tomography/pages \
  --jq '{html_url, cname, build_type, https_enforced, cert: .https_certificate.state}'
```

Both workflows begin with `python scripts/build.py --check`, which validates `data/`
and the i18n overlays. `validate.yml` (pushes to `main` and pull requests) additionally
checks sole authorship, that `data/meta.yaml` `last_updated` is not older than the newest
commit touching `data/` (`scripts/check_last_updated.py`), that both READMEs are
byte-identical to a rebuild, that `build_site.py` succeeds, and runs all three test
suites. Because deploy waits for it, every one of those checks now blocks publication.

**Cache-busting.** GitHub Pages serves every file with `max-age=600`. So that a deploy
never pairs new HTML with a cached old script, every page references `styles.css`,
`search.js`, `app.js`, `chrome.js` and `lang.js` with `?v=<content hash>` (as the graph
and lineage assets already did); `tests/test_seo.js` fails on any unversioned reference.

**Sitemap dates.** Every `<lastmod>` is `data/meta.yaml` `last_updated`, the content
date, not the build date, so a rebuild that changes no data does not tell search engines
that all pages changed.

**IndexNow.** After a deploy, the `indexnow` job sends Bing/Yandex the URLs whose page
changed, not the whole sitemap. `scripts/changed_urls.py` (run in the build job) hashes
every sitemap page with build-day noise removed (the payload's `generated` date and the
`?v=` asset hashes), ships the hashes as `/page-hashes.json`, and compares them with the
copy that is live. If the live copy cannot be read, every URL counts as changed.

**Homepage weight.** Each paper's blurb is stored once, in the server-rendered title's
`title=`; the embedded `#site-data` payload leaves blurbs out and `app.js` reads them
back by `data-id` before its first render (`data.json` still has them). There is no
papers `ItemList` in the JSON-LD: its items all pointed off-site, and it was a third copy
of every title. Together this took the page from 1.33 MB to 1.02 MB (gzip 308 → 228 KB).

**Link check.** `.github/workflows/links.yml` runs `scripts/check_links.py --strict`
every Monday and on demand. A PROBLEM opens an issue labelled `link-check` (or comments
on the open one); the full report is attached to the run.

## Switching to a custom domain

One line, then a rebuild. This has already been done once — the site is configured for
`https://computedtomography.org/`.

```yaml
# site.config.yml
url: "https://computedtomography.org/"
```

```bash
python scripts/build_site.py
```

Every absolute address is derived from that single value: `<link rel="canonical">`,
`og:url`, the JSON-LD `@id` / `url`, `<loc>` in `sitemap.xml`, the `Sitemap:` line in
`robots.txt`, and the `CNAME` file. There is no second place to edit.

### DNS

For an apex domain, point it at GitHub Pages (`@` is the apex):

| Type | Name | Value |
| --- | --- | --- |
| `A` | `@` | `185.199.108.153` |
| `A` | `@` | `185.199.109.153` |
| `A` | `@` | `185.199.110.153` |
| `A` | `@` | `185.199.111.153` |
| `CNAME` | `www` | `cslht11.github.io` |

The four `A` records are GitHub Pages' own addresses and are what make the apex resolve.
All four, not one — they are not redundancy for its own sake but the documented set.
`AAAA` records (`2606:50c0:8000::153` … `8003::153`) are optional; add them only if IPv6
matters.

If the registrar puts a proxy in front of the records (Cloudflare's orange cloud, say),
set them to **DNS only** while the domain is being verified, then decide. A proxy that
itself terminates TLS can stop Pages from issuing its certificate, and the symptom is an
HTTPS error that looks like a wrong `A` record.

Then, in the repository: **Settings -> Pages -> Custom domain**, enter the apex, and wait
for the DNS check to pass before ticking **Enforce HTTPS**. The certificate is issued
after the domain resolves, so ticking it early just produces a warning.

**The build refuses to produce a split-identity site.** After writing, `build_site.py`
asserts that canonical and `og:url` match the configured origin, that `robots.txt`
advertises the same sitemap, that `CNAME` names the same host, and — when a custom domain
is configured — that **this repository's own Pages address appears nowhere in the
output**. A violation exits non-zero. This is copied from a larger project that got
bitten by it: a site reachable at two origins gets its search ranking divided between
them, and that is invisible for weeks.

That last check tests for `<owner>.github.io` specifically, not for the substring
`github.io`. A corpus of CT papers links to plenty of authors' project pages
(`ooonesevennn.github.io/DiffNR/`, `open-pros.github.io`, …), so the blunt version fails
the build on perfectly good data. It did, the first time this was run against a real
domain.

`url` left empty falls back to `https://<owner>.github.io/<repo>/`, no `CNAME` is
written, and the origin check is skipped — which is the correct behaviour before a domain
exists.

## What the page does

- **Search** — typing in the top box (80 ms debounce) shows a dropdown of the best
  matches across all five sections; **Enter** is what filters the paper list. A query is
  scored and ranked rather than AND-ed: a record matching one word out of three is ranked
  lower instead of being dropped, and only records matching nothing disappear. Matches are
  highlighted in the titles.
- **Enter's fallback** — when the query finds no paper, Enter opens the top-ranked match
  only if it scored at least 2 (i.e. it hit a name or the metadata); a weaker lone body hit
  filters instead. Without that floor, typing an arXiv id whose digits also occur inside
  some other record's URL would navigate to the wrong page.
- **Filters** — one chip per topic (multi-select, with counts), `All / Peer-reviewed /
  Preprints`, `has code`, `from <year>`, and sorting by newest, oldest or title.
- **Tabs** — Papers, Toolkits, Datasets, Benchmarks, Learning.
- **Deep links** — the whole filter state lives in the URL
  (`?q=&topic=&type=&code=&from=&sort=&tab=`), so any view can be shared. There is a
  *copy link* button.
- **`/`** focuses the search box.
- **Light and dark**, following the system, with a manual toggle remembered in
  `localStorage`.
- **Works without JavaScript.** Every paper row is rendered into the HTML at build
  time, so a crawler — or a reader with JS off — still gets the complete list. Search and
  filters are progressive enhancement on top.

The search is a plain substring match against a pre-computed lower-case blob shipped with
the page. There is no index to download and no query parser to trip over. That last point
is deliberate: a comparable project lost search entirely on any title containing a colon,
because the query string was fed to a parser that treats `:` as field syntax. Titles here
are full of colons (`DM4CT: ...`, `$K$-NeAS: ...`).

## Two constraints that look arbitrary but are not

**1. `web/app.js` must stay a classic script.** Do not add `type="module"`. Browsers
refuse to load ES modules over `file://` (CORS), which would break double-click preview
for every future maintainer.

**2. The payload is inlined into `index.html`; it is not fetched.** Same reason — `fetch`
is blocked on `file://`. The cost is size: the inlined JSON makes `index.html` the largest
file the build produces. Run `python scripts/build_site.py` and read the size it prints
rather than trusting a number here — this figure goes stale every time papers are added.
`site/data.json` is written as well, for anything that wants the data
programmatically, and it is what the callers of `export_site_data.py` should use.
That script takes `--lang <code>` and defaults to `en`; pass a language to get a
payload whose notes are already in it.

If you ever want the smaller `index.html` more than you want double-click preview, switch
`app.js` to read `./data.json` — but then the site only works over HTTP, and the
no-JavaScript rendering below becomes the only thing a `file://` visitor sees.

## Maintaining the data side

`id` is the permanent URL key for a paper. Every existing `id` is already unique
lower-case ASCII, so nothing needed to be added to the data. Two rules follow:

- **Never rename an existing `id`.** External links and the JSON payload both key on it.
- New ids must be lower-case ASCII and globally unique.

(A handful of existing ids are truncated slugs and end in a hyphen, like
`...-for-low-`. They are ugly but deliberate: the id is permanent, so a tidier
spelling would mean a broken external reference. New ids should not do this.)

`abbr` and `title` are display text and may change freely.

`scripts/export_site_data.py` calls `build.py`'s own `validate()`, so a corpus that would
fail CI also fails the site build, with the same diagnostics. There is no second
validator to keep in sync.

## Failure modes seen so far

| Symptom | Cause |
| --- | --- |
| Tabs switch, but a `?q=` deep link shows every paper | The initial state was read from the URL but nothing re-rendered. The served HTML already contains every row, so the page *looks* fine — this is why it hid. `init()` must call `apply()` after `readUrl()`. |
| `init()` dies silently and nothing is interactive | `history.replaceState` throws on `file://`. It is wrapped in `try/catch`; keep it that way. |
| A custom-domain deploy is rejected at build time | Working as intended: a `github.io` URL leaked into the output. Fix the value that produced it rather than removing the check. |
| Empty topic chips, or a table with no rows | The corresponding `data/*.yaml` list is empty. `build_site.py` renders whatever is there. |

## Verifying a build

Eyeballing is not enough — the failure mode above looks correct on screen. Headless
Chrome will load the page, run the JavaScript and dump the resulting DOM:

```bash
chrome --headless=new --disable-gpu --user-data-dir=/tmp/prof \
       --virtual-time-budget=5000 --dump-dom "file:///abs/path/to/site/index.html?q=diffusion"
```

Then check `<strong id="count">` against what the filter should have produced. Load the
page with `?topic=sparse-view`, `?code=1`, `?type=preprint`, `?from=2024`, `?sort=old` and
a query that is a bare arXiv id (`?q=2607.14415`, which should return exactly 1) — between
them those exercise every filter. A clean run also means no console errors, so add
`--enable-logging=stderr` and read stderr.
