#!/usr/bin/env python3
"""Extract Emerald ability names and localized descriptions for all six unique releases."""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
from emerald_text import decode,read_terminated
COUNT=78

def sha1(b):return hashlib.sha1(b).hexdigest()
def load(ref,romdir):
 d=(romdir/ref['source_filename']).read_bytes()
 if sha1(d)!=ref['sha1']:raise ValueError(f"SHA-1 mismatch: {ref['id']}")
 return d

def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom_dir',type=Path);ap.add_argument('--manifest',type=Path,default=Path('manifests/roms.json'))
 ap.add_argument('--headers',type=Path,default=Path('analysis/gf_rom_headers.json'));ap.add_argument('--out-dir',type=Path,default=Path('text/abilities'));a=ap.parse_args()
 refs={r['id']:r for r in json.loads(a.manifest.read_text())['references']};headers=json.loads(a.headers.read_text())['records'];a.out_dir.mkdir(parents=True,exist_ok=True);meta=[]
 for h in headers:
  rid=h['id'];jp=rid=='JPN';d=load(refs[rid],a.rom_dir);name_w=8 if jp else 13;nr=h['abilityNames_rom_offset'];dr=h['abilityDescriptions_rom_offset'];rows=[];unknown=[]
  jpn_cursor=dr
  for i in range(COUNT):
   nraw=d[nr+i*name_w:nr+(i+1)*name_w];name,u=decode(nraw,jp,rid);unknown+=u
   if jp:
    draw=read_terminated(d,jpn_cursor);doff=jpn_cursor;jpn_cursor+=len(draw)
   else:
    ptr=int.from_bytes(d[dr+i*4:dr+i*4+4],'little');doff=ptr-0x08000000;draw=read_terminated(d,doff)
   desc,u=decode(draw,jp,rid);unknown+=u
   rows.append({'ability_id':i,'name':name,'name_raw_hex':nraw.hex().upper(),'description_rom_offset':f'0x{doff:08X}','description':desc,'description_raw_hex':draw.hex().upper()})
  with (a.out_dir/f'{rid.lower()}.csv').open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  meta.append({'release':rid,'ability_name_root':f'0x{nr:08X}','ability_name_width':name_w,'description_root':f'0x{dr:08X}',
   'description_storage':'concatenated_eos_strings' if jp else 'pointer_table','unknown_decoded_byte_count':len(unknown),'unknown_decoded_bytes':sorted(set(unknown))})
 (a.out_dir/'manifest.json').write_text(json.dumps({'schema_version':1,'record_count':COUNT,'releases':meta},indent=2)+'\n')
if __name__=='__main__':main()
