#!/usr/bin/env bash
set -euo pipefail
ROM_DIR="${1:?usage: $0 ROM_DIR}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
python3 "$ROOT/tools/run_all.py" "$ROM_DIR" "$ROOT"
python3 "$ROOT/tools/verify.py" "$ROM_DIR"
python3 "$ROOT/tests/roundtrip_all.py" "$ROM_DIR"
