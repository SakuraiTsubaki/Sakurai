#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import argparse,csv,gzip,hashlib,json,math,struct,zlib
ROMS=[('JA-JP','Pocket Monsters - Emerald (Japan).gba'),('ES-ES','Pokemon - Edicion Esmeralda (Spain).gba'),('EN-US-EU','Pokemon - Emerald Version (USA, Europe).gba'),('EN-US-EU-ALIAS','Pokemon - Emerald Version (U).gba'),('DE-DE','Pokemon - Smaragd-Edition (Germany).gba'),('FR-FR','Pokemon - Version Emeraude (France).gba'),('IT-IT','Pokemon - Versione Smeraldo (Italy).gba')]
CHUNK=0x4000; BASE='EN-US-EU'
CLASSES=[('ROM',0x08000000,0x0A000000),('EWRAM',0x02000000,0x02040000),('IWRAM',0x03000000,0x03008000),('IO',0x04000000,0x04000400),('PALRAM',0x05000000,0x05000400),('VRAM',0x06000000,0x06018000),('OAM',0x07000000,0x07000400)]
def H(b,n='sha256'): x=hashlib.new(n);x.update(b);return x.hexdigest()
def ent(b):
 c=Counter(b);n=len(b);return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0
def header(b):
 s=b[0xBD];c=(-sum(b[0xA0:0xBD])-0x19)&255
 return {'title':b[0xA0:0xAC].rstrip(b'\0').decode('ascii','replace'),'game_code':b[0xAC:0xB0].decode('ascii','replace'),'maker_code':b[0xB0:0xB2].decode('ascii','replace'),'fixed_value':b[0xB2],'software_version':b[0xBC],'header_checksum_stored':s,'header_checksum_calculated':c,'header_checksum_valid':s==c,'entry_branch_word_le':f"0x{struct.unpack_from('<I',b)[0]:08X}"}
def wc(p,rows,fields):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def pointers(tag,b,out):
 counts=Counter();p=out/'analysis'/f'pointer_index_{tag}.csv.gz';p.parent.mkdir(parents=True,exist_ok=True)
 with gzip.open(p,'wt',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['source_offset_hex','value_hex','pointer_class','target_offset_hex'])
  for o in range(0,len(b)-3,4):
   v=struct.unpack_from('<I',b,o)[0]
   for name,lo,hi in CLASSES:
    if lo<=v<hi:
     counts[name]+=1;t=v-(0x08000000 if name=='ROM' else 0x02000000 if name=='EWRAM' else 0x03000000 if name=='IWRAM' else lo)
     w.writerow([f'0x{o:08X}',f'0x{v:08X}',name,f'0x{t:08X}']);break
 return counts
def main():
 a=argparse.ArgumentParser();a.add_argument('--rom-dir',default='.');a.add_argument('--out',default='./emerald_repro_output');x=a.parse_args();root=Path(x.rom_dir);out=Path(x.out);out.mkdir(parents=True,exist_ok=True)
 data={};inv=[];hdr=[];freq=[];ps=[];chunks=[]
 for tag,fn in ROMS:
  b=(root/fn).read_bytes();data[tag]=b;r={'tag':tag,'filename':fn,'size':len(b),'md5':H(b,'md5'),'sha1':H(b,'sha1'),'sha256':H(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','unique_image':tag!='EN-US-EU-ALIAS','canonical_duplicate_of':'EN-US-EU' if tag=='EN-US-EU-ALIAS' else ''};inv.append(r);hdr.append({'tag':tag,**header(b)});c=Counter(b)
  for v in range(256):freq.append({'tag':tag,'byte_hex':f'{v:02X}','count':c[v],'ratio':f'{c[v]/len(b):.10f}'})
  pc=pointers(tag,b,out) if tag!='EN-US-EU-ALIAS' else pointers('EN-US-EU-ALIAS',b,out)
  for k in [z[0] for z in CLASSES]:ps.append({'tag':tag,'pointer_class':k,'count':pc[k]})
  ps.append({'tag':tag,'pointer_class':'TOTAL_RECOGNIZED','count':sum(pc.values())})
  for i,s in enumerate(range(0,len(b),CHUNK)):
   q=b[s:s+CHUNK];chunks.append({'tag':tag,'chunk_index':i,'start_hex':f'0x{s:08X}','end_hex':f'0x{s+len(q):08X}','size':len(q),'sha256':H(q),'crc32':f'{zlib.crc32(q)&0xffffffff:08x}','entropy_bits_per_byte':f'{ent(q):.6f}','zero_ratio':f'{q.count(0)/len(q):.8f}','ff_ratio':f'{q.count(255)/len(q):.8f}','distinct_byte_values':len(set(q))})
 tags=[t for t,_ in ROMS];pair=[]
 for i,a0 in enumerate(tags):
  for b0 in tags[i+1:]:
   a1,b1=data[a0],data[b0];d=sum(x!=y for x,y in zip(a1,b1));pair.append({'a':a0,'b':b0,'size_a':len(a1),'size_b':len(b1),'different_bytes':d,'equal_bytes':len(a1)-d,'similarity_ratio':f'{(len(a1)-d)/len(a1):.10f}'})
 delta=[];base=data[BASE]
 for t in [z for z in tags if z!='EN-US-EU-ALIAS']:
  b=data[t]
  for i,s in enumerate(range(0,len(base),CHUNK)):
   q,r=base[s:s+CHUNK],b[s:s+CHUNK];d=sum(x!=y for x,y in zip(q,r));delta.append({'tag':t,'baseline':BASE,'chunk_index':i,'start_hex':f'0x{s:08X}','different_bytes':d,'identical':d==0,'difference_ratio':f'{d/len(q):.8f}'})
 regions=[]
 for t in [z for z in tags if z!='EN-US-EU-ALIAS']:
  b=data[t]
  for i,s in enumerate(range(0,len(b),0x100000)):
   q=b[s:s+0x100000];regions.append({'tag':t,'region_index':i,'start_hex':f'0x{s:08X}','end_hex':f'0x{s+len(q):08X}','sha256':H(q),'entropy_bits_per_byte':f'{ent(q):.6f}'})
 for name,rows in [('rom_inventory',inv),('gba_headers',hdr),('byte_frequency',freq),('pointer_summary',ps),('chunks_16k',chunks),('pairwise_similarity',pair),('baseline_delta_16k',delta),('regions_1m',regions)]:wc(out/'analysis'/f'{name}.csv',rows,list(rows[0]))
 m={'format_version':1,'game':'Pokemon Emerald','generation':3,'chunk_size':CHUNK,'canonical_comparison_tag':BASE,'files':inv,'header_records':hdr,'duplicate_groups':[['EN-US-EU','EN-US-EU-ALIAS']]};(out/'manifest').mkdir(exist_ok=True);(out/'manifest'/'rom_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 for n in ['md5','sha1','sha256']:(out/'manifest'/f'{n.upper()}SUMS.txt').write_text(''.join(f"{r[n]}  {r['filename']}\n" for r in inv))
 ids=out/'identities';ids.mkdir(exist_ok=True)
 for r in inv:
  if r['tag']!='EN-US-EU-ALIAS':(ids/f"{r['tag']}.json").write_text(json.dumps({'file':r,'header':next(h for h in hdr if h['tag']==r['tag'])},indent=2)+'\n')
if __name__=='__main__':main()
