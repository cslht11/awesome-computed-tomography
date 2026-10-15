# Tests

Two suites for `web/search.js`, and one for the structured data search engines
read. Run the site build first — all three read the generated files under
`site/`, which is git-ignored.

```bash
python scripts/build_site.py
node tests/test_search.js          # runs in CI; no packages needed
node tests/test_seo.js             # runs in CI; no packages needed
node tests/test_site_dom.js        # local only; needs jsdom
```

## `test_seo.js` — structured data and the changelog page

Checks the homepage `DataCatalog` JSON-LD (English and Chinese) against the
live `data.json` — counts, `dateModified`, the Organization reference — and the
`/changelog/` pages: canonical, hreflang, `BreadcrumbList`, every
`CHANGELOG.md` entry listed newest first, every `CHANGELOG.zh-CN.md`
translation shown on `/zh/changelog/` (untranslated entries fall back to
English, and the page says how many), and presence in `sitemap.xml`,
`llms.txt` and the About page body. No dependencies, so it runs in
`validate.yml`.

## `test_search.js` — the search core

Tokenising, field weighting, ranking, tie stability, the Latin substring
fallback, CJK recall across a gap, and that highlighting cannot emit markup.
Loads `web/search.js` into a Node sandbox and runs it against both the English
and the Chinese payload, because Chinese query quality depends on the Chinese
topic names and notes, and those exist only in the zh payload.

No dependencies, so this is the one wired into `validate.yml`.

## `test_site_dom.js` — the built pages

Loads `site/index.html` and `site/zh/index.html` in jsdom with their real
scripts, then types into both search boxes and inspects what got rendered. It
asserts, among other things, that every section table has rows — which is how it
catches a render throwing and silently aborting `init()` before the search box
is wired. That failure mode is invisible in the served HTML, because the HTML is
server-rendered and still looks complete.

Needs jsdom:

```bash
npm install --prefix /tmp/ct-test jsdom
NODE_PATH=/tmp/ct-test/node_modules node tests/test_site_dom.js
```

> Install into a scratch prefix. `npm install` without `--prefix` writes to
> `~/node_modules`, which on a developer machine is usually where editor tooling
> (vue-language-server, pyright, playwright) keeps its packages.

### Why this one is not in CI

It would have to `npm install` on every run, and a job that can go red because a
registry was unreachable is worse than no job: people learn to ignore red. The
same argument SITE.md makes for keeping the deploy workflow off pull requests.
Run it by hand before pushing anything that touches `web/`.
