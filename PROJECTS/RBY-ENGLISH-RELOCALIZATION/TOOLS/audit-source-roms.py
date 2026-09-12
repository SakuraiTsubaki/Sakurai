#!/usr/bin/env python3
"""Reproduce the RBY source-ROM audit without committing ROM bytes.

Usage:
  python audit-source-roms.py ROM_DIR OUTPUT_DIR

Expected filenames are recorded in SOURCES. Generated output is metadata only.
Long 00/FF runs are candidates, never proof of safe free space.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math,collections
BANK=0x4000
SOURCES=[
('RED','JP-JA-HV0','Pocket Monsters - Aka (Japan) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('RED','JP-JA-HV1','Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('GREEN','JP-JA-HV0','Pocket Monsters - Midori (Japan) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('GREEN','JP-JA-HV1','Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('BLUE','JP-JA-HV0','Pocket Monsters - Ao (Japan) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('YELLOW','JP-JA-HV0','Pocket Monsters - Pikachu (Japan) (Rev 0A) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('YELLOW','JP-JA-HV1','Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('YELLOW','JP-JA-HV2','Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('YELLOW','JP-JA-HV3','Pocket Monsters - Pikachu (Japan) (Rev D) (SGB Enhanced).gb',['TRANSLATION-ORIGINAL','BUILD-BASE']),
('RED','US-EU-EN-HV0','Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb',['IMPLEMENTATION-REFERENCE']),
('BLUE','US-EU-EN-HV0','Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb',['IMPLEMENTATION-REFERENCE']),
('YELLOW','US-EU-EN-HV0','Pokemon - Yellow Version (USA, Europe).gbc',['IMPLEMENTATION-REFERENCE']),
]
PAIRS=[
('RED','JP-JA-HV0','JP-JA-HV1','REVISION'),('GREEN','JP-JA-HV0','JP-JA-HV1','REVISION'),
('YELLOW','JP-JA-HV0','JP-JA-HV1','REVISION'),('YELLOW','JP-JA-HV1','JP-JA-HV2','REVISION'),('YELLOW','JP-JA-HV2','JP-JA-HV3','REVISION'),('YELLOW','JP-JA-HV0','JP-JA-HV3','REVISION-SPAN'),
('RED','JP-JA-HV0','US-EU-EN-HV0','IMPLEMENTATION-COMPARE'),('BLUE','JP-JA-HV0','US-EU-EN-HV0','IMPLEMENTATION-COMPARE'),('YELLOW','JP-JA-HV3','US-EU-EN-HV0','IMPLEMENTATION-COMPARE')]
def digest(d,n):return hashlib.new(n,d).hexdigest()
def entropy(d):
 c=collections.Counter(d);n=len(d);return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0
def hchk(d):
 x=0
 for b in d[0x134:0x14D]:x=(x-b-1)&255
 return x==d[0x14D]
def gchk(d):return ((sum(d)-d[0x14E]-d[0x14F])&0xffff)==((d[0x14E]<<8)|d[0x14F])
def writecsv(path,rows):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
def runs(d,minlen=256):
 for val in (0,255):
  i=0
  while i<len(d):
   if d[i]!=val:i+=1;continue
   j=i+1
   while j<len(d) and d[j]==val:j+=1
   if j-i>=minlen:yield i,j,val
   i=j
def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom_dir',type=Path);ap.add_argument('output_dir',type=Path);a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 inv=[];banks=[];pads=[];data={}
 for game,rid,fn,roles in SOURCES:
  p=a.rom_dir/fn;d=p.read_bytes();data[(game,rid)]=d
  inv.append({'game_id':game,'release_id':rid,'filename_local':fn,'roles':';'.join(roles),'size_bytes':len(d),'bank_count_16k':len(d)//BANK,'header_version':d[0x14c],'header_checksum_ok':hchk(d),'global_checksum_ok':gchk(d),'sha1':digest(d,'sha1'),'sha256':digest(d,'sha256')})
  for b in range(len(d)//BANK):
   x=d[b*BANK:(b+1)*BANK];banks.append({'game_id':game,'release_id':rid,'bank':f'{b:02X}','offset_start':f'0x{b*BANK:06X}','sha256':digest(x,'sha256'),'entropy_bits_per_byte':round(entropy(x),6)})
  for i,j,val in runs(d):
   pos=i
   while pos<j:
    bank=pos//BANK;end=min(j,(bank+1)*BANK)
    if end-pos>=256:pads.append({'game_id':game,'release_id':rid,'bank':f'{bank:02X}','rom_offset_start':f'0x{pos:06X}','rom_offset_end_exclusive':f'0x{end:06X}','length':end-pos,'fill_byte':f'0x{val:02X}','status':'UNVERIFIED-PADDING-CANDIDATE'})
    pos=end
 diffs=[];bdiffs=[]
 for game,ra,rb,kind in PAIRS:
  x=data[(game,ra)];y=data[(game,rb)];n=min(len(x),len(y));idx=[i for i in range(n) if x[i]!=y[i]];changed=sorted({i//BANK for i in idx})
  diffs.append({'game_id':game,'compare_type':kind,'base_release_id':ra,'other_release_id':rb,'base_size':len(x),'other_size':len(y),'overlap_bytes':n,'different_bytes_in_overlap':len(idx),'difference_percent_overlap':round(len(idx)*100/n,6),'changed_bank_count':len(changed),'changed_banks_hex':';'.join(f'{b:02X}' for b in changed),'size_delta':len(y)-len(x)})
  for b in range((n+BANK-1)//BANK):
   xa=x[b*BANK:min((b+1)*BANK,n)];ya=y[b*BANK:min((b+1)*BANK,n)];cnt=sum(a!=b for a,b in zip(xa,ya));bdiffs.append({'game_id':game,'compare_type':kind,'base_release_id':ra,'other_release_id':rb,'bank':f'{b:02X}','different_bytes':cnt,'bank_overlap_bytes':len(xa),'difference_percent':round(cnt*100/len(xa),6),'identical':cnt==0})
 writecsv(a.output_dir/'rom-inventory.csv',inv);writecsv(a.output_dir/'bank-fingerprints.csv',banks);writecsv(a.output_dir/'padding-candidates.csv',pads);writecsv(a.output_dir/'comparison-summary.csv',diffs);writecsv(a.output_dir/'bank-comparison.csv',bdiffs)
 (a.output_dir/'audit-manifest.json').write_text(json.dumps({'schema':'rby-source-rom-audit-v4','bank_size':BANK,'rom_binary_policy':'Original ROM binaries remain local/read-only and are not committed.','releases':inv,'notes':['00/FF runs are unverified padding candidates, not safe-space proof.']},indent=2),encoding='utf-8')
if __name__=='__main__':main()
