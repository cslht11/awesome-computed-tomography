/* Knowledge graph 3D explorer for /graph/ and /zh/graph/.
 *
 * Renders the same graph.json as the 2D view (web/graph.js) with the
 * vendored 3d-force-graph (three.js), for readers who want to rotate,
 * drag and fly through the network instead of reading a flat layout.
 * The interaction model is the 2D one's: the page opens on the team /
 * topic / toolkit backbone, selecting a node expands its one-hop
 * neighbourhood and fills the same detail panel, search flies the
 * camera to a node, and a full-graph mode exists behind a toggle.
 *
 * Labels are the clutter problem in 3D as much as in 2D, so only hubs
 * (teams, topics, and nodes above a degree threshold — stricter in
 * full-graph mode) carry a permanent in-scene text sprite, always with
 * the full, untruncated label; every other node is identified by the
 * hover tooltip. Sprites fade with camera distance.
 *
 * Activation is cooperative with graph.js: this file loads first and,
 * when WebGL and the vendored libraries are present and the reader has
 * not chosen 2D (a localStorage preference the 2D/3D toggle sets),
 * claims the page synchronously (window.__GRAPH_3D_CLAIMED) before
 * graph.js runs; graph.js then stands down. If the 3D build itself
 * fails, the server-rendered static fallback remains in charge.
 */
(function () {
  "use strict";

  var S = window.GRAPH_STRINGS || {};
  var LANG = window.GRAPH_LANG || "en";
  var ROOT = window.GRAPH_ROOT || "../";
  var PREF_KEY = "ct-graph-view";

  window.__GRAPH_3D_AVAILABLE = false;
  window.__GRAPH_3D_ACTIVE = false;

  var container = document.getElementById("graph3d");
  if (!container) return;
  if (typeof window.ForceGraph3D === "undefined" ||
      typeof window.SpriteText === "undefined" ||
      typeof window.THREE === "undefined") return;

  var webgl = false;
  try {
    var probe = document.createElement("canvas");
    webgl = !!(window.WebGLRenderingContext &&
               (probe.getContext("webgl2") || probe.getContext("webgl")));
  } catch (e) { webgl = false; }
  if (!webgl) return;
  window.__GRAPH_3D_AVAILABLE = true;

  var pref = null;
  try { pref = window.localStorage.getItem(PREF_KEY); } catch (e) { pref = null; }
  if (pref === "2d") return;   // graph.js owns the page; it wires the 3D button

  // Claim the page synchronously: graph.js runs right after this file,
  // long before the graph.json fetch resolves, and it stands down when
  // it sees the claim. If the 3D view then fails to build, the static
  // fallback list (which nothing has hidden) serves the page.
  window.__GRAPH_3D_CLAIMED = true;

  function t(key, fallback) { return S[key] || fallback || key; }
  function label(n) { return (LANG === "zh" && n.lz) ? n.lz : n.l; }

  fetch(ROOT + "graph.json")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (G) {
      try { init(G); }
      catch (err) { showLoadNote(); }
    })
    .catch(function () { showLoadNote(); });

  function showLoadNote() {
    var note = document.getElementById("graph-load-note");
    if (note) note.hidden = false;
  }

  function init(G) {
    var byId = {};
    G.nodes.forEach(function (n) { byId[n.id] = n; });

    var degree = {};
    G.edges.forEach(function (e) {
      degree[e[0]] = (degree[e[0]] || 0) + 1;
      degree[e[1]] = (degree[e[1]] || 0) + 1;
    });
    var neighbours = {};   // id -> [{id, kind, dir}]
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
    var TYPE_ORDER = ["team", "topic", "paper", "toolkit", "dataset",
                      "benchmark", "author", "venue", "learning", "guide"];

    function lighten(hex) {
      var n = parseInt(hex.slice(1), 16);
      function mix(c) { return Math.round(c + (255 - c) * 0.78); }
      return "rgb(" + mix((n >> 16) & 255) + "," + mix((n >> 8) & 255) +
             "," + mix(n & 255) + ")";
    }
    var DIM_COLORS = {};
    Object.keys(COLORS).forEach(function (k) { DIM_COLORS[k] = lighten(COLORS[k]); });

    function radius(id) {
      return 2.2 + Math.min(9, Math.sqrt(degree[id] || 0) * 1.15);
    }

    // ------------------------------------------------------------ state
    var expanded = {};
    var fullMode = false;
    var egoOnly = null;
    var typeOn = {};
    TYPE_ORDER.forEach(function (ty) { typeOn[ty] = true; });
    var backbone = {};
    (G.backbone || []).forEach(function (id) { backbone[id] = true; });
    var regionWant = "";        // team-region dimming ("" = all)
    var selected = null;
    var hoverId = null;

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

    // ------------------------------------------------- 3D node/link data
    var nodeObjs = {};   // id -> the object handed to the engine (persistent,
                         // so positions survive refreshes)
    function nodeObj(id) {
      if (!nodeObjs[id]) {
        var n = byId[id];
        nodeObjs[id] = { id: id, name: label(n), t: n.t, deg: degree[id] || 0 };
      }
      return nodeObjs[id];
    }

    function graphDataFor(vis) {
      var nodes = [], links = [];
      Object.keys(vis).forEach(function (id) { nodes.push(nodeObj(id)); });
      G.edges.forEach(function (e) {
        if (vis[e[0]] && vis[e[1]]) {
          links.push({ source: e[0], target: e[1], kind: e[2] });
        }
      });
      return { nodes: nodes, links: links };
    }

    // ------------------------------------------------------------ sprites
    // Permanent labels: teams and topics always; other types only above
    // a degree threshold — and a stricter one in full-graph mode, where
    // a thousand permanent labels would bury the scene.
    var sprites = {};   // id -> SpriteText (created lazily by the accessor)
    function spriteWanted(n) {
      if (n.t === "team" || n.t === "topic") return true;
      var min = fullMode ? 60 : 24;
      return (degree[n.id] || 0) >= min;
    }
    function makeSprite(n) {
      var prev = sprites[n.id];
      if (prev && prev.__full === fullMode) return prev;   // already current
      var text = label(byId[n.id]);
      var sp = new window.SpriteText(text);
      sp.__full = fullMode;
      var th = 3.1 + Math.min(3.4, Math.sqrt(degree[n.id] || 0) * 0.5);
      sp.textHeight = th;
      sp.color = "#3d4451";
      sp.fontWeight = (n.t === "team" || n.t === "topic") ? "700" : "600";
      sp.material.depthWrite = false;
      sp.material.transparent = true;
      // Anchor trick from the library's text-nodes example: shifting the
      // sprite's centre up by (radius + a margin), in text-height units,
      // so the label floats above its sphere instead of crossing it.
      sp.center.y = -(0.35 + radius(n.id) / th);
      sprites[n.id] = sp;
      return sp;
    }

    // ------------------------------------------------------------- forces
    // A small collision force (uniform grid) — the charge force alone
    // lets big topic spheres swallow their neighbours.
    function collideForce() {
      var nodes = [];
      function force(alpha) {
        if (!nodes.length) return;
        var cell = 26, grid = {}, i, n, key;
        for (i = 0; i < nodes.length; i++) {
          n = nodes[i];
          if (n.x === undefined || n.fx !== undefined) continue;
          key = Math.floor(n.x / cell) + ":" + Math.floor(n.y / cell) + ":" +
                Math.floor(n.z / cell);
          (grid[key] = grid[key] || []).push(n);
        }
        var k = Math.min(1, 0.35 + alpha);
        for (i = 0; i < nodes.length; i++) {
          n = nodes[i];
          if (n.x === undefined || n.fx !== undefined) continue;
          var cx = Math.floor(n.x / cell), cy = Math.floor(n.y / cell),
              cz = Math.floor(n.z / cell);
          for (var dx = -1; dx <= 1; dx++)
          for (var dy = -1; dy <= 1; dy++)
          for (var dz = -1; dz <= 1; dz++) {
            var cellNodes = grid[(cx + dx) + ":" + (cy + dy) + ":" + (cz + dz)];
            if (!cellNodes) continue;
            for (var j = 0; j < cellNodes.length; j++) {
              var m = cellNodes[j];
              if (m === n || m.x === undefined) continue;
              var ox = m.x - n.x, oy = m.y - n.y, oz = m.z - n.z;
              var d2 = ox * ox + oy * oy + oz * oz;
              var min = radius(n.id) + radius(m.id) + 2.5;
              if (d2 >= min * min || d2 === 0) continue;
              var d = Math.sqrt(d2), push = (min - d) / d * 0.5 * k;
              n.x -= ox * push; n.y -= oy * push; n.z -= oz * push;
            }
          }
        }
      }
      force.initialize = function (ns) { nodes = ns; };
      return force;
    }

    // ----------------------------------------------------------- highlight
    // The node/link sets currently emphasised (hover wins over selection).
    var hlNodes = null, hlLinks = null;   // Sets of ids / "s|t|kind" keys
    function linkKey(l) {
      var s = typeof l.source === "object" ? l.source.id : l.source;
      var tg = typeof l.target === "object" ? l.target.id : l.target;
      return s + "|" + tg + "|" + l.kind;
    }
    function computeHighlight() {
      var focus = hoverId || selected;
      if (!focus || !nodeObjs[focus]) { hlNodes = null; hlLinks = null; return; }
      hlNodes = {}; hlLinks = {};
      hlNodes[focus] = true;
      (neighbours[focus] || []).forEach(function (x) {
        hlNodes[x.id] = true;
        hlLinks[x.dir === "out" ? focus + "|" + x.id + "|" + x.kind
                                : x.id + "|" + focus + "|" + x.kind] = true;
      });
    }
    function nodeDimmed(id) {
      var n = byId[id];
      if (regionWant && n && n.t === "team" && n.m && n.m.region !== regionWant) {
        return true;
      }
      if (hlNodes && !hlNodes[id]) return true;
      return false;
    }
    function applyEmphasis() {
      computeHighlight();
      Graph.nodeColor(Graph.nodeColor());
      Graph.linkColor(Graph.linkColor());
      Object.keys(sprites).forEach(function (id) {
        if (sprites[id]) {
          sprites[id].material.opacity = nodeDimmed(id) ? 0.13 : 1;
        }
      });
    }

    // -------------------------------------------------------------- engine
    // The container must be visible before the engine is constructed:
    // it measures the element to size its canvas.
    container.hidden = false;
    var cyEl0 = document.getElementById("cy");
    if (cyEl0) cyEl0.hidden = true;

    var bg = "#ffffff";
    try {
      var cs = window.getComputedStyle(container);
      if (cs && cs.backgroundColor) bg = cs.backgroundColor;
    } catch (e) { /* keep the default */ }

    var smallScreen = Math.min(window.innerWidth || 9999,
                               window.innerHeight || 9999) < 720;

    var Graph = window.ForceGraph3D({
      rendererConfig: { antialias: true, powerPreference: "high-performance" },
      controlType: "orbit"
    })(container)
      .backgroundColor(bg)
      .showNavInfo(false)
      .nodeRelSize(4)
      .nodeVal(function (n) { var r = radius(n.id); return Math.pow(r / 4, 3); })
      .nodeColor(function (n) {
        return nodeDimmed(n.id) ? (DIM_COLORS[n.t] || "#ccc")
                                : (COLORS[n.t] || "#999");
      })
      .nodeLabel(function (n) { return label(byId[n.id]); })
      .nodeThreeObject(function (n) {
        return spriteWanted(n) ? makeSprite(n) : null;
      })
      .nodeThreeObjectExtend(true)
      .linkColor(function (l) {
        if (hlLinks) {
          return hlLinks[linkKey(l)]
            ? (l.kind === "cites" ? "rgba(214,39,40,0.95)" : "rgba(90,98,112,0.9)")
            : "rgba(196,202,212,0.55)";
        }
        if (l.kind === "cites") return "rgba(225,87,89,0.5)";
        if (l.kind === "coauthor") return "rgba(168,173,184,0.32)";
        return "rgba(150,158,172,0.42)";
      })
      .linkWidth(function (l) {
        return (hlLinks && hlLinks[linkKey(l)]) ? 1.6 : 0.6;
      })
      .linkDirectionalArrowLength(function (l) {
        return l.kind === "cites" ? 3.2 : 0;
      })
      .linkDirectionalArrowRelPos(0.93)
      .linkDirectionalParticles(function (l) {
        // Particles only in the backbone view, and only on citations:
        // pretty there, pure noise (and cost) anywhere larger.
        return (!fullMode && !egoOnly && l.kind === "cites") ? 2 : 0;
      })
      .linkDirectionalParticleWidth(2.4)
      .linkDirectionalParticleSpeed(0.004)
      .d3AlphaDecay(0.022)
      .d3VelocityDecay(0.34)
      .warmupTicks(50)
      .cooldownTicks(140)
      .cooldownTime(9000)
      .onNodeHover(function (n) {
        hoverId = n ? n.id : null;
        container.style.cursor = n ? "pointer" : "";
        applyEmphasis();
      })
      .onNodeClick(function (n, ev) {
        var now = (ev && ev.timeStamp) || 0;
        if (lastClick.id === n.id && now - lastClick.at < 350) {
          lastClick = { id: null, at: 0 };
          flyTo(nodeObj(n.id), 95);
          return;
        }
        lastClick = { id: n.id, at: now };
        selectNode(n.id, false);
      })
      .onNodeDragEnd(function (n) {
        // Pin where the reader dropped it; the forces leave it alone.
        n.fx = n.x; n.fy = n.y; n.fz = n.z;
      })
      .onBackgroundClick(function () {
        selected = null;
        if (panel) panel.hidden = true;
        applyEmphasis();
      })
      .onEngineTick(function () {
        // Distance fade for the permanent labels, throttled: far labels
        // step aside instead of stacking into grey mush.
        if ((tick++ & 7) !== 0) return;
        var cam = Graph.camera().position;
        Object.keys(sprites).forEach(function (id) {
          var sp = sprites[id], o = nodeObjs[id];
          if (!sp || !o || o.x === undefined) return;
          if (nodeDimmed(id)) return;   // emphasis already set its opacity
          var dx = cam.x - o.x, dy = cam.y - o.y, dz = cam.z - o.z;
          var d = Math.sqrt(dx * dx + dy * dy + dz * dz);
          sp.material.opacity = d < 300 ? 1
            : d > 580 ? 0.12 : 1 - (d - 300) / 280 * 0.88;
        });
      });

    var lastClick = { id: null, at: 0 };
    var tick = 0;

    Graph.d3Force("charge").strength(-170).distanceMax(520);
    Graph.d3Force("link").distance(function (l) {
      return l.kind === "coauthor" ? 55 : 34;
    });
    Graph.d3Force("collide", collideForce());

    try {
      var renderer = Graph.renderer();
      if (renderer && renderer.setPixelRatio) {
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1,
                                        smallScreen ? 1.5 : 2));
      }
    } catch (e) { /* default pixel ratio */ }

    var controls = null;
    try { controls = Graph.controls(); } catch (e) { controls = null; }
    if (controls) {
      controls.enableDamping = true;
      controls.dampingFactor = 0.14;
      controls.rotateSpeed = 0.65;
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { Graph.pauseAnimation(); }
      else { Graph.resumeAnimation(); }
    });

    // The engine is built: the page is fully ours.
    window.__GRAPH_3D_ACTIVE = true;
    var fallback = document.getElementById("graph-fallback");
    if (fallback) fallback.hidden = true;
    var bar = document.getElementById("graph-bar");
    if (bar) bar.hidden = false;

    // ------------------------------------------------------------- camera
    function flyTo(o, dist) {
      if (!o || o.x === undefined) return;
      var cam = Graph.camera().position;
      var vx = cam.x - o.x, vy = cam.y - o.y, vz = cam.z - o.z;
      var len = Math.sqrt(vx * vx + vy * vy + vz * vz);
      if (!isFinite(len) || len === 0) { vx = 0.4; vy = 0.3; vz = 1; len = 1.1; }
      var d = dist || 120;
      Graph.cameraPosition(
        { x: o.x + vx / len * d, y: o.y + vy / len * d, z: o.z + vz / len * d },
        o, 1100);
    }
    function flyToSoon(id, dist) {
      var o = nodeObj(id);
      if (o.x !== undefined && isFinite(o.x)) { flyTo(o, dist); return; }
      setTimeout(function () {
        if (o.x !== undefined && isFinite(o.x)) flyTo(o, dist);
      }, 350);
    }
    var framed = false;
    Graph.onEngineStop(function () {
      if (!framed) { framed = true; Graph.zoomToFit(700, 45); }
    });

    // --------------------------------------------------------- data refresh
    var lastFullMode = null;
    function refresh() {
      var vis = visibleIds();
      if (lastFullMode !== null && lastFullMode !== fullMode) {
        // The sprite threshold depends on the mode; re-setting the
        // accessor makes the engine rebuild node objects under it.
        Graph.nodeThreeObject(Graph.nodeThreeObject());
      }
      lastFullMode = fullMode;
      Graph.graphData(graphDataFor(vis));
      applyEmphasis();
      updateCounts(vis);
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
      if (expandIt && !expanded[id]) { expanded[id] = true; refresh(); }
      selected = id;
      applyEmphasis();
      showPanel(id);
      flyToSoon(id, 120);
    }

    function selectNode(id, fly) {
      if (!fullMode && !expanded[id]) { expanded[id] = true; refresh(); }
      selected = id;
      applyEmphasis();
      showPanel(id);
      if (fly) flyToSoon(id, 120);
    }

    // ------------------------------------------------------------- controls
    document.getElementById("gp-expand").addEventListener("click", function () {
      if (!selected) return;
      if (expanded[selected]) delete expanded[selected];
      else expanded[selected] = true;
      refresh(); showPanel(selected);
    });
    var egoBtn = document.getElementById("gp-ego");
    egoBtn.addEventListener("click", function () {
      if (!selected) return;
      egoOnly = (egoOnly === selected) ? null : selected;
      egoBtn.textContent = egoOnly ? t("showAll2", "Back to overview")
                                   : t("egoOnly", "Only this network");
      refresh(); showPanel(selected);
    });
    document.getElementById("gp-close").addEventListener("click", function () {
      panel.hidden = true; selected = null; applyEmphasis();
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
      framed = false;
      refresh();
    });
    var resetBtn = document.getElementById("graph-reset");
    if (resetBtn) resetBtn.addEventListener("click", function () {
      expanded = {}; egoOnly = null; fullMode = false;
      selected = null; hoverId = null;
      if (panel) panel.hidden = true;
      if (fullBtn) fullBtn.textContent = t("fullGraph", "Full graph");
      framed = false;
      refresh();
    });

    // 2D/3D toggle: 3D is active here; the 2D button stores the choice
    // and reloads into graph.js.
    var view2d = document.getElementById("graph-view-2d");
    var view3d = document.getElementById("graph-view-3d");
    if (view3d) view3d.setAttribute("aria-pressed", "true");
    if (view2d) {
      view2d.setAttribute("aria-pressed", "false");
      view2d.addEventListener("click", function () {
        try { window.localStorage.setItem(PREF_KEY, "2d"); } catch (e) {}
        window.location.reload();
      });
    }

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
          typeOn[ty] = cb.checked; refresh();
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
      applyEmphasis();
    });

    // Search: datalist over every node's label; choosing one flies there.
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

    refresh();
  }
})();

