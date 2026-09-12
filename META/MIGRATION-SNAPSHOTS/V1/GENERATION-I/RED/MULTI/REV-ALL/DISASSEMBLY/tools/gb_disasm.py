#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from pathlib import Path

R8 = ['b','c','d','e','h','l','[hl]','a']
RP = ['bc','de','hl','sp']
RP2 = ['bc','de','hl+','hl-']
RP2S = ['bc','de','hl','af']
CC = ['nz','z','nc','c']
ALU = ['add a,','adc a,','sub','sbc a,','and','xor','or','cp']
ROT = ['rlc','rrc','rl','rr','sla','sra','swap','srl']
MISC = ['rlca','rrca','rla','rra','daa','cpl','scf','ccf']

ILLEGAL = {0xD3,0xDB,0xDD,0xE3,0xE4,0xEB,0xEC,0xED,0xF4,0xFC,0xFD}

class Inst:
    __slots__=('pc','op','size','raw','text','kind','target')
    def __init__(self,pc,op,size,raw,text,kind='flow',target=None):
        self.pc=pc; self.op=op; self.size=size; self.raw=raw; self.text=text; self.kind=kind; self.target=target

def s8(x): return x-256 if x >= 128 else x

def u16le(data,i):
    if i+1 >= len(data): return None
    return data[i] | (data[i+1]<<8)

def decode(data, i, base=0):
    pc=base+i
    if i>=len(data): return None
    op=data[i]
    if op in ILLEGAL:
        return Inst(pc,op,1,data[i:i+1],f'db ${op:02x} ; illegal opcode','stop')
    if op==0xCB:
        if i+1>=len(data): return Inst(pc,op,1,data[i:i+1],'db $cb ; truncated prefix','stop')
        cb=data[i+1]; x=cb>>6; y=(cb>>3)&7; z=cb&7
        if x==0: text=f'{ROT[y]} {R8[z]}'
        elif x==1: text=f'bit {y},{R8[z]}'
        elif x==2: text=f'res {y},{R8[z]}'
        else: text=f'set {y},{R8[z]}'
        return Inst(pc,op,2,data[i:i+2],text)
    x=op>>6; y=(op>>3)&7; z=op&7; p=y>>1; q=y&1
    n8 = data[i+1] if i+1 < len(data) else None
    n16 = u16le(data,i+1)
    def imm8(): return f'${n8:02x}' if n8 is not None else '$??'
    def imm16(): return f'${n16:04x}' if n16 is not None else '$????'
    size=1; text=''; kind='flow'; target=None
    if x==0:
        if z==0:
            if y==0: text='nop'
            elif y==1: size=3; text=f'ld [{imm16()}],sp'
            elif y==2: size=2; text='stop $00'; kind='stop'
            elif y==3:
                size=2; target=(pc+2+s8(n8 or 0))&0xffff; text=f'jr ${target:04x}'; kind='jump'
            else:
                size=2; target=(pc+2+s8(n8 or 0))&0xffff; text=f'jr {CC[y-4]},${target:04x}'; kind='cjump'
        elif z==1:
            if q==0: size=3; text=f'ld {RP[p]},{imm16()}'
            else: text=f'add hl,{RP[p]}'
        elif z==2:
            if q==0: text=f'ld [{RP2[p]}],a'
            else: text=f'ld a,[{RP2[p]}]'
        elif z==3:
            text=f'{"inc" if q==0 else "dec"} {RP[p]}'
        elif z==4: text=f'inc {R8[y]}'
        elif z==5: text=f'dec {R8[y]}'
        elif z==6: size=2; text=f'ld {R8[y]},{imm8()}'
        else: text=MISC[y]
    elif x==1:
        if y==6 and z==6: text='halt'; kind='stop'
        else: text=f'ld {R8[y]},{R8[z]}'
    elif x==2:
        text=f'{ALU[y]} {R8[z]}'
    else:
        if z==0:
            if y<4: text=f'ret {CC[y]}'; kind='cret'
            elif y==4: size=2; text=f'ldh [{imm8()}],a'
            elif y==5: size=2; text=f'add sp,{s8(n8 or 0):+d}'
            elif y==6: size=2; text=f'ldh a,[{imm8()}]'
            else: size=2; text=f'ld hl,sp{s8(n8 or 0):+d}'
        elif z==1:
            if q==0: text=f'pop {RP2S[p]}'
            else:
                if p==0: text='ret'; kind='ret'
                elif p==1: text='reti'; kind='ret'
                elif p==2: text='jp hl'; kind='jump_indirect'
                else: text='ld sp,hl'
        elif z==2:
            if y<4: size=3; target=n16; text=f'jp {CC[y]},{imm16()}'; kind='cjump'
            elif y==4: text='ldh [c],a'
            elif y==5: size=3; text=f'ld [{imm16()}],a'
            elif y==6: text='ldh a,[c]'
            else: size=3; text=f'ld a,[{imm16()}]'
        elif z==3:
            if y==0: size=3; target=n16; text=f'jp {imm16()}'; kind='jump'
            elif y==1: text='prefix cb'; kind='stop'
            elif y==6: text='di'
            elif y==7: text='ei'
            else: text=f'db ${op:02x} ; illegal opcode'; kind='stop'
        elif z==4:
            if y<4: size=3; target=n16; text=f'call {CC[y]},{imm16()}'; kind='ccall'
            else: text=f'db ${op:02x} ; illegal opcode'; kind='stop'
        elif z==5:
            if q==0: text=f'push {RP2S[p]}'
            elif p==0: size=3; target=n16; text=f'call {imm16()}'; kind='call'
            else: text=f'db ${op:02x} ; illegal opcode'; kind='stop'
        elif z==6:
            size=2; text=f'{ALU[y]} {imm8()}'
        else:
            target=y*8; text=f'rst ${target:02x}'; kind='call'
    raw=data[i:min(i+size,len(data))]
    if len(raw)<size:
        return Inst(pc,op,len(raw),raw,'db '+','.join(f'${b:02x}' for b in raw)+' ; truncated','stop')
    return Inst(pc,op,size,raw,text,kind,target)

def linear_listing(bankdata, bank):
    base=0 if bank==0 else 0x4000
    out=[]; i=0
    while i < len(bankdata):
        ins=decode(bankdata,i,base)
        raw=' '.join(f'{b:02X}' for b in ins.raw)
        out.append(f'{ins.pc:04X}: {raw:<8}  {ins.text}')
        i += max(1,ins.size)
    return '\n'.join(out)+'\n'

def lossless_skeleton(bankdata, bank, width=16):
    base=0 if bank==0 else 0x4000
    lines=[f'; Lossless byte skeleton — ROM bank ${bank:02X}',
           '; ROM-equivalent data. Keep local; semantic conversion replaces confirmed ranges.',
           f'SECTION "bank_{bank:02x}_raw", ROM{0 if bank==0 else "X"}' + ('' if bank==0 else f', BANK[${bank:02X}]'), '']
    for i in range(0,len(bankdata),width):
        chunk=bankdata[i:i+width]
        lines.append('    db ' + ', '.join(f'${b:02x}' for b in chunk) + f' ; ${base+i:04X}')
    return '\n'.join(lines)+'\n'

def parse_sym(path):
    syms={}
    if not path: return syms
    rx=re.compile(r'^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(.+?)\s*$')
    for line in Path(path).read_text(errors='replace').splitlines():
        m=rx.match(line)
        if m:
            b=int(m.group(1),16); a=int(m.group(2),16); name=m.group(3)
            syms.setdefault((b,a),[]).append(name)
    return syms

def annotated_listing(bankdata, bank, syms):
    base=0 if bank==0 else 0x4000
    out=[]; i=0
    while i<len(bankdata):
        pc=base+i
        for name in syms.get((bank,pc),[]): out.append(f'\n{name}:')
        ins=decode(bankdata,i,base)
        raw=' '.join(f'{b:02X}' for b in ins.raw)
        note=''
        if ins.target is not None:
            tb = 0 if ins.target < 0x4000 else bank if ins.target < 0x8000 else None
            if tb is not None and (tb,ins.target) in syms:
                note=' ; -> '+syms[(tb,ins.target)][0]
        out.append(f'{pc:04X}: {raw:<8}  {ins.text}{note}')
        i+=max(1,ins.size)
    return '\n'.join(out)+'\n'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom')
    ap.add_argument('-o','--out',required=True)
    ap.add_argument('--sym')
    ap.add_argument('--banks',default='all',help='all or comma/ranges e.g. 00,02-05')
    args=ap.parse_args()
    rom=Path(args.rom).read_bytes(); n=(len(rom)+0x3fff)//0x4000
    if args.banks=='all': banks=range(n)
    else:
        bs=[]
        for p in args.banks.split(','):
            if '-' in p:
                a,b=p.split('-',1); bs.extend(range(int(a,16),int(b,16)+1))
            else: bs.append(int(p,16))
        banks=[b for b in bs if b<n]
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    syms=parse_sym(args.sym)
    manifest={'rom':Path(args.rom).name,'size':len(rom),'sha1':hashlib.sha1(rom).hexdigest(),'banks':n,'outputs':[]}
    for b in banks:
        chunk=rom[b*0x4000:(b+1)*0x4000]
        sk=out/f'bank_{b:02X}.raw.asm'; ls=out/f'bank_{b:02X}.linear.lst'
        sk.write_text(lossless_skeleton(chunk,b))
        ls.write_text(annotated_listing(chunk,b,syms) if syms else linear_listing(chunk,b))
        manifest['outputs'].append({'bank':b,'size':len(chunk),'sha1':hashlib.sha1(chunk).hexdigest(),'raw_asm':sk.name,'linear_listing':ls.name})
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
