#!/usr/bin/env python3
"""Deterministic full-ROM analysis toolkit for Pocket Monsters Green JP.
Does not contain ROM data. Python 3.10+; standard library only.
"""
from pathlib import Path
import argparse, hashlib, zlib, json, csv, math, sys
BANK=0x4000; PAGE=0x100
KNOWN={
 '82c0eef40a5e2423699d9fd8ba15dfaa8b51d196':'REV-0',
 '4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b':'REV-A',
}
def hs(d): return {'size':len(d),'crc32':f'{zlib.crc32(d)&0xffffffff:08x}','md5':hashlib.md5(d).hexdigest(),'sha1':hashlib.sha1(d).hexdigest(),'sha256':hashlib.sha256(d).hexdigest()}
def ent(d):
 c=[0]*256
 for b in d:c[b]+=1
 n=len(d); return -sum((x/n)*math.log2(x/n) for x in c if x) if n else 0
def cpu(off):
 b=off//BANK; w=off%BANK; return w if b==0 else 0x4000+w
def head(d):
 h=0
 for b in d[0x134:0x14d]: h=(h-b-1)&255
 g=(sum(d[:0x14e])+sum(d[0x150:]))&0xffff
 return {'title':d[0x134:0x144].split(b'\0')[0].decode('ascii','replace'),'sgb_flag':d[0x146],'cartridge_type':d[0x147],'rom_size_code':d[0x148],'ram_size_code':d[0x149],'destination_code':d[0x14a],'old_licensee_code':d[0x14b],'rom_version':d[0x14c],'header_checksum_stored':d[0x14d],'header_checksum_computed':h,'header_checksum_ok':h==d[0x14d],'global_checksum_stored':int.from_bytes(d[0x14e:0x150],'big'),'global_checksum_computed':g,'global_checksum_ok':g==int.from_bytes(d[0x14e:0x150],'big')}
def identify(p):
 d=Path(p).read_bytes(); h=hs(d); print(json.dumps({**h,'known_revision':KNOWN.get(h['sha1']),'header':head(d)},indent=2))
def split(p,out):
 d=Path(p).read_bytes(); out=Path(out); out.mkdir(parents=True,exist_ok=True)
 if len(d)%BANK: raise SystemExit('ROM size is not a multiple of 16 KiB')
 for b in range(len(d)//BANK):(out/f'bank_{b:02x}.bin').write_bytes(d[b*BANK:(b+1)*BANK])
def join(inp,out):
 inp=Path(inp); parts=sorted(inp.glob('bank_??.bin'))
 if not parts: raise SystemExit('No bank_??.bin files')
 d=b''.join(x.read_bytes() for x in parts)
 Path(out).write_bytes(d); print(json.dumps(hs(d),indent=2))
def diff(a,b,out=None):
 A=Path(a).read_bytes(); B=Path(b).read_bytes()
 if len(A)!=len(B): raise SystemExit('ROM sizes differ')
 idx=[i for i,(x,y) in enumerate(zip(A,B)) if x!=y]; runs=[]
 if idx:
  s=pr=idx[0]
  for x in idx[1:]:
   if x==pr+1: pr=x
   else: runs.append((s,pr)); s=pr=x
  runs.append((s,pr))
 print(json.dumps({'different_bytes':len(idx),'runs':len(runs),'identical_bytes':len(A)-len(idx),'identical_percent':100*(len(A)-len(idx))/len(A)},indent=2))
 if out:
  with Path(out).open('w') as f:
   for s,e in runs:f.write(json.dumps({'offset':s,'old':A[s:e+1].hex(),'new':B[s:e+1].hex()},separators=(',',':'))+'\n')
def apply(base,delta,out):
 d=bytearray(Path(base).read_bytes())
 for n,line in enumerate(Path(delta).read_text().splitlines(),1):
  r=json.loads(line); off=r['offset']; old=bytes.fromhex(r['old']); new=bytes.fromhex(r['new'])
  if d[off:off+len(old)]!=old: raise SystemExit(f'delta preimage mismatch at line {n}, offset 0x{off:x}')
  if len(old)!=len(new): raise SystemExit('delta changes length; unsupported')
  d[off:off+len(new)]=new
 Path(out).write_bytes(d); print(json.dumps({**hs(d),'known_revision':KNOWN.get(hashlib.sha1(d).hexdigest())},indent=2))
def banks(p,out):
 d=Path(p).read_bytes(); rows=[]
 for b in range(len(d)//BANK):
  x=d[b*BANK:(b+1)*BANK]; rows.append({'bank':f'{b:02X}','offset':f'0x{b*BANK:05X}','entropy':f'{ent(x):.6f}',**hs(x)})
 with Path(out).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
def pages(p,out):
 d=Path(p).read_bytes(); rows=[]
 for off in range(0,len(d),PAGE):
  x=d[off:off+PAGE]; rows.append({'page':off//PAGE,'bank':f'{off//BANK:02X}','offset':f'0x{off:05X}','cpu':f'0x{cpu(off):04X}','entropy':f'{ent(x):.6f}','sha256':hashlib.sha256(x).hexdigest()})
 with Path(out).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
def pointers(p,out):
 d=Path(p).read_bytes(); rows=[]
 for off in range(len(d)-1):
  v=d[off]|(d[off+1]<<8)
  if v<0x8000: rows.append({'source_file_offset':f'0x{off:05X}','source_bank':f'{off//BANK:02X}','value':f'0x{v:04X}','kind':'ROM0-window' if v<0x4000 else 'switchable-window','target_bank':'00' if v<0x4000 else f'{off//BANK:02X}'})
 with Path(out).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
def emit_db(p,out):
 d=Path(p).read_bytes()
 with Path(out).open('w') as f:
  f.write('; Byte-exact local representation. Generated from user-supplied ROM.\n')
  for b in range(len(d)//BANK):
   f.write(f'\nSECTION "Bank {b:02X}", ROM0[$0000]' if b==0 else f'\nSECTION "Bank {b:02X}", ROMX[$4000], BANK[$%02X]'%b); f.write('\n')
   x=d[b*BANK:(b+1)*BANK]
   for i in range(0,len(x),16): f.write('    db '+', '.join(f'${q:02X}' for q in x[i:i+16])+'\n')
def verify(p):
 d=Path(p).read_bytes(); h=hs(d); he=head(d); ok=(h['sha1'] in KNOWN and he['header_checksum_ok'] and he['global_checksum_ok'] and len(d)==0x80000)
 print(json.dumps({'ok':ok,'known_revision':KNOWN.get(h['sha1']),**h,'header':he},indent=2)); raise SystemExit(0 if ok else 1)
def main():
 ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
 for c in ['identify','verify']:
  x=sp.add_parser(c); x.add_argument('rom')
 x=sp.add_parser('split'); x.add_argument('rom'); x.add_argument('outdir')
 x=sp.add_parser('join'); x.add_argument('indir'); x.add_argument('out')
 x=sp.add_parser('diff'); x.add_argument('a'); x.add_argument('b'); x.add_argument('--out')
 x=sp.add_parser('apply'); x.add_argument('base'); x.add_argument('delta'); x.add_argument('out')
 for c in ['banks','pages','pointers','emit-db']:
  x=sp.add_parser(c); x.add_argument('rom'); x.add_argument('out')
 a=ap.parse_args(); {'identify':lambda:identify(a.rom),'verify':lambda:verify(a.rom),'split':lambda:split(a.rom,a.outdir),'join':lambda:join(a.indir,a.out),'diff':lambda:diff(a.a,a.b,a.out),'apply':lambda:apply(a.base,a.delta,a.out),'banks':lambda:banks(a.rom,a.out),'pages':lambda:pages(a.rom,a.out),'pointers':lambda:pointers(a.rom,a.out),'emit-db':lambda:emit_db(a.rom,a.out)}[a.cmd]()
if __name__=='__main__': main()
