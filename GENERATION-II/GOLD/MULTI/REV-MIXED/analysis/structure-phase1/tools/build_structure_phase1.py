#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,subprocess,sys
from pathlib import Path

ROMS={
 'KR-REV-0':('Pocket Monsters Geum (Korea).gbc','KR','REV-0'),
 'JP-REV-0':('Pocket Monsters Kin (Japan).gbc','JP','REV-0'),
 'JP-REV-A':('Pocket Monsters Kin (Japan) (Rev A).gbc','JP','REV-A'),
 'USA-EUROPE-REV-0':('Pokemon - Gold Version (USA, Europe).gbc','USA-EUROPE','REV-0'),
 'DE-REV-0':('Pokemon - Goldene Edition (Germany).gbc','DE','REV-0'),
 'FR-REV-0':('Pokemon - Version Or (France).gbc','FR','REV-0'),
 'IT-REV-0':('Pokemon - Versione Oro (Italy).gbc','IT','REV-0'),
 'ES-REV-0':('Pokemon - Edicion Oro (Spain).gbc','ES','REV-0'),
}
BANK=0x4000

def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(p,header,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(rows)

def cross(src,out):
 data={k:(src/fn).read_bytes()[:BANK] for k,(fn,_,_) in ROMS.items()}
 c=out/'GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/structure-phase1/cross-version';c.mkdir(parents=True,exist_ok=True)
 names=list(data); rows=[]
 for i,a in enumerate(names):
  for b in names[i+1:]:
   diff=sum(x!=y for x,y in zip(data[a],data[b]))
   rows.append((a,b,diff,BANK-diff,f'{(BANK-diff)/BANK:.6f}'))
 write_csv(c/'bank00_pairwise.csv',['a','b','different_bytes','equal_bytes','identity'],rows)
 da,db=data['KR-REV-0'],data['USA-EUROPE-REV-0'];spans=[];i=0
 while i<BANK:
  if da[i]==db[i]:i+=1;continue
  s=i
  while i<BANK and da[i]!=db[i]:i+=1
  spans.append((f'0x{s:04X}',f'0x{i-1:04X}',i-s))
 write_csv(c/'kr_vs_usa_bank00_diff_spans.csv',['start','end','length'],spans)
 jp=sum(x!=y for x,y in zip(data['JP-REV-0'],data['JP-REV-A']))
 kr=sum(x!=y for x,y in zip(da,db))
 (c/'README.md').write_text(f'''# Gold Bank 00 Cross-Version Survey\n\n- Korean vs USA/Europe differing bytes: {kr:,} / {BANK:,}\n- Korean vs USA/Europe changed spans: {len(spans):,}\n- JP Rev 0 vs Rev A differing bytes: {jp:,} / {BANK:,}\n\nExact ROM payload bytes are not stored here; the CSVs record structural comparison facts only.\n''',encoding='utf-8')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('source_dir',type=Path);ap.add_argument('out_dir',type=Path);ap.add_argument('--survey-tool',type=Path,default=Path(__file__).with_name('survey_rom_structure.py'));a=ap.parse_args()
 out=a.out_dir;out.mkdir(parents=True,exist_ok=True)
 for label,(fn,region,rev) in ROMS.items():
  rom=a.source_dir/fn
  if not rom.exists(): raise SystemExit(f'missing source ROM: {rom}')
  dest=out/f'GENERATION-II/GOLD/{region}/{rev}/analysis/structure-phase1'
  subprocess.run([sys.executable,str(a.survey_tool),str(rom),str(dest),'--label',label],check=True)
 cross(a.source_dir,out)
 multi=out/'GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/structure-phase1'; multi.mkdir(parents=True,exist_ok=True)
 (multi/'PRET-CROSS-REFERENCE.md').write_text('''# pret/pokegold semantic cross-reference\n\nReference repository: `pret/pokegold` (public disassembly), used only as a semantic cross-check.\n\nConfirmed vector semantics used by this corpus:\n\n- `$0008`: `FarCall`\n- `$0010`: `Bankswitch`\n- `$0028`: `JumpTable`\n- `$0040`: VBlank interrupt vector\n- `$0048`: LCD interrupt vector\n- `$0058`: Serial interrupt vector\n- `$0060`: Joypad interrupt vector\n- `$0100`: cartridge entry point (`Start`), which reaches `_Start`\n\nAddresses beyond these stable vector semantics are **not** copied from the upstream English disassembly into the Korean map without ROM-local evidence.\n''',encoding='utf-8')
 # Preserve the exact generators/validators used for this corpus.
 tools=multi/'tools'; tools.mkdir(parents=True,exist_ok=True)
 import shutil
 shutil.copy2(Path(__file__), tools/'build_structure_phase1.py')
 shutil.copy2(a.survey_tool, tools/'survey_rom_structure.py')
 verifier=Path(__file__).with_name('verify_structure_phase1.py')
 if verifier.exists(): shutil.copy2(verifier, tools/'verify_structure_phase1.py')

 (multi/'README.md').write_text('''# Gold Structural Survey — Phase 1\n\nThis layer starts converting the whole-ROM reproducible corpus into classified source material. It does not redistribute ROM images.\n\nPer ROM it records a control-flow-derived candidate disassembly for fixed Bank 00, symbol candidates, coverage ranges, header constants, entropy map, long zero/FF runs, pointer-table candidates, immediate-address candidates, and a machine-readable manifest.\n\n`fixed_bank_cfg.asm` intentionally covers only instructions reachable from reset/RST/interrupt entry points via direct control flow. Unvisited bytes remain unclassified rather than being falsely treated as code.\n''',encoding='utf-8')
 # global manifest last
 files=[]
 for p in sorted(out.rglob('*')):
  if p.is_file(): files.append({'path':p.relative_to(out).as_posix(),'size':p.stat().st_size,'sha256':sha256(p)})
 (multi/'PHASE1-MANIFEST.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
 print(json.dumps({'files':len(files)+1,'roms':len(ROMS)},ensure_ascii=False))
if __name__=='__main__':main()
