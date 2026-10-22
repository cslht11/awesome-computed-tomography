/* Knowledge graph explorer for /graph/ and /zh/graph/.
 *
 * The data is graph.json, generated at build time from the same payload
 * as the rest of the site (scripts/graph.py). The page starts from a
 * backbone (teams + topics + toolkits) instead of the full graph: with
 * ~1000 nodes the full graph is a hairball, so papers, datasets and the
 * rest arrive by expanding a node (its one-hop neighbourhood), by
 * searching, or via the explicit full-graph toggle.
 *
 * Plain script, no modules, in the same style as app.js/search.js. If
 * Cytoscape or the data fails to load, the server-rendered fallback list
 * stays visible and this file simply does nothing.
 */
(function () {
  "use strict";

  var S = window.GRAPH_STRINGS || {};
  var LANG = window.GRAPH_LANG || "en";
  var ROOT = window.GRAPH_ROOT || "../";

  function t(key, fallback) { return S[key] || fallback || key; }
  function label(n) { return (LANG === "zh" && n.lz) ? n.lz : n.l; }

  var cyEl = document.getElementById("cy");
  if (!cyEl || typeof window.cytoscape === "undefined") return;
  // web/graph3d.js loads first and claims the page when it can run;
  // in that case the 2D view stands down entirely.
  if (window.__GRAPH_3D_ACTIVE || window.__GRAPH_3D_CLAIMED) return;

  fetch(ROOT + "graph.json")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (G) { init(G); })
    .catch(function () {
      var note = document.getElementById("graph-load-note");
      if (note) note.hidden = false;
    });

  function init(G) {
    var byId = {};
    G.nodes.forEach(function (n) { byId[n.id] = n; });

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
    var TYPE_ORDER = ["team", "topic", "paper", "toolkit", "dataset",
                      "benchmark", "author", "venue", "learning", "guide"];

    var expanded = {};     // id -> true once its neighbourhood is shown
    var fullMode = false;
    var egoOnly = null;    // id whose ego network alone is shown
    var typeOn = {};       // type -> bool (filter checkboxes)
    TYPE_ORDER.forEach(function (ty) { typeOn[ty] = true; });

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

    function elementsFor(vis) {
      var els = [];
      Object.keys(vis).forEach(function (id) {
        var n = byId[id];
        els.push({ data: {
          id: id, label: label(n), type: n.t,
          size: 14 + Math.min(30, Math.sqrt(degree[id] || 0) * 5),
          color: COLORS[n.t] || "#999"
        }});
      });
      G.edges.forEach(function (e, i) {
        if (vis[e[0]] && vis[e[1]]) {
          els.push({ data: { id: "e" + i, source: e[0], target: e[1], kind: e[2] } });
        }
      });
      return els;
    }

    var cy = window.cytoscape({
      container: cyEl,
      elements: elementsFor(visibleIds()),
      style: [
        { selector: "node", style: {
            "background-color": "data(color)", "width": "data(size)",
            "height": "data(size)", "label": "data(label)",
            "font-size": 10, "color": "#888",
            "text-valign": "bottom", "text-margin-y": 3,
            "text-max-width": 110, "text-wrap": "ellipsis",
            "border-width": 1, "border-color": "#fff"
        }},
        { selector: "node[type='topic'], node[type='team']", style: {
            "font-size": 12, "font-weight": "bold", "color": "#666"
        }},
        { selector: "edge", style: {
            "width": 1, "line-color": "#c9ced6", "curve-style": "bezier",
            "target-arrow-shape": "none", "opacity": 0.75
        }},
        { selector: "edge[kind='cites']", style: {
            "line-color": "#e15759", "line-style": "dashed", "width": 1.6,
            "target-arrow-shape": "triangle", "target-arrow-color": "#e15759",
            "opacity": 0.9
        }},
        { selector: "edge[kind='authored']", style: { "line-color": "#e8b4d8" } },
        { selector: "edge[kind='coauthor']", style: {
            "line-color": "#d8d8d8", "line-style": "dotted"
        }},
        { selector: "edge[kind='focus'], edge[kind='works'], edge[kind='leads']",
          style: { "line-color": "#b39ddb", "width": 1.4 } },
        { selector: "node:selected", style: {
            "border-width": 3, "border-color": "#f2c230"
        }},
        { selector: ".dim", style: { "opacity": 0.12 } },
        { selector: "edge.dim", style: { "opacity": 0.05 } }
      ],
      layout: { name: "cose", animate: false, padding: 24 },
      minZoom: 0.15, maxZoom: 2.5
    });

    var fallback = document.getElementById("graph-fallback");
    if (fallback) fallback.hidden = true;
    var bar = document.getElementById("graph-bar");
    if (bar) bar.hidden = false;

    // 2D/3D toggle: 2D is active here; the 3D button stores the choice
    // and reloads into graph3d.js — or is hidden when 3D cannot run.
    var view2dBtn = document.getElementById("graph-view-2d");
    var view3dBtn = document.getElementById("graph-view-3d");
    if (view2dBtn) view2dBtn.setAttribute("aria-pressed", "true");
    if (view3dBtn) {
      if (window.__GRAPH_3D_AVAILABLE) {
        view3dBtn.setAttribute("aria-pressed", "false");
        view3dBtn.addEventListener("click", function () {
          try { window.localStorage.setItem("ct-graph-view", "3d"); }
          catch (e) { /* preference is best-effort */ }
          window.location.reload();
        });
      } else {
        view3dBtn.hidden = true;
      }
    }

    function relayout() {
      cy.layout({ name: "cose", animate: false, padding: 24,
                  nodeRepulsion: fullMode ? 9000 : 5000 }).run();
    }

    function refresh(keepLayout) {
      var vis = visibleIds();
      var want = {};
      elementsFor(vis).forEach(function (el) { want[el.data.id] = el; });
      cy.elements().forEach(function (el) {
        if (!want[el.id()]) el.remove();
      });
      Object.keys(want).forEach(function (id) {
        if (cy.getElementById(id).empty()) cy.add(want[id]);
      });
      if (!keepLayout) relayout();
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
    var selected = null;

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
      selected = id;
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
      if (fullMode) { /* everything already visible */ }
      else if (egoOnly && egoOnly !== id) { egoOnly = null; }
      if (expandIt) expanded[id] = true;
      refresh(true);
      var el = cy.getElementById(id);
      if (el.nonempty()) {
        cy.animate({ center: { eles: el }, zoom: Math.max(cy.zoom(), 0.9) },
                   { duration: 250 });
        el.select();
      }
      showPanel(id);
      relayoutSoft();
    }

    var layoutTimer = null;
    function relayoutSoft() {
      if (layoutTimer) return;
      layoutTimer = setTimeout(function () { layoutTimer = null; relayout(); }, 60);
    }

    cy.on("tap", "node", function (ev) {
      var id = ev.target.id();
      if (!expanded[id] && !fullMode) { expanded[id] = true; refresh(true); relayoutSoft(); }
      showPanel(id);
    });
    cy.on("tap", function (ev) {
      if (ev.target === cy) { panel.hidden = true; selected = null; }
    });

    // ------------------------------------------------------------- controls
    document.getElementById("gp-expand").addEventListener("click", function () {
      if (!selected) return;
      if (expanded[selected]) delete expanded[selected]; else expanded[selected] = true;
      refresh(true); relayoutSoft(); showPanel(selected);
    });
    document.getElementById("gp-ego").addEventListener("click", function () {
      if (!selected) return;
      egoOnly = (egoOnly === selected) ? null : selected;
      this.textContent = egoOnly ? t("showAll2", "Back to overview")
                                 : t("egoOnly", "Only this network");
      refresh(); showPanel(selected);
    });
    document.getElementById("gp-close").addEventListener("click", function () {
      panel.hidden = true; selected = null;
    });

    var fullBtn = document.getElementById("graph-full");
    if (fullBtn) fullBtn.addEventListener("click", function () {
      fullMode = !fullMode;
      egoOnly = null;
      fullBtn.textContent = fullMode ? t("backbone", "Backbone view")
                                     : t("fullGraph", "Full graph");
      var warn = document.getElementById("graph-full-note");
      if (warn) warn.hidden = !fullMode;
      refresh();
    });
    var resetBtn = document.getElementById("graph-reset");
    if (resetBtn) resetBtn.addEventListener("click", function () {
      expanded = {}; egoOnly = null; fullMode = false;
      if (fullBtn) fullBtn.textContent = t("fullGraph", "Full graph");
      refresh();
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
          typeOn[ty] = cb.checked; refresh(true);
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
      var want = regionSel.value;
      cy.nodes().forEach(function (el) {
        var n = byId[el.id()];
        var dim = want && n && n.t === "team" && n.m && n.m.region !== want;
        el.toggleClass("dim", !!dim);
      });
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

    updateCounts(visibleIds());
  }
})();
