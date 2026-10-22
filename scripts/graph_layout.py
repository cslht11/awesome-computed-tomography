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

Cost at the current size (~1,000 nodes / ~6,600 edges): ~600
iterations, on the order of 20 s of build time.
"""

import math
import random

_SEED = 20261022
_K = 55.0            # target edge length (FR "optimal distance")
_ITERATIONS = 600
_THETA2 = 1.0        # Barnes-Hut acceptance: (cell half-size)^2 / d^2
_MAX_DEPTH = 24      # quadtree guard: coincident points share a leaf


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


def compute_positions(nodes, edges):
    """Lay out the graph; return {node_id: [x, y]} with int coords.

    `nodes` is graph.py's node list (dicts with "id"), `edges` its
    [source, target, kind] triples. Every node gets a position,
    including degree-0 nodes (ring placement, see module docstring).
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
    k2 = _K * _K
    t_start, t_end = width / 8.0, width / 500.0
    cx = cy = width / 2.0

    for it in range(_ITERATIONS):
        frac = it / float(_ITERATIONS - 1)
        temp = t_start * (t_end / t_start) ** frac
        cells = _build_tree(x, y, n)
        dx = [0.0] * n
        dy = [0.0] * n
        # Repulsion (Barnes-Hut).
        for i in range(n):
            if degree[i] == 0:
                continue
            xi, yi = x[i], y[i]
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
        for a, b in pairs:
            ddx = x[a] - x[b]
            ddy = y[a] - y[b]
            d = math.sqrt(ddx * ddx + ddy * ddy) + 0.01
            f = d / _K
            dx[a] -= f * ddx
            dy[a] -= f * ddy
            dx[b] += f * ddx
            dy[b] += f * ddy
        # Apply, capped by the temperature; weak centering gravity.
        for i in range(n):
            if degree[i] == 0:
                continue
            dx[i] += (cx - x[i]) * 0.004
            dy[i] += (cy - y[i]) * 0.004
            dl = math.sqrt(dx[i] * dx[i] + dy[i] * dy[i]) or 1.0
            step = dl if dl < temp else temp
            x[i] += dx[i] / dl * step
            y[i] += dy[i] / dl * step

    # Degree-0 nodes: a tidy ring around the laid-out mass.
    linked = [i for i in range(n) if degree[i] > 0]
    if linked:
        ccx = sum(x[i] for i in linked) / len(linked)
        ccy = sum(y[i] for i in linked) / len(linked)
        radius = max(math.hypot(x[i] - ccx, y[i] - ccy) for i in linked)
    else:
        ccx = ccy = 0.0
        radius = width / 2.0
    orphans = sorted((i for i in range(n) if degree[i] == 0),
                     key=lambda i: ids[i])
    for j, i in enumerate(orphans):
        ang = 2.0 * math.pi * j / max(1, len(orphans))
        x[i] = ccx + (radius + 160.0) * math.cos(ang)
        y[i] = ccy + (radius + 160.0) * math.sin(ang)

    return dict((ids[i], [int(round(x[i])), int(round(y[i]))])
                for i in range(n))
