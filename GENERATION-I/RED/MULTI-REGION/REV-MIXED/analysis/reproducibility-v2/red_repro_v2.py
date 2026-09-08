#!/usr/bin/env python3
"""GitHub-safe deterministic full-ROM work-corpus generator for Pokémon Red.
Supply the user's local .gb files. It never embeds or exports ROM bytes.
"""
from pathlib import Path
from collections import defaultdict
import csv, hashlib, json, shutil, sys
BANK=0x4000
CAT={
'392ce450d708c8d127aaed7afc20001a48625bd83a5fa5325be82f5c0972ccfa':('JP','REV-0','jp_rev0'),
'751abb1fb2b2d6b91dc631fa10ed36bd07f682cb5c3febe6c8f0e3dabc1fae1c':('JP','REV-A','jp_reva'),
'5ca7ba01642a3b27b0cc0b5349b52792795b62d3ed977e98a09390659af96b7b':('USA-EUROPE','REV-0','en_rev0'),
'9cd186b288dbcd52413d561ae449f1f700c32b45af56dbf849095d4a0c8637a6':('DE','REV-0','de_rev0'),
'23766290f3b2347f815f1e8977c3b84047ed880cadda8c4f1a3595a633daa303':('FR','REV-0','fr_rev0'),
'e805d00b0002156d38b96efd57c823b0db3a3ef4cd32f98bd9bb4779bda3dd5b':('IT','REV-0','it_rev0'),
'a756cf7ad888aa46de4b9699a177a0edf1775e59eb6330014c6f5c139be9c45d':('ES','REV-0','es_rev0')}
ABS={0xC3:'JP',0xC2:'JP NZ',0xCA:'JP Z',0xD2:'JP NC',0xDA:'JP C',0xCD:'CALL',0xC4:'CALL NZ',0xCC:'CALL Z',0xD4:'CALL NC',0xDC:'CALL C'}
MEM={0xEA:'LD [a16],A',0xFA:'LD A,[a16]',0x08:'LD [a16],SP'}
RST={0xC7:0,0xCF:8,0xD7:0x10,0xDF:0x18,0xE7:0x20,0xEF:0x28,0xF7:0x30,0xFF:0x38}
def h(b):return hashlib.sha256(b).hexdigest()
def cpu(bank,off):return off if bank==0 else 0x4000+off
def mkdir(p):p.mkdir(parents=True,exist_ok=True);return p
def wc(p,rows,fields):
 mkdir(p.parent)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def wj(p,o):mkdir(p.parent);p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def runs(b):
 out=[];i=0
 while i<len(b):
  v=b[i]
  if v not in (0,255):i+=1;continue
  j=i+1
  while j<len(b) and b[j]==v:j+=1
  if j-i>=64:out.append((i,j,v))
  i=j
 return out
def scan(b):
 bc=len(b)//BANK;far=[];xref=[];mem=[];mbc=[]
 for i in range(len(b)-2):
  sb=i//BANK;so=i%BANK;op=b[i];bank=b[i];a=b[i+1]|b[i+2]<<8
  if 1<=bank<bc and 0x4000<=a<0x8000:far.append((i,sb,f'0x{cpu(sb,so):04X}',bank,f'0x{a:04X}',bank*BANK+a-0x4000))
  if op in ABS and a<0x8000:xref.append((i,sb,f'0x{cpu(sb,so):04X}',f'0x{op:02X}',ABS[op],f'0x{a:04X}',0 if a<0x4000 else sb))
  if op in MEM:
   cls='SRAM' if 0xA000<=a<=0xBFFF else 'WRAM' if 0xC000<=a<=0xDFFF else 'ECHO' if 0xE000<=a<=0xFDFF else 'OAM' if 0xFE00<=a<=0xFE9F else 'IO' if 0xFF00<=a<=0xFF7F else 'HRAM' if 0xFF80<=a<=0xFFFE else 'IE' if a==0xFFFF else None
   if cls:mem.append((i,sb,f'0x{cpu(sb,so):04X}',f'0x{op:02X}',MEM[op],f'0x{a:04X}',cls))
 for i,op in enumerate(b):
  if op in RST:
   sb=i//BANK;xref.append((i,sb,f'0x{cpu(sb,i%BANK):04X}',f'0x{op:02X}','RST',f'0x{RST[op]:04X}',0))
  if op in (0xE0,0xF0) and i+1<len(b):
   a=0xFF00+b[i+1];sb=i//BANK;mem.append((i,sb,f'0x{cpu(sb,i%BANK):04X}',f'0x{op:02X}','LDH',f'0x{a:04X}','IO' if a<0xFF80 else 'HRAM'))
 for i in range(len(b)-4):
  if b[i]==0x3E and b[i+2]==0xEA:
   v=b[i+1];a=b[i+3]|b[i+4]<<8
   if 0x2000<=a<=0x3FFF and v<max(0x80,bc):
    sb=i//BANK;mbc.append((i,sb,f'0x{cpu(sb,i%BANK):04X}',v,f'0x{a:04X}'))
 return far,xref,mem,mbc
def skeleton(base,b):
 src=mkdir(base/'source-layout');bd=mkdir(src/'banks');bc=len(b)//BANK;cov=[];sym=[];mp=[]
 for a,n in [(0,'RST00'),(8,'RST08'),(0x10,'RST10'),(0x18,'RST18'),(0x20,'RST20'),(0x28,'RST28'),(0x30,'RST30'),(0x38,'RST38'),(0x40,'VBlankInterrupt'),(0x48,'LCDStatInterrupt'),(0x50,'TimerInterrupt'),(0x58,'SerialInterrupt'),(0x60,'JoypadInterrupt'),(0x100,'EntryPoint'),(0x104,'NintendoLogo'),(0x134,'CartridgeTitle'),(0x14D,'HeaderChecksum'),(0x14E,'GlobalChecksum')]:sym.append(f'00:{a:04X} {n}')
 inc=[]
 for n in range(bc):
  st=n*BANK;ca=0 if n==0 else 0x4000;sec='ROM0[$0000]' if n==0 else f'ROMX[$4000], BANK[${n:02X}]';name=f'Bank{n:02X}_Start'
  (bd/f'bank_{n:02X}.asm').write_text(f'SECTION "Bank {n:02X}", {sec}\n{name}::\n    INCBIN "baserom.gb", ${st:X}, $4000\n')
  inc.append(f'INCLUDE "banks/bank_{n:02X}.asm"');sym.append(f'{n:02X}:{ca:04X} {name}');mp.append(f'{n:02X} {st:06X}-{st+BANK-1:06X} {ca:04X}-{ca+BANK-1:04X}')
  cov.append((n,f'{n:02X}',st,st+BANK,BANK,f'0x{ca:04X}',f'0x{ca+BANK-1:04X}',1))
 (src/'main.asm').write_text('\n'.join(inc)+'\n');(src/'rom.sym').write_text('\n'.join(sym)+'\n');(src/'rom.map').write_text('\n'.join(mp)+'\n')
 wc(src/'coverage.csv',[dict(zip(['bank','bank_hex','file_start','file_end_exclusive','length','cpu_start','cpu_end_inclusive','coverage_count'],r)) for r in cov],['bank','bank_hex','file_start','file_end_exclusive','length','cpu_start','cpu_end_inclusive','coverage_count'])
 rebuilt=b''.join(b[n*BANK:(n+1)*BANK] for n in range(bc));return {'rom_size':len(b),'covered_bytes':sum(r[4] for r in cov),'coverage_exact':rebuilt==b,'sha256':h(b),'rebuilt_sha256':h(rebuilt),'bank_count':bc}
def main(inp,out):
 inp=Path(inp);out=Path(out);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True);by=defaultdict(list)
 for p in sorted(inp.glob('*.gb')):
  b=p.read_bytes();s=h(b)
  if s in CAT:by[s].append((p,b))
 summary=[]
 for s,items in sorted(by.items(),key=lambda kv:CAT[kv[0]][2]):
  region,rev,rid=CAT[s];b=items[0][1];base=mkdir(out/f'GENERATION-I/RED/{region}/{rev}/analysis/reproducibility-v2');far,xr,mr,mb=scan(b)
  wc(base/'far-pointer-candidates.csv',[dict(zip(['source_file_offset','source_bank','source_cpu_addr','target_bank','target_cpu_addr','target_file_offset'],r)) for r in far],['source_file_offset','source_bank','source_cpu_addr','target_bank','target_cpu_addr','target_file_offset'])
  wc(base/'code-xref-pattern-candidates.csv',[dict(zip(['source_file_offset','source_bank','source_cpu_addr','opcode','mnemonic_pattern','target_cpu_addr','target_bank_assumption'],r)) for r in xr],['source_file_offset','source_bank','source_cpu_addr','opcode','mnemonic_pattern','target_cpu_addr','target_bank_assumption'])
  wc(base/'memory-reference-candidates.csv',[dict(zip(['source_file_offset','source_bank','source_cpu_addr','opcode','mnemonic_pattern','target_addr','memory_class'],r)) for r in mr],['source_file_offset','source_bank','source_cpu_addr','opcode','mnemonic_pattern','target_addr','memory_class'])
  wc(base/'mbc-bank-switch-candidates.csv',[dict(zip(['source_file_offset','source_bank','source_cpu_addr','bank_value','mbc_register_addr'],r)) for r in mb],['source_file_offset','source_bank','source_cpu_addr','bank_value','mbc_register_addr'])
  wc(base/'padding-candidates.csv',[{'file_start':a,'file_end_exclusive':z,'length':z-a,'value':f'0x{v:02X}','classification':'candidate_only'} for a,z,v in runs(b)],['file_start','file_end_exclusive','length','value','classification'])
  proof=skeleton(base,b);wj(base/'roundtrip-proof.json',proof);summary.append({'rom_id':rid,'input_count':len(items),'far_pointer_candidates':len(far),'xref_patterns':len(xr),'memory_ref_patterns':len(mr),'mbc_switch_candidates':len(mb),**proof})
 wc(out/'summary.csv',summary,list(summary[0]));print(json.dumps(summary,indent=2))
if __name__=='__main__':
 if len(sys.argv)!=3:raise SystemExit('usage: red_repro_v2.py INPUT_ROM_DIR OUTPUT_DIR')
 main(sys.argv[1],sys.argv[2])
