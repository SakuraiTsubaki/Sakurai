#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,math,pathlib,zlib
from collections import Counter
BANK=0x4000; PAGE=0x100
LOGO=bytes.fromhex('CEED6666CC0D000B03730083000C000D0008111F8889000EDCCC6EE6DDDDD999BBBB67636E0EECCCDDDC999FBBB9333E')
RAM={0:0,1:2048,2:8192,3:32768,4:131072,5:65536}
ROMSZ={0:32768,1:65536,2:131072,3:262144,4:524288,5:1048576,6:2097152,7:4194304,8:8388608,0x52:1179648,0x53:1310720,0x54:1572864}
CART={0x0f:'MBC3+TIMER+BATTERY',0x10:'MBC3+TIMER+RAM+BATTERY',0x11:'MBC3',0x12:'MBC3+RAM',0x13:'MBC3+RAM+BATTERY'}
def h256(b):return hashlib.sha256(b).hexdigest()
def ent(b):
 c=Counter(b);n=len(b);return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0
def wcsv(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True); fields=list(rows[0]) if rows else []
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def hdr(d):
 hc=0
 for x in d[0x134:0x14d]:hc=(hc-x-1)&255
 gs=(sum(d)-d[0x14e]-d[0x14f])&0xffff; g0=(d[0x14e]<<8)|d[0x14f]
 rc=d[0x148];ram=d[0x149];ct=d[0x147]
 return {'entry_point_hex':d[0x100:0x104].hex(),'nintendo_logo_valid':d[0x104:0x134]==LOGO,
 'title':d[0x134:0x143].split(b'\0',1)[0].decode('ascii','backslashreplace'),'cgb_flag_hex':f'{d[0x143]:02X}',
 'cartridge_type_hex':f'{ct:02X}','cartridge_type':CART.get(ct,'OTHER'),'rom_size_code_hex':f'{rc:02X}',
 'rom_size_header_bytes':ROMSZ.get(rc),'rom_size_actual_bytes':len(d),'ram_size_code_hex':f'{ram:02X}',
 'ram_size_header_bytes':RAM.get(ram),'destination_code_hex':f'{d[0x14a]:02X}','mask_rom_version':d[0x14c],
 'header_checksum_stored_hex':f'{d[0x14d]:02X}','header_checksum_calculated_hex':f'{hc:02X}','header_checksum_valid':d[0x14d]==hc,
 'global_checksum_stored_hex':f'{g0:04X}','global_checksum_calculated_hex':f'{gs:04X}','global_checksum_valid':g0==gs,
 'mbc_note':'64 KiB RAM header on MBC3-family cartridge; consistent with MBC30-style usage.' if ct in (0x0f,0x10,0x11,0x12,0x13) and ram==5 else ''}
def fillruns(d):
 out=[];i=0
 while i<len(d):
  j=i+1
  while j<len(d) and d[j]==d[i]:j+=1
  if j-i>=32:out.append({'file_start_hex':f'{i:06X}','file_end_exclusive_hex':f'{j:06X}','length':j-i,'byte_hex':f'{d[i]:02X}','bank_start_hex':f'{i//BANK:02X}','bank_end_hex':f'{(j-1)//BANK:02X}'})
  i=j
 return out
def audit(label,rom,out):
 d=rom.read_bytes();out.mkdir(parents=True,exist_ok=True);h=hdr(d)
 ident={'label':label,'source_filename':rom.name,'size_bytes':len(d),'md5':hashlib.md5(d).hexdigest(),'sha1':hashlib.sha1(d).hexdigest(),'sha256':h256(d),'crc32':f'{zlib.crc32(d)&0xffffffff:08x}','header':h}
 (out/'identity.json').write_text(json.dumps(ident,indent=2)+'\n');(out/'header.json').write_text(json.dumps(h,indent=2)+'\n')
 banks=[];pages=[]
 for bn,off in enumerate(range(0,len(d),BANK)):
  b=d[off:off+BANK];c=Counter(b);mb,mc=c.most_common(1)[0]
  banks.append({'bank_hex':f'{bn:02X}','bank_dec':bn,'file_start_hex':f'{off:06X}','file_end_exclusive_hex':f'{off+len(b):06X}','cpu_range':'0000-3FFF' if bn==0 else '4000-7FFF','size':len(b),'sha256':h256(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','entropy_bits_per_byte':f'{ent(b):.6f}','unique_byte_values':len(c),'count_00':c.get(0,0),'count_FF':c.get(255,0),'most_common_byte_hex':f'{mb:02X}','most_common_fraction':f'{mc/len(b):.6f}','all_00':int(len(c)==1 and mb==0),'all_FF':int(len(c)==1 and mb==255)})
  for pn,po in enumerate(range(0,len(b),PAGE)):
   p=b[po:po+PAGE];pc=Counter(p);pb,pm=pc.most_common(1)[0];e=ent(p);frac=pm/len(p)
   cls=f'constant_{pb:02X}' if len(pc)==1 else ('fill_dominant' if frac>=.9 else ('very_low_entropy' if e<2 else ('low_entropy' if e<4.5 else ('high_entropy' if e>7.3 else 'mixed'))))
   pages.append({'bank_hex':f'{bn:02X}','page_in_bank_hex':f'{pn:02X}','file_offset_hex':f'{off+po:06X}','size':len(p),'sha256':h256(p),'crc32':f'{zlib.crc32(p)&0xffffffff:08x}','entropy_bits_per_byte':f'{e:.6f}','unique_byte_values':len(pc),'most_common_byte_hex':f'{pb:02X}','most_common_fraction':f'{frac:.6f}','classification':cls})
 wcsv(out/'bank_manifest.csv',banks);wcsv(out/'page_manifest.csv',pages);fr=fillruns(d);wcsv(out/'fill_runs_ge32.csv',fr)
 s={'rom_bytes':len(d),'banks':len(banks),'pages_256':len(pages),'bank_bytes_accounted':sum(x['size'] for x in banks),'page_bytes_accounted':sum(x['size'] for x in pages),'all_zero_banks':[x['bank_hex'] for x in banks if x['all_00']],'all_ff_banks':[x['bank_hex'] for x in banks if x['all_FF']],'fill_runs_ge32_count':len(fr),'largest_fill_runs':sorted(fr,key=lambda x:x['length'],reverse=True)[:20],'coverage_valid':sum(x['size'] for x in pages)==sum(x['size'] for x in banks)==len(d),'header_checksum_valid':h['header_checksum_valid'],'global_checksum_valid':h['global_checksum_valid']}
 (out/'coverage_summary.json').write_text(json.dumps(s,indent=2)+'\n');return d,ident,s
def main():
 a=argparse.ArgumentParser();a.add_argument('--catalog',required=True);a.add_argument('--output',required=True);x=a.parse_args();cp=pathlib.Path(x.catalog).resolve();cat=json.loads(cp.read_text());root=pathlib.Path(x.output);data={};ids={};sums={}
 for item in cat['roms']:
  p=pathlib.Path(item['path']);p=p if p.is_absolute() else (cp.parent/p).resolve();actual=h256(p.read_bytes())
  if item.get('expected_sha256') and actual.lower()!=item['expected_sha256'].lower():raise SystemExit(f"SHA-256 mismatch for {item['label']}: {actual}")
  d,i,s=audit(item['label'],p,root/item['output_subdir']);data[item['label']]=d;ids[item['label']]=i;sums[item['label']]=s
 labels=list(data);pair=[]
 for i in range(len(labels)):
  for j in range(i+1,len(labels)):
   A,B=labels[i],labels[j];aa,bb=data[A],data[B];same=len(aa)==len(bb);diff=sum(x!=y for x,y in zip(aa,bb)) if same else ''
   ib=[];db=[]
   if same:
    for off in range(0,len(aa),BANK):(ib if aa[off:off+BANK]==bb[off:off+BANK] else db).append(f'{off//BANK:02X}')
   pair.append({'a':A,'b':B,'same_size':int(same),'byte_differences':diff,'identical_banks':' '.join(ib),'different_banks':' '.join(db)})
 sh=root/'MULTI-REGION'/'REV-MIXED'/'ROM-REPRODUCIBILITY';wcsv(sh/'pairwise_diff_summary.csv',pair)
 if 'USA-EUROPE_REV0' in data and 'USA-EUROPE_REV1' in data:
  aa,bb=data['USA-EUROPE_REV0'],data['USA-EUROPE_REV1'];br=[]
  for off,(u,v) in enumerate(zip(aa,bb)):
   if u!=v:br.append({'file_offset_hex':f'{off:06X}','bank_hex':f'{off//BANK:02X}','offset_in_bank_hex':f'{off%BANK:04X}','rev0_hex':f'{u:02X}','rev1_hex':f'{v:02X}'})
  wcsv(sh/'usa_europe_rev0_rev1_changed_bytes.csv',br)
 (sh/'rom_catalog.generated.json').write_text(json.dumps({'schema_version':1,'bank_size':BANK,'page_size':PAGE,'roms':ids},indent=2)+'\n')
 print(json.dumps({'roms':len(data),'summaries':sums},indent=2))
if __name__=='__main__':main()
