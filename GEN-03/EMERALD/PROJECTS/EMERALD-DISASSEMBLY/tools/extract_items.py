#!/usr/bin/env python3
"""Extract Emerald item core parameters and localized names/descriptions."""
from __future__ import annotations
import argparse,csv,gzip,hashlib,io,json
from pathlib import Path
from emerald_text import decode,read_terminated

COUNT=377

def sha1(b:bytes)->str:return hashlib.sha1(b).hexdigest()
def load(ref,rom_dir):
 d=(rom_dir/ref['source_filename']).read_bytes()
 if sha1(d)!=ref['sha1']:raise ValueError(f"SHA-1 mismatch: {ref['id']}")
 return d

def layout(rid): return (10,40) if rid=='JPN' else (14,44)
def core(i,b,n):
 o=n
 return {'slot_id':i,'item_id_field':int.from_bytes(b[o:o+2],'little'),'price':int.from_bytes(b[o+2:o+4],'little'),
 'hold_effect':b[o+4],'hold_effect_param':b[o+5],'importance':b[o+10],'registrability':b[o+11],
 'pocket':b[o+12],'type':b[o+13],'battle_usage':b[o+18],'secondary_id':b[o+26]}

def csv_bytes(rows, fields):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=fields);w.writeheader();w.writerows(rows);return s.getvalue().encode('utf-8')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('rom_dir',type=Path)
 ap.add_argument('--manifest',type=Path,default=Path('manifests/roms.json'));ap.add_argument('--headers',type=Path,default=Path('analysis/gf_rom_headers.json'))
 ap.add_argument('--data-out',type=Path,default=Path('data/items'));ap.add_argument('--text-out',type=Path,default=Path('text/items'));a=ap.parse_args()
 refs={r['id']:r for r in json.loads(a.manifest.read_text())['references']};headers=json.loads(a.headers.read_text())['records']
 a.data_out.mkdir(parents=True,exist_ok=True);a.text_out.mkdir(parents=True,exist_ok=True)
 canonical=None; release_meta=[]
 for h in headers:
  rid=h['id']; d=load(refs[rid],a.rom_dir); n,stride=layout(rid);root=h['items_rom_offset']; rows=[];cores=[];unknown=[]
  for i in range(COUNT):
   b=d[root+i*stride:root+(i+1)*stride]; c=core(i,b,n); cores.append(c)
   name_raw=b[:n];name,u=decode(name_raw,rid=='JPN',rid);unknown+=u
   desc_ptr=int.from_bytes(b[n+6:n+10],'little'); desc_off=desc_ptr-0x08000000; desc_raw=read_terminated(d,desc_off);desc,u=decode(desc_raw,rid=='JPN',rid);unknown+=u
   field=int.from_bytes(b[n+14:n+18],'little');battle=int.from_bytes(b[n+22:n+26],'little')
   rows.append({'slot_id':i,'name':name,'name_raw_hex':name_raw.hex().upper(),'description_rom_offset':f'0x{desc_off:08X}',
    'description':desc,'description_raw_hex':desc_raw.hex().upper(),'field_use_func':f'0x{field:08X}','battle_use_func':f'0x{battle:08X}'})
  if canonical is None: canonical=cores
  elif cores!=canonical: raise ValueError(f'item semantic core differs: {rid}')
  source=[{'slot_id':r['slot_id'],'name':r['name'],'description':r['description']} for r in rows]
  (a.text_out/f'{rid.lower()}_source.csv').write_bytes(csv_bytes(source,['slot_id','name','description']))
  raw=csv_bytes(rows,list(rows[0]))
  with (a.text_out/f'{rid.lower()}.full.csv.gz').open('wb') as outf:
   with gzip.GzipFile(filename='',mode='wb',fileobj=outf,mtime=0) as gz: gz.write(raw)
  release_meta.append({'release':rid,'root_rom_offset':f'0x{root:08X}','name_length':n,'record_stride':stride,
    'table_sha1':sha1(d[root:root+COUNT*stride]),'full_csv_sha1':sha1(raw),'unknown_decoded_byte_count':len(unknown),'unknown_decoded_bytes':sorted(set(unknown))})
 with (a.data_out/'items_core.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(canonical[0]));w.writeheader();w.writerows(canonical)
 norm=json.dumps(canonical,separators=(',',':'),sort_keys=True).encode()
 (a.data_out/'manifest.json').write_text(json.dumps({'schema_version':1,'record_count':COUNT,'all_unique_releases_semantic_core_identical':True,
   'normalized_core_sha1':sha1(norm),'localized_artifacts':{'source_suffix':'_source.csv','full_analysis_suffix':'.full.csv.gz'},
   'release_layouts':release_meta},indent=2)+'\n')
if __name__=='__main__':main()
