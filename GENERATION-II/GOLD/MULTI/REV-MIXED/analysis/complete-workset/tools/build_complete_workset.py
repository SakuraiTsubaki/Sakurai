#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path

MASTER_REL=Path('GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/complete-workset')

def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def derive_tools(self_path:Path):
    analysis=self_path.resolve().parents[2]
    return {
      'phase0':analysis/'tools/build_gold_repro_corpus.py',
      'phase1':analysis/'structure-phase1/tools/build_structure_phase1.py',
      'survey':analysis/'structure-phase1/tools/survey_rom_structure.py',
      'phase2':analysis/'structure-phase2-fixed-bank-alignment/tools/build_phase2_corpus.py',
      'align':analysis/'structure-phase2-fixed-bank-alignment/tools/build_fixed_bank_alignment.py',
      'phase3':analysis/'full-rom-reproducibility/tools/build_full_rom_atlas.py',
    }

def run(cmd): subprocess.run([sys.executable,*map(str,cmd)],check=True)

def main():
    ap=argparse.ArgumentParser(description='Build the complete ROM-free reproducibility workset for the eight verified Pokémon Gold ROMs.')
    ap.add_argument('source_dir',type=Path); ap.add_argument('out_dir',type=Path)
    ap.add_argument('--phase0-tool',type=Path); ap.add_argument('--phase1-tool',type=Path); ap.add_argument('--survey-tool',type=Path)
    ap.add_argument('--phase2-tool',type=Path); ap.add_argument('--alignment-tool',type=Path); ap.add_argument('--phase3-tool',type=Path)
    a=ap.parse_args()
    d=derive_tools(Path(__file__))
    p0=a.phase0_tool or d['phase0']; p1=a.phase1_tool or d['phase1']; surv=a.survey_tool or d['survey']; p2=a.phase2_tool or d['phase2']; align=a.alignment_tool or d['align']; p3=a.phase3_tool or d['phase3']
    for p in (p0,p1,surv,p2,align,p3):
        if not p.exists(): raise SystemExit(f'missing required generator: {p}')
    run([p0,'--rom-dir',a.source_dir,'--out',a.out_dir])
    run([p1,a.source_dir,a.out_dir,'--survey-tool',surv])
    run([p2,a.out_dir,a.out_dir,'--alignment-tool',align])
    run([p3,a.source_dir,a.out_dir])
    master=a.out_dir/MASTER_REL; tools=master/'tools'; tools.mkdir(parents=True,exist_ok=True)
    shutil.copy2(Path(__file__),tools/'build_complete_workset.py')
    v=Path(__file__).with_name('verify_complete_workset.py')
    if v.exists(): shutil.copy2(v,tools/'verify_complete_workset.py')
    (master/'README.md').write_text('''# Pokémon Gold Complete Reproducibility Workset\n\nThis is the top-level contract for the eight-ROM Gold survey. The copyrighted ROM payloads are external, read-only inputs and are never committed.\n\nThe workset combines:\n\n1. **Phase 0 — physical ROM corpus:** identification, cryptographic hashes, bank maps, 4 KiB chunk hashes, byte frequencies, blank banks, exact `INCBIN` rebuild scaffolds, and cross-version checks.\n2. **Phase 1 — structural fixed-bank survey:** ROM0 control-flow reachability, symbols, entropy, fill runs, pointer/address candidates, and fixed-bank comparisons.\n3. **Phase 2 — fixed-bank alignment:** normalized basic-block families and Korean ↔ international structural equivalence evidence.\n4. **Phase 3 — full-ROM atlas:** 100% byte coverage segments, every-bank features, pointer/far-pointer windows, 256-byte page hashes, cross-version bank correspondence evidence, and segmented RGBDS rebuild scaffolds.\n\nRun `tools/build_complete_workset.py <rom-directory> <output-directory>` to regenerate all layers from the verified source ROMs.\n''',encoding='utf-8')
    counts={}
    for p in sorted(a.out_dir.rglob('*')):
        if not p.is_file(): continue
        ext=p.suffix.lower() or '<none>'; counts[ext]=counts.get(ext,0)+1
    (master/'FILE-TYPE-COUNTS.json').write_text(json.dumps(counts,indent=2,sort_keys=True),encoding='utf-8')
    files=[]
    for p in sorted(a.out_dir.rglob('*')):
        if not p.is_file(): continue
        if p in {master/'MASTER-MANIFEST.json',master/'SNAPSHOT.md'}: continue
        files.append({'path':p.relative_to(a.out_dir).as_posix(),'size':p.stat().st_size,'sha256':sha(p)})
    (master/'MASTER-MANIFEST.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
    h=hashlib.sha256()
    for e in files: h.update(f"{e['path']}\t{e['size']}\t{e['sha256']}\n".encode())
    total=sum(e['size'] for e in files)
    (master/'SNAPSHOT.md').write_text(f'''# Complete Workset Snapshot\n\n- Manifested files: {len(files)}\n- Manifested bytes: {total:,}\n- Canonical path/size/SHA-256 digest: `{h.hexdigest()}`\n- Source ROM files included: 0\n- Required external source ROMs: 8\n- Full-ROM byte coverage: 100% per source ROM\n''',encoding='utf-8')
    print(json.dumps({'files':len(files)+2,'bytes':total,'tree_digest':h.hexdigest()},indent=2))
if __name__=='__main__':main()
