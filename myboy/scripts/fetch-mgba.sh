#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
CPP="$HERE/app/src/main/cpp"
PIN="25ca25612eb806ad3a70f3209ccd93890ea0c2c6"
DEST="$CPP/third_party/mgba"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch --all --tags
else
  mkdir -p "$(dirname "$DEST")"
  git clone https://github.com/mgba-emu/mgba.git "$DEST"
fi
git -C "$DEST" checkout --detach "$PIN"
echo "mGBA pinned at $(git -C "$DEST" rev-parse HEAD)"
