#!/usr/bin/env python3
"""Generate a ROM-free, byte-exact reproducibility corpus for Pokémon Blue/Ao.

Input ROMs stay local. Outputs are metadata, CSV maps, source scaffolds, and tools.
No ROM image or extracted bank binary is written into the distributable tree.
"""
from __future__ import annotations
import argparse, csv, hashlib, itertools, json, math, os, zlib
from collections import Counter, defaultdict
from pathlib import Path

BANK=0x4000
PREFIX=Path('GENERATION-I')/'BLUE'
TARGETS=[
 {'code':'JP','language_region':'JAPANESE-JAPAN','revision':'REV-0','sha256':'71a70e5f77c109177d21c998310ffe01a68e8cd2f41e72e7129093b890c7d3d1','size':524288,'reference_filename':'Pocket Monsters - Ao (Japan) (SGB Enhanced).gb'},
 {'code':'EN','language_region':'ENGLISH-USA-EUROPE','revision':'REV-0','sha256':'2a951313c2640e8c2cb21f25d1db019ae6245d9c7121f754fa61afd7bee6452d','size':1048576,'reference_filename':'Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb'},
 {'code':'DE','language_region':'GERMAN-GERMANY','revision':'REV-0','sha256':'2cfec2223090dc9f544aa36c99c48801be5018757a1366b88d8f40739541458e','size':1048576,'reference_filename':'Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb'},
 {'code':'FR','language_region':'FRENCH-FRANCE','revision':'REV-0','sha256':'73dee67befed0c39cd0a6ed53a98ff5b98b3bddc3e7a0dae1d982776a4d0889b','size':1048576,'reference_filename':'Pokemon - Version Bleue (France) (SGB Enhanced).gb'},
 {'code':'IT','language_region':'ITALIAN-ITALY','revision':'REV-0','sha256':'e197c7535135a516fe9bf92cf7821c9f72926bf90fce3a2a5742d1b0b6a0564b','size':1048576,'reference_filename':'Pokemon - Versione Blu (Italy) (SGB Enhanced).gb'},
 {'code':'ES','language_region':'SPANISH-SPAIN','revision':'REV-0','sha256':'31317f74fed2935dfc5fbb6ada766cf8515949c85c6c6e8d32d0f752b85b8f9e','size':1048576,'reference_filename':'Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb'},
]
CART={0x03:'MBC1+RAM+BATTERY',0x13:'MBC3+RAM+BATTERY',0x1B:'MBC5+RAM+BATTERY'}

def digest(d,n): return hashlib.new(n,d).hexdigest()
def ent(d):
 c=Counter(d); n=len(d); return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0.0
def hdr(d):
 x=0
 for b in d[0x134:0x14D]: x=(x-b-1)&255
 return x
def glob(d): return (sum(d)-d[0x14E]-d[0x14F])&0xffff
def tail(d,v):
 i=len(d)
 while i and d[i-1]==v:i-=1
 return len(d)-i

def write_csv(p,rows,fields):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def discover(rom_dir):
 need={t['sha256']:t for t in TARGETS}; found={}
 for p in rom_dir.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in {'.gb','.gbc'}: continue
  d=p.read_bytes(); h=hashlib.sha256(d).hexdigest()
  if h in need: found[h]=p
 miss=[t for t in TARGETS if t['sha256'] not in found]
 if miss: raise SystemExit('Missing ROMs:\n'+'\n'.join('  '+t['reference_filename'] for t in miss))
 return found

def fill_runs(d,min_len=256):
 i=0
 while i<len(d):
  v=d[i]
  if v not in (0,255): i+=1; continue
  j=i+1
  while j<len(d) and d[j]==v:j+=1
  if j-i>=min_len: yield i,j,j-i,v
  i=j

def layout(bank_count):
 lines=['; byte-exact physical-bank scaffold; local baserom.gb required','']
 for b in range(bank_count):
  off=b*BANK
  if b==0: lines += [f'SECTION "bank {b:02X}", ROM0[$0000]',f'    INCBIN "baserom.gb", ${off:06X}, $4000','']
  else: lines += [f'SECTION "bank {b:02X}", ROMX[$4000], BANK[${b:02X}]',f'    INCBIN "baserom.gb", ${off:06X}, $4000','']
 return '\n'.join(lines)+'\n'

def shared_runs(data,codes,min_len=16):
 n=min(len(data[c]) for c in codes); out=[]; i=0
 while i<n:
  v=data[codes[0]][i]
  if not all(data[c][i]==v for c in codes[1:]): i+=1; continue
  j=i+1
  while j<n:
   vv=data[codes[0]][j]
   if not all(data[c][j]==vv for c in codes[1:]): break
   j+=1
  if j-i>=min_len:
   out.append({'codes':'+'.join(codes),'offset_start':i,'offset_start_hex':f'0x{i:06X}','offset_end_exclusive':j,'offset_end_exclusive_hex':f'0x{j:06X}','length_bytes':j-i,'start_bank_hex':f'0x{i//BANK:02X}','end_bank_hex':f'0x{(j-1)//BANK:02X}','crosses_bank_boundary':i//BANK!=(j-1)//BANK})
  i=j
 return out

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('rom_dir',type=Path); ap.add_argument('out_root',type=Path); a=ap.parse_args()
 found=discover(a.rom_dir); data={}; manifests=[]; allbanks=[]; allfills=[]
 for t in TARGETS:
  p=found[t['sha256']]; d=p.read_bytes(); data[t['code']]=d
  title=d[0x134:0x144].rstrip(b'\0').decode('ascii','replace')
  m={'code':t['code'],'language_region':t['language_region'],'revision':t['revision'],'source_filename_reference':t['reference_filename'],'matched_local_filename':p.name,'rom_binary_included':False,'size_bytes':len(d),'bank_count':len(d)//BANK,'title':title,'cartridge_type_code':f'0x{d[0x147]:02X}','cartridge_type':CART.get(d[0x147],f'0x{d[0x147]:02X}'),'version':d[0x14C],'header_checksum_valid':d[0x14D]==hdr(d),'global_checksum_valid':int.from_bytes(d[0x14E:0x150],"big")==glob(d),'md5':digest(d,'md5'),'sha1':digest(d,'sha1'),'sha256':digest(d,'sha256'),'crc32':f'{zlib.crc32(d)&0xffffffff:08x}'}
  manifests.append(m)
  td=a.out_root/PREFIX/t['language_region']/t['revision']/'ANALYSIS'/'reproducibility'; td.mkdir(parents=True,exist_ok=True)
  (td/'manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
  (td/'expected.sha256').write_text(t['sha256']+'  baserom.gb\n',encoding='utf-8')
  (td/'layout.asm').write_text(layout(len(d)//BANK),encoding='utf-8')
  banks=[]
  for b in range(len(d)//BANK):
   q=d[b*BANK:(b+1)*BANK]; r={'rom_code':t['code'],'bank':b,'bank_hex':f'0x{b:02X}','offset_start_hex':f'0x{b*BANK:06X}','offset_end_exclusive_hex':f'0x{(b+1)*BANK:06X}','sha256':digest(q,'sha256'),'crc32':f'{zlib.crc32(q)&0xffffffff:08x}','entropy_bits_per_byte':f'{ent(q):.6f}','unique_byte_values':len(set(q)),'zero_bytes':q.count(0),'ff_bytes':q.count(255),'trailing_zero_bytes':tail(q,0),'trailing_ff_bytes':tail(q,255),'all_zero':all(x==0 for x in q),'all_ff':all(x==255 for x in q)}; banks.append(r); allbanks.append(r)
  write_csv(td/'bank_manifest.csv',banks,list(banks[0]))
  fills=[]
  for s,e,l,v in fill_runs(d):
   r={'rom_code':t['code'],'fill_byte':f'0x{v:02X}','offset_start_hex':f'0x{s:06X}','offset_end_exclusive_hex':f'0x{e:06X}','length_bytes':l,'start_bank_hex':f'0x{s//BANK:02X}','end_bank_hex':f'0x{(e-1)//BANK:02X}','classification':'ENTIRE_BANK_OR_LARGER_BLANK' if l>=BANK and s%BANK==0 else ('TRAILING_PADDING_CANDIDATE' if e%BANK==0 else 'FILL_RUN_CANDIDATE')}; fills.append(r); allfills.append(r)
  write_csv(td/'fill_run_candidates.csv',fills,list(fills[0]) if fills else ['rom_code','fill_byte','offset_start_hex','offset_end_exclusive_hex','length_bytes','start_bank_hex','end_bank_hex','classification'])
  (td/'rom_identity.md').write_text(f"# ROM identity — {t['code']}\n\n- Language/region: `{t['language_region']}`\n- Revision: `{t['revision']}`\n- Size: {len(d)} bytes\n- Banks: {len(d)//BANK}\n- Mapper: {m['cartridge_type']}\n- MD5: `{m['md5']}`\n- SHA-1: `{m['sha1']}`\n- SHA-256: `{m['sha256']}`\n- CRC32: `{m['crc32']}`\n- Header checksum: {'OK' if m['header_checksum_valid'] else 'FAIL'}\n- Global checksum: {'OK' if m['global_checksum_valid'] else 'FAIL'}\n\nROM bytes are intentionally excluded.\n",encoding='utf-8')

 cross=a.out_root/PREFIX/'ALL-REGIONS'/'REV-0'/'ANALYSIS'/'reproducibility'; cross.mkdir(parents=True,exist_ok=True)
 (cross/'rom_manifest.json').write_text(json.dumps(manifests,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 write_csv(cross/'bank_manifest.csv',allbanks,list(allbanks[0]))
 write_csv(cross/'fill_run_candidates.csv',allfills,list(allfills[0]))
 pairs=[]
 for ca,cb in itertools.combinations([t['code'] for t in TARGETS],2):
  da,db=data[ca],data[cb]
  for b in range(min(len(da),len(db))//BANK):
   x=da[b*BANK:(b+1)*BANK]; y=db[b*BANK:(b+1)*BANK]; diff=sum(a!=b for a,b in zip(x,y)); pairs.append({'rom_a':ca,'rom_b':cb,'bank_hex':f'0x{b:02X}','different_bytes':diff,'same_bytes':BANK-diff,'similarity_ratio':f'{(BANK-diff)/BANK:.8f}','identical':diff==0})
 write_csv(cross/'pairwise_bank_diff.csv',pairs,list(pairs[0]))
 groups=[]
 for b in range(max(len(d) for d in data.values())//BANK):
  g=defaultdict(list)
  for c,d in data.items():
   if (b+1)*BANK<=len(d): g[digest(d[b*BANK:(b+1)*BANK],'sha256')].append(c)
  for sha,codes in g.items():
   if len(codes)>=2: groups.append({'bank_hex':f'0x{b:02X}','rom_codes':'+'.join(sorted(codes)),'rom_count':len(codes),'sha256':sha})
 write_csv(cross/'identical_bank_groups.csv',groups,list(groups[0]))
 wr=shared_runs(data,['EN','DE','FR','IT','ES']); ar=shared_runs(data,['JP','EN','DE','FR','IT','ES'])
 write_csv(cross/'western_shared_byte_runs_ge16.csv',wr,list(wr[0])); write_csv(cross/'all6_shared_byte_runs_ge16.csv',ar,list(ar[0]))
 fs=[]
 for t in TARGETS:
  c=t['code']; blank=[r for r in allbanks if r['rom_code']==c and r['all_zero'] is True]
  fs.append({'rom_code':c,'entire_zero_banks':len(blank),'bank_list':' '.join(r['bank_hex'] for r in blank),'entire_zero_bytes':len(blank)*BANK})
 write_csv(cross/'free_space_summary.csv',fs,list(fs[0]))
 (cross/'README.md').write_text('# Pokémon Blue/Ao full-ROM reproducibility corpus\n\nPhysical ROM layer, cross-version alignment, free/fill candidates, and byte-exact INCBIN scaffolds. ROM binaries are not included.\n\nAll outputs are regenerated from exact SHA-256-matched local inputs using `generate_blue_reproducibility.py`.\n',encoding='utf-8')
 print('generated',a.out_root/PREFIX)
if __name__=='__main__': main()
