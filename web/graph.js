/* Knowledge graph explorer for /graph/ and /zh/graph/.
 *
 * The data is graph.json, generated at build time from the same payload
 * as the rest of the site (scripts/graph.py), INCLUDING static node
 * positions computed offline by scripts/graph_layout.py. Nothing is
 * simulated or laid out in the browser: the renderer (vendored
 * sigma.js, WebGL, batched programs) only draws. Visibility is a
 * filter over precomputed coordinates, so expanding a node, switching
 * to the full graph or jumping via search never triggers a relayout —
 * the page opens on a backbone (teams + topics + toolkits) and the
 * rest arrives by expanding nodes, searching, or the full-graph
 * toggle, exactly as before, just without the wait.
 *
 * Plain script, no modules, in the same style as app.js/search.js. If
 * sigma/graphology or the data fails to load, the server-rendered
 * fallback list stays visible and this file simply does nothing.
 */
(function () {
  "use strict";

  var S = window.GRAPH_STRINGS || {};
  var LANG = window.GRAPH_LANG || "en";
  var ROOT = window.GRAPH_ROOT || "../";

  function t(key, fallback) { return S[key] || fallback || key; }
  function label(n) { return (LANG === "zh" && n.lz) ? n.lz : n.l; }

  var stage = document.getElementById("graph-stage");
  if (!stage || typeof window.Sigma === "undefined" ||
      typeof window.graphology === "undefined") return;

  fetch(ROOT + "graph.json")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (G) {
      try { init(G); }
      catch (err) {
        // Surface init failures in the console before the catch below
        // turns them into the generic load note — a swallowed init
        // error once masqueraded as a data-load failure for a day.
        if (window.console) console.error("graph init failed:", err);
        throw err;
      }
    })
    .catch(function () {
      var note = document.getElementById("graph-load-note");
      if (note) note.hidden = false;
    });

  function init(G) {
    var byId = {};
    G.nodes.forEach(function (n) { byId[n.id] = n; });
    var pos = G.pos || {};

    // Degree over the *whole* graph drives node size, so a hub looks
    // like a hub even before it is expanded.
    var degree = {};
    G.edges.forEach(function (e) {
      degree[e[0]] = (degree[e[0]] || 0) + 1;
      degree[e[1]] = (degree[e[1]] || 0) + 1;
    });
    var neighbours = {};   // id -> [{id, kind, dir}] dir: 'out'|'in'
    G.edges.forEach(function (e) {
      (neighbours[e[0]] = neighbours[e[0]] || []).push({ id: e[1], kind: e[2], dir: "out" });
      (neighbours[e[1]] = neighbours[e[1]] || []).push({ id: e[0], kind: e[2], dir: "in" });
    });

    var COLORS = {
      paper: "#4e79a7", toolkit: "#59a14f", dataset: "#f28e2b",
      benchmark: "#e15759", team: "#9467bd", topic: "#17becf",
      venue: "#8c564b", author: "#e377c2", learning: "#7f7f7f",
      guide: "#bcbd22"
    };
    var EDGE_COLORS = {
      cites: "#e15759", authored: "#e8b4d8", coauthor: "#d8d8d8",
      focus: "#b39ddb", works: "#b39ddb", leads: "#b39ddb"
    };
    var TYPE_ORDER = ["team", "topic", "paper", "toolkit", "dataset",
                      "benchmark", "author", "venue", "learning", "guide"];

    function lighten(hex) {
      var n = parseInt(hex.slice(1), 16);
      function mix(c) { return Math.round(c + (255 - c) * 0.8); }
      return "rgb(" + mix((n >> 16) & 255) + "," + mix((n >> 8) & 255) +
             "," + mix(n & 255) + ")";
    }
    var DIM_COLORS = {};
    Object.keys(COLORS).forEach(function (k) { DIM_COLORS[k] = lighten(COLORS[k]); });

    // ------------------------------------------------------------- state
    var expanded = {};     // id -> true once its neighbourhood is shown
    var fullMode = false;
    var egoOnly = null;    // id whose ego network alone is shown
    var typeOn = {};       // type -> bool (filter checkboxes)
    TYPE_ORDER.forEach(function (ty) { typeOn[ty] = true; });
    var regionWant = "";   // team-region dimming ("" = all regions)
    var selected = null;
    var hoverId = null;

    var backbone = {};
    (G.backbone || []).forEach(function (id) { backbone[id] = true; });

    function visibleIds() {
      var vis = {};
      if (fullMode) {
        G.nodes.forEach(function (n) { vis[n.id] = true; });
      } else if (egoOnly) {
        vis[egoOnly] = true;
        (neighbours[egoOnly] || []).forEach(function (x) { vis[x.id] = true; });
      } else {
        Object.keys(backbone).forEach(function (id) { vis[id] = true; });
        Object.keys(expanded).forEach(function (id) {
          vis[id] = true;
          (neighbours[id] || []).forEach(function (x) { vis[x.id] = true; });
        });
      }
      Object.keys(vis).forEach(function (id) {
        if (byId[id] && !typeOn[byId[id].t]) delete vis[id];
      });
      return vis;
    }
    var visNow = visibleIds();

    // Highlight set for hover/selection emphasis (ids + edge keys).
    var hlNodes = null, hlEdges = null;
    function computeHighlight() {
      var focus = hoverId || selected;
      hlNodes = null; hlEdges = null;
      if (!focus) return;
      hlNodes = {}; hlEdges = {};
      hlNodes[focus] = true;
      (neighbours[focus] || []).forEach(function (x) {
        hlNodes[x.id] = true;
      });
      G.edges.forEach(function (e, i) {
        if (e[0] === focus || e[1] === focus) hlEdges["e" + i] = true;
      });
    }

    // ------------------------------------------------- graphology + sigma
    var graph = new window.graphology.MultiGraph();
    G.nodes.forEach(function (n) {
      var p = pos[n.id] || [0, 0];
      graph.addNode(n.id, {
        label: label(n),
        x: p[0], y: p[1],
        size: 2.6 + Math.min(13, Math.sqrt(degree[n.id] || 0) * 1.5),
        color: COLORS[n.t] || "#999",
        ntype: n.t
      });
    });
    G.edges.forEach(function (e, i) {
      graph.addEdgeWithKey("e" + i, e[0], e[1], {
        kind: e[2],
        size: e[2] === "cites" ? 0.9 : 0.5,
        color: EDGE_COLORS[e[2]] || "#c3c9d4",
        type: e[2] === "cites" ? "arrow" : "line"
      });
    });

    var sigma = new window.Sigma(graph, stage, {
      renderLabels: true,
      labelRenderedSizeThreshold: 5.5,
      labelDensity: 0.12,
      labelGridCellSize: 60,
      labelSize: 12,
      labelColor: { color: "#5a6270" },
      defaultNodeColor: "#999",
      defaultEdgeColor: "#c3c9d4",
      minCameraRatio: 0.04,
      maxCameraRatio: 6,
      zIndex: true,
      stagePadding: 30
    });

    function nodeDimmed(id) {
      var n = byId[id];
      if (regionWant && n && n.t === "team" && n.m &&
          n.m.region !== regionWant) return true;
      if (hlNodes && !hlNodes[id]) return true;
      return false;
    }

    // Sigma 3's reducer contract: the return value REPLACES the node's
    // display data — it is not merged with the raw attributes. A
    // partial return therefore drops x/y, sigma throws inside
    // setSetting below, init() dies before any control is wired, and
    // the fetch .catch() unhides the "could not be loaded" note even
    // though the graph rendered. Always start from a copy of `data`.
    sigma.setSetting("nodeReducer", function (id, data) {
      var out = Object.assign({}, data);
      if (!visNow[id]) { out.hidden = true; return out; }
      var n = byId[id];
      // Backbone hubs always carry their (full) label; everyone else
      // is labelled by the zoom threshold, and hover/selection forces
      // the label of the node being inspected.
      if ((backbone[id] && !egoOnly) || id === selected || id === hoverId) {
        out.forceLabel = true;
      }
      if (nodeDimmed(id)) {
        out.color = DIM_COLORS[n.t] || "#ddd";
        out.zIndex = 0;
      }
      if (id === selected) { out.size = data.size * 1.3; out.zIndex = 3; }
      else if (id === hoverId) { out.zIndex = 2; }
      return out;
    });
    sigma.setSetting("edgeReducer", function (key, data) {
      var out = Object.assign({}, data);
      var s = graph.source(key), tg = graph.target(key);
      if (!visNow[s] || !visNow[tg]) { out.hidden = true; return out; }
      if (hlEdges && !hlEdges[key]) {
        out.color = "rgba(196,202,212,0.13)";
        out.zIndex = 0;
      } else if (hlEdges) {
        out.size = data.size * 1.7;
        out.zIndex = 2;
      }
      return out;
    });

    var fallback = document.getElementById("graph-fallback");
    if (fallback) fallback.hidden = true;
    var bar = document.getElementById("graph-bar");
    if (bar) bar.hidden = false;

    // -------------------------------------------------------------- camera
    // Camera ratio = graph units per screen pixel (smaller = closer).
    function frameIds(ids, animate) {
      if (!ids.length) return;
      var minx = 1e18, miny = 1e18, maxx = -1e18, maxy = -1e18;
      ids.forEach(function (id) {
        var p = pos[id];
        if (!p) return;
        if (p[0] < minx) minx = p[0];
        if (p[0] > maxx) maxx = p[0];
        if (p[1] < miny) miny = p[1];
        if (p[1] > maxy) maxy = p[1];
      });
      if (minx > maxx) return;
      var cw = stage.clientWidth || 800, ch = stage.clientHeight || 500;
      var w = Math.max(60, maxx - minx), h = Math.max(60, maxy - miny);
      var ratio = Math.max(w / cw, h / ch) * 1.12;
      ratio = Math.min(6, Math.max(0.04, ratio));
      var cam = sigma.getCamera();
      var target = { x: (minx + maxx) / 2, y: (miny + maxy) / 2, ratio: ratio };
      if (animate === false) cam.setState(target);
      else cam.animate(target, { duration: 550 });
    }
    function frameVisible(animate) {
      frameIds(Object.keys(visNow), animate);
    }
    frameVisible(false);

    function refresh(frame) {
      visNow = visibleIds();
      computeHighlight();
      sigma.refresh();
      updateCounts(visNow);
      if (frame) frameVisible(true);
    }

    function updateCounts(vis) {
      var el = document.getElementById("graph-counts");
      if (!el) return;
      var shown = Object.keys(vis).length;
      el.textContent = t("counts", "")
        .replace("{shown}", shown).replace("{total}", G.nodes.length)
        .replace("{edges}", G.edges.length);
    }

    // ---------------------------------------------------------- detail panel
    var panel = document.getElementById("graph-panel");

    function metaRows(n) {
      var m = n.m || {};
      var rows = [];
      function row(k, v) { if (v) rows.push([t(k, k), v]); }
      if (n.y) row("mYear", String(n.y));
      if (m.title) row("mTitle", m.title);
      if (m.venue) row("mVenue", m.venue);
      if (m.institution) row("mInstitution", m.institution + (m.city ? ", " + m.city : "") + (m.country ? ", " + m.country : ""));
      if (m.pi) row("mPi", m.pi.join(", "));
      if (m.language) row("mLanguage", m.language);
      if (m.license) row("mLicense", m.license);
      if (m.stars) row("mStars", String(m.stars));
      if (m.modality) row("mModality", m.modality);
      if (m.type) row("mKind", m.type);
      if (m.papers) row("mPapersHere", String(m.papers));
      if (m.count) row("mCount", String(m.count));
      if (m.openalex) rows.push(["OpenAlex", m.openalex]);
      return rows;
    }

    function showPanel(id) {
      var n = byId[id];
      if (!panel || !n) return;
      document.getElementById("gp-type").textContent = t("type_" + n.t, n.t);
      document.getElementById("gp-type").style.background = COLORS[n.t] || "#999";
      document.getElementById("gp-name").textContent = label(n);
      var meta = document.getElementById("gp-meta");
      meta.innerHTML = "";
      metaRows(n).forEach(function (r) {
        var dt = document.createElement("dt"); dt.textContent = r[0];
        var dd = document.createElement("dd"); dd.textContent = r[1];
        meta.appendChild(dt); meta.appendChild(dd);
      });
      // Neighbours grouped by edge kind, each a jump link.
      var groups = {};
      (neighbours[id] || []).forEach(function (x) {
        (groups[x.kind] = groups[x.kind] || []).push(x);
      });
      var wrap = document.getElementById("gp-neighbours");
      wrap.innerHTML = "";
      Object.keys(groups).sort().forEach(function (kind) {
        var h = document.createElement("h4");
        h.textContent = t("edge_" + kind, kind) + " · " + groups[kind].length;
        wrap.appendChild(h);
        var ul = document.createElement("ul");
        groups[kind].slice(0, 40).forEach(function (x) {
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#";
          a.textContent = label(byId[x.id]);
          a.addEventListener("click", function (ev) {
            ev.preventDefault();
            focusNode(x.id, true);
          });
          li.appendChild(a);
          ul.appendChild(li);
        });
        if (groups[kind].length > 40) {
          var more = document.createElement("li");
          more.textContent = "… +" + (groups[kind].length - 40);
          ul.appendChild(more);
        }
        wrap.appendChild(ul);
      });
      var open = document.getElementById("gp-open");
      if (n.href) {
        open.hidden = false;
        open.href = /^https?:/.test(n.href) ? n.href
          : new URL(n.href, new URL(ROOT, window.location.href)).href;
        open.target = /^https?:/.test(n.href) ? "_blank" : "";
        open.rel = "noopener";
      } else {
        open.hidden = true;
      }
      document.getElementById("gp-expand").textContent =
        expanded[id] ? t("collapse", "Collapse") : t("expand", "Expand");
      panel.hidden = false;
    }

    function focusNode(id, expandIt) {
      if (!fullMode && egoOnly && egoOnly !== id) egoOnly = null;
      if (expandIt) expanded[id] = true;
      selected = id;
      refresh(false);
      showPanel(id);
      // Fly to a window around the node (never zoom back out).
      var p = pos[id];
      if (p) {
        var cw = stage.clientWidth || 800;
        var cam = sigma.getCamera();
        var ratio = Math.min(cam.ratio, Math.max(0.04, 620 / cw));
        cam.animate({ x: p[0], y: p[1], ratio: ratio }, { duration: 550 });
      }
    }

    sigma.on("clickNode", function (ev) {
      var id = ev.node;
      if (!expanded[id] && !fullMode) expanded[id] = true;
      selected = id;
      refresh(false);
      showPanel(id);
    });
    sigma.on("clickStage", function () {
      selected = null;
      if (panel) panel.hidden = true;
      refresh(false);
    });
    sigma.on("enterNode", function (ev) {
      hoverId = ev.node;
      stage.style.cursor = "pointer";
      computeHighlight();
      sigma.refresh();
    });
    sigma.on("leaveNode", function () {
      hoverId = null;
      stage.style.cursor = "";
      computeHighlight();
      sigma.refresh();
    });

    // ------------------------------------------------------------- controls
    document.getElementById("gp-expand").addEventListener("click", function () {
      if (!selected) return;
      if (expanded[selected]) delete expanded[selected]; else expanded[selected] = true;
      refresh(false); showPanel(selected);
    });
    var egoBtn = document.getElementById("gp-ego");
    egoBtn.addEventListener("click", function () {
      if (!selected) return;
      egoOnly = (egoOnly === selected) ? null : selected;
      egoBtn.textContent = egoOnly ? t("showAll2", "Back to overview")
                                   : t("egoOnly", "Only this network");
      refresh(true); showPanel(selected);
    });
    document.getElementById("gp-close").addEventListener("click", function () {
      panel.hidden = true; selected = null; refresh(false);
    });

    var fullBtn = document.getElementById("graph-full");
    if (fullBtn) fullBtn.addEventListener("click", function () {
      fullMode = !fullMode;
      egoOnly = null;
      egoBtn.textContent = t("egoOnly", "Only this network");
      fullBtn.textContent = fullMode ? t("backbone", "Backbone view")
                                     : t("fullGraph", "Full graph");
      var warn = document.getElementById("graph-full-note");
      if (warn) warn.hidden = !fullMode;
      refresh(true);
    });
    var resetBtn = document.getElementById("graph-reset");
    if (resetBtn) resetBtn.addEventListener("click", function () {
      expanded = {}; egoOnly = null; fullMode = false;
      selected = null; hoverId = null;
      if (panel) panel.hidden = true;
      if (fullBtn) fullBtn.textContent = t("fullGraph", "Full graph");
      egoBtn.textContent = t("egoOnly", "Only this network");
      refresh(true);
    });

    // Type filters + legend (one checkbox per type present in the data).
    var legend = document.getElementById("graph-types");
    if (legend) {
      var present = {};
      G.nodes.forEach(function (n) { present[n.t] = true; });
      TYPE_ORDER.forEach(function (ty) {
        if (!present[ty]) return;
        var lab = document.createElement("label");
        lab.className = "g-type";
        var cb = document.createElement("input");
        cb.type = "checkbox"; cb.checked = true; cb.value = ty;
        cb.addEventListener("change", function () {
          typeOn[ty] = cb.checked; refresh(false);
        });
        var dot = document.createElement("span");
        dot.className = "g-dot"; dot.style.background = COLORS[ty];
        lab.appendChild(cb); lab.appendChild(dot);
        lab.appendChild(document.createTextNode(t("type_" + ty, ty)));
        legend.appendChild(lab);
      });
    }

    // Topic focus: jump straight to a topic's ego network.
    var topicSel = document.getElementById("graph-topic");
    if (topicSel) {
      G.nodes.filter(function (n) { return n.t === "topic"; })
        .sort(function (a, b) { return label(a).localeCompare(label(b)); })
        .forEach(function (n) {
          var o = document.createElement("option");
          o.value = n.id; o.textContent = label(n);
          topicSel.appendChild(o);
        });
      topicSel.addEventListener("change", function () {
        if (topicSel.value) { egoOnly = null; focusNode(topicSel.value, true); }
      });
    }

    // Region dimming for teams.
    var regionSel = document.getElementById("graph-region");
    if (regionSel) regionSel.addEventListener("change", function () {
      regionWant = regionSel.value;
      sigma.refresh();
    });

    // Search: datalist over every node's label.
    var search = document.getElementById("graph-search");
    var list = document.getElementById("graph-search-list");
    if (search && list) {
      var byLabel = {};
      G.nodes.forEach(function (n) {
        var o = document.createElement("option");
        o.value = label(n);
        list.appendChild(o);
        byLabel[label(n)] = n.id;
        if (n.l && n.l !== label(n)) byLabel[n.l] = n.id;
      });
      search.addEventListener("change", function () {
        var id = byLabel[search.value.trim()];
        if (id) { egoOnly = null; focusNode(id, true); }
      });
    }

    updateCounts(visNow);
  }
})();

