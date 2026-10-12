#!/bin/sh
# 把 hooks/ 下的守卫安装到 .git/hooks/。
#
# Git 不会自动启用仓库里提交的 hooks —— 那是有意的（否则克隆一个仓库就能
# 在你机器上执行它的代码），代价是每次克隆之后都得手动跑一次：
#
#     sh scripts/install-hooks.sh
#
# 装了什么、为什么：
#   pre-commit  拒绝 user.email 不是 cslht11@users.noreply.github.com 的提交
#   pre-push    拒绝任何一笔作者不是 cslht11 的提交被推上去
#
# 两道缺一不可。pre-commit 管不住 squash 合并 —— 那是用 PR 作者身份署名的，
# 跟本机配置毫无关系，2026-10-12 就是这样把 dependabot[bot] 放进贡献者图的。

set -e

root=$(cd "$(dirname "$0")/.." && pwd)
src="$root/hooks"
dst="$root/.git/hooks"

if [ ! -d "$dst" ]; then
  echo "找不到 $dst —— 这里不是一个 git 工作副本？" >&2
  exit 1
fi

for h in pre-commit pre-push; do
  if [ ! -f "$src/$h" ]; then
    echo "缺少 $src/$h" >&2
    exit 1
  fi
  cp "$src/$h" "$dst/$h"
  chmod +x "$dst/$h"
  echo "已安装 .git/hooks/$h"
done

cat <<'EOF'

自检（应当放行）：
    printf 'refs/heads/main HEAD refs/heads/main HEAD~1\n' | sh .git/hooks/pre-push

若要临时绕过（不推荐）：git push --no-verify
EOF
