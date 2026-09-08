#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path

def tree(root:Path):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}

def verify_segments(source_dir:Path, ref_root:Path):
    import csv
    roms=json.loads((ref_root/'GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/full-rom-reproducibility/ROM-SET.json').read_text())
    checks=[]
    for t in roms:
        d=(source_dir/t['filename']).read_bytes(); assert hashlib.sha256(d).hexdigest()==t['sha256']
        seg=ref_root/f"GENERATION-II/GOLD/{t['region']}/{t['rev']}/analysis/full-rom-reproducibility/source_segments.csv"
        with seg.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
        cursor=0
        for r in rows:
            start=int(r['rom_start'],16); end=int(r['rom_end'],16)+1; ln=int(r['length'])
            if start!=cursor or end-start!=ln: raise SystemExit(f'coverage gap/overlap: {t["label"]} at {cursor:#x}')
            if r['kind']=='fill':
                v=int(r['fill_value'],16)
                if d[start:end] != bytes([v])*ln: raise SystemExit(f'fill mismatch: {t["label"]} {start:#x}')
            cursor=end
        if cursor!=len(d): raise SystemExit(f'coverage ended at {cursor:#x}, expected {len(d):#x}')
        checks.append({'label':t['label'],'bytes':cursor,'segments':len(rows)})
    return checks

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source_dir',type=Path); ap.add_argument('reference_root',type=Path); ap.add_argument('--builder',type=Path,default=Path(__file__).with_name('build_full_rom_atlas.py')); a=ap.parse_args()
    checks=verify_segments(a.source_dir,a.reference_root)
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'out'; subprocess.run([sys.executable,str(a.builder),str(a.source_dir),str(out)],check=True,stdout=subprocess.DEVNULL)
        ref=tree(a.reference_root); got=tree(out)
        missing=sorted(set(ref)-set(got)); extra=sorted(set(got)-set(ref)); changed=sorted(k for k in ref.keys()&got.keys() if ref[k]!=got[k])
        result={'pass':not(missing or extra or changed),'coverage_checks':checks,'reference_files':len(ref),'regenerated_files':len(got),'missing':missing,'extra':extra,'changed':changed}
        print(json.dumps(result,indent=2)); raise SystemExit(0 if result['pass'] else 1)
if __name__=='__main__': main()
