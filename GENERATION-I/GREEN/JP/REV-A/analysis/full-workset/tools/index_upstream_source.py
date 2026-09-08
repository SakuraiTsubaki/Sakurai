#!/usr/bin/env python3
"""Index a pinned pokegreen checkout into reproducible file and dependency manifests."""
from pathlib import Path
import argparse,csv,hashlib,re
INCLUDE_RE=re.compile(r'^\s*(INCLUDE|INCBIN)\s+["\']([^"\']+)["\']',re.I)
SKIP_DIRS={'.git','__pycache__','symbols'};BUILD_SUFFIXES={'.o','.gb','.gbc','.map','.sym','.patch'}
def category(rel):
 top=rel.parts[0] if len(rel.parts)>1 else ''
 if top in {'audio','constants','data','engine','gfx','home','macros','maps','ram','scripts','text','tools','vc','garbage'}:return top
 if rel.suffix.lower() in {'.asm','.inc'}:return 'top-level-source'
 if rel.suffix.lower() in {'.md','.txt'}:return 'documentation'
 return 'project/build-metadata'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('outdir',type=Path);a=ap.parse_args();src=a.source.resolve();out=a.outdir;out.mkdir(parents=True,exist_ok=True);files=[];edges=[]
 for p in sorted(src.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(src)
  if any(x in SKIP_DIRS for x in rel.parts) or p.suffix.lower() in BUILD_SUFFIXES:continue
  raw=p.read_bytes();text=b'\0' not in raw;lines=raw.count(b'\n')+(1 if raw and not raw.endswith(b'\n') else 0) if text else ''
  files.append({'path':rel.as_posix(),'category':category(rel),'extension':p.suffix.lower(),'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'text':str(text),'lines':lines})
  if text and p.suffix.lower() in {'.asm','.inc','.mk',''}:
   for n,line in enumerate(raw.decode('utf-8','replace').splitlines(),1):
    m=INCLUDE_RE.match(line)
    if m:target=m.group(2);edges.append({'source':rel.as_posix(),'line':n,'directive':m.group(1).upper(),'target':target,'target_exists':str((src/target).exists())})
 def write(name,rows,fields):
  with (out/name).open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 write('source_files.csv',files,['path','category','extension','size','sha256','text','lines']);write('include_edges.csv',edges,['source','line','directive','target','target_exists']);counts={}
 for r in files:counts[r['category']]=counts.get(r['category'],0)+1
 with (out/'source_summary.csv').open('w',newline='',encoding='utf-8') as f:w=csv.writer(f);w.writerow(['category','files']);w.writerows(sorted(counts.items()));w.writerow(['TOTAL',len(files)])
 print(f"{len(files)} source/assets indexed; {len(edges)} INCLUDE/INCBIN edges; {sum(r['target_exists']=='False' for r in edges)} unresolved targets")
if __name__=='__main__':main()
