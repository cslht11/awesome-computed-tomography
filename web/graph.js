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
 * sigma/graphology or the data fails to load — or if, after a
 * successful load, nothing actually lands in the viewport — the
 * server-rendered fallback list is (re)shown together with the load
 * note, never a silent white box.
 *
 * CAMERA SPACE (hard-won, do not regress): sigma 3 normalizes the
 * graph into a [0,1]x[0,1] square (extent centred on 0.5,0.5, scaled
 * by the larger span) and its camera lives in THAT normalized space.
 * Camera x/y are NOT raw layout units: framing with raw coordinates
 * (e.g. x=397.5 for a slice spanning ~1000 units) parks the camera
 * hundreds of graph-widths away, every node is culled, and the stage
 * stays pure white while every DOM signal (counters, panels) reports
 * success. That bug shipped twice (the monolith "fix" and the split)
 * because headless checks never asserted painted pixels. All camera
 * work below therefore goes through toNorm().
 */
(function () {
  "use strict";

  var S = window.GRAPH_STRINGS || {};
  var LANG = window.GRAPH_LANG || "en";
  var ROOT = window.GRAPH_ROOT || "../";
  var DATA = window.GRAPH_DATA || "data.json";

  function t(key, fallback) { return S[key] || fallback || key; }
  function label(n) { return (LANG === "zh" && n.lz) ? n.lz : n.l; }

  function showLoadNote() {
    var note = document.getElementById("graph-load-note");
    if (note) note.hidden = false;
  }

  var stage = document.getElementById("graph-stage");
  if (!stage) return;
  if (typeof window.Sigma === "undefined" ||
      typeof window.graphology === "undefined") {
    // Library failed to load: say so instead of leaving a white box.
    showLoadNote();
    return;
  }

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
    .catch(showLoadNote);

  function init(G) {
    var byId = {};
    G.nodes.forEach(function (n) { byId[n.id] = n; });
    // The wire format is compact (scripts/graph_slices.py): edges are
    // [source, target, kind] index triples into the nodes array, with
    // the kind strings in G.kinds; positions align with the nodes.
    // Expand both back to id space once, here.
    var pos = {};
    G.nodes.forEach(function (n, i) { pos[n.id] = (G.pos || [])[i] || [0, 0]; });

    // Slice extent, and the exact normalization sigma 3 applies to
    // the graph (centre of the extent, uniform scale by the larger
    // span — see createNormalizationFunction in sigma's source).
    // Camera targets must be expressed through toNorm(); raw layout
    // units park the camera outside the graph (see header comment).
    var ext = null;
    G.nodes.forEach(function (n) {
      var p = pos[n.id];
      if (!ext) { ext = { minx: p[0], maxx: p[0], miny: p[1], maxy: p[1] }; return; }
      if (p[0] < ext.minx) ext.minx = p[0];
      if (p[0] > ext.maxx) ext.maxx = p[0];
      if (p[1] < ext.miny) ext.miny = p[1];
      if (p[1] > ext.maxy) ext.maxy = p[1];
    });
    var spanR = ext ? Math.max(ext.maxx - ext.minx, ext.maxy - ext.miny) : 0;
    if (!(spanR > 0)) spanR = 1;
    var extCx = ext ? (ext.minx + ext.maxx) / 2 : 0;
    var extCy = ext ? (ext.miny + ext.maxy) / 2 : 0;
    function toNorm(p) {
      return { x: 0.5 + (p[0] - extCx) / spanR, y: 0.5 + (p[1] - extCy) / spanR };
    }
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

    var stageStyle = getComputedStyle(stage);
    var haloColor = stageStyle.backgroundColor || "#fff";
    var textColor = stageStyle.getPropertyValue("--fg").trim() || "#1d1d1f";
    var sigma = new window.Sigma(graph, stage, {
      renderLabels: true,
      // How many labels show is decided by the rank budget in the node
      // reducer below; sigma's grid only keeps those from colliding.
      labelRenderedSizeThreshold: 1,
      labelDensity: 0.7,
      labelGridCellSize: 120,
      labelSize: 12.5,
      labelColor: { color: "#5a6270" },
      // Labels sit over a dense field of dots and edges: draw each with a
      // halo in the stage's own background colour (dark mode included) so
      // it stays legible, in the page's text colour.
      defaultDrawNodeLabel: function (ctx, data, settings) {
        if (!data.label) return;
        // Long paper titles are cut on the canvas; the panel shows them whole.
        var text = data.label.length > 42 ? data.label.slice(0, 40).replace(/\s+\S*$/, "") + "\u2026" : data.label;
        var size = settings.labelSize;
        ctx.font = "500 " + size + "px " + settings.labelFont;
        var x = data.x + data.size + 4, y = data.y + size / 3;
        ctx.lineJoin = "round";
        ctx.lineWidth = 3.5;
        ctx.strokeStyle = haloColor;
        ctx.strokeText(text, x, y);
        ctx.fillStyle = textColor;
        ctx.fillText(text, x, y);
      },
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
    // Labels: at the opening zoom only the best-connected nodes carry one
    // (about one per 70 px of stage width), and more appear as the reader
    // zooms in. Labelling every team and every node above a small size
    // piled hundreds of names on top of each other on the large topics.
    var rank = {};
    G.nodes.map(function (n) { return n.id; })
      .sort(function (a, b) { return (degree[b] || 0) - (degree[a] || 0); })
      .forEach(function (id, i) { rank[id] = i; });
    function labelBudget() {
      var k = Math.max(8, Math.min(22, Math.round(stage.clientWidth / 70)));
      return k * Math.max(1, 1.12 / sigma.getCamera().ratio);
    }
    var budget = 0;
    sigma.setSetting("nodeReducer", function (id, data) {
      var out = Object.assign({}, data);
      var n = byId[id];
      var focus = id === selected || id === hoverId;
      if (focus || (n && n.t === "topic" && rank[id] === 0)) out.forceLabel = true;
      // The inspected node's neighbours may be labelled too (sigma's own
      // grid still keeps them from colliding); everything else waits for
      // its rank to come within the zoom-dependent budget.
      else if (!(hlNodes && hlNodes[id]) && rank[id] >= budget) out.label = null;
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

    // The list of every node stays as the graph's text alternative (the
    // canvas has none): collapsed under the graph once the graph runs, and
    // opened by the watchdog below if nothing was painted.
    var fallback = document.getElementById("graph-fallback");
    var fbDetails = null;
    if (fallback) {
      fbDetails = document.createElement("details");
      fbDetails.className = "graph-list";
      var sum = document.createElement("summary");
      sum.textContent = t("listToggle", "Show this graph as a list");
      fbDetails.appendChild(sum);
      fallback.parentNode.insertBefore(fbDetails, fallback);
      fbDetails.appendChild(fallback);
    }
    var bar = document.getElementById("graph-bar");
    if (bar) bar.hidden = false;

    // -------------------------------------------------------------- camera
    // In normalized space the slice always sits centred on (0.5, 0.5)
    // and ratio 1 frames it exactly (sigma's own correction fits it
    // to the stage); 1.12 adds a small margin. Smaller ratio = closer.
    function frameAll(animate) {
      if (!G.nodes.length) return;
      var cam = sigma.getCamera();
      var target = { x: 0.5, y: 0.5, ratio: 1.12 };
      if (animate === false) cam.setState(target);
      else cam.animate(target, { duration: 550 });
    }
    frameAll(false);
    budget = labelBudget();
    sigma.refresh();     // the reducers first ran with budget 0
    // Re-run the reducers only when the zoom changes the label budget.
    sigma.getCamera().on("updated", function () {
      var b = labelBudget();
      if (Math.round(b) !== Math.round(budget)) { budget = b; sigma.refresh(); }
    });

    function refresh() {
      computeHighlight();
      sigma.refresh();
    }

    var countsEl = document.getElementById("graph-counts");
    if (countsEl) {
      countsEl.textContent = t("counts", "")
        .replace("{shown}", G.nodes.length)
        .replace("{total}", G.total || G.nodes.length)
        .replace("{edges}", EDGES.length);
    }

    // Legend: what each colour is, with this graph's counts, and what the
    // red arrows are. Citation links come from OpenAlex, which has no
    // reference list yet for many recent papers; say so where they appear.
    if (bar) {
      var types = {}, kinds = {};
      G.nodes.forEach(function (n) { types[n.t] = (types[n.t] || 0) + 1; });
      EDGES.forEach(function (e) { kinds[e[2]] = true; });
      var leg = document.createElement("div");
      leg.className = "g-types g-legend";
      Object.keys(types).sort(function (a, b) { return types[b] - types[a]; })
        .forEach(function (ty) {
          var item = document.createElement("span");
          item.className = "g-type";
          var dot = document.createElement("span");
          dot.className = "g-dot";
          dot.style.background = COLORS[ty] || "#999";
          item.appendChild(dot);
          item.appendChild(document.createTextNode(t("type_" + ty, ty) + " " + types[ty]));
          leg.appendChild(item);
        });
      if (kinds.cites) {
        var cite = document.createElement("span");
        cite.className = "g-type";
        var line = document.createElement("span");
        line.className = "g-line";
        line.style.background = EDGE_COLORS.cites;
        cite.appendChild(line);
        cite.appendChild(document.createTextNode(t("edge_cites", "cites")));
        leg.appendChild(cite);
      }
      bar.appendChild(leg);
      if (kinds.cites && t("coverage", "")) {
        var cov = document.createElement("p");
        cov.className = "g-note g-coverage";
        cov.textContent = t("coverage", "");
        bar.appendChild(cov);
      }
    }

    // Paint watchdog: a successful init is not proof anything was
    // drawn (the normalized-camera bug left every counter green over
    // a white stage). Shortly after load, verify at least one node
    // projects inside the stage; if none does, surface the failure —
    // load note plus the static fallback list — instead of silence.
    setTimeout(function () {
      try {
        if (!G.nodes.length) return;
        var w = stage.clientWidth, h = stage.clientHeight, inside = 0;
        for (var i = 0; i < G.nodes.length; i++) {
          var p = pos[G.nodes[i].id];
          var vp = sigma.graphToViewport({ x: p[0], y: p[1] });
          if (vp.x >= -60 && vp.x <= w + 60 && vp.y >= -60 && vp.y <= h + 60) {
            inside++;
            break;
          }
        }
        if (!inside) {
          if (window.console) {
            console.error("graph: no node projects into the viewport; " +
                          "showing the fallback list");
          }
          showLoadNote();
          if (fbDetails) fbDetails.open = true;
        }
      } catch (e) { /* the watchdog must never break the page */ }
    }, 900);

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
      // Fly to a window around the node (never zoom back out). The
      // target is the node's NORMALIZED position; ratio 0.35 shows
      // roughly the node's third of the slice around it.
      var p = pos[id];
      if (p) {
        var cam = sigma.getCamera();
        var ratio = Math.min(cam.ratio, 0.35);
        var target = toNorm(p);
        target.ratio = ratio;
        cam.animate(target, { duration: 550 });
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
