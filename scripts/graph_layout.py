# -*- coding: utf-8 -*-
"""Offline layout for the knowledge graph (scripts/graph.py's output).

The graph page used to run a force simulation in the reader's browser
(Cytoscape's cose in 2D, d3-force inside 3d-force-graph in 3D). On a
1,004-node / 6,600-edge graph that meant seconds of main-thread layout
on every page load and every expand, and thousands of per-object draw
calls in the 3D scene — the page felt broken on ordinary hardware.

The data only changes when the library changes, i.e. at deploy time,
so the layout is computed here instead, once per build, and shipped as
static coordinates in graph.json (the same pattern Connected Papers
uses: precomputed x/y per node, no runtime simulation). The browser
then only renders: positions are data, visibility is a filter.

Algorithm: Fruchterman–Reingold with a Barnes–Hut quadtree for the
repulsive forces (theta = 1.0), a geometric temperature schedule, and a
whisper of centering gravity so disconnected components stay in
frame. Pure stdlib — the build deliberately depends on PyYAML and
nothing else (see requirements.txt), so no numpy/networkx here.
Deterministic: a fixed seed makes rebuilds byte-stable, which keeps
deploys diffable. Degree-0 nodes (nothing to lay out against) are
placed on a ring around the finished layout instead of being dropped
into the middle by the force model.

Two phases, because the page opens on the backbone (teams + topics +
toolkits, ~90 nodes) and that view must be legible on its own: a
single full-graph layout buries those hubs in the dense centre (the
shipped layout had backbone pairs at 0 px and a 15 px median
nearest-neighbour distance on screen). Phase 1 lays out the backbone
subgraph alone in the full frame, then a relaxation pass enforces a
minimum pairwise separation between backbone nodes. Phase 2 runs the
full layout with the backbone nodes pinned at their phase-1 positions
— they exert forces but never move — so every other node arranges
itself around a skeleton that is already spread out, and backbone,
ego and full views share one consistent coordinate system.

Cost at the current size (~1,000 nodes / ~6,600 edges): ~600
iterations for the full phase plus a trivial backbone phase, on the
order of 20 s of build time.
"""

import math
import random

_SEED = 20261022
_K = 55.0            # target edge length (FR "optimal distance")
_ITERATIONS = 600
_THETA2 = 1.0        # Barnes-Hut acceptance: (cell half-size)^2 / d^2
_MAX_DEPTH = 24      # quadtree guard: coincident points share a leaf
_BB_ITERATIONS = 700       # phase 1: backbone-only FR
_BB_MIN_SEP = 150.0        # phase 1: enforced min backbone separation
_BB_RELAX_PASSES = 600     # phase 1: separation relaxation passes


def _build_tree(x, y, n):
    """Flat quadtree over the current positions.

    Each cell is a list: [cx, cy, half, count, sum_x, sum_y,
    first_child_index_or_-1, points] where `points` holds the node
    indices of a leaf (usually one; more when the depth cap stopped a
    split, or when points coincide exactly).
    """
    minx, maxx = min(x), max(x)
    miny, maxy = min(y), max(y)
    half = max(maxx - minx, maxy - miny) * 0.5 + 1.0
    cells = [[(minx + maxx) / 2.0, (miny + maxy) / 2.0, half,
              0.0, 0.0, 0.0, -1, []]]
    for i in range(n):
        c = 0
        depth = 0
        while True:
            cell = cells[c]
            cell[3] += 1.0
            cell[4] += x[i]
            cell[5] += y[i]
            if cell[6] < 0:
                if not cell[7]:
                    cell[7].append(i)
                    break
                if depth >= _MAX_DEPTH:
                    cell[7].append(i)
                    break
                h = cell[2] * 0.5
                base = len(cells)
                cell[6] = base
                for qx, qy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
                    cells.append([cell[0] + qx * h, cell[1] + qy * h, h,
                                  0.0, 0.0, 0.0, -1, []])
                old = cell[7]
                cell[7] = []
                for p in old:
                    cc = base + (1 if x[p] >= cell[0] else 0) \
                              + (2 if y[p] >= cell[1] else 0)
                    oc = cells[cc]
                    oc[3] += 1.0
                    oc[4] += x[p]
                    oc[5] += y[p]
                    oc[7].append(p)
                # fall through and descend with point i
            q = (1 if x[i] >= cell[0] else 0) + (2 if y[i] >= cell[1] else 0)
            c = cell[6] + q
            depth += 1
    return cells


def _fr_subset(x, y, present, moving, pairs, degree, iterations, width,
               k=None, gravity=0.004, clamp=False):
    """FR iterations over a subset, mutating the full-length x/y.

    Only indices in `present` take part (the Barnes–Hut tree is built
    over them alone, so fixed nodes still repel and attract); only
    indices in `moving` are displaced. `pairs` holds (a, b) global
    index pairs with both ends in `present`; `degree` is the
    full-graph degree (present nodes all have degree > 0). `k` is the
    FR optimal distance for this subset — it must scale with the
    subset's node count (k = frame / sqrt(m)) or a small subset's
    repulsion overwhelms its few attractions and the layout explodes
    out of the frame.
    """
    pos_of = dict((g, i) for i, g in enumerate(present))
    lx = [x[g] for g in present]
    ly = [y[g] for g in present]
    lpairs = [(pos_of[a], pos_of[b]) for a, b in pairs]
    m = len(present)
    if k is None:
        k = _K
    k2 = k * k
    t_start, t_end = width / 8.0, width / 500.0
    cx = cy = width / 2.0

    for it in range(iterations):
        frac = it / float(iterations - 1) if iterations > 1 else 1.0
        temp = t_start * (t_end / t_start) ** frac
        cells = _build_tree(lx, ly, m)
        dx = [0.0] * m
        dy = [0.0] * m
        # Repulsion (Barnes-Hut).
        for i in range(m):
            xi, yi = lx[i], ly[i]
            fx = fy = 0.0
            stack = [0]
            while stack:
                cell = cells[stack.pop()]
                cnt = cell[3]
                if cnt == 0:
                    continue
                ddx = xi - cell[4] / cnt
                ddy = yi - cell[5] / cnt
                d2 = ddx * ddx + ddy * ddy
                if d2 == 0.0:
                    continue
                if cell[6] < 0:
                    if len(cell[7]) == 1 and cell[7][0] == i:
                        continue
                    f = k2 * cnt / d2
                    fx += f * ddx
                    fy += f * ddy
                elif cell[2] * cell[2] / d2 < _THETA2:
                    f = k2 * cnt / d2
                    fx += f * ddx
                    fy += f * ddy
                else:
                    base = cell[6]
                    stack.append(base)
                    stack.append(base + 1)
                    stack.append(base + 2)
                    stack.append(base + 3)
            dx[i] = fx
            dy[i] = fy
        # Attraction along edges.
        for a, b in lpairs:
            ddx = lx[a] - lx[b]
            ddy = ly[a] - ly[b]
            d = math.sqrt(ddx * ddx + ddy * ddy) + 0.01
            f = d / k
            dx[a] -= f * ddx
            dy[a] -= f * ddy
            dx[b] += f * ddx
            dy[b] += f * ddy
        # Apply to moving nodes only, capped by the temperature, plus
        # centering gravity. A sparse subset (the backbone phase) has
        # too little attraction to balance repulsion on gravity alone,
        # so it can also clamp positions to the frame: the layout then
        # fills the frame instead of drifting out of it.
        pad = width * 0.05
        for li, g in enumerate(present):
            if g not in moving:
                continue
            dx[li] += (cx - lx[li]) * gravity
            dy[li] += (cy - ly[li]) * gravity
            dl = math.sqrt(dx[li] * dx[li] + dy[li] * dy[li]) or 1.0
            step = dl if dl < temp else temp
            lx[li] += dx[li] / dl * step
            ly[li] += dy[li] / dl * step
            if clamp:
                lx[li] = min(max(lx[li], -pad), width + pad)
                ly[li] = min(max(ly[li], -pad), width + pad)
    for li, g in enumerate(present):
        if g in moving:
            x[g], y[g] = lx[li], ly[li]


def _relax_separation(x, y, idxs, min_sep, width):
    """Push the given indices apart until every pair is >= min_sep
    apart (bounded by _BB_RELAX_PASSES), clamping every moved node
    back into the [0, width] frame — an unclamped relaxation just
    expands the bounding box, which zooms the framed view out and
    cancels the separation it bought. Deterministic: pairs are
    visited in index order and coincident pairs separate along a
    golden-angle direction keyed by pair order."""
    limit2 = min_sep * min_sep
    for _ in range(_BB_RELAX_PASSES):
        moved = False
        for ii in range(len(idxs)):
            for jj in range(ii + 1, len(idxs)):
                a, b = idxs[ii], idxs[jj]
                ddx = x[b] - x[a]
                ddy = y[b] - y[a]
                d2 = ddx * ddx + ddy * ddy
                if d2 >= limit2:
                    continue
                if d2 < 1e-9:
                    ang = (ii * len(idxs) + jj) * 2.399963
                    ux, uy = math.cos(ang), math.sin(ang)
                    push = min_sep / 2.0
                else:
                    d = math.sqrt(d2)
                    ux, uy = ddx / d, ddy / d
                    push = (min_sep - d) / 2.0
                x[a] = min(max(x[a] - ux * push, 0.0), width)
                y[a] = min(max(y[a] - uy * push, 0.0), width)
                x[b] = min(max(x[b] + ux * push, 0.0), width)
                y[b] = min(max(y[b] + uy * push, 0.0), width)
                moved = True
        if not moved:
            break


def compute_positions(nodes, edges, backbone_ids=None):
    """Lay out the graph; return {node_id: [x, y]} with int coords.

    `nodes` is graph.py's node list (dicts with "id"), `edges` its
    [source, target, kind] triples, `backbone_ids` the backbone node
    ids (teams/topics/toolkits — derived from node types when not
    given). Every node gets a position, including degree-0 nodes
    (ring placement, see module docstring).
    """
    ids = [nd["id"] for nd in nodes]
    index = dict((nid, i) for i, nid in enumerate(ids))
    n = len(ids)
    if n == 0:
        return {}

    pairs = []
    degree = [0] * n
    for s, t, _kind in edges:
        a, b = index.get(s), index.get(t)
        if a is None or b is None or a == b:
            continue
        pairs.append((a, b))
        degree[a] += 1
        degree[b] += 1

    rng = random.Random(_SEED)
    width = math.sqrt(_K * _K * n)
    x = [rng.uniform(0.0, width) for _ in range(n)]
    y = [rng.uniform(0.0, width) for _ in range(n)]

    if backbone_ids is None:
        backbone_ids = [nd["id"] for nd in nodes
                        if nd.get("t") in ("team", "topic", "toolkit")]
    # Degree-0 backbone nodes (toolkits with no topic/team links —
    # 14 of the current 89) still belong to the backbone view, so they
    # join phase 1 and get spread by repulsion + separation like the
    # rest; otherwise they land on the orphan ring far outside the
    # skeleton and blow up the framed backbone view.
    bb = sorted(index[i] for i in backbone_ids if i in index)
    bbset = set(bb)
    linked = [i for i in range(n) if degree[i] > 0]

    if bb:
        # Phase 1: the backbone alone, in the full frame, with an
        # enforced minimum separation — this is the view the page
        # opens on, so it gets the whole canvas to itself.
        bb_pairs = [(a, b) for a, b in pairs if a in bbset and b in bbset]
        _fr_subset(x, y, bb, bbset, bb_pairs, degree,
                   _BB_ITERATIONS, width, k=width / math.sqrt(len(bb)),
                   gravity=0.01, clamp=True)
        _relax_separation(x, y, bb, _BB_MIN_SEP, width)
        # Phase 2: everything else, backbone pinned as anchors.
        _fr_subset(x, y, linked, set(linked) - bbset, pairs, degree,
                   _ITERATIONS, width)
    else:
        _fr_subset(x, y, linked, set(linked), pairs, degree,
                   _ITERATIONS, width)

    # Degree-0 nodes: a tidy ring around the laid-out mass.
    if linked:
        ccx = sum(x[i] for i in linked) / len(linked)
        ccy = sum(y[i] for i in linked) / len(linked)
        radius = max(math.hypot(x[i] - ccx, y[i] - ccy) for i in linked)
    else:
        ccx = ccy = 0.0
        radius = width / 2.0
    # Backbone orphans already hold phase-1 positions; the ring is
    # only for the remaining degree-0 nodes.
    orphans = sorted((i for i in range(n)
                      if degree[i] == 0 and i not in bbset),
                     key=lambda i: ids[i])
    for j, i in enumerate(orphans):
        ang = 2.0 * math.pi * j / max(1, len(orphans))
        x[i] = ccx + (radius + 160.0) * math.cos(ang)
        y[i] = ccy + (radius + 160.0) * math.sin(ang)

    return dict((ids[i], [int(round(x[i])), int(round(y[i]))])
                for i in range(n))
