#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'data/lossless_rebuild_results.json').read_text())
p=json.loads((root/'data/patch_verification.json').read_text())
assert all(x['exact_match'] for x in r), r
assert all(x['exact_match'] for x in p), p
print(f"PASS: {len(r)} lossless bank rebuilds; {len(p)} IPS patch rebuilds")
