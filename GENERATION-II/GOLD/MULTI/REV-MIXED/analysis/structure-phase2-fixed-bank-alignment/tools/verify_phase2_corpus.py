#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path

def tree(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase1_root',type=Path);ap.add_argument('reference_root',type=Path);ap.add_argument('--builder',type=Path,default=Path(__file__).with_name('build_phase2_corpus.py'));ap.add_argument('--alignment-tool',type=Path,default=Path(__file__).with_name('build_fixed_bank_alignment.py'));a=ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'out'
        subprocess.run([sys.executable,str(a.builder),str(a.phase1_root),str(out),'--alignment-tool',str(a.alignment_tool)],check=True,stdout=subprocess.DEVNULL)
        ref=tree(a.reference_root);got=tree(out)
        missing=sorted(set(ref)-set(got));extra=sorted(set(got)-set(ref));changed=sorted(k for k in set(ref)&set(got) if ref[k]!=got[k])
        result={'pass':not(missing or extra or changed),'reference_files':len(ref),'regenerated_files':len(got),'missing':missing,'extra':extra,'changed':changed}
        print(json.dumps(result,indent=2));raise SystemExit(0 if result['pass'] else 1)
if __name__=='__main__':main()
