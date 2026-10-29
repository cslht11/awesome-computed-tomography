# Vendored libraries

Third-party JavaScript served with the site (no CDN at runtime). Each file
is the unmodified release build from its project, pinned to the version
below; `scripts/build_site.py` copies the files to the site root and the
graph page degrades gracefully when any of them is absent.

| File | Project | Version | License |
| --- | --- | --- | --- |
| `graphology.min.js` | graphology — https://github.com/graphology/graphology | 0.25.4 | MIT |
| `sigma.min.js` | sigma.js — https://github.com/jacomyal/sigma.js | 3.0.2 | MIT |

Each library's MIT licence is kept beside it (`graphology.LICENSE.txt`,
`sigma.LICENSE.txt`, copied from the npm packages of the same versions).
The release builds carry no licence text of their own, so the build
prepends that file as a `/*! … */` comment to the copy it deploys; the
files here stay byte-identical to the releases.

Notes:

- Both are UMD builds defining browser globals (`graphology`, `Sigma`);
  `web/graph.js` checks for both before touching the page, so a missing
  file leaves the server-rendered static fallback in charge.
- sigma.js renders with WebGL (batched node/edge programs). On a
  browser where its WebGL2-era code cannot run, the globals stay
  undefined and the static fallback serves the page instead.
- Retired 2026-10-22, when the graph page moved to precomputed layout +
  sigma: `cytoscape.min.js` (canvas renderer, runtime cose layout),
  `3d-force-graph.min.js`, `three-spritetext.min.js`, `three.min.js`
  (the 3D view: per-object three.js rendering + runtime force
  simulation — too slow at ~1,000 nodes / ~6,600 edges, and its 2D/3D
  toggle needed a full-page reload for every switch).
