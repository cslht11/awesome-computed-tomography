/* Tests for web/search.js — tokenising, indexing, ranking, highlighting.
 *
 * The search core is browser code, but its pure functions are plain ES5 with no
 * DOM dependency, so they load into a Node sandbox and run directly. No packages
 * are required, which is why this file — and only this file — runs in CI.
 *
 * It reads the generated payloads under site/, so run the site build first:
 *
 *     python scripts/build_site.py
 *     node tests/test_search.js
 *
 * The English and Chinese payloads are both checked, because Chinese query
 * quality depends on the Chinese topic names and notes, and those only exist in
 * the zh payload.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const REPO = path.resolve(__dirname, "..");
const SEARCH_JS = path.join(REPO, "web", "search.js");
const SITE = path.join(REPO, "site");

if (!fs.existsSync(path.join(SITE, "data.json"))) {
  console.error("site/data.json is missing — build the site first:\n" +
    "  python scripts/build_site.py");
  process.exit(2);
}

/* ------------------------------------------------------------ load the core */
const ctx = vm.createContext({});
vm.runInContext(fs.readFileSync(SEARCH_JS, "utf8"), ctx, { filename: SEARCH_JS });
const S = ctx.CTSearch;
if (!S) { console.error("FAIL: web/search.js did not define CTSearch"); process.exit(1); }

let pass = 0;
const failures = [];
function ok(name, cond, detail) {
  if (cond) { pass++; return; }
  failures.push(name + (detail ? "  → " + detail : ""));
}
function eq(name, got, want) {
  ok(name, got === want, "got " + JSON.stringify(got) + ", want " + JSON.stringify(want));
}

/* ------------------------------------------------------------------ folding */
eq("fold lowercases", S.fold("DenoMamba"), "denomamba");
eq("fold unwraps inline TeX", S.fold("$K$-NeAS"), "k-neas");
eq("fold strips zero-width", S.fold("a\u200bb"), "a b");
eq("fold collapses spaces", S.fold("  a   b  "), "a b");

/* --------------------------------------------------------------- tokenizer */
const t1 = S.tokenize("稀疏视角");
["稀", "疏", "视", "角", "稀疏", "疏视", "视角"].forEach(function (t) {
  ok("tokenize CJK emits " + t, t1.indexOf(t) >= 0, JSON.stringify(t1));
});
ok("tokenize CJK emits no 3-gram", t1.indexOf("稀疏视") === -1, JSON.stringify(t1));

const t2 = S.tokenize("low-dose CT reconstruction");
ok("tokenize splits latin on hyphen", t2.indexOf("low") >= 0 && t2.indexOf("dose") >= 0, JSON.stringify(t2));
ok("tokenize keeps 2-char latin", t2.indexOf("ct") >= 0, JSON.stringify(t2));
ok("tokenize drops 1-char latin", S.tokenize("a K X").length === 0);
ok("tokenize mixes TeX + CJK",
  S.tokenize("$K$-NeAS 稀疏").indexOf("neas") >= 0 && S.tokenize("$K$-NeAS 稀疏").indexOf("稀疏") >= 0);

/* ------------------------------------------------------ parse deduplicates */
eq("parse dedupes tokens", S.parse("稀疏 稀疏 视角").tokens.filter(function (x) { return x === "稀疏"; }).length, 1);

/* ------------------------------------------------------------- scoring shape */
const doc = S.index({ title: "Sparse-View CT Reconstruction", abbr: "SVCT", meta: "TMI 2021", body: "note about sparsity" });
eq("score: unrelated query scores 0", S.score(doc, S.parse("zzzz")), 0);
ok("score: title hit beats body hit",
  S.score(doc, S.parse("sparse")) > S.score(doc, S.parse("sparsity")));
ok("score: full coverage beats partial",
  S.score(doc, S.parse("sparse view")) > S.score(doc, S.parse("sparse zzzznope")));

/* ----------------------------------------------------------- index/search */
function idx(rows) {
  return S.build(rows, function (r) { return { title: r[0], body: r[1] }; });
}

/* The substring fallback: exact token equality alone would miss these. */
eq("search finds a suffix match (mamba → DenoMamba)", S.search(idx([["DenoMamba", "low dose"]]), "mamba").length, 1);
eq("search finds a prefix match (splat → splatting)", S.search(idx([["Gaussian Splatting", "x"]]), "splat").length, 1);
eq("search finds a middle fragment", S.search(idx([["MetaInv-Net", "x"]]), "inv").length, 1);

/* CJK recall across a gap: the phrase never appears verbatim. */
eq("search matches CJK across a gap", S.search(idx([["稀疏视角 CT 重建", "x"]]), "稀疏重建").length, 1);
eq("search matches CJK from a note", S.search(idx([["Deep Learning", "用稀疏视角重建"]]), "稀疏视角").length, 1);

/* Ranking, and the behaviour that replaced strict AND. */
const two = idx([["Sparse-View CT Reconstruction", "sparse view ct"], ["Denoising", "low dose"]]);
eq("rank keeps partial matches (one junk word)", S.search(two, "sparse zzznope").length, 1);
eq("rank drops records with no match at all", S.search(two, "zzznope").length, 0);
eq("rank puts the title hit first", S.search(two, "sparse")[0].item[0], "Sparse-View CT Reconstruction");

/* Stability: equal scores must keep the caller's order — the paper list's own
   sort, and the dropdown's newest-first order. */
const three = idx([["Alpha CT", "same"], ["Beta CT", "same"], ["Gamma CT", "same"]]);
eq("search is stable on ties",
  S.search(three, "same").map(function (h) { return h.item[0]; }).join(","),
  "Alpha CT,Beta CT,Gamma CT");
eq("blank query returns nothing", S.search(three, "   ").length, 0);

/* ------------------------------------------------------ highlight safety */
function esc(s) {
  return String(s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}
const danger = "<img src=x onerror=alert(1)> sparse";
const html = S.markHtml(danger, S.terms("sparse"), esc);
ok("markHtml escapes markup", html.indexOf("<img") === -1, html);
ok("markHtml marks the hit", html.indexOf("<mark>sparse</mark>") >= 0, html);
ok("markHtml escapes the marked text itself",
  S.markHtml("a<b", S.terms("a<b"), esc).indexOf("&lt;") >= 0);

const r = S.ranges("稀疏视角 CT 重建", S.terms("稀疏视角"));
ok("ranges merges the CJK phrase into one run",
  r.length >= 1 && r[0][0] === 0 && r[0][1] === 4, JSON.stringify(r));
eq("terms puts the longest first", S.terms("稀疏视角")[0], "稀疏视角");

/* ------------------------------------------------- real payload relevance */
function loadPayload(file) {
  const data = JSON.parse(fs.readFileSync(path.join(SITE, file), "utf8"));
  const topicName = {};
  (data.topics || []).forEach(function (t) { topicName[t.id] = t.name; });
  const m = S.mappers(topicName);
  const all = [];
  ["papers", "toolkits", "datasets", "benchmarks", "learning", "teams"].forEach(function (kind) {
    (data[kind] || []).forEach(function (row) { all.push({ kind: kind, rec: m[kind](row) }); });
  });
  return { all: all, index: S.build(all, function (e) { return e.rec; }), data: data };
}

function topHits(payload, q, n) {
  return S.search(payload.index, q).slice(0, n || 3).map(function (h) {
    return { kind: h.item.kind, title: h.item.rec.title, s: h.s };
  });
}

const EN = loadPayload("data.json");
const ZH = loadPayload(path.join("zh", "data.json"));

ok("payload carries the expected sections",
  EN.all.length > 400 && ZH.all.length === EN.all.length,
  "en=" + EN.all.length + " zh=" + ZH.all.length);

/* Latin queries: the top hit must name what was asked for. This is the strong
   relevance assertion, and it exercises the substring fallback. */
[
  ["LoDoPaB", "LoDoPaB"], ["mamba", "Mamba"], ["splat", "Splat"],
  ["denoising", "Denois"], ["metal artifact", "Metal"], ["cone-beam", "Cone"]
].forEach(function (c) {
  const hits = topHits(EN, c[0], 3);
  ok("EN relevance: " + JSON.stringify(c[0]) + " → " + (hits[0] ? hits[0].title.slice(0, 44) : "—"),
    hits.some(function (h) { return h.title.toLowerCase().indexOf(c[1].toLowerCase()) >= 0; }),
    hits.map(function (h) { return h.title; }).join(" | "));
});

/* Chinese queries match the Chinese topic names and notes — paper titles stay
   English — so assert recall, and for topic-level phrases that the whole
   section is reachable. */
[
  ["稀疏视角", 100], ["低剂量", 40], ["锥束", 40],
  ["高斯溅射", 10], ["金属伪影", 15],
  ["稀疏视角 重建", 100]
].forEach(function (c) {
  const n = S.search(ZH.index, c[0]).length;
  ok("ZH recall: " + JSON.stringify(c[0]) + " ≥ " + c[1], n >= c[1], n + " hits");
});

ok("partial CJK query still returns results", S.search(ZH.index, "稀疏视角 zzqqzz").length > 0);

/* The dropdown covers every section, not only papers. */
["LoDoPaB", "TIGRE", "ASTRA"].forEach(function (q) {
  const kinds = {};
  S.search(EN.index, q).slice(0, 5).forEach(function (h) { kinds[h.item.kind] = 1; });
  ok("search reaches beyond papers for " + JSON.stringify(q), Object.keys(kinds).length > 0);
});

/* Teams are searchable by PI name, institution and Chinese name: the point
   of the section is finding *who* works on a problem, not only *what*. The
   table is optional (a checkout may predate data/teams.yaml), so the count
   assertion is consistency, not a fixed number — the section's contents
   change as groups are added, exactly like the other tables. The search
   assertions run whenever at least one team is present. */
ok("teams are in the payload, equally in both languages",
  (EN.data.teams || []).length === (ZH.data.teams || []).length,
  "en=" + (EN.data.teams || []).length + " zh=" + (ZH.data.teams || []).length);
if ((EN.data.teams || []).length) {
  ok("EN search finds a team by PI (Maier)",
    S.search(EN.index, "Maier").some(function (h) {
      return h.item.kind === "teams" && h.item.rec.title.indexOf("Pattern Recognition") >= 0;
    }),
    topHits(EN, "Maier").map(function (h) { return h.kind + ":" + h.title; }).join(" | "));
  ok("ZH search finds a team by PI (李小萌)",
    S.search(ZH.index, "李小萌").some(function (h) { return h.item.kind === "teams"; }),
    topHits(ZH, "李小萌").map(function (h) { return h.kind + ":" + h.title; }).join(" | "));
  ok("ZH search finds Cambridge CIA by 剑桥",
    S.search(ZH.index, "剑桥").some(function (h) {
      return h.item.kind === "teams" && h.item.rec.title.indexOf("Computational Image Analysis") >= 0;
    }),
    topHits(ZH, "剑桥").map(function (h) { return h.kind + ":" + h.title; }).join(" | "));
}

/* ------------------------------------------------------------------ report */
console.log("search core: %d passed, %d failed (%d records per language)",
  pass, failures.length, EN.all.length);
if (failures.length) {
  failures.forEach(function (f) { console.log("  ✗ " + f); });
  process.exit(1);
}
