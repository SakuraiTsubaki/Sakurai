#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,json,zlib,math
BANK=0x4000; PAGE=0x100
KNOWN={'82c0eef40a5e2423699d9fd8ba15dfaa8b51d196':'REV-0','4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b':'REV-A'}
def digest(d): return {'size':len(d),'crc32':f'{zlib.crc32(d)&0xffffffff:08x}','md5':hashlib.md5(d).hexdigest(),'sha1':hashlib.sha1(d).hexdigest(),'sha256':hashlib.sha256(d).hexdigest()}
def entropy(d):
 c=[0]*256
 for x in d:c[x]+=1
 n=len(d); return -sum((v/n)*math.log2(v/n) for v in c if v) if n else 0.0
def cpu(off):
 b=off//BANK; x=off%BANK; return x if b==0 else 0x4000+x
def header(d):
 hc=0
 for b in d[0x134:0x14d]: hc=(hc-b-1)&255
 gc=(sum(d[:0x14e])+sum(d[0x150:]))&0xffff
 return {'title':d[0x134:0x144].split(b'\0')[0].decode('ascii','replace'),'sgb_flag':d[0x146],'cartridge_type':d[0x147],'rom_size_code':d[0x148],'ram_size_code':d[0x149],'destination_code':d[0x14a],'old_licensee_code':d[0x14b],'rom_version':d[0x14c],'header_checksum_stored':d[0x14d],'header_checksum_computed':hc,'header_checksum_ok':hc==d[0x14d],'global_checksum_stored':int.from_bytes(d[0x14e:0x150],'big'),'global_checksum_computed':gc,'global_checksum_ok':gc==int.from_bytes(d[0x14e:0x150],'big')}
def write_csv(path,rows):
 rows=list(rows); Path(path).parent.mkdir(parents=True,exist_ok=True)
 if not rows: Path(path).write_text(''); return
 with Path(path).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def analyze(rom,out):
 d=Path(rom).read_bytes(); h=digest(d); rev=KNOWN.get(h['sha1'],'UNKNOWN'); out=Path(out); out.mkdir(parents=True,exist_ok=True)
 meta={**h,'revision':rev,'header':header(d)}; (out/'rom.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
 banks=[]
 for b in range(len(d)//BANK):
  x=d[b*BANK:(b+1)*BANK]; banks.append({'bank':f'{b:02X}','offset_start':f'0x{b*BANK:05X}','offset_end':f'0x{(b+1)*BANK-1:05X}','cpu_start':'0x0000' if b==0 else '0x4000','cpu_end':'0x3FFF' if b==0 else '0x7FFF','entropy':f'{entropy(x):.6f}','zero_bytes':x.count(0),'ff_bytes':x.count(255),**digest(x)})
 write_csv(out/'bank_manifest.csv',banks)
 pages=[]
 for off in range(0,len(d),PAGE):
  x=d[off:off+PAGE]; pages.append({'page':off//PAGE,'bank':f'{off//BANK:02X}','offset':f'0x{off:05X}','cpu':f'0x{cpu(off):04X}','entropy':f'{entropy(x):.6f}','crc32':f'{zlib.crc32(x)&0xffffffff:08x}','sha256':hashlib.sha256(x).hexdigest()})
 write_csv(out/'page_manifest.csv',pages)
 runs=[]; i=0
 while i<len(d):
  v=d[i]; j=i+1
  while j<len(d) and d[j]==v:j+=1
  if j-i>=16 and v in (0,255): runs.append({'bank':f'{i//BANK:02X}','offset_start':f'0x{i:05X}','offset_end':f'0x{j-1:05X}','cpu_start':f'0x{cpu(i):04X}','length':j-i,'value':f'0x{v:02X}','classification':'homogeneous filler candidate; NOT proven free'})
  i=j
 write_csv(out/'filler_candidates.csv',runs)
 ptr=[]
 for off in range(len(d)-1):
  v=d[off]|d[off+1]<<8
  if 0x0150<=v<0x8000:
   sb=off//BANK; target_bank=0 if v<0x4000 else sb
   ptr.append({'source_offset':f'0x{off:05X}','source_bank':f'{sb:02X}','source_cpu':f'0x{cpu(off):04X}','value':f'0x{v:04X}','window':'ROM0' if v<0x4000 else 'ROMX-same-bank-candidate','target_bank':f'{target_bank:02X}'})
 write_csv(out/'pointer_candidates.csv',ptr)
 regs=[('rst00',0x0000,0x0007),('rst08',0x0008,0x000f),('rst10',0x0010,0x0017),('rst18',0x0018,0x001f),('rst20',0x0020,0x0027),('rst28',0x0028,0x002f),('rst30',0x0030,0x0037),('rst38',0x0038,0x003f),('vblank',0x0040,0x0047),('lcd',0x0048,0x004f),('timer',0x0050,0x0057),('serial',0x0058,0x005f),('joypad',0x0060,0x0067),('entrypoint',0x0100,0x0103),('logo',0x0104,0x0133),('header_title',0x0134,0x0143),('header_rest',0x0144,0x014f)]
 write_csv(out/'fixed_regions.csv',({'name':n,'offset_start':f'0x{s:04X}','offset_end':f'0x{e:04X}','sha256':hashlib.sha256(d[s:e+1]).hexdigest()} for n,s,e in regs))
 return meta
def compare(a,b,out,semantic_csv=None):
 A=Path(a).read_bytes();B=Path(b).read_bytes();out=Path(out);out.mkdir(parents=True,exist_ok=True)
 if len(A)!=len(B):raise SystemExit('size mismatch')
 sem={}
 if semantic_csv:
  with Path(semantic_csv).open() as f:
   for r in csv.DictReader(f):sem[int(r['bank'],16)]=r['sections']
 changed=[]; runs=[]; start=None; prev=None
 for i,(x,y) in enumerate(zip(A,B)):
  if x!=y:
   changed.append({'offset':f'0x{i:05X}','bank':f'{i//BANK:02X}','cpu':f'0x{cpu(i):04X}','rev0':f'{x:02X}','reva':f'{y:02X}','semantic_bank_sections':sem.get(i//BANK,'')})
   if start is None:start=prev=i
   elif i==prev+1:prev=i
   else:runs.append((start,prev));start=prev=i
 if start is not None:runs.append((start,prev))
 write_csv(out/'changed_bytes.csv',changed)
 rr=[]
 for s,e in runs:
  rr.append({'offset_start':f'0x{s:05X}','offset_end':f'0x{e:05X}','bank':f'{s//BANK:02X}','cpu_start':f'0x{cpu(s):04X}','length':e-s+1,'rev0_sha256':hashlib.sha256(A[s:e+1]).hexdigest(),'reva_sha256':hashlib.sha256(B[s:e+1]).hexdigest(),'semantic_bank_sections':sem.get(s//BANK,'')})
 write_csv(out/'diff_runs.csv',rr)
 per=[]
 for b in range(len(A)//BANK):
  aa=A[b*BANK:(b+1)*BANK];bb=B[b*BANK:(b+1)*BANK];n=sum(x!=y for x,y in zip(aa,bb))
  per.append({'bank':f'{b:02X}','different_bytes':n,'identical_bytes':BANK-n,'different_percent':f'{100*n/BANK:.6f}','semantic_sections':sem.get(b,''),'rev0_sha1':hashlib.sha1(aa).hexdigest(),'reva_sha1':hashlib.sha1(bb).hexdigest()})
 write_csv(out/'bank_diff.csv',per)
 (out/'summary.json').write_text(json.dumps({'size':len(A),'different_bytes':len(changed),'identical_bytes':len(A)-len(changed),'identical_percent':100*(len(A)-len(changed))/len(A),'diff_runs':len(runs)},indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
 x=sp.add_parser('analyze');x.add_argument('rom');x.add_argument('out')
 x=sp.add_parser('compare');x.add_argument('rev0');x.add_argument('reva');x.add_argument('out');x.add_argument('--semantic-map')
 a=ap.parse_args(); analyze(a.rom,a.out) if a.cmd=='analyze' else compare(a.rev0,a.reva,a.out,a.semantic_map)
if __name__=='__main__':main()
