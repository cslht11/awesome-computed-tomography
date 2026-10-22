/* Small-graph explorer for the per-category graph pages under
 * /graph/ (backbone, datasets, one page per topic; EN + ZH).
 *
 * Each page loads ONLY its own slice — a small data.json generated at
 * build time from the same payload as the rest of the site
 * (scripts/graph.py + scripts/graph_slices.py), including static node
 * positions computed offline by scripts/graph_layout.py. A slice is at
 * most a few hundred nodes, so the page renders instantly and there is
 * deliberately no full-graph mode: the category split is the filter.
 * Nothing is simulated or laid out in the browser; the renderer
 * (vendored sigma.js, WebGL, batched programs) only draws, and every
 * node of the slice is visible at once. Clicking a node opens its
 * detail panel and highlights its neighbours.
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
  var DATA = window.GRAPH_DATA || "data.json";

  function t(key, fallback) { return S[key] || fallback || key; }
  function label(n) { return (LANG === "zh" && n.lz) ? n.lz : n.l; }

  var stage = document.getElementById("graph-stage");
  if (!stage || typeof window.Sigma === "undefined" ||
      typeof window.graphology === "undefined") return;

  fetch(DATA)
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
    // The wire format is compact (scripts/graph_slices.py): edges are
    // [source, target, kind] index triples into the nodes array, with
    // the kind strings in G.kinds; positions align with the nodes.
    // Expand both back to id space once, here.
    var pos = {};
    G.nodes.forEach(function (n, i) { pos[n.id] = (G.pos || [])[i] || [0, 0]; });
    var EDGES = G.edges.map(function (e) {
      return [G.nodes[e[0]].id, G.nodes[e[1]].id, G.kinds[e[2]]];
    });

    // Degree within the slice drives node size, so a hub looks like a
    // hub on its own page.
    var degree = {};
    EDGES.forEach(function (e) {
      degree[e[0]] = (degree[e[0]] || 0) + 1;
      degree[e[1]] = (degree[e[1]] || 0) + 1;
    });
    var neighbours = {};   // id -> [{id, kind, dir}] dir: 'out'|'in'
    EDGES.forEach(function (e) {
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

    function lighten(hex) {
      var n = parseInt(hex.slice(1), 16);
      function mix(c) { return Math.round(c + (255 - c) * 0.8); }
      return "rgb(" + mix((n >> 16) & 255) + "," + mix((n >> 8) & 255) +
             "," + mix(n & 255) + ")";
    }
    var DIM_COLORS = {};
    Object.keys(COLORS).forEach(function (k) { DIM_COLORS[k] = lighten(COLORS[k]); });

    // ------------------------------------------------------------- state
    var selected = null;
    var hoverId = null;

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
      EDGES.forEach(function (e, i) {
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
    EDGES.forEach(function (e, i) {
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

    // Sigma 3's reducer contract: the return value REPLACES the node's
    // display data — it is not merged with the raw attributes. A
    // partial return therefore drops x/y and sigma throws inside
    // setSetting, killing init before any control is wired. Always
    // start from a copy of `data`.
    sigma.setSetting("nodeReducer", function (id, data) {
      var out = Object.assign({}, data);
      var n = byId[id];
      // Structural hubs always carry their label; everyone else is
      // labelled by the zoom threshold, and hover/selection forces the
      // label of the node being inspected.
      if ((n && (n.t === "team" || n.t === "topic")) ||
          id === selected || id === hoverId) {
        out.forceLabel = true;
      }
      if (hlNodes && !hlNodes[id]) {
        out.color = DIM_COLORS[n.t] || "#ddd";
        out.zIndex = 0;
      }
      if (id === selected) { out.size = data.size * 1.3; out.zIndex = 3; }
      else if (id === hoverId) { out.zIndex = 2; }
      return out;
    });
    sigma.setSetting("edgeReducer", function (key, data) {
      var out = Object.assign({}, data);
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
    function frameAll(animate) {
      var minx = 1e18, miny = 1e18, maxx = -1e18, maxy = -1e18;
      G.nodes.forEach(function (n) {
        var p = pos[n.id];
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
    frameAll(false);

    function refresh() {
      computeHighlight();
      sigma.refresh();
    }

    var countsEl = document.getElementById("graph-counts");
    if (countsEl) {
      countsEl.textContent = t("counts", "")
        .replace("{shown}", G.nodes.length)
        .replace("{total}", G.nodes.length)
        .replace("{edges}", EDGES.length);
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
            focusNode(x.id);
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
      panel.hidden = false;
    }

    function focusNode(id) {
      selected = id;
      refresh();
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
      focusNode(ev.node);
    });
    sigma.on("clickStage", function () {
      selected = null;
      if (panel) panel.hidden = true;
      refresh();
    });
    sigma.on("enterNode", function (ev) {
      hoverId = ev.node;
      stage.style.cursor = "pointer";
      refresh();
    });
    sigma.on("leaveNode", function () {
      hoverId = null;
      stage.style.cursor = "";
      refresh();
    });

    // ------------------------------------------------------------- controls
    var closeBtn = document.getElementById("gp-close");
    if (closeBtn) closeBtn.addEventListener("click", function () {
      panel.hidden = true; selected = null; refresh();
    });
    var resetBtn = document.getElementById("graph-reset");
    if (resetBtn) resetBtn.addEventListener("click", function () {
      selected = null; hoverId = null;
      if (panel) panel.hidden = true;
      refresh();
      frameAll(true);
    });

    // Search: datalist over this slice's node labels.
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
        if (id) focusNode(id);
      });
    }
  }
})();
