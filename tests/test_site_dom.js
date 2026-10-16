/* End-to-end smoke test for the built site's search UI.
 *
 * Runs the ACTUAL built pages (site/index.html and site/zh/index.html) in jsdom,
 * with their real scripts loaded from disk, then drives the DOM the way a user
 * would: types in the top-bar box and in the paper filter, and inspects what got
 * rendered. This is the check that catches wiring mistakes the pure-function
 * test cannot see — a missing element, a script that throws on load, a render
 * that aborts before the search box is wired.
 *
 * It is deliberately NOT part of CI. It needs jsdom from npm, and a workflow that
 * can go red for a reason unrelated to the change teaches people to ignore red —
 * the same argument SITE.md makes for the deploy workflow. Run it by hand before
 * pushing anything that touches web/:
 *
 *     python scripts/build_site.py
 *     npm install --prefix "$(mktemp -d)" jsdom      # or any scratch dir
 *     NODE_PATH=<that dir>/node_modules node tests/test_site_dom.js
 *
 * (Install jsdom into a scratch or isolated prefix, never into your home
 * directory — npm without --prefix writes to ~/node_modules, which is where
 * editor tooling such as vue-language-server and pyright lives.)
 */
"use strict";

const fs = require("fs");
const path = require("path");

let JSDOM;
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  console.error("jsdom is not installed (this test is local-only, by design).\n" +
    "Install it into a scratch prefix, then point NODE_PATH at it:\n" +
    "  npm install --prefix /tmp/ct-test jsdom\n" +
    "  NODE_PATH=/tmp/ct-test/node_modules node tests/test_site_dom.js");
  process.exit(2);
}

const REPO = path.resolve(__dirname, "..");
const SITE = path.join(REPO, "site");

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
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function openPage(rel) {
  const dom = await JSDOM.fromFile(path.join(SITE, rel), {
    runScripts: "dangerously",
    resources: "usable",
    pretendToBeVisual: true
  });
  await new Promise((resolve) => {
    if (dom.window.document.readyState === "complete") { resolve(); }
    else { dom.window.addEventListener("load", resolve); }
  });
  /* app.js renders on load; the search boxes debounce at 80–180 ms. */
  await wait(350);
  return dom;
}

function typeInput(win, el, value) {
  el.value = value;
  el.dispatchEvent(new win.Event("input", { bubbles: true }));
}

function paperTitles(win) {
  return Array.prototype.map.call(
    win.document.querySelectorAll("#papers-list .paper .p-title"),
    (n) => n.textContent.trim()
  );
}

/* Dataset / benchmark names link to their own page (official link kept
   beside it), and the Learning tab opens with the Guides group. Every such
   link must resolve to a page in the build. */
function homeDetailLinks(doc, prefix) {
  const exists = (href) => fs.existsSync(path.join(SITE, prefix, href, "index.html"));
  ["datasets", "benchmarks"].forEach(function (kind) {
    const rows = Array.prototype.slice.call(doc.querySelectorAll("#t-" + kind + " tbody tr"));
    const linked = rows.filter((r) => {
      const a = r.querySelector("td:first-child a");
      return a && a.getAttribute("href").indexOf(kind + "/") === 0;
    });
    ok(kind + " tab: names link to detail pages", linked.length > 0, linked.length + " of " + rows.length + " rows");
    ok(kind + " tab: those rows keep the official link (new tab)",
      linked.every((r) => !!r.querySelector('td:first-child a.ext[target="_blank"][href^="http"]')));
    const broken = linked.map((r) => r.querySelector("td:first-child a").getAttribute("href")).filter((h) => !exists(h));
    ok(kind + " tab: every detail link resolves", broken.length === 0, broken.join(", "));
  });
  const gl = Array.prototype.map.call(doc.querySelectorAll("#t-learning tbody.grp-guides a"),
    (a) => a.getAttribute("href"));
  ok("learning tab: Guides group lists 3 guides + /guides/",
    gl.length === 4 && gl.indexOf("guides/") !== -1 && gl.every((h) => exists(h)), gl.join(", "));
  const first = doc.querySelector("#t-learning table tbody");
  ok("learning tab: Guides group is at the top", !!first && first.classList.contains("grp-guides"));
}

async function testEnglish() {
  console.log("\n[en] site/index.html");
  const dom = await openPage("index.html");
  const win = dom.window, doc = win.document;

  ok("search.js loaded (window.CTSearch)", typeof win.CTSearch === "object" && win.CTSearch !== null);
  ok("paper list rendered on load", paperTitles(win).length > 300, paperTitles(win).length + " rows");

  /* init() runs the five section renders in sequence, so a throw in any one of
     them silently skips every step after it — including the search wiring. Row
     counts are therefore the guard that init() actually finished. */
  ["t-toolkits", "t-datasets", "t-benchmarks", "t-learning"].forEach(function (id) {
    const n = doc.querySelectorAll("#" + id + " tr").length;
    ok("init() completed: #" + id + " has rows", n > 0, n + " rows");
  });

  homeDetailLinks(doc, "");

  /* ---- hover cards -----------------------------------------------------
     A paper title used to be an <a> to the same URL as the `paper` link beside
     it, so clicking either went to the same place. It is plain text now, and
     papers we hold a blurb for explain themselves instead of navigating. This
     is the interaction, so it is worth asserting rather than eyeballing. */
  ok("title is no longer a link",
    doc.querySelectorAll("#papers-list .p-title a").length === 0);
  const blurred = doc.querySelectorAll("#papers-list .p-titletext.has-blurb[data-blurb]");
  ok("papers with a blurb are marked", blurred.length > 0, blurred.length + " titles");
  /* Coverage is a moving target — every paper carries a blurb today, none
     might tomorrow. What has to hold either way: only titles marked
     `has-blurb` carry a `data-blurb`, so a title without one can never become
     hoverable. (The earlier form asserted that at least one paper lacked a
     blurb, which quietly turned into a false failure once coverage hit 100%.) */
  const allTitles = doc.querySelectorAll("#papers-list .p-titletext");
  const marked = doc.querySelectorAll("#papers-list .p-titletext.has-blurb");
  const withData = doc.querySelectorAll("#papers-list .p-titletext[data-blurb]");
  ok("has-blurb and data-blurb agree",
    marked.length === withData.length && marked.length <= allTitles.length,
    marked.length + " of " + allTitles.length + " titles carry a blurb");
  if (blurred.length) {
    const first = blurred[0];
    const want = first.getAttribute("data-blurb").trim();
    first.dispatchEvent(new win.MouseEvent("mouseover", { bubbles: true }));
    const card = doc.getElementById("blurb-card");
    ok("hover opens the card", !!card && card.hidden === false);
    ok("card shows that paper's blurb verbatim",
      !!card && card.textContent.trim() === want,
      (card ? card.textContent.trim().slice(0, 60) : "—") + "…");
    doc.dispatchEvent(new win.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    ok("Escape closes the card", !!card && card.hidden === true);
  }

  const q = doc.getElementById("q");
  typeInput(win, q, "mamba");
  await wait(150);
  ok("filter: \"mamba\" finds a Mamba paper",
    paperTitles(win).some((t2) => /mamba/i.test(t2)), paperTitles(win)[0] || "—");
  ok("filter: matched text is marked",
    doc.querySelectorAll("#papers-list .p-title mark").length > 0);

  typeInput(win, q, "sparse zzqqzz");
  await wait(150);
  ok("filter: one junk word still returns results (strict AND used to empty the list)",
    paperTitles(win).length > 0, paperTitles(win).length + " rows");

  typeInput(win, q, "denomamba");
  await wait(150);
  ok("filter: relevance puts DenoMamba first", /denomamba/i.test(paperTitles(win)[0] || ""),
    paperTitles(win)[0] || "—");
  typeInput(win, q, "");
  await wait(150);

  const gq = doc.getElementById("gq");
  typeInput(win, gq, "LoDoPaB");
  await wait(250);
  const rows = doc.querySelectorAll("#gres .gr");
  ok("top box: \"LoDoPaB\" produces a dropdown", rows.length > 0, rows.length + " rows");
  const kinds = Array.prototype.map.call(rows, (r) => r.querySelector(".gk").textContent);
  ok("top box: the dataset is among the results", kinds.some((k) => /Dataset/i.test(k)), kinds.join(", "));
  ok("top box: result titles are marked", doc.querySelectorAll("#gres .gt mark").length > 0);

  typeInput(win, gq, "denoising");
  await wait(250);
  ok("top box: a paper match offers \"show all papers\"", !!doc.querySelector("#gres .gall"));

  win.close();
}

async function testChinese() {
  console.log("\n[zh] site/zh/index.html");
  const dom = await openPage(path.join("zh", "index.html"));
  const win = dom.window, doc = win.document;

  homeDetailLinks(doc, "zh");

  const q = doc.getElementById("q");
  typeInput(win, q, "稀疏视角");
  await wait(180);
  ok("zh filter: \"稀疏视角\" has broad recall (CJK bigrams)",
    paperTitles(win).length > 100, paperTitles(win).length + " rows");

  typeInput(win, q, "稀疏视角 zzqqzz");
  await wait(180);
  ok("zh filter: one junk word still returns results", paperTitles(win).length > 0);

  typeInput(win, q, "稀疏重建");
  await wait(180);
  ok("zh filter: matches across a gap (稀疏…重建 not adjacent)",
    paperTitles(win).length > 50, paperTitles(win).length + " rows");

  typeInput(win, q, "锥束");
  await wait(200);
  ok("zh filter: topic names are marked", doc.querySelectorAll("#papers-list .topics mark").length > 0,
    doc.querySelectorAll("#papers-list .topics mark").length + " marks");

  typeInput(win, q, "");
  const gq = doc.getElementById("gq");
  typeInput(win, gq, "锥束");
  await wait(250);
  ok("top box: Chinese query produces a dropdown", doc.querySelectorAll("#gres .gr").length > 0);

  win.close();
}

(async function () {
  console.log("site search smoke test (jsdom, against the real build)");
  await testEnglish();
  await testChinese();
  console.log("\n%d passed, %d failed", pass, failures.length);
  if (failures.length) {
    failures.forEach((f) => console.log("  ✗ " + f));
    process.exit(1);
  }
  console.log("site search smoke test passed ✓");
})().catch((e) => { console.error("the test itself threw:", e); process.exit(2); });
