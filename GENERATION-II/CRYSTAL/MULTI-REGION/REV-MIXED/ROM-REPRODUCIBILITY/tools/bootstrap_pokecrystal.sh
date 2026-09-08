#!/usr/bin/env sh
set -eu
PIN=7a7881d0d62e0ddbd82dcf10e7116807487ac651
DEST=${1:-pokecrystal-pinned}
if [ -e "$DEST" ]; then
  echo "destination already exists: $DEST" >&2
  exit 1
fi
git clone https://github.com/pret/pokecrystal.git "$DEST"
cd "$DEST"
git checkout "$PIN"
printf '%s\n' "Pinned pret/pokecrystal at $PIN"
printf '%s\n' "Build with RGBDS 1.0.3: make && make crystal11"
