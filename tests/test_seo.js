/* Structured-data and changelog checks against the built site.
 *
 * Reads the generated files under site/ (run `python scripts/build_site.py`
 * first) and checks what search engines read rather than what users click:
 *
 *   - the homepage DataCatalog JSON-LD (English and Chinese) sits beside the
 *     Organization / WebSite / ItemList blocks, references the Organization,
 *     and its counts and dateModified equal the live payload in data.json —
 *     the same numbers the stat tiles show;
 *   - /changelog/ and /zh/changelog/ exist with their own title, description,
 *     canonical, hreflang (each language + x-default) and BreadcrumbList, list
 *     every CHANGELOG.md entry newest first, and are in sitemap.xml, llms.txt
 *     and the About page body;
 *   - every dataset, benchmark and guide page (and the /datasets/ and /guides/
 *     indexes): unique title and description, canonical, hreflang, a
 *     BreadcrumbList, working internal links, an inbound link (no orphans);
 *     the Dataset JSON-LD agrees with the visible name, description, licence,
 *     DOI and citation; each guide's FAQPage JSON-LD equals its visible FAQ and
 *     its Article dateModified equals the visible last-updated date.
 *
 * No packages needed, so it runs in CI next to test_search.js.
 *
 *     python scripts/build_site.py
 *     node tests/test_seo.js
 */
"use strict";

const fs = require("fs");
const path = require("path");

const REPO = path.resolve(__dirname, "..");
const SITE = path.join(REPO, "site");
const ORIGIN = "https://computedtomography.org/";

if (!fs.existsSync(path.join(SITE, "index.html"))) {
  console.error("site/index.html is missing — build the site first:\n" +
    "  python scripts/build_site.py");
  process.exit(2);
}

let pass = 0;
const failures = [];
function ok(name, cond, detail) {
  if (cond) { pass++; console.log("  ✓ " + name + (detail ? "  (" + detail + ")" : "")); return; }
  failures.push(name + (detail ? "  → " + detail : ""));
  console.log("  ✗ " + name + (detail ? "  (" + detail + ")" : ""));
}
const read = (rel) => fs.readFileSync(path.join(SITE, rel), "utf8");

function jsonld(html) {
  const out = [];
  const re = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g;
  let m;
  while ((m = re.exec(html))) out.push(JSON.parse(m[1]));
  return out;
}
function attr(html, re) { const m = html.match(re); return m ? m[1] : null; }

/* CHANGELOG.md's own dates, file order. */
const clDates = fs.readFileSync(path.join(REPO, "CHANGELOG.md"), "utf8")
  .split("\n").filter((l) => l.startsWith("## ")).map((l) => l.slice(3, 13));

const LANGS = [
  { code: "en", prefix: "", hreflang: "en" },
  { code: "zh", prefix: "zh/", hreflang: "zh-Hans" }
];

const titles = new Set();
const descs = new Set();
const sitemap = read("sitemap.xml");
const llms = read("llms.txt");

for (const L of LANGS) {
  console.log("\n[" + L.code + "] homepage DataCatalog");
  const base = ORIGIN + L.prefix;
  const home = read(L.prefix + "index.html");
  const data = JSON.parse(read(L.prefix + "data.json"));
  const blocks = jsonld(home);
  const types = blocks.map((b) => b["@type"]);
  ["Organization", "WebSite", "ItemList", "DataCatalog"].forEach((t) =>
    ok(t + " JSON-LD present", types.includes(t), types.join(", ")));
  const org = blocks.find((b) => b["@type"] === "Organization") || {};
  const cat = blocks.find((b) => b["@type"] === "DataCatalog") || {};
  ok("url is the page URL", cat.url === base, cat.url);
  ok("name matches the page title", cat.name &&
     home.includes("<title>" + cat.name.replace(/&/g, "&amp;")), cat.name);
  const metaDesc = attr(home, /<meta name="description" content="([^"]*)">/);
  ok("description equals the meta description",
     metaDesc && metaDesc.replace(/&amp;/g, "&") === cat.description);
  ok("inLanguage", cat.inLanguage === L.hreflang, cat.inLanguage);
  ok("license is CC BY-NC-SA 4.0",
     cat.license === "https://creativecommons.org/licenses/by-nc-sa/4.0/");
  ok("dateModified is data's last_updated", cat.dateModified === data.counts.updated,
     cat.dateModified + " vs " + data.counts.updated);
  ok("the Updated stat tile shows the same date",
     home.includes("<dd>" + data.counts.updated + "</dd>"));
  ok("creator and publisher reference the Organization",
     cat.creator && cat.publisher && cat.creator["@id"] === org["@id"] &&
     cat.publisher["@id"] === org["@id"], org["@id"]);
  const ds = cat.dataset || [];
  ok("three datasets", ds.length === 3, String(ds.length));
  for (const key of ["papers", "datasets", "benchmarks"]) {
    const d = ds.find((x) => x["@id"] === base + "#dataset-" + key) || {};
    const n = data.counts[key];
    ok("dataset " + key + ": count " + n + " from live data",
       typeof d.description === "string" && d.description.startsWith(n + " "), d.description);
    ok("dataset " + key + ": same count on a stat tile", home.includes("<dd>" + n + "</dd>"));
    ok("dataset " + key + ": dateModified + license", d.dateModified === data.counts.updated &&
       d.license === cat.license);
  }

  console.log("\n[" + L.code + "] changelog page");
  const url = base + "changelog/";
  const rel = L.prefix + "changelog/index.html";
  ok("page written", fs.existsSync(path.join(SITE, rel)));
  const page = read(rel);
  const title = attr(page, /<title>([^<]*)<\/title>/);
  const desc = attr(page, /<meta name="description" content="([^"]*)">/);
  ok("has a title and a description", !!title && !!desc && desc.length > 50, title);
  titles.add(title); descs.add(desc);
  ok("canonical", page.includes('<link rel="canonical" href="' + url + '">'));
  for (const [hl, u] of [["en", ORIGIN + "changelog/"],
                         ["zh-Hans", ORIGIN + "zh/changelog/"],
                         ["x-default", ORIGIN + "changelog/"]]) {
    ok("hreflang " + hl, page.includes('<link rel="alternate" hreflang="' + hl + '" href="' + u + '">'));
  }
  const crumbs = jsonld(page).find((b) => b["@type"] === "BreadcrumbList");
  ok("BreadcrumbList ends at this page", !!crumbs &&
     crumbs.itemListElement[crumbs.itemListElement.length - 1].item === url &&
     crumbs.itemListElement[0].item === base);
  const dates = [...page.matchAll(/<article class="cl-entry" id="[^"]+"(?: lang="[^"]+")?>\s*<h2><a href="#[^"]+"><time datetime="(\d{4}-\d{2}-\d{2})">/g)]
    .map((m) => m[1]);
  ok("every CHANGELOG.md entry is listed", dates.length === clDates.length,
     dates.length + " of " + clDates.length);
  ok("entries are newest first", dates.every((d, i) => i === 0 || dates[i - 1] >= d));
  ok("same multiset of dates as CHANGELOG.md",
     JSON.stringify([...dates].sort()) === JSON.stringify([...clDates].sort()));
  ok("no template placeholder leaked", !/\{\{[A-Z_]+\}\}/.test(page));
  const fallback = (page.match(/<article class="cl-entry" id="[^"]+" lang="en">/g) || []).length;
  if (L.code === "en") {
    ok("English entries carry no lang override", !/class="cl-entry" id="[^"]+" lang=/.test(page));
  } else {
    // Translated entries are matched by date + English title; every heading in
    // CHANGELOG.zh-CN.md must reach the page, and only untranslated entries
    // may fall back to English, with the page saying how many.
    const zhHeads = fs.readFileSync(path.join(REPO, "CHANGELOG.zh-CN.md"), "utf8")
      .split("\n").filter((l) => l.startsWith("## ")).map((l) => l.slice(3).replace(/^\S+\s+\S+\s+/, ""));
    const shown = [...page.matchAll(/<time datetime="[^"]+">[^<]+<\/time><\/a> \u2014 ([^<]*)<\/h2>/g)].map((m) => m[1]);
    const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const plain = (h) => esc(h.replace(/`([^`]+)`/g, "$1"));
    const strip = (h) => h.replace(/<[^>]+>/g, "");
    ok("every translated entry is shown in Chinese",
       zhHeads.every((h) => shown.map(strip).includes(plain(h))), zhHeads.length + " translations");
    ok("translated + English fallbacks = all entries",
       zhHeads.length + fallback === clDates.length, zhHeads.length + " + " + fallback + " of " + clDates.length);
    ok("untranslated note shown only when something falls back",
       (fallback > 0) === page.includes("暂以英文显示"));
    ok("no blanket 'entries are in English' notice", !page.includes("各条目以英文记录"));
  }
  ok("in sitemap.xml", sitemap.includes("<loc>" + url + "</loc>"));
  ok("in llms.txt", llms.includes(url));
  const about = read(L.prefix + "about/index.html");
  const main = (about.match(/<main\b[\s\S]*?<\/main>/) || [""])[0];
  ok("linked from the About page body", main.includes('href="../changelog/"'));
  const homeMain = (home.match(/<main\b[\s\S]*?<\/main>/) || [""])[0];
  ok("not linked from the homepage body", !homeMain.includes("changelog/"));
}

/* ---------------------------------------------------------------------------
 * Dataset / benchmark pages, the /datasets/ index and the guides.
 */
const text = (h) => h.replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<")
  .replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'")
  .replace(/\s+/g, " ").trim();
const mainOf = (h) => (h.match(/<main\b[\s\S]*?<\/main>/) || [""])[0];
const fileFor = (u) => path.join(SITE, u.slice(ORIGIN.length), "index.html");
/* Resolve every relative href in a page to a site URL (or null if outside). */
function internalLinks(h, pageUrl) {
  const out = [];
  for (const m of mainOf(h).matchAll(/href="([^"#?]*)(?:[?#][^"]*)?"/g)) {
    const href = m[1];
    if (/^(https?:|mailto:)/.test(href)) continue;
    out.push(new URL(href || "./", pageUrl).href);
  }
  return out;
}
const newUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1])
  .filter((u) => /\/(datasets|benchmarks|guides)\//.test(u));

for (const L of LANGS) {
  const base = ORIGIN + L.prefix;
  const mine = newUrls.filter((u) => u.startsWith(base) && (L.prefix || !u.startsWith(ORIGIN + "zh/")));
  const resources = mine.filter((u) => /\/(datasets|benchmarks)\/[^/]+\/$/.test(u));
  const guides = mine.filter((u) => /\/guides\/[^/]+\/$/.test(u));
  console.log("\n[" + L.code + "] dataset, benchmark and guide pages");
  ok("/datasets/ and /guides/ in sitemap", mine.includes(base + "datasets/") && mine.includes(base + "guides/"));
  ok("at least one dataset and one benchmark page", resources.some((u) => u.includes("/datasets/")) &&
     resources.some((u) => u.includes("/benchmarks/")), resources.length + " pages");
  ok("three guides", guides.length === 3, String(guides.length));

  const home = read(L.prefix + "index.html");
  const homeLd = jsonld(home).find((b) => b["@type"] === "DataCatalog") || {};
  const ptitles = new Set(), pdescs = new Set();
  const inbound = {};
  let bad = [];
  for (const url of mine) {
    const f = fileFor(url);
    if (!fs.existsSync(f)) { bad.push(url + ": file missing"); continue; }
    const h = fs.readFileSync(f, "utf8");
    const title = attr(h, /<title>([^<]*)<\/title>/);
    const desc = attr(h, /<meta name="description" content="([^"]*)">/);
    if (!title || ptitles.has(title)) bad.push(url + ": title missing or duplicate");
    if (!desc || desc.length < (L.code === "zh" ? 25 : 50) || pdescs.has(desc)) bad.push(url + ": description missing, short or duplicate");
    ptitles.add(title); pdescs.add(desc);
    if (!h.includes('<link rel="canonical" href="' + url + '">')) bad.push(url + ": canonical");
    const rel = url.slice(base.length);
    for (const [hl, u] of [["en", ORIGIN + rel], ["zh-Hans", ORIGIN + "zh/" + rel], ["x-default", ORIGIN + rel]]) {
      if (!h.includes('<link rel="alternate" hreflang="' + hl + '" href="' + u + '">')) bad.push(url + ": hreflang " + hl);
    }
    const blocks = jsonld(h);
    const crumbs = blocks.find((b) => b["@type"] === "BreadcrumbList");
    if (!crumbs || crumbs.itemListElement[0].item !== base ||
        crumbs.itemListElement[crumbs.itemListElement.length - 1].item !== url) bad.push(url + ": BreadcrumbList");
    if (/\{\{[A-Z_]+\}\}/.test(h)) bad.push(url + ": placeholder leaked");
    for (const target of internalLinks(h, url)) {
      if (!target.startsWith(ORIGIN)) continue;
      const tf = path.join(SITE, target.slice(ORIGIN.length), target.endsWith("/") ? "index.html" : "");
      if (!fs.existsSync(tf)) bad.push(url + ": broken internal link " + target);
      if (target !== url) (inbound[target] = inbound[target] || []).push(url);
    }
    const main = mainOf(h);
    if (resources.includes(url)) {
      const ds = blocks.find((b) => b["@type"] === "Dataset");
      if (!ds) { bad.push(url + ": no Dataset JSON-LD"); continue; }
      const h1 = text((main.match(/<h1>([\s\S]*?)<\/h1>/) || ["", ""])[1]);
      const lede = text((main.match(/<p class="lede">([\s\S]*?)<\/p>/) || ["", ""])[1]);
      if (ds.name !== h1) bad.push(url + ": Dataset name != h1");
      if (ds.description !== lede) bad.push(url + ": Dataset description != visible lede");
      if (ds.url !== url) bad.push(url + ": Dataset url");
      if (ds.license && !(main.includes('href="' + ds.license + '"') || text(main).includes(ds.license)))
        bad.push(url + ": license not visible");
      [].concat(ds.identifier || []).forEach((id) => {
        if (!main.includes(id.replace("https://doi.org/", ""))) bad.push(url + ": identifier not visible");
      });
      (ds.citation || []).forEach((c) => { if (!text(main).includes(c.name)) bad.push(url + ": citation not visible"); });
      (ds.sameAs || []).forEach((u) => { if (!main.includes('href="' + u + '"')) bad.push(url + ": sameAs not visible"); });
      if (!ds.includedInDataCatalog || ds.includedInDataCatalog["@id"] !== homeLd["@id"])
        bad.push(url + ": includedInDataCatalog does not point at the homepage DataCatalog");
    }
    if (guides.includes(url)) {
      const faq = blocks.find((b) => b["@type"] === "FAQPage");
      const art = blocks.find((b) => b["@type"] === "Article");
      const sec = (main.match(/<section class="faq">([\s\S]*?)<\/section>/) || ["", ""])[1];
      const pairs = [...sec.matchAll(/<h3>([\s\S]*?)<\/h3>\s*<p>([\s\S]*?)<\/p>/g)].map((m) => [text(m[1]), text(m[2])]);
      if (!faq || !pairs.length || faq.mainEntity.length !== pairs.length ||
          faq.mainEntity.some((q, i) => q.name !== pairs[i][0] || q.acceptedAnswer.text !== pairs[i][1]))
        bad.push(url + ": FAQPage JSON-LD does not match the visible FAQ");
      const shown = attr(main, /<p class="updated">[^<]*<time datetime="(\d{4}-\d{2}-\d{2})">/);
      if (!art || !shown || art.dateModified !== shown) bad.push(url + ": visible last-updated date != Article dateModified");
      if (!/<table class="grid"/.test(main)) bad.push(url + ": no comparison table");
      if (!/href="\.\.\/\.\.\/topics\/[^"]+\/"/.test(main) && !/href="\.\.\/\.\.\/datasets\//.test(main))
        bad.push(url + ": links to no topic or dataset page");
    }
    if (llms.indexOf(url) === -1 && L.code === "en") bad.push(url + ": not in llms.txt");
  }
  ok("every new page: title, description, canonical, hreflang, BreadcrumbList, links",
     bad.length === 0, bad.slice(0, 5).join("; ") || (mine.length + " pages"));
  ok("titles and descriptions unique", ptitles.size === mine.length && pdescs.size === mine.length);

  const idx = read(L.prefix + "datasets/index.html");
  ok("/datasets/ links every dataset and benchmark page",
     resources.every((u) => idx.includes('href="../' + u.slice(base.length) + '"')), resources.length + " pages");
  const gidx = read(L.prefix + "guides/index.html");
  ok("/guides/ links every guide", guides.every((u) => gidx.includes('href="../' + u.slice(base.length) + '"')));
  const about = mainOf(read(L.prefix + "about/index.html"));
  ok("About links /datasets/ and /guides/", about.includes('href="../datasets/"') && about.includes('href="../guides/"'));
  const orphans = mine.filter((u) => u !== base + "datasets/" && u !== base + "guides/" && !(inbound[u] || []).length);
  ok("no orphan pages", orphans.length === 0, orphans.join(", "));
  // Topic pages link the dataset pages they list and the relevant guides.
  let topicLinks = 0, topicBroken = [];
  for (const t of fs.readdirSync(path.join(SITE, L.prefix, "topics"))) {
    const tu = base + "topics/" + t + "/";
    const th = read(L.prefix + "topics/" + t + "/index.html");
    for (const target of internalLinks(th, tu)) {
      if (/\/(datasets|benchmarks|guides)\//.test(target)) {
        topicLinks++;
        if (!fs.existsSync(path.join(SITE, target.slice(ORIGIN.length), "index.html"))) topicBroken.push(target);
      }
    }
  }
  ok("topic pages link dataset/benchmark pages and guides", topicLinks > 0 && !topicBroken.length,
     topicLinks + " links" + (topicBroken.length ? ", broken: " + topicBroken.join(", ") : ""));
  // The homepage links the new pages only from its Datasets, Benchmarks and
  // Learning tabs, which web/app.js renders from data.json: a row's `page`
  // and the Guides group. Exactly these links: every page row and guide, plus
  // the /guides/ index, nothing else, and each resolves to a built page.
  const homeMain = mainOf(home);
  const data = JSON.parse(read(L.prefix + "data.json"));
  const pageRels = [].concat(data.datasets, data.benchmarks).filter((r) => r.page).map((r) => r.page);
  const G = data.guides || {};
  const homeRels = pageRels.concat((G.items || []).map((g) => g.url), G.index ? [G.index] : []);
  const wantRels = resources.concat(guides).map((u) => u.slice(base.length)).concat(["guides/"]);
  const same = (a, b) => a.length === b.length && [...a].sort().join("|") === [...b].sort().join("|");
  ok("homepage links exactly the dataset/benchmark pages, the guides and /guides/",
     same(homeRels, wantRels), pageRels.length + " entries + " + (G.items || []).length + " guides + index");
  const missing = homeRels.filter((r) => !fs.existsSync(path.join(SITE, L.prefix, r, "index.html")));
  ok("every homepage detail/guide link resolves to a built page", missing.length === 0, missing.join(", "));
  const allowed = new Set(wantRels);
  const stray = [...homeMain.matchAll(/href="(?!https?:)([^"]*(?:datasets|guides|benchmarks)\/[^"]*)"/g)]
    .map((m) => m[1].replace(/^\.\//, "")).filter((h) => !allowed.has(h));
  ok("homepage body: no other link to the new pages", stray.length === 0, stray.join(", "));
}

/* ---------------------------------------------------------------------------
 * Curated lineage pages (/graph/lineage/<id>/): static card chains under
 * the graph index. Scoped strictly to the /graph/lineage/ prefix — the
 * dataset/benchmark/guide sweep above keys on URL segments and must
 * never grow to cover these (the 2026-10-22 /graph/datasets/ incident),
 * so lineage pages get their own block instead.
 */
const lineageUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1])
  .filter((u) => u.includes("/graph/lineage/"));

for (const L of LANGS) {
  const base = ORIGIN + L.prefix;
  const mine = lineageUrls.filter((u) => u.startsWith(base) && (L.prefix || !u.startsWith(ORIGIN + "zh/")));
  console.log("\n[" + L.code + "] curated lineage pages");
  ok("at least one lineage page in the sitemap", mine.length > 0, mine.length + " pages");
  const ltitles = new Set(), ldescs = new Set();
  const gindex = read(L.prefix + "graph/index.html");
  let bad = [];
  for (const url of mine) {
    const f = fileFor(url);
    if (!fs.existsSync(f)) { bad.push(url + ": file missing"); continue; }
    const h = fs.readFileSync(f, "utf8");
    const title = attr(h, /<title>([^<]*)<\/title>/);
    const desc = attr(h, /<meta name="description" content="([^"]*)">/);
    if (!title || ltitles.has(title)) bad.push(url + ": title missing or duplicate");
    if (!desc || ldescs.has(desc)) bad.push(url + ": description missing or duplicate");
    ltitles.add(title); ldescs.add(desc);
    if (!h.includes('<link rel="canonical" href="' + url + '">')) bad.push(url + ": canonical");
    const rel = url.slice(base.length);
    for (const [hl, u] of [["en", ORIGIN + rel], ["zh-Hans", ORIGIN + "zh/" + rel], ["x-default", ORIGIN + rel]]) {
      if (!h.includes('<link rel="alternate" hreflang="' + hl + '" href="' + u + '">')) bad.push(url + ": hreflang " + hl);
    }
    const crumbs = jsonld(h).find((b) => b["@type"] === "BreadcrumbList");
    if (!crumbs || crumbs.itemListElement[crumbs.itemListElement.length - 1].item !== url)
      bad.push(url + ": BreadcrumbList does not end at this page");
    if (/\{\{[A-Z_]+\}\}/.test(h)) bad.push(url + ": placeholder leaked");
    if (!gindex.includes('href="' + rel.slice("graph/".length) + '"'))
      bad.push(url + ": graph index does not link it (orphan)");
    for (const target of internalLinks(h, url)) {
      if (!target.startsWith(ORIGIN)) continue;
      const tf = path.join(SITE, target.slice(ORIGIN.length), target.endsWith("/") ? "index.html" : "");
      if (!fs.existsSync(tf)) bad.push(url + ": broken internal link " + target);
    }
    if (L.code === "en" && !llms.includes(url)) bad.push(url + ": not in llms.txt");
  }
  ok("every lineage page: title, description, canonical, hreflang, BreadcrumbList, index link, working links",
     bad.length === 0, bad.slice(0, 5).join("; ") || (mine.length + " pages"));
  ok("lineage titles and descriptions unique", ltitles.size === mine.length && ldescs.size === mine.length);
}

console.log("\nacross languages");
ok("titles are unique per language", titles.size === LANGS.length);
ok("descriptions are unique per language", descs.size === LANGS.length);

console.log("\n%d passed, %d failed", pass, failures.length);
if (failures.length) {
  failures.forEach((f) => console.log("  ✗ " + f));
  process.exit(1);
}
console.log("seo checks passed ✓");
