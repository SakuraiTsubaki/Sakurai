#!/usr/bin/env bash
set -euo pipefail
ROM_DIR="${1:-./roms}"
OUT_DIR="${2:-./generated-local}"
python3 tools/verify_manifest.py "$ROM_DIR" data/source_manifest.json
python3 tools/analyze_sapphire.py "$ROM_DIR" --out "$OUT_DIR"
python3 tools/verify_generated.py "$OUT_DIR" data/generated_dataset_manifest.json
echo "Reproducibility analysis complete and baseline-matched: $OUT_DIR"
