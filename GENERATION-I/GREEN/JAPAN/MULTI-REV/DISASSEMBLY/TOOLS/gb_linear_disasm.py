#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, csv

R = ["b","c","d","e","h","l","[hl]","a"]
RP = ["bc","de","hl","sp"]
RP2 = ["bc","de","hl","af"]
CC = ["nz","z","nc","c"]
ROT = ["rlc","rrc","rl","rr","sla","sra","swap","srl"]
ALU = ["add a,{}","adc a,{}","sub {}","sbc a,{}","and {}","xor {}","or {}","cp {}"]
MISC = ["rlca","rrca","rla","rra","daa","cpl","scf","ccf"]
ILLEGAL = {0xD3,0xDB,0xDD,0xE3,0xE4,0xEB,0xEC,0xED,0xF4,0xFC,0xFD}

def s8(v): return v-256 if v >= 128 else v

def cpu_addr(bank:int, off:int)->int:
    return off if bank == 0 else 0x4000 + off

def logical(bank:int, addr:int)->str:
    if addr < 0x4000:
        return f"00:{addr:04X}"
    return f"{bank:02X}:{addr:04X}"

def imm8(data,i):
    if i+1 >= len(data): return None
    return data[i+1]

def imm16(data,i):
    if i+2 >= len(data): return None
    return data[i+1] | (data[i+2]<<8)

def cb_decode(cb:int)->str:
    x,y,z = cb>>6, (cb>>3)&7, cb&7
    if x == 0: return f"{ROT[y]} {R[z]}"
    if x == 1: return f"bit {y},{R[z]}"
    if x == 2: return f"res {y},{R[z]}"
    return f"set {y},{R[z]}"

def decode(data:bytes, i:int, bank:int):
    op = data[i]
    remain = len(data)-i
    addr = cpu_addr(bank,i)
    if op in ILLEGAL:
        return 1, f"db ${op:02X} ; illegal/unused opcode"
    x,y,z = op>>6, (op>>3)&7, op&7
    p,q = y>>1, y&1
    n8 = imm8(data,i)
    n16 = imm16(data,i)
    n8v = 0 if n8 is None else n8
    n16v = 0 if n16 is None else n16
    def need(n, text):
        if remain < n:
            return 1, f"db ${op:02X} ; truncated instruction ({text})"
        return n, text
    if op == 0xCB:
        if remain < 2: return 1, "db $CB ; truncated CB prefix"
        return 2, cb_decode(data[i+1])
    if x == 0:
        if z == 0:
            if y == 0: return 1,"nop"
            if y == 1: return need(3, f"ld [${n16v:04X}],sp")
            if y == 2: return need(2, f"stop ${n8v:02X}")
            if y == 3:
                if n8 is None: return need(2,"jr <truncated>")
                target=(addr+2+s8(n8)) & 0xffff
                return 2, f"jr ${target:04X} ; -> {logical(bank,target)}"
            if n8 is None: return need(2,"jr cc,<truncated>")
            target=(addr+2+s8(n8)) & 0xffff
            return 2, f"jr {CC[y-4]},${target:04X} ; -> {logical(bank,target)}"
        if z == 1:
            if q == 0: return need(3, f"ld {RP[p]},${n16v:04X}")
            return 1, f"add hl,{RP[p]}"
        if z == 2:
            if q == 0:
                return 1, ["ld [bc],a","ld [de],a","ld [hli],a","ld [hld],a"][p]
            return 1, ["ld a,[bc]","ld a,[de]","ld a,[hli]","ld a,[hld]"][p]
        if z == 3:
            return 1, f"{'inc' if q==0 else 'dec'} {RP[p]}"
        if z == 4: return 1, f"inc {R[y]}"
        if z == 5: return 1, f"dec {R[y]}"
        if z == 6: return need(2, f"ld {R[y]},${n8v:02X}")
        return 1, MISC[y]
    if x == 1:
        if y == 6 and z == 6: return 1,"halt"
        return 1, f"ld {R[y]},{R[z]}"
    if x == 2:
        return 1, ALU[y].format(R[z])
    if z == 0:
        if y < 4: return 1, f"ret {CC[y]}"
        if y == 4: return need(2, f"ldh [${0xFF00+n8v:04X}],a")
        if y == 5: return need(2, f"add sp,{s8(n8v):+d}")
        if y == 6: return need(2, f"ldh a,[${0xFF00+n8v:04X}]")
        return need(2, f"ld hl,sp{s8(n8v):+d}")
    if z == 1:
        if q == 0: return 1, f"pop {RP2[p]}"
        return 1, ["ret","reti","jp hl","ld sp,hl"][p]
    if z == 2:
        if y < 4:
            return need(3, f"jp {CC[y]},${n16v:04X} ; -> {logical(bank,n16v)}")
        if y == 4: return 1,"ld [$ff00+c],a"
        if y == 5: return need(3, f"ld [${n16v:04X}],a")
        if y == 6: return 1,"ld a,[$ff00+c]"
        return need(3, f"ld a,[${n16v:04X}]")
    if z == 3:
        if y == 0: return need(3, f"jp ${n16v:04X} ; -> {logical(bank,n16v)}")
        if y == 6: return 1,"di"
        if y == 7: return 1,"ei"
        return 1, f"db ${op:02X} ; illegal/unused opcode"
    if z == 4:
        if y < 4: return need(3, f"call {CC[y]},${n16v:04X} ; -> {logical(bank,n16v)}")
        return 1, f"db ${op:02X} ; illegal/unused opcode"
    if z == 5:
        if q == 0: return 1, f"push {RP2[p]}"
        if p == 0: return need(3, f"call ${n16v:04X} ; -> {logical(bank,n16v)}")
        return 1, f"db ${op:02X} ; illegal/unused opcode"
    if z == 6:
        return need(2, ALU[y].format(f"${n8v:02X}"))
    return 1, f"rst ${y*8:02X}"

def sha(path):
    h1=hashlib.sha1(); h256=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h1.update(b); h256.update(b)
    return h1.hexdigest(),h256.hexdigest()

def disasm_rom(path:str, outdir:str, tag:str):
    raw=pathlib.Path(path).read_bytes()
    if len(raw)%0x4000: raise SystemExit('ROM size is not a multiple of 16 KiB')
    os.makedirs(os.path.join(outdir,'listing'),exist_ok=True)
    os.makedirs(os.path.join(outdir,'lossless'),exist_ok=True)
    rows=[]
    for bank in range(len(raw)//0x4000):
        b=raw[bank*0x4000:(bank+1)*0x4000]
        lstp=os.path.join(outdir,'listing',f'bank_{bank:02X}.lst')
        asmp=os.path.join(outdir,'lossless',f'bank_{bank:02X}.asm')
        with open(lstp,'w',encoding='utf-8',newline='\n') as L, open(asmp,'w',encoding='utf-8',newline='\n') as A:
            L.write(f'; {tag} bank {bank:02X} raw linear disassembly\n')
            L.write('; NOTE: linear decoding intentionally does not claim code/data boundaries.\n')
            A.write(f'; {tag} bank {bank:02X} byte-exact lossless layer\n')
            A.write('; Every source line emits original bytes; mnemonic is commentary only.\n')
            if bank==0:
                A.write(f'SECTION "{tag} Bank {bank:02X}", ROM0[$0000]\n')
            else:
                A.write(f'SECTION "{tag} Bank {bank:02X}", ROMX[$4000], BANK[${bank:02X}]\n')
            i=0; ins=0; illegal=0
            while i<len(b):
                n,m=decode(b,i,bank)
                n=max(1,min(n,len(b)-i))
                bs=b[i:i+n]
                caddr=cpu_addr(bank,i)
                foff=bank*0x4000+i
                hexs=' '.join(f'{x:02X}' for x in bs)
                L.write(f'{bank:02X}:{caddr:04X}  {foff:06X}  {hexs:<8}  {m}\n')
                db=', '.join(f'${x:02X}' for x in bs)
                A.write(f'    db {db:<16} ; {bank:02X}:{caddr:04X} file ${foff:06X} | {m}\n')
                if 'illegal/unused opcode' in m: illegal+=1
                ins+=1; i+=n
        h1=hashlib.sha1(b).hexdigest()
        rows.append({'bank':f'{bank:02X}','file_start':f'0x{bank*0x4000:06X}','file_end':f'0x{(bank+1)*0x4000-1:06X}','instructions_linear':ins,'illegal_opcode_hits':illegal,'sha1':h1})
    with open(os.path.join(outdir,'bank_manifest.csv'),'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    main=os.path.join(outdir,'main_lossless.asm')
    with open(main,'w',encoding='utf-8',newline='\n') as f:
        f.write(f'; {tag} full byte-exact banked source\n')
        for bank in range(len(raw)//0x4000): f.write(f'INCLUDE "lossless/bank_{bank:02X}.asm"\n')
    h1,h256=sha(path)
    return {'tag':tag,'path':path,'size':len(raw),'banks':len(raw)//0x4000,'sha1':h1,'sha256':h256,'bank_rows':rows}

def rebuild(lossless_dir:str, outpath:str):
    out=bytearray()
    files=sorted(pathlib.Path(lossless_dir).glob('bank_*.asm'))
    for p in files:
        for line in p.read_text(encoding='utf-8').splitlines():
            code=line.split(';',1)[0]
            if 'db ' not in code: continue
            rhs=code.split('db ',1)[1]
            for tok in rhs.split(','):
                tok=tok.strip()
                if tok.startswith('$'): out.append(int(tok[1:],16))
    pathlib.Path(outpath).write_bytes(out)
    return bytes(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rom',action='append',nargs=3,metavar=('PATH','OUTDIR','TAG'))
    ap.add_argument('--manifest')
    ap.add_argument('--verify',action='store_true')
    args=ap.parse_args()
    results=[]
    for path,outdir,tag in args.rom or []:
        r=disasm_rom(path,outdir,tag); results.append(r)
        if args.verify:
            rebuilt=rebuild(os.path.join(outdir,'lossless'),os.path.join(outdir,f'{tag.lower()}_rebuilt_verify.gb'))
            orig=pathlib.Path(path).read_bytes()
            if rebuilt != orig: raise SystemExit(f'rebuild mismatch: {tag}')
            os.remove(os.path.join(outdir,f'{tag.lower()}_rebuilt_verify.gb'))
            r['lossless_rebuild_verified']=True
    if args.manifest:
        pathlib.Path(args.manifest).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='bank_rows'} for r in results],indent=2))
if __name__=='__main__': main()
