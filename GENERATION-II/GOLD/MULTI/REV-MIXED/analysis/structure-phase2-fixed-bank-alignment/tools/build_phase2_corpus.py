#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path

REL=Path('GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/structure-phase2-fixed-bank-alignment')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase1_root',type=Path);ap.add_argument('out_root',type=Path);ap.add_argument('--alignment-tool',type=Path,default=Path(__file__).with_name('build_fixed_bank_alignment.py'));a=ap.parse_args()
    dest=a.out_root/REL;dest.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(a.alignment_tool),str(a.phase1_root),str(dest)],check=True,stdout=subprocess.DEVNULL)
    tools=dest/'tools';tools.mkdir(exist_ok=True)
    shutil.copy2(a.alignment_tool,tools/'build_fixed_bank_alignment.py')
    shutil.copy2(Path(__file__),tools/'build_phase2_corpus.py')
    verifier=Path(__file__).with_name('verify_phase2_corpus.py')
    if verifier.exists():shutil.copy2(verifier,tools/'verify_phase2_corpus.py')
    (dest/'SOURCE-PHASE1.md').write_text('''# Phase 1 dependency\n\nThis phase consumes the Phase 1 structural corpus.\n\n- Expected Phase 1 canonical tree SHA-256: `e569b41ec2a5c085edb0f529d4ad0ac1e20795d4c105c8f481cc2c56df7cae9c`\n- Phase 1 generated file count: 105\n\nNo ROM bytes are copied into this Phase 2 corpus.\n''',encoding='utf-8')
    # Replace inner output manifest with final package manifest that includes tools/dependency note.
    man=dest/'MANIFEST.json'
    if man.exists():man.unlink()
    files=[]
    for p in sorted(dest.rglob('*')):
        if p.is_file():files.append({'path':p.relative_to(dest).as_posix(),'size':p.stat().st_size,'sha256':sha(p)})
    man.write_text(json.dumps(files,indent=2),encoding='utf-8')
    print(json.dumps({'files':len(files)+1,'path':str(REL)},indent=2))
if __name__=='__main__':main()
