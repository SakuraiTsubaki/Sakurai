#!/usr/bin/env python3
"""Pokémon LeafGreen multi-ROM full-image census.

Reads local .gba inputs and emits only derived metadata/candidate inventories.
No source ROM is copied to output.
"""
from __future__ import annotations
import argparse,csv,gzip,hashlib,math,struct,zlib
from collections import Counter
from pathlib import Path

BLOCK=0x4000; ENT_BLOCK=0x10000

def sha(b): return hashlib.sha256(b).hexdigest()
def code(b): return b[0xAC:0xB0].decode('ascii','replace')
def entropy(b):
 c=Counter(b);n=len(b);return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0.0

def write_csv(path,rows):
 rows=list(rows)
 with path.open('w',newline='',encoding='utf-8') as f:
  if not rows:return
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def diff_runs(a,b):
 i=0;n=len(a)
 while i<n:
  if a[i]==b[i]:i+=1;continue
  s=i
  while i<n and a[i]!=b[i]:i+=1
  yield s,i-s

def ptr_tables(b):
 n=len(b);i=0
 def ok(v):
  v&=~1;return 0x08000000<=v<0x08000000+n
 while i<=n-4:
  v=struct.unpack_from('<I',b,i)[0]
  if not ok(v):i+=4;continue
  s=i;vals=[]
  while i<=n-4:
   v=struct.unpack_from('<I',b,i)[0]
   if not ok(v):break
   vals.append(v);i+=4
  if len(vals)>=4:
   tg=[(x&~1)-0x08000000 for x in vals]
   yield s,len(vals),min(tg),max(tg),len(set(tg)),sum(x&1 for x in vals)

def try_lz(b,off):
 n=len(b);size=b[off+1]|b[off+2]<<8|b[off+3]<<16
 if not 16<=size<=0x200000:return None
 src=off+4;out=0
 while out<size:
  if src>=n:return None
  flags=b[src];src+=1
  for bit in range(8):
   if out>=size:break
   if flags&(0x80>>bit):
    if src+2>n:return None
    v=b[src]<<8|b[src+1];src+=2;ln=(v>>12)+3;disp=(v&0xfff)+1
    if disp>out:return None
    out+=ln
   else:
    if src>=n:return None
    src+=1;out+=1
   if out>size+18:return None
 return size,src-off

def lz_candidates(b):
 for off in range(0,len(b)-4,4):
  if b[off]==0x10:
   r=try_lz(b,off)
   if r:yield off,*r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom_dir',type=Path);ap.add_argument('out_dir',type=Path);a=ap.parse_args()
 a.out_dir.mkdir(parents=True,exist_ok=True)
 paths=sorted(a.rom_dir.glob('*.gba'));data={p.name:p.read_bytes() for p in paths}
 if not data:raise SystemExit('no .gba files')
 meta=[];coverage=[];ent=[];ptr=[];lz=[]
 for name,b in data.items():
  c=code(b);meta.append({'file':name,'game_code':c,'size':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'})
  for idx,s in enumerate(range(0,len(b),BLOCK)):
   x=b[s:s+BLOCK];coverage.append({'file':name,'game_code':c,'block_index':idx,'start':f'0x{s:07X}','sha256':sha(x),'ff':x.count(255),'zero':x.count(0),'entropy':round(entropy(x),6)})
  for idx,s in enumerate(range(0,len(b),ENT_BLOCK)):
   x=b[s:s+ENT_BLOCK];ent.append({'file':name,'game_code':c,'block_index':idx,'start':f'0x{s:07X}','entropy':round(entropy(x),6),'ff_percent':round(x.count(255)*100/len(x),4),'zero_percent':round(x.count(0)*100/len(x),4)})
  for s,n,t0,t1,u,th in ptr_tables(b):ptr.append({'file':name,'game_code':c,'start':f'0x{s:07X}','count':n,'target_min':f'0x{t0:07X}','target_max':f'0x{t1:07X}','unique_targets':u,'thumb_bits':th})
  for s,d,comp in lz_candidates(b):lz.append({'file':name,'game_code':c,'start':f'0x{s:07X}','decompressed_size':d,'compressed_bytes':comp,'ratio':round(comp/d,5)})
 write_csv(a.out_dir/'roms.csv',meta);write_csv(a.out_dir/'coverage_16k.csv',coverage);write_csv(a.out_dir/'entropy_64k.csv',ent);write_csv(a.out_dir/'pointer_tables.csv',ptr);write_csv(a.out_dir/'lz77_candidates.csv',lz)
 base_name=next(n for n,b in data.items() if code(b)=='BPGE' and b[0xBC]==0);base=data[base_name]
 for name,b in data.items():
  if name==base_name:continue
  out=a.out_dir/f'diff_rle_{code(b)}_{b[0xBC]}_{hashlib.sha1(name.encode()).hexdigest()[:8]}.txt.gz'
  prev=0
  with gzip.open(out,'wt',encoding='ascii',compresslevel=6) as f:
   f.write(f'# baseline={base_name}\n# other={name}\n# format=gap_from_previous_end:length\n')
   for s,L in diff_runs(base,b):f.write(f'{s-prev}:{L}\n');prev=s+L

if __name__=='__main__':main()
