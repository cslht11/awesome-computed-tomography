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

  /* Minimal inline markdown for the `note` fields: **bold**, *em* / _em_,
     `code`, [text](url). Everything is escaped first, so the output is safe.
     The emphasis rules match italics() in scripts/build_site.py: delimiters
     only at word edges, so snake_case names and URLs are left alone. */
  function mdInline(s) {
    var out = esc(s == null ? "" : s);
    out = out.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
      function (_m, text, url) {
        return '<a href="' + url + '" target="_blank" rel="noopener">' + text + "</a>";
      });
    out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
    out = out.replace(/(^|[^\w*])\*(?![\s*])([^*\n]+?)\*(?![\w*])/g, function (m, pre, body) {
      return /\s$/.test(body) ? m : pre + "<em>" + body + "</em>";
    });
    out = out.replace(/(^|[^\w])_(?![\s_])([^_\n]+?)_(?![\w])/g, function (m, pre, body) {
      return /\s$/.test(body) ? m : pre + "<em>" + body + "</em>";
    });
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

  /* ------------------------------------------------------------ hover card

     One card, re-used, parked on <body> and positioned in viewport
     coordinates — the paper list can scroll and clip, and a card nested inside
     a row would be cut off. The content is read with textContent, so a blurb
     can never escape as markup.

     Three ways in, because "hover" is not universal: pointer hover (desktop),
     tap (touch, where hover does not exist), and keyboard focus. Escape and
     clicking anywhere else put it away. `pointer-events: none` in the CSS
     keeps the card from stealing the pointer from the row underneath it. */

  var cardEl = null;

  function card() {
    if (cardEl) { return cardEl; }
    cardEl = document.createElement("div");
    cardEl.className = "blurb-card";
    cardEl.id = "blurb-card";
    cardEl.setAttribute("role", "tooltip");
    cardEl.hidden = true;
    document.body.appendChild(cardEl);
    return cardEl;
  }

  function showCard(el) {
    var text = el.getAttribute("data-blurb");
    if (!text) { return; }
    var c = card();
    c.textContent = text;
    c.hidden = false;
    el.setAttribute("aria-describedby", "blurb-card");
    var r = el.getBoundingClientRect();
    var cr = c.getBoundingClientRect();
    var left = Math.min(Math.max(8, r.left), window.innerWidth - cr.width - 8);
    var top = r.bottom + 8;
    /* Flip above the title when there is no room below, then clamp. */
    if (top + cr.height > window.innerHeight - 8) { top = r.top - cr.height - 8; }
    if (top < 8) { top = 8; }
    c.style.left = Math.round(left) + "px";
    c.style.top = Math.round(top) + "px";
  }

  function hideCard() {
    if (cardEl) { cardEl.hidden = true; }
    var prev = document.querySelector(".p-titletext[aria-describedby]");
    if (prev) { prev.removeAttribute("aria-describedby"); }
  }

  function cardTarget(e) {
    var el = e.target;
    return el && el.closest ? el.closest(".p-titletext[data-blurb]") : null;
  }

  /* ------------------------------------------------------------ rendering */

  var listEl, countEl, emptyEl;

  function renderPapers() {
    var rows = selectedPapers();
    var toks = queryTerms();
    var frag = document.createDocumentFragment();
    /* The row the card was describing may be about to disappear. */
    hideCard();

    /* Year headings while the list is in year order (not when it is sorted
       by title or ranked by a search), so a long list can be scanned by year
       and a screen reader can jump between years by heading. */
    var byYear = !state.q && state.sort !== "title";
    var perYear = {}, lastYear = null;
    if (byYear) {
      rows.forEach(function (p) { perYear[p.year] = (perYear[p.year] || 0) + 1; });
    }

    rows.forEach(function (p) {
      if (byYear && p.year !== lastYear) {
        lastYear = p.year;
        var yl = document.createElement("li");
        yl.className = "year-sep";
        var yh = document.createElement("h2");
        yh.textContent = String(p.year);
        var yn = document.createElement("span");
        yn.className = "n";
        yn.textContent = perYear[p.year];
        yh.appendChild(yn);
        yl.appendChild(yh);
        frag.appendChild(yl);
      }
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
      // NB: not `var t` — that shadows the i18n helper t() used a few lines
      // below for the preprint label, and the resulting throw aborted init()
      // before the search box was ever wired up. (`parts` also reads better.)
      var parts = titleParts(p);
      /* The title is NOT a link any more. It used to point at the same URL as
         the `paper` link rendered two lines below, so clicking either went to
         the same place. The links below are the way out; the title instead
         explains the work, via a hover card, when we have a blurb for it. */
      var span = document.createElement("span");
      span.className = "p-titletext";
      span.appendChild(highlight(parts.text, toks));
      if (p.blurb) {
        span.className = "p-titletext has-blurb";
        span.setAttribute("data-blurb", p.blurb);
        span.tabIndex = 0;                 // reachable without a pointer
        span.setAttribute("role", "button");
        /* No aria-label: the title text is the accessible name. A fixed label
           here replaced it, so a screen reader announced every one of the
           papers as the same phrase. */
      }
      h.appendChild(span);
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

  // Toolkit groups, in display order; keep in sync with TOOLKIT_GROUPS in
  // scripts/build.py. Rows inside a group sort by stars, highest first.
  var TOOLKIT_GROUPS = [
    ["engines", "toolkitGroupEngines", "Reconstruction engines"],
    ["classical", "toolkitGroupClassical", "Operators, solvers & classical algorithms"],
    ["learning", "toolkitGroupLearning", "Differentiable & learned reconstruction"],
    ["simulation", "toolkitGroupSimulation", "Simulation, phantoms & physics"],
    ["correction", "toolkitGroupCorrection", "Artefact correction & calibration"],
    ["platforms", "toolkitGroupPlatforms", "Data, viewers & platforms"]
  ];

  // NB: the callback parameter must NOT be named `t` — that would shadow the
  // i18n helper t() above, and the `t("homepageTitle")` call below would
  // then be calling a row object. It threw for every toolkit that carries a
  // homepage, which aborted init() before the search box was ever wired up.
  function toolkitRow(row) {
    var nm = esc(row.label || row.name);
    var html = '<a href="' + esc(row.url) + '" target="_blank" rel="noopener">' + nm + "</a>";
    if (row.homepage) {
      html += ' <a href="' + esc(row.homepage) + '" target="_blank" rel="noopener" title="' + t("homepageTitle", "homepage") + '">'
            + '<span class="mono">[site]</span></a>';
    }
    return ["@@HTML@@" + html, row.language || "-", row.license || "-",
            row.stars == null ? "-" : String(row.stars), "@@HTML@@" + mdInline(row.note)];
  }

  function renderToolkits() {
    var cols = [{ label: t("tableToolkit", "Toolkit") }, { label: t("tableLanguage", "Language") },
      { label: t("tableLicense", "License"), cls: "lic" },
      { label: t("tableStars", "Stars"), cls: "n" },
      { label: t("tableNotes", "Notes"), cls: "note" }];
    var byStars = function (a, b) { return (b.stars || 0) - (a.stars || 0); };
    var html = "";
    var seen = {};
    TOOLKIT_GROUPS.forEach(function (g) {
      var rows = DATA.toolkits.filter(function (r) { return r.group === g[0]; }).sort(byStars);
      if (!rows.length) return;
      rows.forEach(function (r) { seen[r.name] = true; });
      var tmp = document.createElement("div");
      renderTable(tmp, cols, rows.map(toolkitRow));
      html += '<h3 class="toolkit-group">' + esc(t(g[1], g[2])) + " (" + rows.length + ")</h3>" + tmp.innerHTML;
    });
    // Defensive fallback: an entry with an unknown or missing group must
    // never vanish from the tab; it lands in "Other" at the end.
    var rest = DATA.toolkits.filter(function (r) { return !seen[r.name]; }).sort(byStars);
    if (rest.length) {
      var tmp = document.createElement("div");
      renderTable(tmp, cols, rest.map(toolkitRow));
      html += '<h3 class="toolkit-group">' + esc(t("toolkitGroupOther", "Other")) + " (" + rest.length + ")</h3>" + tmp.innerHTML;
    }
    document.getElementById("t-toolkits").innerHTML = html;
  }

  /* A dataset / benchmark name links to its own page on this site when it has
     one (payload `page`, relative to the language root); the official page
     stays one click away as a separate external link. */
  function resourceName(r) {
    var label = esc(r.label || r.name);
    if (!r.page) {
      return '<a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + label + "</a>";
    }
    var G = DATA.guides || {};
    var html = '<a href="' + esc(r.page) + '">' + label + "</a>";
    if (r.url) {
      html += ' <a class="ext" href="' + esc(r.url) + '" target="_blank" rel="noopener" title="' +
        esc(G.officialTitle || "official page") + '"><span class="mono">' +
        esc(G.official || "[official]") + "</span></a>";
    }
    return html;
  }

  function renderDatasets() {
    renderTable(document.getElementById("t-datasets"),
      [{ label: t("tableDataset", "Dataset") }, { label: t("tableModality", "Modality") },
       { label: t("tableTasks", "Tasks"), cls: "tasks" },
       { label: t("tableLicense", "License"), cls: "lic" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      DATA.datasets.map(function (d) {
        var nm = resourceName(d);
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
        var nm = resourceName(b);
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
    var host = document.getElementById("t-learning");
    var cols = [{ label: t("tableResource", "Resource") }, { label: t("tableType", "Type"), cls: "n" },
       { label: t("tableNotes", "Notes"), cls: "note" }];
    renderTable(host, cols,
      rows.map(function (l) {
        var nm = '<a href="' + esc(l.url) + '" target="_blank" rel="noopener">' + esc(l.label || l.name) + "</a>";
        return ["@@HTML@@" + nm, l.type || "-", "@@HTML@@" + mdInline(l.note)];
      }));
    /* The site's own guides, as a small group above the outside resources. */
    var G = DATA.guides;
    var table = host.querySelector("table");
    if (!G || !(G.items || []).length || !table) return;
    var lab = function (i) { return ' data-label="' + esc(cols[i].label) + '"'; };
    var html = '<tr class="grp-head"><th colspan="3" scope="rowgroup">' + esc(G.label) +
      ' <a href="' + esc(G.index) + '">' + esc(G.indexLabel) + " \u2192</a></th></tr>" +
      G.items.map(function (g) {
        return "<tr><td" + lab(0) + '><a href="' + esc(g.url) + '">' + esc(g.title) + "</a></td>" +
          '<td class="n"' + lab(1) + ">" + esc(G.kind) + "</td>" +
          '<td class="note"' + lab(2) + ">" + esc(g.note) + "</td></tr>";
      }).join("");
    var tb = document.createElement("tbody");
    tb.className = "grp-guides";
    tb.innerHTML = html;
    table.insertBefore(tb, table.querySelector("tbody"));
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

  /* Visibility only: the panel switch itself, without any rendering. */
  function showTab(name) {
    Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (b) {
      b.setAttribute("aria-selected", String(b.dataset.tab === name));
    });
    Array.prototype.forEach.call(document.querySelectorAll("section[role=tabpanel]"), function (s) {
      s.hidden = s.id !== "panel-" + name;
    });
    /* The CSS shows the right panel from this attribute before app.js has
       run (it is first set by the inline script in index.html). */
    if (name === "papers") document.documentElement.removeAttribute("data-tab");
    else document.documentElement.setAttribute("data-tab", name);
  }

  function setTab(name, push) {
    state.tab = name;
    showTab(name);
    if (name === "papers") {
      if (papersStale) { apply(); }
    } else {
      renderTab(name);
    }
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
      /* The chips were rendered before the address was read; without this the
         list was filtered but no chip showed as selected. */
      syncTopicChips();
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

  /* Section tables render on first use, not all at load: a datasets deep
     link used to pay for every table before the visible one appeared. */
  var renderedTabs = {};
  function renderTab(name) {
    if (renderedTabs[name]) { return; }
    renderedTabs[name] = true;
    if (name === "toolkits") { renderToolkits(); }
    else if (name === "datasets") { renderDatasets(); }
    else if (name === "benchmarks") { renderBenchmarks(); }
    else if (name === "learning") { renderLearning(); }
    /* papers renders through apply()/upgradeServerList; teams and graph are static. */
  }

  /* True when the URL asks for anything beyond the plain newest-first
     papers view. Only then does the first render need the full rebuild;
     the plain view upgrades the served list in place instead. */
  function hasFilters() {
    return !!state.q || state.topics.length > 0 || state.type !== "all" ||
      state.code || state.from !== 0 || state.sort !== "new";
  }

  /* The served papers list already shows the plain view, so rebuilding it
     from DATA would only swap identical rows and block the first paint
     behind 678 fresh nodes. Upgrade it in place instead: the year
     headings renderPapers would insert, and the data-blurb the hover
     cards read (served titles carry the blurb as a plain `title` tooltip
     for no-JS readers; the card needs data-blurb, and keeping both
     would show two tooltips at once). */
  function upgradeServerList() {
    var byId = {};
    DATA.papers.forEach(function (p) { byId[p.id] = p; });
    var perYear = {};
    DATA.papers.forEach(function (p) { perYear[p.year] = (perYear[p.year] || 0) + 1; });
    var lastYear = null;
    Array.prototype.forEach.call(listEl.querySelectorAll("li.paper"), function (li) {
      var span = li.querySelector(".p-titletext");
      var p = span ? byId[span.getAttribute("data-id")] : null;
      if (p && p.year !== lastYear) {
        lastYear = p.year;
        var yl = document.createElement("li");
        yl.className = "year-sep";
        var yh = document.createElement("h2");
        yh.textContent = String(p.year);
        var yn = document.createElement("span");
        yn.className = "n";
        yn.textContent = perYear[p.year];
        yh.appendChild(yn);
        yl.appendChild(yh);
        listEl.insertBefore(yl, li);
      }
      if (span && span.hasAttribute("title")) {
        span.setAttribute("data-blurb", span.getAttribute("title"));
        span.removeAttribute("title");
      }
    });
    countEl.textContent = DATA.papers.length;
    emptyEl.hidden = DATA.papers.length !== 0;
  }

  /* Nothing JS-rendered yet: the served list is pre-JS markup until init
     upgrades or replaces it. */
  var papersStale = true;

  function apply() {
    if (state.tab === "papers") {
      renderPapers();
      papersStale = false;
    } else {
      /* The papers panel is hidden: rendering 678 rows into it now would
         only block the visible tab. Defer it until papers is opened. */
      papersStale = true;
    }
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

    /* The embedded payload carries no blurbs: each one is already in the
       server-rendered title's `title=`, so read them back from there before
       the first render replaces that list. */
    var blurbs = {};
    listEl.querySelectorAll(".p-titletext[data-id][title]").forEach(function (el) {
      blurbs[el.getAttribute("data-id")] = el.getAttribute("title");
    });
    DATA.papers.forEach(function (p) {
      if (!p.blurb && blurbs[p.id]) { p.blurb = blurbs[p.id]; }
    });

    /* Hover cards are delegated from the list, so re-rendering it (every
       keystroke) never has to rebind anything. */
    listEl.addEventListener("mouseover", function (e) {
      var t = cardTarget(e);
      if (t) { showCard(t); }
    });
    listEl.addEventListener("mouseout", function (e) {
      if (cardTarget(e)) { hideCard(); }
    });
    listEl.addEventListener("focusin", function (e) {
      var t = cardTarget(e);
      if (t) { showCard(t); }
    });
    listEl.addEventListener("focusout", function (e) {
      if (cardTarget(e)) { hideCard(); }
    });
    /* Tap: touch has no hover, so a tap toggles. On desktop the click lands
       while the card is already up, and hiding it then keeps the card from
       covering the text the reader is trying to select. */
    listEl.addEventListener("click", function (e) {
      var t = cardTarget(e);
      if (!t) { return; }
      if (cardEl && !cardEl.hidden) { hideCard(); } else { showCard(t); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { hideCard(); }
    });

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
      learning: DATA.learning.length, teams: (DATA.teams || []).length
    };
    Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (b) {
      var n = document.createElement("span");
      n.className = "n";
      n.textContent = counts[b.dataset.tab] || 0;
      b.appendChild(n);
      b.addEventListener("click", function () { setTab(b.dataset.tab); });
    });

    /* The URL decides the visible tab BEFORE anything heavy renders, so a
       ?tab= deep link never flashes the papers list while the other
       tables build. */
    readUrl();
    if (state.tab === "papers" && !hasFilters()) {
      /* Plain view: the served list already shows exactly this, so upgrade
         it in place (year headings, data-blurb cards) instead of
         rebuilding 678 rows. */
      upgradeServerList();
      papersStale = false;
      showTab(state.tab);
    } else {
      /* A filtered papers view renders through apply(); any other tab
         renders its own table on first open (see setTab). */
      setTab(state.tab, false);
    }
    renderTopics();
    writeUrl();

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
