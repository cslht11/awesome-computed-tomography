#!/bin/bash
# 定向核验已知的 CT / 断层重建工具库
cd "$(dirname "$0")" || exit 1
OUT="toolkits_core.tsv"
: > "$OUT"

REPOS="
CERN/TIGRE
astra-toolbox/astra-toolbox
cicwi/tomosipo
odlgroup/odl
deepinv/deepinv
matteo-ronchetti/torch-radon
llnl/LEAP
tomopy/tomopy
analysiscenter/radio
cabouman/svmbir
djvine/pySART
tatsy/libcbct
ufo-kit/tofu
villekf/OMEGA
TomographicProcessing/CIL
sigpy/sigpy
PyTomography/PyTomography
RTKConsortium/RTK
chenyangh/LEARN
CambridgeCIA/LION
gvxr/gvxr
spekpy/spekpy
tsadakane/tomophantom
xraylib/xraylib
pydicom/pydicom
Project-MONAI/MONAI
scikit-image/scikit-image
SimpleITK/SimpleITK
CERN/TIGRE
"

for repo in $REPOS; do
  [ -z "$repo" ] && continue
  for try in 1 2 3; do
    line=$(gh api "repos/$repo" --jq '[.full_name, (.stargazers_count|tostring), (.language // "-"), (.license.spdx_id // "-"), (.pushed_at[0:10]), (.archived|tostring), ((.description // "-")|gsub("[\t\n]";" ")|.[0:100])] | @tsv' 2>/dev/null)
    if [ -n "$line" ]; then printf '%s\n' "$line" >> "$OUT"; break; fi
    sleep 2
  done
done
echo "核验完成 $(wc -l < "$OUT") 条"
