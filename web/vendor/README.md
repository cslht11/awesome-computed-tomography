# Vendored libraries

Third-party JavaScript served with the site (no CDN at runtime). Each file
is the unmodified release build from its project, pinned to the version
below; `scripts/build_site.py` copies the files to the site root and the
graph page degrades gracefully when any of them is absent.

| File | Project | Version | License |
| --- | --- | --- | --- |
| `cytoscape.min.js` | Cytoscape.js — https://github.com/cytoscape/cytoscape.js | 3.30.2 | MIT |
| `3d-force-graph.min.js` | 3d-force-graph — https://github.com/vasturiano/3d-force-graph | 1.80.1 | MIT |
| `three-spritetext.min.js` | three-spritetext — https://github.com/vasturiano/three-spritetext | 1.10.0 | MIT |
| `three.min.js` | three.js — https://github.com/mrdoob/three.js | 0.160.0 | MIT |

Notes:

- `3d-force-graph.min.js` is a self-contained UMD bundle (it inlines its
  own three.js, r186) and defines the global `ForceGraph3D`.
- `three-spritetext.min.js` needs a global `THREE`, which is the only job
  of `three.min.js` here (0.160.0 is the last three.js release with an
  official UMD build; the sprites it creates are rendered by the three.js
  inlined in 3d-force-graph — the same arrangement as the library's own
  text-nodes example).
