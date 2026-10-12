/* awesome-computed-tomography — client-side filtering.
   Classic script (NOT a module) so the page also works when opened from
   file://, where ES modules are blocked by CORS.

   Search runs on web/search.js, which builds its index in the browser from the
   payload already in the page — nothing extra to download, and no query parser
   to trip over. Still no lunr: a general-purpose engine scores short Chinese
   titles badly, and pulling one in would add a failure mode this list does not
   need. */

(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("site-data").textContent);
  var TOPIC = {};
  DATA.topics.forEach(function (t) { TOPIC[t.id] = t; });

  var S = window.CTSearch;

  /* One weighted index over the papers, built on first use. `build` preserves
     input order, which is what lets a paper's score be looked up by the same
     index the filters use. */
  var paperIndex = null;
  function ensurePaperIndex() {
    if (paperIndex) { return paperIndex; }
    var topicName = {};
    DATA.topics.forEach(function (t) { topicName[t.id] = t.name; });
    paperIndex = S.build(DATA.papers, S.mappers(topicName).papers);
    return paperIndex;
  }

  /* null when nothing is being searched for; otherwise one score per
     DATA.papers entry, 0 meaning "no match". */
  function relevance() {
    if (!state.q) { return null; }
    var q = S.parse(state.q);
    if (!q.tokens.length) { return null; }
    var idx = ensurePaperIndex();
    var sets = S.matchSets(q, idx.vocab);
    var out = [];
    for (var i = 0; i < DATA.papers.length; i++) {
      out[i] = S.score(idx.entries[i].doc, q, sets);
    }
    return out;
  }

  /* Strings to mark in a result: the query's own phrases plus its tokens, so
     what gets highlighted is exactly what was matched. */
  function queryTerms() {
    return state.q ? S.terms(state.q) : [];
  }

  // Interface strings for the language this page was built in. Handed over by
  // build_site.py as payload.ui; every entry falls back to the English key so a
  // half-finished translation still renders a whole page.
  var UI = DATA.ui || {};
  function t(key, fallback) { return UI[key] || fallback; }
  function tf(key, fallback, subs) {
    var s = t(key, fallback);
    for (var k in subs) if (subs.hasOwnProperty(k)) {
      s = s.split("{" + k + "}").join(subs[k]);
    }
    return s;
  }

  var state = {
    tab: "papers",
    q: "",
    topics: [],          // [] == all
    type: "all",         // all | peer | preprint
    code: false,
    from: 0,             // 0 == all years
    sort: "new"          // new | old | title
  };

  var YEARS = DATA.papers.map(function (p) { return p.year; });
  var YEAR_MIN = Math.min.apply(null, YEARS);
  var YEAR_MAX = Math.max.apply(null, YEARS);

  /* ------------------------------------------------------------ helpers */

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* Minimal inline markdown for the `note` fields: **bold**, `code`, [text](url).
     Everything is escaped first, so the output is safe. */
  function mdInline(s) {
    var out = esc(s == null ? "" : s);
    out = out.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
      function (_m, text, url) {
        return '<a href="' + url + '" target="_blank" rel="noopener">' + text + "</a>";
      });
    out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
    return out;
  }

  /* The link target for a paper row; the paper link wins, then project/code. */
  function primaryUrl(p) {
    return p.links.paper || p.links.project || p.links.code || "";
  }

  /* First whitespace-delimited token of a title, punctuation trimmed. An
     abbreviation only heads the title if it IS that token: abbr "A" matches
     "A benchmark ...", abbr "AR" does not match "ART ...". Mirrors
     scripts/build.py:head_token so the site and README never disagree. */
  function headToken(title) {
    var first = title.trim().split(/\s+/)[0] || "";
    return first.replace(/[.,:;]+$/, "").toLowerCase();
  }

  /* Titles harvested from Crossref often repeat the abbreviation in trailing
     parentheses ("... reconstruction (LoDoPaB-CT)"). The head already shows
     it, so drop that group. Mirrors scripts/build.py:drop_trailing_parens. */
  function dropTrailingParens(rest, name) {
    var m = rest.match(/\(([^()]*)\)\s*$/);
    if (!m) { return rest; }
    var body = m[1].trim().toLowerCase();
    var low = name.toLowerCase();
    if (body === low || body.slice(-(low.length + 2)) === ": " + low ||
        body.split(", ").pop() === low) {
      return rest.slice(0, m.index).replace(/[ ,;]+$/, "");
    }
    return rest;
  }

  /* Title with the leading abbreviation stripped, mirroring README.md:
     "DM4CT: Benchmarking ..." renders as [DM4CT] Benchmarking ... */
  function titleParts(p) {
    // Inline TeX like "$K$-NeAS" shows as plain text: drop the $ delimiters.
    var title = p.title.replace(/\$([^$]+)\$/g, "$1");
    if (p.abbr && title.toLowerCase().indexOf(p.abbr.toLowerCase()) === 0 &&
        headToken(title) === p.abbr.toLowerCase()) {
      var rest = title.slice(p.abbr.length).replace(/^[\s:,\u2014\u2013-]+/, "");
      rest = dropTrailingParens(rest, p.abbr);
      return { abbr: p.abbr, text: rest || title };
    }
    return { abbr: p.abbr || "", text: title };
  }

  /* Mark the query's terms in a plain-text title. The ranges come from the same
     tokeniser that scored the record, and textContent is used throughout, so
     nothing in a title can escape as markup. */
  function highlight(text, terms) {
    var frag = document.createDocumentFragment();
    if (!terms || !terms.length) {
      frag.appendChild(document.createTextNode(text));
      return frag;
    }
    return S.markInto(frag, text, terms);
  }

  /* ------------------------------------------------------------ filtering */

  /* Hard filters first (kind, code, year, topic), then the query.
     A query no longer means "every word must appear": each record is scored and
     ranked, and only records matching nothing are dropped — so one extra or
     misspelt word lowers a record's rank instead of emptying the list.
     Ranking is applied with a stable sort *after* the user's own sort, so equal
     scores keep the order they asked for. */
  function selectedPapers() {
    var rel = relevance();
    var rows = [];
    var i;
    for (i = 0; i < DATA.papers.length; i++) {
      var p = DATA.papers[i];
      if (rel && !rel[i]) { continue; }
      if (state.type === "peer" && p.preprint) { continue; }
      if (state.type === "preprint" && !p.preprint) { continue; }
      if (state.code && !p.links.code) { continue; }
      if (state.from && p.year < state.from) { continue; }
      if (state.topics.length && !hasTopic(p)) { continue; }
      rows.push({ p: p, s: rel ? rel[i] : 0 });
    }

    /* Sort on the title as it is *displayed*: "$K$-NeAS" shows as "K-NeAS",
       and sorting on the raw string would file it under "$" (0x24), ahead of
       every digit and letter. Also returns 0 for equal keys — a comparator
       that only ever returns -1/1 is not a valid ordering. */
    function nameKey(p) {
      return (p.abbr || S.plain(p.title)).toLowerCase();
    }
    function byName(a, b) {
      var x = nameKey(a.p), y = nameKey(b.p);
      return x < y ? -1 : x > y ? 1 : 0;
    }
    if (state.sort === "title") { rows.sort(byName); }
    else if (state.sort === "old") {
      rows.sort(function (a, b) { return a.p.year - b.p.year || byName(a, b); });
    }
    /* "new" keeps the server-side order, which is already (-year, abbr|title). */
    if (rel) { rows.sort(function (a, b) { return b.s - a.s; }); }

    var out = [];
    for (i = 0; i < rows.length; i++) { out.push(rows[i].p); }
    return out;
  }

  function hasTopic(p) {
    for (var i = 0; i < state.topics.length; i++) {
      if (p.topics.indexOf(state.topics[i]) !== -1) { return true; }
    }
    return false;
  }

  /* ------------------------------------------------------------ rendering */

  var listEl, countEl, emptyEl;

  function renderPapers() {
    var rows = selectedPapers();
    var toks = queryTerms();
    var frag = document.createDocumentFragment();

    rows.forEach(function (p) {
      var li = document.createElement("li");
      li.className = "paper";

      var h = document.createElement("p");
      h.className = "p-title";
      if (p.abbr) {
        var ab = document.createElement("span");
        ab.className = "abbr";
        ab.textContent = p.abbr;
        h.appendChild(ab);
      }
      var url = primaryUrl(p);
      // NB: not `var t` — that shadows the i18n helper t() used a few lines
      // below for the preprint label, and the resulting throw aborted init()
      // before the search box was ever wired up. (`parts` also reads better.)
      var parts = titleParts(p);
      if (url) {
        var a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener";
        a.appendChild(highlight(parts.text, toks));
        h.appendChild(a);
      } else {
        h.appendChild(highlight(parts.text, toks));
      }
      li.appendChild(h);

      var meta = document.createElement("p");
      meta.className = "p-meta";
      var v = document.createElement("span");
      v.className = "venue" + (p.preprint ? " is-preprint" : "");
      v.textContent = p.venue || t("venuePreprint", "preprint");
      meta.appendChild(v);
      meta.appendChild(sep());
      meta.appendChild(text(String(p.year)));
      if (p.topics.length) {
        meta.appendChild(sep());
        var tp = document.createElement("span");
        tp.className = "topics";
        // Mark the topic names too: a Chinese query normally matches the topic
        // rather than the (English) paper title, and without this the results
        // look like nothing was matched.
        tp.appendChild(highlight(p.topics.map(function (id) {
          return TOPIC[id] ? TOPIC[id].name : id;
        }).join(" \u00b7 "), toks));
        meta.appendChild(tp);
      }
      li.appendChild(meta);

      var links = document.createElement("div");
      links.className = "p-links";
      ["paper", "code", "project", "data"].forEach(function (k) {
        if (!p.links[k]) return;
        var a2 = document.createElement("a");
        a2.href = p.links[k];
        a2.target = "_blank";
        a2.rel = "noopener";
        a2.className = k;
        a2.textContent = k;
        links.appendChild(a2);
      });
      li.appendChild(links);

      frag.appendChild(li);
    });

    listEl.textContent = "";
    listEl.appendChild(frag);
    countEl.textContent = rows.length;
    emptyEl.hidden = rows.length !== 0;
  }

  function text(s) { return document.createTextNode(s); }
  function sep() {
    var s = document.createElement("span");
    s.className = "sep";
    s.textContent = "\u00b7";
    return s;
  }

  function linkCell(p, url) {
    if (!url) return document.createTextNode(p.name);
    var a = document.createElement("a");
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = p.name;
    return a;
  }

  function renderTable(host, cols, rows) {
    var head = "<thead><tr>" + cols.map(function (c) {
      return "<th>" + esc(c.label) + "</th>";
    }).join("") + "</tr></thead>";
    var body = "<tbody>" + rows.map(function (r) {
      return "<tr>" + r.map(function (cell, i) {
        var cls = cols[i] && cols[i].cls;
        var lab = cols[i] ? ' data-label="' + esc(cols[i].label) + '"' : "";
        var open = "<td" + (cls ? ' class="' + cls + '"' : "") + lab + ">";
        return cell.indexOf("@@HTML@@") === 0
          ? open + cell.slice(8) + "</td>"
          : open + esc(cell) + "</td>";
      }).join("") + "</tr>";
    }).join("") + "</tbody>";
    host.innerHTML = '<table class="grid">' + head + body + "</table>";
  }

  function renderToolkits() {
    var rows = DATA.toolkits.slice().sort(function (a, b) { return (b.stars || 0) - (a.stars || 0); });
    renderTable(document.getElementById("t-toolkits"),
      [{ label: t("tableToolkit", "Toolkit") }, { label: t("tableLanguage", "Language") },
       { label: t("tableLicense", "License"), cls: "n" },
       { label: t("tableStars", "Stars"), cls: "n" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      // NB: the callback parameter must NOT be named `t` — that would shadow the
      // i18n helper t() above, and the `t("homepageTitle")` call below would
      // then be calling a row object. It threw for every toolkit that carries a
      // homepage, which aborted init() before the search box was ever wired up.
      rows.map(function (row) {
        var nm = esc(row.label || row.name);
        var html = '<a href="' + esc(row.url) + '" target="_blank" rel="noopener">' + nm + "</a>";
        if (row.homepage) {
          html += ' <a href="' + esc(row.homepage) + '" target="_blank" rel="noopener" title="' + t("homepageTitle", "homepage") + '">'
                + '<span class="mono">[site]</span></a>';
        }
        return ["@@HTML@@" + html, row.language || "-", row.license || "-",
                row.stars == null ? "-" : String(row.stars), "@@HTML@@" + mdInline(row.note)];
      }));
  }

  function renderDatasets() {
    renderTable(document.getElementById("t-datasets"),
      [{ label: t("tableDataset", "Dataset") }, { label: t("tableModality", "Modality") },
       { label: t("tableTasks", "Tasks"), cls: "tasks" },
       { label: t("tableLicense", "License"), cls: "n" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      DATA.datasets.map(function (d) {
        var nm = '<a href="' + esc(d.url) + '" target="_blank" rel="noopener">' + esc(d.label || d.name) + "</a>";
        return ["@@HTML@@" + nm, d.modality || "-",
                (d.tasks || []).join(", ") || "-",
                d.license || "-", "@@HTML@@" + mdInline(d.note)];
      }));
  }

  function renderBenchmarks() {
    var rows = DATA.benchmarks.slice().sort(function (a, b) { return (b.year || 0) - (a.year || 0); });
    renderTable(document.getElementById("t-benchmarks"),
      [{ label: t("tableBenchmark", "Benchmark / Challenge") },
       { label: t("tableYear", "Year"), cls: "n" },
       { label: t("tableTasks", "Tasks"), cls: "tasks" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      rows.map(function (b) {
        var nm = '<a href="' + esc(b.url) + '" target="_blank" rel="noopener">' + esc(b.label || b.name) + "</a>";
        return ["@@HTML@@" + nm, b.year == null ? "-" : String(b.year),
                (b.tasks || []).join(", ") || "-", "@@HTML@@" + mdInline(b.note)];
      }));
  }

  function renderLearning() {
    var order = { book: 1, course: 2, tutorial: 3, tool: 4, list: 5 };
    var rows = DATA.learning.slice().sort(function (a, b) {
      return (order[a.type] || 9) - (order[b.type] || 9) ||
             (a.label || a.name).localeCompare(b.label || b.name);
    });
    renderTable(document.getElementById("t-learning"),
      [{ label: t("tableResource", "Resource") }, { label: t("tableType", "Type"), cls: "n" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      rows.map(function (l) {
        var nm = '<a href="' + esc(l.url) + '" target="_blank" rel="noopener">' + esc(l.label || l.name) + "</a>";
        return ["@@HTML@@" + nm, l.type || "-", "@@HTML@@" + mdInline(l.note)];
      }));
  }

  function renderTopics() {
    var host = document.getElementById("topics");
    host.textContent = "";
    DATA.topics.forEach(function (t) {
      if (!t.count) return;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "chip";
      b.setAttribute("aria-pressed", String(state.topics.indexOf(t.id) !== -1));
      b.dataset.topic = t.id;
      b.appendChild(document.createTextNode(t.name));
      var n = document.createElement("span");
      n.className = "n";
      n.textContent = t.count;
      b.appendChild(n);
      b.title = t.desc || t.name;
      b.addEventListener("click", function () { toggleTopic(t.id); });
      host.appendChild(b);
    });
  }

  /* ---------------------------------------------------------------- state */

  function syncTopicChips() {
    Array.prototype.forEach.call(document.querySelectorAll("#topics .chip"), function (b) {
      b.setAttribute("aria-pressed", String(state.topics.indexOf(b.dataset.topic) !== -1));
    });
  }

  function toggleTopic(id) {
    var i = state.topics.indexOf(id);
    if (i === -1) state.topics.push(id); else state.topics.splice(i, 1);
    syncTopicChips();
    apply();
  }

  function setType(t) {
    state.type = t;
    Array.prototype.forEach.call(document.querySelectorAll("#typeseg button"), function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.type === t));
    });
  }

  function setTab(name, push) {
    state.tab = name;
    Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (b) {
      b.setAttribute("aria-selected", String(b.dataset.tab === name));
    });
    Array.prototype.forEach.call(document.querySelectorAll("section[role=tabpanel]"), function (s) {
      s.hidden = s.id !== "panel-" + name;
    });
    if (push !== false) writeUrl();
  }

  function reset() {
    state.q = "";
    state.topics = [];
    state.type = "all";
    state.code = false;
    state.from = 0;
    state.sort = "new";
    document.getElementById("q").value = "";
    document.getElementById("from").value = "0";
    document.getElementById("sort").value = "new";
    document.getElementById("has-code").checked = false;
    syncTopicChips();
    setType("all");
    apply();
  }

  /* --------------------------------------------------------------- url io */

  function writeUrl() {
    var p = new URLSearchParams();
    if (state.tab !== "papers") p.set("tab", state.tab);
    if (state.q) p.set("q", state.q);
    if (state.topics.length) p.set("topic", state.topics.join(","));
    if (state.type !== "all") p.set("type", state.type);
    if (state.code) p.set("code", "1");
    if (state.from) p.set("from", String(state.from));
    if (state.sort !== "new") p.set("sort", state.sort);
    var qs = p.toString();
    try {
      history.replaceState(null, "", qs ? "?" + qs : location.pathname);
    } catch (err) {
      /* file:// and some sandboxed contexts refuse history rewrites; the page
         still works, only the address bar stops tracking the filters. */
    }
    syncShare();
  }

  function readUrl() {
    var p = new URLSearchParams(location.search);
    var tab = p.get("tab");
    if (tab && document.getElementById("panel-" + tab)) state.tab = tab;
    if (p.get("q")) { state.q = p.get("q"); document.getElementById("q").value = state.q; }
    if (p.get("topic")) {
      state.topics = p.get("topic").split(",").filter(function (t) { return !!TOPIC[t] || t === "other"; });
    }
    if (p.get("type") === "peer" || p.get("type") === "preprint") setType(p.get("type"));
    if (p.get("code") === "1") { state.code = true; document.getElementById("has-code").checked = true; }
    if (p.get("from")) {
      var f = parseInt(p.get("from"), 10);
      if (f >= YEAR_MIN && f <= YEAR_MAX) { state.from = f; document.getElementById("from").value = String(f); }
    }
    if (["new", "old", "title"].indexOf(p.get("sort")) !== -1) {
      state.sort = p.get("sort");
      document.getElementById("sort").value = state.sort;
    }
  }

  function syncShare() {
    var b = document.getElementById("share");
    if (b) b.textContent = t("labelShare", "Copy link");
  }

  /* ---------------------------------------------------------------- wiring */

  function apply() {
    renderPapers();
    writeUrl();
  }

  function debounce(fn, ms) {
    var timer;
    return function () {
      var self = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () { fn.apply(self, args); }, ms);
    };
  }

  function init() {
    listEl = document.getElementById("papers-list");
    countEl = document.getElementById("count");
    emptyEl = document.getElementById("empty");

    /* year options */
    var fromSel = document.getElementById("from");
    var years = {};
    DATA.papers.forEach(function (p) { years[p.year] = true; });
    Object.keys(years).map(Number).sort(function (a, b) { return b - a; })
      .forEach(function (y) {
        var o = document.createElement("option");
        o.value = String(y);
        o.textContent = tf("yearAndLater", "{year} and later", { year: y });
        fromSel.appendChild(o);
      });

    /* tab counts */
    var counts = {
      papers: DATA.papers.length, toolkits: DATA.toolkits.length,
      datasets: DATA.datasets.length, benchmarks: DATA.benchmarks.length,
      learning: DATA.learning.length
    };
    Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (b) {
      var n = document.createElement("span");
      n.className = "n";
      n.textContent = counts[b.dataset.tab] || 0;
      b.appendChild(n);
      b.addEventListener("click", function () { setTab(b.dataset.tab); });
    });

    renderTopics();
    renderToolkits();
    renderDatasets();
    renderBenchmarks();
    renderLearning();
    readUrl();
    setTab(state.tab, false);
    /* Render once with whatever the URL asked for. The list is also present in
       the served HTML so the page works without JS and stays crawlable; this
       call is what makes ?q= / ?topic= / ?code= deep links actually filter. */
    apply();

    document.getElementById("q").addEventListener("input", debounce(function (e) {
      state.q = e.target.value.trim();
      apply();
    }, 120));

    Array.prototype.forEach.call(document.querySelectorAll("#typeseg button"), function (b) {
      b.addEventListener("click", function () { setType(b.dataset.type); apply(); });
    });

    document.getElementById("has-code").addEventListener("change", function (e) {
      state.code = e.target.checked;
      apply();
    });
    fromSel.addEventListener("change", function (e) {
      state.from = parseInt(e.target.value, 10) || 0;
      apply();
    });
    document.getElementById("sort").addEventListener("change", function (e) {
      state.sort = e.target.value;
      apply();
    });
    document.getElementById("reset").addEventListener("click", reset);

    var share = document.getElementById("share");
    if (share) {
      share.addEventListener("click", function () {
        var url = location.href;
        function done() { share.textContent = t("copied", "copied"); setTimeout(syncShare, 1400); }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done, function () { window.prompt(t("copyLinkTitle", "Copy this URL"), url); });
        } else {
          window.prompt(t("copyLinkTitle", "Copy this URL"), url);
        }
      });
    }

    /* "/" focuses search — but never while typing in a field */
    document.addEventListener("keydown", function (e) {
      if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
      var el = e.target;
      if (el && (el.tagName === "INPUT" || el.tagName === "SELECT" || el.tagName === "TEXTAREA")) return;
      e.preventDefault();
      (document.getElementById("gq") || document.getElementById("q")).focus();
    });

    /* The colour-theme toggle is deliberately NOT wired here. index.html owns
       it in an inline head script, so the theme still works when this file
       never runs, and a second listener cannot cancel the first one out. */
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
