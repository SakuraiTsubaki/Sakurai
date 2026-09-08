#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,tempfile,subprocess,sys
from pathlib import Path

def digest_tree(root):
 return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('source_dir',type=Path);ap.add_argument('reference_dir',type=Path);ap.add_argument('--builder',type=Path,default=Path(__file__).with_name('build_structure_phase1.py'));ap.add_argument('--survey-tool',type=Path,default=Path(__file__).with_name('survey_rom_structure.py'));a=ap.parse_args()
 with tempfile.TemporaryDirectory() as td:
  test=Path(td)/'out'
  subprocess.run([sys.executable,str(a.builder),str(a.source_dir),str(test),'--survey-tool',str(a.survey_tool)],check=True,stdout=subprocess.DEVNULL)
  ref=digest_tree(a.reference_dir); got=digest_tree(test)
  # Manifest is generated before itself and is deterministic; compare everything.
  missing=sorted(set(ref)-set(got)); extra=sorted(set(got)-set(ref)); changed=sorted(k for k in set(ref)&set(got) if ref[k]!=got[k])
  result={'pass':not(missing or extra or changed),'reference_files':len(ref),'regenerated_files':len(got),'missing':missing,'extra':extra,'changed':changed}
  print(json.dumps(result,indent=2)); raise SystemExit(0 if result['pass'] else 1)
if __name__=='__main__':main()
