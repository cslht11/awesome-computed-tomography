/* Lineage tree viewport controller (/graph/lineage/<id>/).
 * The layout is computed at build time; this script only moves
 * the stage: fit on load, drag to pan (with click suppression),
 * wheel zoom at the pointer, two-pointer pinch, toolbar
 * buttons, double-click to refit, keyboard pan/zoom, and
 * #<paper-id> deep links. Without JS the stage simply scrolls
 * inside its viewport (the data-live switch below turns the
 * native scrolling off only once this controller runs). */
(function () {
  var root = document.currentScript.parentNode;
  var vp = root.querySelector(".tree-viewport");
  var stage = root.querySelector(".tree-stage");
  var data = JSON.parse(root.querySelector("script.tree-layout").textContent);
  var W = data.width, H = data.height;
  var scale = 1, tx = 0, ty = 0, MIN = 0.05, MAX = 3, interacted = false;
  function apply() {
    // The browser may have scrolled the (then scrollable) viewport
    // towards a #fragment target; that residue offsets the stage from
    // the transform's math, so it is zeroed whenever we render.
    if (vp.scrollLeft || vp.scrollTop) { vp.scrollLeft = 0; vp.scrollTop = 0; }
    stage.style.transform =
      "translate(" + tx + "px," + ty + "px) scale(" + scale + ")";
  }
  function fit() {
    var r = vp.getBoundingClientRect();
    // A degenerate rect (script ran before the stylesheet laid the page
    // out) would fling the tree off-view with a near-zero scale and
    // nothing would ever repair it, so refuse to fit on one.
    if (r.width < 50 || r.height < 50) return;
    scale = Math.max(MIN, Math.min(r.width / W, r.height / H, 1));
    tx = (r.width - W * scale) / 2;
    ty = (r.height - H * scale) / 2;
    apply();
  }
  function zoomAt(mx, my, ns) {
    ns = Math.max(MIN, Math.min(MAX, ns));
    var k = ns / scale;
    tx = mx - (mx - tx) * k;
    ty = my - (my - ty) * k;
    scale = ns;
    apply();
  }
  function zoomCentre(f) {
    var r = vp.getBoundingClientRect();
    zoomAt(r.width / 2, r.height / 2, scale * f);
  }
  fit();
  // Refit once the document has fully loaded: the first fit can run
  // before the stylesheet settles, and a stale transform from that
  // moment is otherwise permanent. Never override a user who has
  // already grabbed the canvas.
  addEventListener("load", function () { if (!interacted) fit(); });
  vp.setAttribute("data-live", "1");
  var linked = null;
  if (location.hash.length > 1) {
    var want = location.hash.slice(1);
    for (var i = 0; i < data.nodes.length; i++) {
      if (data.nodes[i].paper === want || data.nodes[i].key === want) {
        linked = data.nodes[i];
        break;
      }
    }
  }
  function centreLinked() {
    if (!linked) return;
    scale = Math.min(MAX, Math.max(scale, 0.85));
    var r = vp.getBoundingClientRect();
    tx = r.width / 2 - (linked.x + linked.w / 2) * scale;
    ty = r.height / 2 - (linked.y + linked.h / 2) * scale;
    apply();
  }
  centreLinked();
  // The browser applies its own fragment scroll at load, after this
  // script; centre once more then so the card ends up centred.
  if (linked) addEventListener("load", centreLinked);
  vp.addEventListener("wheel", function (e) {
    interacted = true;
    e.preventDefault();
    var r = vp.getBoundingClientRect();
    zoomAt(e.clientX - r.left, e.clientY - r.top,
           scale * (e.deltaY < 0 ? 1.12 : 1 / 1.12));
  }, { passive: false });
  var pointers = new Map(), drag = null, pinch = null, downAt = null, moved = false, capId = null;
  function capture(pid) {
    // Capture only once a gesture is really a drag (or a second finger
    // joins for a pinch). Capturing on pointerdown retargets the
    // following click to the viewport itself, so no card link — title,
    // Paper, Code — could ever be clicked.
    if (capId !== null) return;
    try { vp.setPointerCapture(pid); capId = pid; } catch (err) { /* stale pointer */ }
  }
  vp.addEventListener("pointerdown", function (e) {
    interacted = true;
    pointers.set(e.pointerId, [e.clientX, e.clientY]);
    moved = false;
    if (pointers.size === 1) {
      drag = { x: e.clientX, y: e.clientY };
      downAt = { x: e.clientX, y: e.clientY };
      capId = null;
    } else if (pointers.size === 2) {
      capture(e.pointerId);
      var ps = Array.from(pointers.values());
      pinch = { d: Math.hypot(ps[0][0] - ps[1][0], ps[0][1] - ps[1][1]), s: scale };
      drag = null;
    }
  });
  vp.addEventListener("pointermove", function (e) {
    if (!pointers.has(e.pointerId)) return;
    pointers.set(e.pointerId, [e.clientX, e.clientY]);
    // 10px, not 4: a tap — finger tremor included — wobbles a few px and
    // must still reach its link; a real pan moves far more.
    if (downAt && Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y) > 10) {
      moved = true;
      capture(e.pointerId);
    }
    if (pinch && pointers.size === 2) {
      var ps = Array.from(pointers.values());
      var r = vp.getBoundingClientRect();
      var d = Math.hypot(ps[0][0] - ps[1][0], ps[0][1] - ps[1][1]);
      if (pinch.d > 0)
        zoomAt((ps[0][0] + ps[1][0]) / 2 - r.left,
               (ps[0][1] + ps[1][1]) / 2 - r.top, pinch.s * d / pinch.d);
    } else if (drag) {
      tx += e.clientX - drag.x;
      ty += e.clientY - drag.y;
      drag = { x: e.clientX, y: e.clientY };
      apply();
    }
  });
  function release(e) {
    pointers.delete(e.pointerId);
    if (e.pointerId === capId) capId = null;
    if (pointers.size < 2) pinch = null;
    if (pointers.size === 1) {
      var p = Array.from(pointers.values())[0];
      drag = { x: p[0], y: p[1] };
    } else if (pointers.size === 0) {
      drag = null;
      downAt = null;
    }
  }
  vp.addEventListener("pointerup", release);
  vp.addEventListener("pointercancel", release);
  vp.addEventListener("click", function (e) {
    if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
  }, true);
  vp.addEventListener("dblclick", function (e) {
    if (!e.target.closest("a, button")) fit();
  });
  root.querySelectorAll(".tree-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      interacted = true;
      var act = b.getAttribute("data-act");
      if (act === "in") zoomCentre(1.3);
      else if (act === "out") zoomCentre(1 / 1.3);
      else fit();
    });
  });
  vp.addEventListener("keydown", function (e) {
    interacted = true;
    var step = 48;
    if (e.key === "ArrowLeft") tx += step;
    else if (e.key === "ArrowRight") tx -= step;
    else if (e.key === "ArrowUp") ty += step;
    else if (e.key === "ArrowDown") ty -= step;
    else if (e.key === "+" || e.key === "=") { zoomCentre(1.2); return; }
    else if (e.key === "-") { zoomCentre(1 / 1.2); return; }
    else return;
    e.preventDefault();
    apply();
  });
})();
