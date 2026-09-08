#!/usr/bin/env sh
set -eu
ROM_DIR=${1:-.}
OUT_DIR=${2:-./emerald_repro_output}
python3 "$(dirname "$0")/audit_emerald.py" --rom-dir "$ROM_DIR" --out "$OUT_DIR"
python3 "$(dirname "$0")/verify_roms.py" "$ROM_DIR"
