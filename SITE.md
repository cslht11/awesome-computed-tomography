# The website

Who this is for: anyone with commit access who has to build, deploy or change the
website. If you only want to *add an entry*, read [MAINTENANCE.md](MAINTENANCE.md#adding-entries) —
you never need to touch anything described here.

The site is a second rendering of the same corpus that produces `README.md`. Both read
`data/*.yaml`, so they cannot disagree.

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
| `web/index.html` | yes | Template with `{{PLACEHOLDER}}` markers. Not served directly. |
| `web/styles.css` | yes | All styling. Light and dark token sets. |
| `web/app.js` | yes | Client-side search and filtering. |
| `scripts/export_site_data.py` | yes | `data/*.yaml` -> the JSON payload. Also usable on its own. |
| `scripts/build_site.py` | yes | Assembles template + payload + origin into `site/`. |
| `site/` | **no** | Build output. Git-ignored. Delete it freely; it is regenerated. |

The licence in the page footer, the JSON-LD `license` field and the
`<link rel="license">` tag all come from `code_license` / `content_license` /
`content_license_url` in `site.config.yml`. Content and code are licensed
separately — the reasoning is in [MAINTENANCE.md](MAINTENANCE.md).

## Build and preview

```bash
python scripts/build_site.py            # writes site/
python scripts/build_site.py --url https://example.org/   # one-off origin override
python -m http.server 8899 -d site      # then open http://127.0.0.1:8899/
```

`site/index.html` also opens correctly by **double-clicking** it — see the two design
constraints below, which exist specifically to keep that working.

The build prints the size summary and, if `url` is empty, a note that the GitHub Pages
address was used.

## Deploying

**Live at <https://computedtomography.org/>**, and published automatically:
`.github/workflows/deploy.yml` runs on every push to `main` and rebuilds `site/` from
`data/*.yaml`. Nothing generated is committed.

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

The workflow runs `build.py --check` before building the site, so a PR that leaves
`README.md` stale fails here too. `.github/workflows/validate.yml` *also* runs
`build_site.py` on every push, so a change that breaks the site fails
CI rather than surfacing at the next deploy.

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

- **Search** — filters as you type (120 ms debounce). Multiple words are AND-ed. Matches
  are highlighted in the titles.
- **Filters** — 17 topic chips (multi-select, with counts), `All / Peer-reviewed /
  Preprints`, `has code`, `from <year>`, and sorting by newest, oldest or title.
- **Tabs** — Papers, Toolkits, Datasets, Benchmarks, Learning.
- **Deep links** — the whole filter state lives in the URL
  (`?q=&topic=&type=&code=&from=&sort=&tab=`), so any view can be shared. There is a
  *copy link* button.
- **`/`** focuses the search box.
- **Light and dark**, following the system, with a manual toggle remembered in
  `localStorage`.
- **Works without JavaScript.** The 391 paper rows are rendered into the HTML at build
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
is blocked on `file://`. The cost is size: `index.html` is ~404 KB raw, **73 KB gzipped**,
and the largest part of it is the inlined JSON. First paint is about 82 KB gzipped across
three files. `site/data.json` is written as well, for anything that wants the data
programmatically, and it is what the callers of `export_site_data.py` should use.

If you ever want the smaller `index.html` more than you want double-click preview, switch
`app.js` to read `./data.json` — but then the site only works over HTTP, and the
no-JavaScript rendering below becomes the only thing a `file://` visitor sees.

## Maintaining the data side

`id` is the permanent URL key for a paper. All 391 existing ids are already unique,
kebab-case ASCII, so nothing needed to be added to the data. Two rules follow:

- **Never rename an existing `id`.** External links and the JSON payload both key on it.
- New ids must be lower-case kebab-case ASCII and globally unique.

`abbr` and `title` are display text and may change freely.

`scripts/export_site_data.py` calls `build.py`'s own `validate()`, so a corpus that would
fail CI also fails the site build, with the same diagnostics. There is no second
validator to keep in sync.

## Failure modes seen so far

| Symptom | Cause |
| --- | --- |
| Tabs switch, but a `?q=` deep link shows all 391 papers | The initial state was read from the URL but nothing re-rendered. The served HTML already contains all 391 rows, so the page *looks* fine — this is why it hid. `init()` must call `apply()` after `readUrl()`. |
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
