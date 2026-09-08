#!/usr/bin/env python3
import argparse,csv,hashlib
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("--rom-dir",type=Path,required=True); ap.add_argument("--inventory",type=Path,required=True); a=ap.parse_args()
fail=0
with a.inventory.open(encoding="utf-8") as f:
 for r in csv.DictReader(f):
  p=a.rom_dir/r["filename"]
  if not p.exists(): print("MISSING",p); fail+=1; continue
  data=p.read_bytes(); h=hashlib.sha256(data).hexdigest(); ok=(h==r["sha256"] and len(data)==int(r["size"]))
  print("PASS" if ok else "FAIL",r["language"],r["revision"],p.name)
  fail += 0 if ok else 1
raise SystemExit(1 if fail else 0)
