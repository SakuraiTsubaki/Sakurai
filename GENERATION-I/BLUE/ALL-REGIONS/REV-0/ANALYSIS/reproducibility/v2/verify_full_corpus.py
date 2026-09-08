#!/usr/bin/env python3
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[0]
CHUNK=0x100

def fail(msg): print('FAIL',msg); return False
ok=True
rows=list(csv.DictReader((ROOT/'coverage_proof.csv').open(encoding='utf-8')))
for r in rows:
    if r['exact_cover'] not in ('True','true','1'): ok &= fail(f"coverage {r['code']}")
    if int(r['covered_bytes'])!=int(r['rom_bytes']): ok &= fail(f"byte count {r['code']}")
print('PASS' if ok else 'FAIL','published v2 coverage proof')
raise SystemExit(0 if ok else 1)
