#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

R8 = ["b","c","d","e","h","l","[hl]","a"]
RP = ["bc","de","hl","sp"]
RP2 = ["bc","de","hl","af"]
CC = ["nz","z","nc","c"]
ALU = ["add a, {}","adc a, {}","sub {}","sbc a, {}","and {}","xor {}","or {}","cp {}"]
ROT = ["rlc {}","rrc {}","rl {}","rr {}","sla {}","sra {}","swap {}","srl {}"]


def u16(b, i):
    return b[i] | (b[i+1] << 8)

def s8(x):
    return x - 256 if x >= 128 else x

def h8(x): return f"${x:02x}"
def h16(x): return f"${x:04x}"

def decode_cb(op):
    x=(op>>6)&3; y=(op>>3)&7; z=op&7
    r=R8[z]
    if x==0: return ROT[y].format(r)
    if x==1: return f"bit {y}, {r}"
    if x==2: return f"res {y}, {r}"
    return f"set {y}, {r}"

def decode(buf, i, cpu_addr):
    op=buf[i]
    x=(op>>6)&3; y=(op>>3)&7; z=op&7; p=y>>1; q=y&1
    def need(n):
        return i+n <= len(buf)
    if op==0xCB:
        if not need(2): return 1, f"db {h8(op)} ; truncated"
        return 2, decode_cb(buf[i+1])
    if x==0:
        if z==0:
            if y==0: return 1,"nop"
            if y==1:
                if not need(3): return 1,f"db {h8(op)} ; truncated"
                return 3,f"ld [{h16(u16(buf,i+1))}], sp"
            if y==2:
                if not need(2): return 1,f"db {h8(op)} ; truncated"
                return 2,"stop"
            if y==3:
                if not need(2): return 1,f"db {h8(op)} ; truncated"
                target=(cpu_addr+2+s8(buf[i+1])) & 0xffff
                return 2,f"jr {h16(target)}"
            if not need(2): return 1,f"db {h8(op)} ; truncated"
            target=(cpu_addr+2+s8(buf[i+1])) & 0xffff
            return 2,f"jr {CC[y-4]}, {h16(target)}"
        if z==1:
            if q==0:
                if not need(3): return 1,f"db {h8(op)} ; truncated"
                return 3,f"ld {RP[p]}, {h16(u16(buf,i+1))}"
            return 1,f"add hl, {RP[p]}"
        if z==2:
            if q==0:
                forms=["ld [bc], a","ld [de], a","ld [hli], a","ld [hld], a"]
            else:
                forms=["ld a, [bc]","ld a, [de]","ld a, [hli]","ld a, [hld]"]
            return 1,forms[p]
        if z==3:
            return 1,(f"inc {RP[p]}" if q==0 else f"dec {RP[p]}")
        if z==4: return 1,f"inc {R8[y]}"
        if z==5: return 1,f"dec {R8[y]}"
        if z==6:
            if not need(2): return 1,f"db {h8(op)} ; truncated"
            return 2,f"ld {R8[y]}, {h8(buf[i+1])}"
        ops=["rlca","rrca","rla","rra","daa","cpl","scf","ccf"]
        return 1,ops[y]
    if x==1:
        if y==6 and z==6: return 1,"halt"
        return 1,f"ld {R8[y]}, {R8[z]}"
    if x==2:
        return 1,ALU[y].format(R8[z])
    # x == 3
    if z==0:
        if y<4: return 1,f"ret {CC[y]}"
        if y==4:
            if not need(2): return 1,f"db {h8(op)} ; truncated"
            return 2,f"ldh [{h8(buf[i+1])}], a"
        if y==5:
            if not need(2): return 1,f"db {h8(op)} ; truncated"
            return 2,f"add sp, {s8(buf[i+1]):+d}"
        if y==6:
            if not need(2): return 1,f"db {h8(op)} ; truncated"
            return 2,f"ldh a, [{h8(buf[i+1])}]"
        if not need(2): return 1,f"db {h8(op)} ; truncated"
        return 2,f"ld hl, sp{s8(buf[i+1]):+d}"
    if z==1:
        if q==0: return 1,f"pop {RP2[p]}"
        return 1,["ret","reti","jp hl","ld sp, hl"][p]
    if z==2:
        if y<4:
            if not need(3): return 1,f"db {h8(op)} ; truncated"
            return 3,f"jp {CC[y]}, {h16(u16(buf,i+1))}"
        if y==4: return 1,"ldh [c], a"
        if y==5:
            if not need(3): return 1,f"db {h8(op)} ; truncated"
            return 3,f"ld [{h16(u16(buf,i+1))}], a"
        if y==6: return 1,"ldh a, [c]"
        if not need(3): return 1,f"db {h8(op)} ; truncated"
        return 3,f"ld a, [{h16(u16(buf,i+1))}]"
    if z==3:
        if y==0:
            if not need(3): return 1,f"db {h8(op)} ; truncated"
            return 3,f"jp {h16(u16(buf,i+1))}"
        if y==1: return 1,f"db $cb ; orphan prefix"
        if y==6: return 1,"di"
        if y==7: return 1,"ei"
        return 1,f"db {h8(op)} ; illegal LR35902 opcode"
    if z==4:
        if y<4:
            if not need(3): return 1,f"db {h8(op)} ; truncated"
            return 3,f"call {CC[y]}, {h16(u16(buf,i+1))}"
        return 1,f"db {h8(op)} ; illegal LR35902 opcode"
    if z==5:
        if q==0: return 1,f"push {RP2[p]}"
        if p==0:
            if not need(3): return 1,f"db {h8(op)} ; truncated"
            return 3,f"call {h16(u16(buf,i+1))}"
        return 1,f"db {h8(op)} ; illegal LR35902 opcode"
    if z==6:
        if not need(2): return 1,f"db {h8(op)} ; truncated"
        return 2,ALU[y].format(h8(buf[i+1]))
    return 1,f"rst {h8(y*8)}"

def disassemble_bank(data: bytes, bank: int, start=0, end=None):
    if end is None: end=len(data)
    i=start
    lines=[]
    base_cpu=0 if bank==0 else 0x4000
    while i<end:
        cpu=base_cpu+i
        n,asm=decode(data,i,cpu)
        if i+n>end: n=1; asm=f"db {h8(data[i])} ; boundary"
        raw=' '.join(f'{x:02X}' for x in data[i:i+n])
        lines.append(f"{cpu:04X}: {raw:<9}  {asm}")
        i += n
    return lines

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom')
    ap.add_argument('--bank',type=lambda x:int(x,0),required=True)
    ap.add_argument('--out')
    args=ap.parse_args()
    rom=Path(args.rom).read_bytes()
    off=args.bank*0x4000
    bank=rom[off:off+0x4000]
    if not bank: raise SystemExit('bank absent')
    header=[f"; Mechanical LR35902 decode candidate",f"; source: {Path(args.rom).name}",f"; bank: ${args.bank:02X}",f"; ROM offsets: ${off:06X}-${off+len(bank)-1:06X}","; WARNING: linear decoding does not distinguish code from data; semantic audit overrides this listing.",""]
    text='\n'.join(header+disassemble_bank(bank,args.bank))+"\n"
    if args.out: Path(args.out).write_text(text,encoding='utf-8')
    else: print(text,end='')
if __name__=='__main__': main()
