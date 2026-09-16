#!/usr/bin/env bash
set -euo pipefail

OWNER="${GITHUB_OWNER:-SakuraiTsubaki}"
BASE="${1:-$(pwd)}"
REPOS=(
  PocketMonsters-Sun-Decompilation
  PocketMonsters-Moon-Decompilation
  PocketMonsters-UltraSun-Decompilation
  PocketMonsters-UltraMoon-Decompilation
  PocketMonsters-LetsGoPikachu-Decompilation
  PocketMonsters-LetsGoEevee-Decompilation
)

mkdir -p "$BASE"
for repo in "${REPOS[@]}"; do
  path="$BASE/$repo"
  if [ ! -d "$path/.git" ]; then
    echo "[gen7] cloning $OWNER/$repo"
    git clone "https://github.com/$OWNER/$repo.git" "$path"
  else
    echo "[gen7] updating $repo"
    git -C "$path" pull --ff-only
  fi

  if [ ! -f "$path/tools/use_toolcache.py" ]; then
    echo "[gen7] missing tools/use_toolcache.py in $repo" >&2
    exit 1
  fi

  echo "[gen7] hydrating prebuilt GitHub Release toolcache for $repo"
  python3 "$path/tools/use_toolcache.py"
done

echo "[gen7] all six Generation VII prebuilt toolcaches are ready"
echo "[gen7] no apt install, upstream clone, or tool compilation is performed in the working session"
