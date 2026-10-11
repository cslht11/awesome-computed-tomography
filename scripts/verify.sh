#!/bin/bash
# 逐个核验候选仓库，输出 TSV
cd "$(dirname "$0")" || exit 1
IN="toolkits_raw.txt"
OUT="toolkits_meta.tsv"
: > "$OUT"
n=0
while IFS= read -r repo; do
  [ -z "$repo" ] && continue
  n=$((n+1))
  for try in 1 2 3; do
    line=$(gh api "repos/$repo" --jq '[.full_name, (.stargazers_count|tostring), (.language // "-"), (.license.spdx_id // "-"), (.pushed_at[0:10]), (.archived|tostring), ((.description // "-")|gsub("[\t\n]";" ")|.[0:110]), ((.topics // [])|join(","))] | @tsv' 2>/dev/null)
    if [ -n "$line" ]; then
      printf '%s\n' "$line" >> "$OUT"
      break
    fi
    sleep 2
  done
  if [ $((n % 50)) -eq 0 ]; then echo "  已处理 $n ..."; fi
done < "$IN"
echo "完成，核验成功 $(wc -l < "$OUT") / $n"
