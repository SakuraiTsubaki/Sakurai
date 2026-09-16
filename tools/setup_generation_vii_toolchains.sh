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

  if [ ! -f "$path/tools/setup_toolchain.sh" ]; then
    echo "[gen7] missing tools/setup_toolchain.sh in $repo" >&2
    exit 1
  fi

  echo "[gen7] installing toolchain for $repo"
  bash "$path/tools/setup_toolchain.sh"
done

echo "[gen7] all six Generation VII toolchains processed"
echo "[gen7] each repository keeps installed binaries under its ignored .tools/ directory"
