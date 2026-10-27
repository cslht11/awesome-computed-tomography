# -*- coding: utf-8 -*-
"""Per-category slices of the knowledge graph (scripts/graph.py's output).

The single-page graph shipped the whole 1,004-node / 6,677-edge graph
to every reader: one monolithic graph.json, one canvas, a full-graph
mode. On ordinary hardware that was too big and too slow to be usable,
so the page is now split into small, independent graphs — an index at
/graph/ linking to one page per category, each page loading only its
own slice (data + precomputed positions, tens of KB):

    backbone        the directory's skeleton: every team, topic,
                    toolkit and guide node, and the edges between them
    datasets        every dataset and benchmark, plus the papers that
                    use or describe them (uses / cite edges)
    topic/<id>      one per topic: the topic node, its papers, the
                    datasets/benchmarks those papers use, the teams
                    that focus on the topic, the toolkits assigned to
                    it, and its most prolific authors (see the cap
                    rule below)

Composition rules are deliberately mechanical, so a slice can never
drift from the graph it is cut from:

* Every slice is an induced subgraph: an edge ships iff both of its
  endpoints are in the slice.
* A node with no edge inside its slice does not ship at all: a
  relationship graph shows relationships, and an isolated dot says
  nothing (the datasets slice originally shipped 81 such resources
  -- most of its page was a chessboard grid of unused datasets, and
  compute_positions' orphan ring is what arranged them so neatly).
  build_slices records the dropped ids on each slice ("dropped") so
  the build can account for them, and the datasets page states its
  shown-vs-library totals explicitly.
* Topic slices cap at CAP nodes. The core (topic + papers + used
  resources + focused teams + assigned toolkits) always ships whole.
  Authors enter only on top of the core: candidates are authors with
  at least AUTHOR_MIN_IN_TOPIC papers in the topic, most prolific in
  the topic first (ties: more papers in the library overall, then
  node id), and they are added only while the slice stays at or
  under CAP. Only sparse-view currently reaches the cap.

Positions are computed per slice with scripts/graph_layout.py — the
same offline Fruchterman-Reingold the monolith used — so no page ever
runs a layout, or loads another category's nodes, in the browser.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph_layout as graph_layout_mod  # noqa: E402

CAP = 250                    # hard node cap for a topic slice
AUTHOR_MIN_IN_TOPIC = 2      # in-topic papers an author needs to enter

BACKBONE_TYPES = ("team", "topic", "toolkit", "guide")
RESOURCE_TYPES = ("dataset", "benchmark")


def _induced(nodes_by_id, keep, edges):
    """The induced subgraph on `keep`: graph node order, graph edge
    order, so rebuilds are byte-stable."""
    keep = set(keep)
    ns = [nodes_by_id[i] for i in nodes_by_id if i in keep]
    es = [e for e in edges if e[0] in keep and e[1] in keep]
    return {"nodes": ns, "edges": es}


def _drop_isolates(sl):
    """Remove a slice's degree-0 nodes; record their ids on the slice.

    Removing isolates cannot isolate anything else (they had no
    edges), so one pass is exact. The dropped ids ride along as
    sl["dropped"]: the site build reconciles slice + dropped against
    the library payload, so a trim that ate a linked node would fail
    the build instead of silently shrinking the graph.
    """
    degree = dict((n["id"], 0) for n in sl["nodes"])
    for s, t, _k in sl["edges"]:
        degree[s] += 1
        degree[t] += 1
    dropped = [nid for nid, d in degree.items() if d == 0]
    if dropped:
        gone = set(dropped)
        sl["nodes"] = [n for n in sl["nodes"] if n["id"] not in gone]
    sl["dropped"] = dropped
    return sl


def build_slices(graph):
    """graph.py's {nodes, edges, ...} -> {name: {nodes, edges}}.

    Names are URL tails under /graph/: "backbone", "datasets" and
    "topic/<topic id>" for every topic node, in payload topic order.
    """
    nodes_by_id = dict((n["id"], n) for n in graph["nodes"])
    edges = graph["edges"]
    out = {}

    # ------------------------------------------------------------ backbone
    out["backbone"] = _drop_isolates(_induced(
        nodes_by_id,
        [n["id"] for n in graph["nodes"] if n["t"] in BACKBONE_TYPES],
        edges))

    # ------------------------------------------------------------ datasets
    resources = [n["id"] for n in graph["nodes"]
                 if n["t"] in RESOURCE_TYPES]
    keep = set(resources)
    for s, t, k in edges:
        if k in ("uses", "cite"):
            if s in keep and nodes_by_id[t]["t"] == "paper":
                keep.add(t)
            if t in keep and nodes_by_id[s]["t"] == "paper":
                keep.add(s)
    out["datasets"] = _drop_isolates(_induced(nodes_by_id, keep, edges))

    # -------------------------------------------------------------- topics
    # Global authored counts break in-topic ties deterministically.
    authored_total = {}
    for s, t, k in edges:
        if k == "authored":
            authored_total[s] = authored_total.get(s, 0) + 1

    topics = [n["id"][len("topic:"):] for n in graph["nodes"]
              if n["t"] == "topic"]
    for tid in topics:
        tnode = "topic:" + tid
        core = {tnode}
        papers = set()
        for s, t, k in edges:
            if t == tnode and k in ("topic", "start") \
                    and nodes_by_id[s]["t"] == "paper":
                papers.add(s)
            if t == tnode and k == "focus":
                core.add(s)                       # a focused team
            if t == tnode and k == "topic" \
                    and nodes_by_id[s]["t"] == "toolkit":
                core.add(s)                       # an assigned toolkit
        core |= papers
        for s, t, k in edges:
            if s in papers and k in ("uses", "cite") \
                    and nodes_by_id[t]["t"] in RESOURCE_TYPES:
                core.add(t)                       # a resource they use
        # Authors on top of the core, most prolific in-topic first,
        # only while the slice stays within the cap.
        in_topic = {}
        for s, t, k in edges:
            if k == "authored" and t in papers:
                in_topic[s] = in_topic.get(s, 0) + 1
        candidates = [a for a, n in in_topic.items()
                      if n >= AUTHOR_MIN_IN_TOPIC]
        candidates.sort(key=lambda a: (-in_topic[a],
                                       -authored_total.get(a, 0), a))
        for a in candidates:
            if len(core) >= CAP:
                break
            core.add(a)
        out["topic/" + tid] = _drop_isolates(
            _induced(nodes_by_id, core, edges))

    # Belt and braces: the trim above makes an isolate impossible,
    # and a future composition rule that reintroduced one should
    # fail the build loudly rather than ship a chessboard again.
    for name, sl in out.items():
        degree = dict((n["id"], 0) for n in sl["nodes"])
        for s, t, _k in sl["edges"]:
            degree[s] += 1
            degree[t] += 1
        bad = [nid for nid, d in degree.items() if d == 0]
        if bad:
            raise ValueError("slice %s still has isolates: %s"
                             % (name, bad[:5]))
    return out


# Layout effort per slice: the monolith's 600/700 iterations were
# sized for 1,004 nodes; a slice is at most a quarter of that, and the
# annealing schedule is normalised, so fewer iterations converge just
# as fully — at a quarter of the pure-Python build cost.
_SLICE_ITERATIONS = 320
_SLICE_BB_ITERATIONS = 380

# A multi-component slice is re-packed component by component
# (below): the force model pushes disconnected components kilometres
# apart, leaving a mostly-empty frame with a scattered tail. A
# connected slice keeps its force layout (plus the separation pass
# in slice_payload) exactly as computed.
_PACK_GAP = 110.0            # graph units between packed components
_PACK_ASPECT = 2.2           # target frame width : height (~stage)

# The stage the renderer frames onto is ~1400x610 px and frameAll
# uses ratio 1.12, so one normalized unit is ~545 screen px; since
# positions are normalized by their span, the graph-unit separation
# that buys a given screen separation scales with the span. The
# force model alone leaves coincident and near-coincident pairs in
# every slice: Barnes-Hut repulsion cannot separate points that
# start together, the backbone phase's frame clamp piles nodes into
# corners, and a hub's attraction knots its neighbours together.
# So every slice gets a final min-separation pass: no two nodes
# closer than _MIN_SEP_PX screen px. The pass is size-aware: a
# pair of large nodes must clear the sum of their displayed radii
# (the renderer sizes nodes by degree, and two hubs side by side
# overlap at separations a pair of leaves would clear easily).
_MIN_SEP_PX = 22.0
_SEP_MARGIN_PX = 3.0
_SCREEN_PER_UNIT = 610.0 / 1.12    # px per normalized unit on stage


def _components(sl):
    """Connected components of a slice, as lists of node ids."""
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for n in sl["nodes"]:
        parent[n["id"]] = n["id"]
    for s, t, _k in sl["edges"]:
        ra, rb = find(s), find(t)
        if ra != rb:
            parent[ra] = rb
    groups = {}
    for nid in parent:
        groups.setdefault(find(nid), []).append(nid)
    return list(groups.values())


def _pack_components(sl, pos):
    """Translate a slice's components into one compact composition.

    Each component keeps its internal geometry exactly; only whole
    components move. Components are shelf-packed largest first into
    rows sized for a stage-like aspect ratio, and every row is
    centred horizontally within the frame, so a multi-component
    slice reads as one arranged picture -- not a force-layout sprawl
    whose tail trails off a corner. Isolated nodes never reach this
    function (build_slices drops them), so there is no singleton
    grid any more. Deterministic: ties break on node id.
    """
    comps = _components(sl)

    def bbox(c):
        xs = [pos[i][0] for i in c]
        ys = [pos[i][1] for i in c]
        return min(xs), min(ys), max(xs), max(ys)

    boxes = []
    for c in comps:
        x0, y0, x1, y1 = bbox(c)
        boxes.append([c, x0, y0, x1 - x0, y1 - y0])
    boxes.sort(key=lambda b: (-(b[3] * b[4]), min(b[0])))

    total_area = sum((b[3] + _PACK_GAP) * (b[4] + _PACK_GAP) for b in boxes)
    row_width = max([b[3] for b in boxes]
                    + [(total_area * _PACK_ASPECT) ** 0.5])

    rows = []
    row = []
    x = 0.0
    for b in boxes:
        if row and x + b[3] > row_width:
            rows.append(row)
            row, x = [], 0.0
        row.append((b, x))
        x += b[3] + _PACK_GAP
    if row:
        rows.append(row)

    def row_w(r):
        return sum(b[3] for b, _px in r) + _PACK_GAP * (len(r) - 1)

    frame_w = max(row_w(r) for r in rows)
    out = {}
    y = 0.0
    for r in rows:
        row_h = max(b[4] for b, _px in r)
        xoff = (frame_w - row_w(r)) / 2.0
        for (c, x0, y0, _w, _h), px in r:
            for nid in c:
                out[nid] = [int(round(pos[nid][0] - x0 + xoff + px)),
                            int(round(pos[nid][1] - y0 + y))]
        y += row_h + _PACK_GAP
    return out


def _relax_pairs(x, y, min_sep, rad, max_passes=240):
    """Push every pair of points to its required separation (in place).

    Pair (i, j) must end at least max(min_sep, rad[i] + rad[j])
    apart, rad being displayed radii in the same units. Candidate
    pairs come from a grid bucket whose cell is the largest
    requirement, so a pass costs ~O(n + close pairs), not O(n^2).
    Deterministic: pairs are visited in sorted index order, and
    coincident pairs split along a golden-angle direction keyed by
    the pair. No frame clamp: expanding the frame is fine (framing
    normalizes it away), and clamping is exactly what piled the
    backbone's nodes into corners in the first place.
    """
    n = len(x)
    cell = max([min_sep] + [2.0 * r for r in rad])
    for _ in range(max_passes):
        grid = {}
        for i in range(n):
            key = (int(x[i] // cell), int(y[i] // cell))
            grid.setdefault(key, []).append(i)
        pairs = set()
        for (cx, cy), members in grid.items():
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    other = grid.get((cx + dx, cy + dy))
                    if not other:
                        continue
                    for i in members:
                        for j in other:
                            if i < j:
                                pairs.add((i, j))
        moved = False
        for i, j in sorted(pairs):
            need = max(min_sep, rad[i] + rad[j])
            ddx = x[j] - x[i]
            ddy = y[j] - y[i]
            d2 = ddx * ddx + ddy * ddy
            if d2 >= need * need:
                continue
            if d2 < 1e-9:
                ang = (i * n + j) * 2.399963
                ux, uy = math.cos(ang), math.sin(ang)
                push = need / 2.0
            else:
                d = math.sqrt(d2)
                ux, uy = ddx / d, ddy / d
                push = (need - d) / 2.0
            x[i] -= ux * push
            y[i] -= uy * push
            x[j] += ux * push
            y[j] += uy * push
            moved = True
        if not moved:
            break


def _spread(sl, pos, rounds=5):
    """Enforce the screen-space separation invariant on a layout.

    Every pair ends at least _MIN_SEP_PX screen px apart, and large
    nodes at least the sum of their displayed radii (plus margin)
    -- web/graph.js sizes a node 2.6 + min(13, sqrt(degree) * 1.5),
    displayed at ~2.2 px per size unit, i.e. a radius of ~1.1 size
    units. The graph-unit target is re-derived from the live span
    each round: pushing pairs apart grows the span, which shrinks
    the screen value of a graph unit, so a fixed target undershoots.
    Stops as soon as the invariant holds (usually a round or two)
    or the rounds run out.
    """
    ids = [n["id"] for n in sl["nodes"]]
    degree = dict((nid, 0) for nid in ids)
    for s, t, _k in sl["edges"]:
        degree[s] += 1
        degree[t] += 1
    # Per-node requirement share, in screen px: displayed radius
    # plus half the margin, so rad[i] + rad[j] is the pair's need.
    share = [1.1 * (2.6 + min(13.0, math.sqrt(degree[i]) * 1.5))
             + _SEP_MARGIN_PX / 2.0 for i in ids]
    x = [float(pos[i][0]) for i in ids]
    y = [float(pos[i][1]) for i in ids]
    n = len(ids)
    for _ in range(rounds):
        span = max(max(x) - min(x), max(y) - min(y)) or 1.0
        unit = span / _SCREEN_PER_UNIT     # graph units per screen px
        _relax_pairs(x, y, _MIN_SEP_PX * unit,
                     [s * unit for s in share])
        span = max(max(x) - min(x), max(y) - min(y)) or 1.0
        unit = span / _SCREEN_PER_UNIT
        worst = None
        for i in range(n):
            for j in range(i + 1, n):
                need = max(_MIN_SEP_PX, share[i] + share[j]) * unit
                ratio = math.hypot(x[i] - x[j], y[i] - y[j]) / need
                if worst is None or ratio < worst:
                    worst = ratio
        if worst is not None and worst >= 0.99:
            break
    return dict((ids[i], [int(round(x[i])), int(round(y[i]))])
                for i in range(n))


def slice_payload(sl, total=None):
    """One slice -> the JSON its page loads: the slice's nodes and
    edges plus precomputed positions (and nothing else's).

    The wire format is compact, because a page's whole budget is this
    one file: edges are [source, target, kind] *index* triples into
    the nodes array with a shared kind table, and positions are an
    array aligned with the nodes — node ids are long, and repeating
    them per edge and per position would double the file.
    """
    pos = graph_layout_mod.compute_positions(
        sl["nodes"], sl["edges"], iterations=_SLICE_ITERATIONS,
        bb_iterations=_SLICE_BB_ITERATIONS)
    if pos:
        # The force model leaves coincident/knot pairs in every
        # slice (see _MIN_SEP_PX above); separate first, then pack
        # multi-component slices into one composition, then a final
        # short pass so packing neighbours also honour the minimum.
        pos = _spread(sl, pos)
        if len(_components(sl)) > 1:
            pos = _pack_components(sl, pos)
            pos = _spread(sl, pos, rounds=2)
    index = dict((n["id"], i) for i, n in enumerate(sl["nodes"]))
    kinds = []
    kind_index = {}
    edges = []
    for s, t, k in sl["edges"]:
        if k not in kind_index:
            kind_index[k] = len(kinds)
            kinds.append(k)
        edges.append([index[s], index[t], kind_index[k]])
    if total is None:
        total = len(sl["nodes"])
    return {"nodes": sl["nodes"], "edges": edges, "kinds": kinds,
            "pos": [pos[n["id"]] for n in sl["nodes"]],
            "total": total}


def slice_json(data):
    return json.dumps(data, ensure_ascii=False,
                      separators=(",", ":")) + "\n"
