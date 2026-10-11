/* awesome-computed-tomography — client-side filtering.
   Classic script (NOT a module) so the page also works when opened from
   file://, where ES modules are blocked by CORS.

   Search is a plain substring match over a pre-computed `_q` blob shipped in
   the page, so there is no index to download and no query parser to trip over
   (Paper-Notes lost hours to lunr throwing on ':' in paper titles). */

(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("site-data").textContent);
  var TOPIC = {};
  DATA.topics.forEach(function (t) { TOPIC[t.id] = t; });

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

  /* Title with the leading abbreviation stripped, mirroring README.md:
     "DM4CT: Benchmarking ..." renders as [DM4CT] Benchmarking ... */
  function titleParts(p) {
    // Inline TeX like "$K$-NeAS" shows as plain text: drop the $ delimiters.
    var title = p.title.replace(/\$([^$]+)\$/g, "$1");
    if (p.abbr && title.toLowerCase().indexOf(p.abbr.toLowerCase()) === 0) {
      var rest = title.slice(p.abbr.length).replace(/^[\s:\u2014\u2013-]+/, "");
      return { abbr: p.abbr, text: rest || title };
    }
    return { abbr: p.abbr || "", text: title };
  }

  /* Highlight query tokens in a plain-text title, escaping as we go.
     Builds DOM nodes rather than innerHTML so escaping cannot be bypassed. */
  function highlight(text, tokens) {
    var frag = document.createDocumentFragment();
    if (!tokens.length) { frag.appendChild(document.createTextNode(text)); return frag; }
    var lower = text.toLowerCase();
    var marks = [];
    tokens.forEach(function (tok) {
      var from = 0, at;
      while ((at = lower.indexOf(tok, from)) !== -1) {
        marks.push([at, at + tok.length]);
        from = at + tok.length;
      }
    });
    if (!marks.length) { frag.appendChild(document.createTextNode(text)); return frag; }
    marks.sort(function (a, b) { return a[0] - b[0] || b[1] - a[1]; });
    var merged = [marks[0]];
    for (var i = 1; i < marks.length; i++) {
      var last = merged[merged.length - 1];
      if (marks[i][0] <= last[1]) { last[1] = Math.max(last[1], marks[i][1]); }
      else { merged.push(marks[i]); }
    }
    var pos = 0;
    merged.forEach(function (m) {
      if (m[0] > pos) frag.appendChild(document.createTextNode(text.slice(pos, m[0])));
      var el = document.createElement("mark");
      el.textContent = text.slice(m[0], m[1]);
      frag.appendChild(el);
      pos = m[1];
    });
    if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
    return frag;
  }

  function haystack(p) {
    /* `_q` already holds title + abbr + venue + topic names + link host and id,
       all lower-cased. Year is appended here so "2026" filters by year without
       bloating the shipped data. */
    return p._q + " " + p.year;
  }

  function tokens() {
    return state.q.toLowerCase().split(/\s+/).filter(Boolean);
  }

  /* ------------------------------------------------------------ filtering */

  function selectedPapers() {
    var toks = tokens();
    var out = DATA.papers.filter(function (p) {
      if (state.type === "peer" && p.preprint) return false;
      if (state.type === "preprint" && !p.preprint) return false;
      if (state.code && !p.links.code) return false;
      if (state.from && p.year < state.from) return false;
      if (state.topics.length) {
        var hit = false;
        for (var i = 0; i < state.topics.length; i++) {
          if (p.topics.indexOf(state.topics[i]) !== -1) { hit = true; break; }
        }
        if (!hit) return false;
      }
      if (toks.length) {
        var hay = haystack(p);
        for (var j = 0; j < toks.length; j++) {
          if (hay.indexOf(toks[j]) === -1) return false;
        }
      }
      return true;
    });

    if (state.sort === "title") {
      out.sort(function (a, b) {
        return (a.abbr || a.title).toLowerCase() < (b.abbr || b.title).toLowerCase() ? -1 : 1;
      });
    } else if (state.sort === "old") {
      out.sort(function (a, b) {
        return a.year - b.year ||
          ((a.abbr || a.title).toLowerCase() < (b.abbr || b.title).toLowerCase() ? -1 : 1);
      });
    }
    /* "new" keeps the server-side order, which is already (-year, abbr|title). */
    return out;
  }

  /* ------------------------------------------------------------ rendering */

  var listEl, countEl, emptyEl;

  function renderPapers() {
    var rows = selectedPapers();
    var toks = tokens();
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
      var t = titleParts(p);
      if (url) {
        var a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener";
        a.appendChild(highlight(t.text, toks));
        h.appendChild(a);
      } else {
        h.appendChild(highlight(t.text, toks));
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
        tp.textContent = p.topics.map(function (id) {
          return TOPIC[id] ? TOPIC[id].name : id;
        }).join(" \u00b7 ");
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
      rows.map(function (t) {
        var nm = esc(t.name);
        var html = '<a href="' + esc(t.url) + '" target="_blank" rel="noopener">' + nm + "</a>";
        if (t.homepage) {
          html += ' <a href="' + esc(t.homepage) + '" target="_blank" rel="noopener" title="' + t("homepageTitle", "homepage") + '">'
                + '<span class="mono">[site]</span></a>';
        }
        return ["@@HTML@@" + html, t.language || "-", t.license || "-",
                t.stars == null ? "-" : String(t.stars), "@@HTML@@" + mdInline(t.note)];
      }));
  }

  function renderDatasets() {
    renderTable(document.getElementById("t-datasets"),
      [{ label: t("tableDataset", "Dataset") }, { label: t("tableModality", "Modality") },
       { label: t("tableTasks", "Tasks"), cls: "tasks" },
       { label: t("tableLicense", "License"), cls: "n" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      DATA.datasets.map(function (d) {
        var nm = '<a href="' + esc(d.url) + '" target="_blank" rel="noopener">' + esc(d.name) + "</a>";
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
        var nm = '<a href="' + esc(b.url) + '" target="_blank" rel="noopener">' + esc(b.name) + "</a>";
        return ["@@HTML@@" + nm, b.year == null ? "-" : String(b.year),
                (b.tasks || []).join(", ") || "-", "@@HTML@@" + mdInline(b.note)];
      }));
  }

  function renderLearning() {
    var order = { book: 1, course: 2, tutorial: 3, tool: 4, list: 5 };
    var rows = DATA.learning.slice().sort(function (a, b) {
      return (order[a.type] || 9) - (order[b.type] || 9) || a.name.localeCompare(b.name);
    });
    renderTable(document.getElementById("t-learning"),
      [{ label: t("tableResource", "Resource") }, { label: t("tableType", "Type"), cls: "n" },
       { label: t("tableNotes", "Notes"), cls: "note" }],
      rows.map(function (l) {
        var nm = '<a href="' + esc(l.url) + '" target="_blank" rel="noopener">' + esc(l.name) + "</a>";
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
    var t;
    return function () {
      var self = this, args = arguments;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(self, args); }, ms);
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
        o.textContent = y + " and later";
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
      var t = e.target;
      if (t && (t.tagName === "INPUT" || t.tagName === "SELECT" || t.tagName === "TEXTAREA")) return;
      e.preventDefault();
      (document.getElementById("gq") || document.getElementById("q")).focus();
    });

    var theme = document.getElementById("theme");
    if (theme) {
      var saved = null;
      try { saved = localStorage.getItem("ct-theme"); } catch (err) { saved = null; }
      if (saved) document.documentElement.setAttribute("data-theme", saved);
      theme.addEventListener("click", function () {
        var cur = document.documentElement.getAttribute("data-theme");
        if (!cur) {
          cur = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }
        var next = cur === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try { localStorage.setItem("ct-theme", next); } catch (err) {}
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
