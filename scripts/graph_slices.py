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


def build_slices(graph):
    """graph.py's {nodes, edges, ...} -> {name: {nodes, edges}}.

    Names are URL tails under /graph/: "backbone", "datasets" and
    "topic/<topic id>" for every topic node, in payload topic order.
    """
    nodes_by_id = dict((n["id"], n) for n in graph["nodes"])
    edges = graph["edges"]
    out = {}

    # ------------------------------------------------------------ backbone
    out["backbone"] = _induced(
        nodes_by_id,
        [n["id"] for n in graph["nodes"] if n["t"] in BACKBONE_TYPES],
        edges)

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
    out["datasets"] = _induced(nodes_by_id, keep, edges)

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
        out["topic/" + tid] = _induced(nodes_by_id, core, edges)

    return out


# Layout effort per slice: the monolith's 600/700 iterations were
# sized for 1,004 nodes; a slice is at most a quarter of that, and the
# annealing schedule is normalised, so fewer iterations converge just
# as fully — at a quarter of the pure-Python build cost.
_SLICE_ITERATIONS = 320
_SLICE_BB_ITERATIONS = 380

# A slice whose layout frame is mostly empty space — area per node
# far above what a connected layout of that size needs — is a slice
# of disconnected components the force model pushed kilometres apart
# (the datasets slice: 98 resources, most linked to nothing). Such a
# slice is re-packed component by component (below); a connected
# slice's layout is left exactly as the force model made it.
_PACK_AREA_PER_NODE = 45000.0
_PACK_GAP = 110.0            # graph units between packed components
_SINGLETON_CELL = 120.0      # grid cell for an isolated node


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
    """Translate a slice's components into one compact frame.

    Each component keeps its internal geometry exactly; only whole
    components move. Multi-node components are shelf-packed largest
    first; isolated nodes go into a grid of their own at the end.
    Deterministic: ties break on node id.
    """
    comps = _components(sl)
    multi, singles = [], []
    for c in comps:
        (singles if len(c) == 1 else multi).append(c)

    def bbox(c):
        xs = [pos[i][0] for i in c]
        ys = [pos[i][1] for i in c]
        return min(xs), min(ys), max(xs), max(ys)

    boxes = []
    for c in multi:
        x0, y0, x1, y1 = bbox(c)
        boxes.append([c, x0, y0, x1 - x0, y1 - y0])
    boxes.sort(key=lambda b: (-(b[3] * b[4]), min(b[0])))
    if singles:
        cells = sorted(singles, key=lambda c: c[0])
        per_row = max(1, int(len(cells) ** 0.5 + 0.5))
        w = per_row * _SINGLETON_CELL
        h = ((len(cells) + per_row - 1) // per_row) * _SINGLETON_CELL
        boxes.append([cells, None, None, w, h])

    total_area = sum((b[3] + _PACK_GAP) * (b[4] + _PACK_GAP) for b in boxes)
    row_width = max([b[3] for b in boxes] + [total_area ** 0.5])

    out = {}
    x = y = 0.0
    row_h = 0.0
    for c, x0, y0, w, h in boxes:
        if x > 0 and x + w > row_width:
            x = 0.0
            y += row_h + _PACK_GAP
            row_h = 0.0
        if x0 is None:      # the singleton grid
            per_row = max(1, int(w // _SINGLETON_CELL))
            for j, cell in enumerate(c):
                cx = x + (j % per_row) * _SINGLETON_CELL \
                    + _SINGLETON_CELL / 2.0
                cy = y + (j // per_row) * _SINGLETON_CELL \
                    + _SINGLETON_CELL / 2.0
                out[cell[0]] = [int(round(cx)), int(round(cy))]
        else:
            for nid in c:
                out[nid] = [int(round(pos[nid][0] - x0 + x)),
                            int(round(pos[nid][1] - y0 + y))]
        x += w + _PACK_GAP
        row_h = max(row_h, h)
    return out


def slice_payload(sl):
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
        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        if len(_components(sl)) > 1 \
                and area > _PACK_AREA_PER_NODE * len(pos):
            pos = _pack_components(sl, pos)
    index = dict((n["id"], i) for i, n in enumerate(sl["nodes"]))
    kinds = []
    kind_index = {}
    edges = []
    for s, t, k in sl["edges"]:
        if k not in kind_index:
            kind_index[k] = len(kinds)
            kinds.append(k)
        edges.append([index[s], index[t], kind_index[k]])
    return {"nodes": sl["nodes"], "edges": edges, "kinds": kinds,
            "pos": [pos[n["id"]] for n in sl["nodes"]]}


def slice_json(data):
    return json.dumps(data, ensure_ascii=False,
                      separators=(",", ":")) + "\n"
