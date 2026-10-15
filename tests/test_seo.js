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
 *     and the About page body.
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

console.log("\nacross languages");
ok("titles are unique per language", titles.size === LANGS.length);
ok("descriptions are unique per language", descs.size === LANGS.length);

console.log("\n%d passed, %d failed", pass, failures.length);
if (failures.length) {
  failures.forEach((f) => console.log("  ✗ " + f));
  process.exit(1);
}
console.log("seo checks passed ✓");
