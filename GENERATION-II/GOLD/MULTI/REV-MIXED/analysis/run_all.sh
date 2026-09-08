#!/usr/bin/env sh
set -eu
python3 tools/build_gold_repro_corpus.py --rom-dir "${1:-/mnt/data}" --out "${2:-./rebuild}"
python3 tools/verify_corpus.py --rom-dir "${1:-/mnt/data}" --inventory "${2:-./rebuild}/GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/manifests/rom_inventory.csv"
