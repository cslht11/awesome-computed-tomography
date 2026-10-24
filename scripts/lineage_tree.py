"""Tidy layout for the curated lineage trees (/graph/lineage/<id>/).

Pure geometry, no I/O: build_site.py hands over the node list from
data/lineages.yaml and gets back positioned boxes plus orthogonal
connector paths, all computed at build time so the page ships finished
coordinates (the only runtime script is the pan/zoom viewport in
web/lineage.js). Kept beside the renderer like graph_layout.py sits
beside the graph renderer.
"""

# Card height: the redesign draft's 176px does not fit its own card
# contents at the site's typography -- measured in a browser, the
# stack (year badge, two-line title, venue line, three-line note,
# links row) is 212px for 28 of the 29 cards, so the height is 220
# and the canvas note clamps at three lines (the full text is in the
# reading list below the canvas).
TREE_CARD_W, TREE_CARD_H = 272, 220
TREE_GROUP_W, TREE_GROUP_H = 300, 92
TREE_H_GAP, TREE_V_GAP = 30, 86
TREE_PAD = 24


def normalize_nodes(lineage):
    """Accept the retired v1 chain shape as well as the v2 tree shape.

    v1 stored a plain ordered list of {paper, note, edge?} nodes with no
    keys or parents; v2 nodes always carry "key". When the nodes already
    have keys they are returned unchanged. Otherwise a single-chain tree
    is synthesized in memory: key = the paper id, parent = the previous
    node (the first node is the root), and the v1 "edge" text — the
    writing on the edge INTO this node — serves as both label and prose.
    Group boxes did not exist in v1.

    This exists only so a renderer newer than the data file still builds
    (push sequencing); data/lineages.yaml is v2, where this path is
    unreachable.
    """
    nodes = lineage["nodes"]
    if nodes and "key" in nodes[0]:
        return nodes
    out, prev = [], None
    for n in nodes:
        edge = n.get("edge") or {}
        out.append({"key": n["paper"], "paper": n["paper"], "parent": prev,
                    "note": n.get("note") or {}, "label": edge, "prose": edge})
        prev = n["paper"]
    return out


def num(v):
    """Layout coordinates: whole numbers stay ints, halves stay exact."""
    return int(v) if float(v) == int(v) else round(float(v), 1)


def layout(nodes):
    """Tidy top-down tree layout, computed at build time.

    Depth -> y (each level is as tall as its tallest box), subtree leaf
    span -> x: a node's x centres it over its first/last child centres,
    so boxes never overlap however wide a fork gets. Returns
    (pos, edges, width, height): pos maps key -> (x, y, w, h); edges
    are (parent key, child key, label x, label y, svg path) with the
    orthogonal connector dropping from the parent's bottom edge to a
    shared bus line, across, and into the child's top edge; the label
    anchor is the midpoint of the child's own vertical segment (the
    parent-side drop is shared by all siblings, so per-edge labels can
    only live on the child-side risers).
    """
    by_key = dict((n["key"], n) for n in nodes)
    children, depth, root = {}, {}, None
    for n in nodes:
        if n.get("parent") is None:
            root = n["key"]
        else:
            children.setdefault(n["parent"], []).append(n["key"])

    def size(key):
        n = by_key[key]
        return (TREE_GROUP_W, TREE_GROUP_H) if "group" in n \
            else (TREE_CARD_W, TREE_CARD_H)

    def set_depth(key, d):
        depth[key] = d
        for kid in children.get(key, []):
            set_depth(kid, d + 1)
    set_depth(root, 0)
    level_h = {}
    for key, d in depth.items():
        level_h[d] = max(level_h.get(d, 0), size(key)[1])
    ys, cursor = {}, TREE_PAD
    for d in sorted(level_h):
        ys[d] = cursor
        cursor += level_h[d] + TREE_V_GAP
    height = cursor - TREE_V_GAP + TREE_PAD

    pos, slot = {}, [TREE_PAD]

    def place(key):
        w, h = size(key)
        kids = children.get(key, [])
        if not kids:
            x = slot[0]
            slot[0] += w + TREE_H_GAP
        else:
            lefts = [place(kid) for kid in kids]
            first = lefts[0] + size(kids[0])[0] / 2.0
            last = lefts[-1] + size(kids[-1])[0] / 2.0
            x = (first + last) / 2.0 - w / 2.0
        pos[key] = (x, ys[depth[key]], w, h)
        return x
    place(root)
    width = slot[0] - TREE_H_GAP + TREE_PAD

    edges = []
    for n in nodes:
        par = n.get("parent")
        if par is None:
            continue
        px, py, pw, ph = pos[par]
        cx, cy, cw, ch = pos[n["key"]]
        x1, y1 = px + pw / 2.0, py + ph
        x2, y2 = cx + cw / 2.0, cy
        bus = (y1 + y2) / 2.0
        d = "M %s %s L %s %s L %s %s L %s %s" % (
            num(x1), num(y1), num(x1), num(bus),
            num(x2), num(bus), num(x2), num(y2))
        edges.append((par, n["key"], x2, (bus + y2) / 2.0, d))
    return pos, edges, width, height




def check_layout(lay):
    """Geometry invariants of a layout dict (the page's inline JSON):
    every box inside the stage, no two boxes overlapping. Returns a
    list of problem strings; build_site.py checks the markup counts
    against the same JSON, and tests read it too."""
    out = []
    boxes = lay["nodes"]
    for i, b in enumerate(boxes):
        if (b["x"] < 0 or b["y"] < 0 or b["x"] + b["w"] > lay["width"]
                or b["y"] + b["h"] > lay["height"]):
            out.append("box '%s' leaves the stage" % b["key"])
        for b2 in boxes[i + 1:]:
            if (b["x"] < b2["x"] + b2["w"] and b2["x"] < b["x"] + b["w"]
                    and b["y"] < b2["y"] + b2["h"]
                    and b2["y"] < b["y"] + b["h"]):
                out.append("boxes '%s' and '%s' overlap" % (b["key"], b2["key"]))
    return out
