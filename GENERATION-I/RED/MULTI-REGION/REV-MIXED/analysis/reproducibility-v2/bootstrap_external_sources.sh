#!/usr/bin/env sh
set -eu
mkdir -p external
if [ ! -d external/pokered/.git ]; then git clone https://github.com/pret/pokered.git external/pokered; fi
git -C external/pokered fetch --all --tags
git -C external/pokered checkout --detach a1a22aaf84d1675bcdbaeb194592379d586d838e
if [ ! -d external/pokegreen/.git ]; then git clone https://github.com/Narishma-gb/pokegreen.git external/pokegreen; fi
git -C external/pokegreen fetch --all --tags
git -C external/pokegreen checkout --detach 953f41b34108621b2bf13c3b1e53abfc9c3e5aec
echo 'Pinned semantic source baselines checked out.'
