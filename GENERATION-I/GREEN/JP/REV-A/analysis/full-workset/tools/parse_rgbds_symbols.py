#!/usr/bin/env python3
"""Parse RGBDS .map/.sym artifacts and build ROM-address cross-references."""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import argparse,csv,re
BANK_SIZE=0x4000
MAP_HEADING=re.compile(r"^(ROM0|ROMX|VRAM|SRAM|WRAM0|WRAMX|HRAM)(?: bank #([0-9]+))?:$")
SECTION_RANGE=re.compile(r'^\s*SECTION:\s*\$([0-9a-fA-F]+)-\$([0-9a-fA-F]+)\s*\(\$([0-9a-fA-F]+) bytes\)\s*\["(.*)"\]\s*$')
SECTION_ZERO=re.compile(r'^\s*SECTION:\s*\$([0-9a-fA-F]+)\s*\(\$([0-9a-fA-F]+) bytes\)\s*\["(.*)"\]\s*$')
SYM_LINE=re.compile(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(.+?)\s*$")
def rom_file_offset(bank,addr):
 if addr<0x4000 and bank==0:return addr
 if 0x4000<=addr<0x8000 and bank>0:return bank*BANK_SIZE+(addr-0x4000)
def infer_domain(a):
 if a<0x8000:return 'ROM'
 if a<0xA000:return 'VRAM'
 if a<0xC000:return 'SRAM'
 if a<0xE000:return 'WRAM'
 if a<0xFE00:return 'ECHO'
 if a<0xFEA0:return 'OAM'
 if a<0xFF00:return 'UNUSABLE'
 if a<0xFF80:return 'IO'
 if a<0xFFFF:return 'HRAM'
 return 'IE'
def parse_map(path):
 rows=[];domain=None;bank=0
 for n,line in enumerate(Path(path).read_text(encoding='utf-8',errors='replace').splitlines(),1):
  m=MAP_HEADING.match(line.strip())
  if m:domain=m.group(1);bank=int(m.group(2) or 0);continue
  m=SECTION_RANGE.match(line)
  if m:start,end,size,name=int(m.group(1),16),int(m.group(2),16),int(m.group(3),16),m.group(4)
  else:
   m=SECTION_ZERO.match(line)
   if not m:continue
   start,size,name=int(m.group(1),16),int(m.group(2),16),m.group(3);end=start+max(size-1,0)
  if domain is None:continue
  fs=rom_file_offset(bank,start) if domain in ('ROM0','ROMX') else None;fe=fs+size-1 if fs is not None and size else fs
  rows.append({'domain':domain,'bank':f'{bank:02X}','cpu_start':f'0x{start:04X}','cpu_end':f'0x{end:04X}','size':size,'section':name,'file_offset_start':f'0x{fs:05X}' if fs is not None else '','file_offset_end':f'0x{fe:05X}' if fe is not None else '','source_line':n})
 return rows
def parse_sym(path):
 rows=[]
 for n,line in enumerate(Path(path).read_text(encoding='utf-8',errors='replace').splitlines(),1):
  if not line or line.startswith(';'):continue
  m=SYM_LINE.match(line)
  if not m:continue
  bank=int(m.group(1),16);addr=int(m.group(2),16);name=m.group(3);domain=infer_domain(addr);off=rom_file_offset(bank,addr) if domain=='ROM' else None
  rows.append({'domain':domain,'bank':f'{bank:02X}','address':f'0x{addr:04X}','name':name,'file_offset':f'0x{off:05X}' if off is not None else '','source_line':n})
 return rows
def write(path,rows):
 rows=list(rows);Path(path).parent.mkdir(parents=True,exist_ok=True)
 with Path(path).open('w',newline='',encoding='utf-8') as f:
  if rows:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def section_at(ss,o):
 for s in ss:
  if s['file_offset_start'] and int(s['file_offset_start'],16)<=o<=int(s['file_offset_end'],16):return s['section']
 return ''
def symbol_diff(a,b):
 def locs(rows):
  d=defaultdict(list)
  for r in rows:d[r['name']].append((r['domain'],r['bank'],r['address'],r['file_offset']))
  return d
 A,B=locs(a),locs(b);out=[]
 for name in sorted(set(A)|set(B)):
  x,y=sorted(A.get(name,[])),sorted(B.get(name,[]));status='same' if x==y else 'removed' if not y else 'added' if not x else 'moved_or_redefined'
  out.append({'name':name,'status':status,'rev0_locations':'; '.join('/'.join(q) for q in x),'reva_locations':'; '.join('/'.join(q) for q in y)})
 return out
def section_diff(a,b):
 def collect(rows):
  d=defaultdict(list)
  for r in rows:d[(r['domain'],r['section'])].append(r)
  return d
 A,B=collect(a),collect(b);out=[]
 for k in sorted(set(A)|set(B)):
  x,y=A.get(k,[]),B.get(k,[]);norm=lambda z:[(r['bank'],r['cpu_start'],r['cpu_end'],r['size']) for r in z];fmt=lambda z:'; '.join(f"{r['bank']}:{r['cpu_start']}-{r['cpu_end']}/{r['size']}" for r in z);status='same' if norm(x)==norm(y) else 'removed' if not y else 'added' if not x else 'moved_or_resized'
  out.append({'domain':k[0],'section':k[1],'status':status,'rev0_ranges':fmt(x),'reva_ranges':fmt(y)})
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rev0-map',required=True);ap.add_argument('--rev0-sym',required=True);ap.add_argument('--reva-map',required=True);ap.add_argument('--reva-sym',required=True);ap.add_argument('--outdir',type=Path,required=True);a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
 s0,s1=parse_map(a.rev0_map),parse_map(a.reva_map);y0,y1=parse_sym(a.rev0_sym),parse_sym(a.reva_sym)
 for n,r in [('rev0_sections.csv',s0),('reva_sections.csv',s1),('rev0_symbols.csv',y0),('reva_symbols.csv',y1),('section_diff.csv',section_diff(s0,s1)),('symbol_diff.csv',symbol_diff(y0,y1))]:write(a.outdir/n,r)
 idx=[]
 for rev,ys,ss in [('REV-0',y0,s0),('REV-A',y1,s1)]:
  for r in ys:idx.append({'revision':rev,**r,'section':section_at(ss,int(r['file_offset'],16)) if r['file_offset'] else ''})
 write(a.outdir/'symbol_section_index.csv',idx);print(f'REV-0: {len(s0)} sections, {len(y0)} symbols\nREV-A: {len(s1)} sections, {len(y1)} symbols')
if __name__=='__main__':main()
