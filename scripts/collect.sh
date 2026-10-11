#!/bin/bash
# 收集 CT / 断层重建相关的候选仓库名
cd "$(dirname "$0")" || exit 1
OUT="toolkits_raw.txt"
: > "$OUT"

q() {
  gh search repos "$1" --limit 50 --json fullName --jq '.[].fullName' 2>/dev/null >> "$OUT"
  sleep 2
}
qt() {
  gh search repos --topic "$1" --limit 50 --json fullName --jq '.[].fullName' 2>/dev/null >> "$OUT"
  sleep 2
}

q "tomographic reconstruction"
q "CT reconstruction"
q "radon transform"
q "cone beam CT reconstruction"
q "iterative reconstruction tomography"
q "x-ray tomography"
q "low dose CT"
q "sparse view CT"
q "CT simulation phantom"
q "CT metal artifact reduction"
q "spectral CT reconstruction"
q "limited angle tomography"
q "inverse problems imaging"
qt tomography
qt computed-tomography
qt ct-reconstruction
qt tomographic-reconstruction
qt x-ray-imaging

sort -u "$OUT" -o "$OUT"
echo "候选仓库总数 = $(wc -l < "$OUT")"
