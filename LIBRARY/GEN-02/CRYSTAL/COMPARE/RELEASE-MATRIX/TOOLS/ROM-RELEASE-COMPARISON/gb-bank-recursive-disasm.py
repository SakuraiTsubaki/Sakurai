#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, collections

# LR35902 recursive control-flow disassembler.
# Conservative: only follows explicit intra-bank control-flow targets.

R8 = ['b','c','d','e','h','l','[hl]','a']
RP = ['bc','de','hl','sp']
RP2 = ['bc','de','hl','af']
CC = ['nz','z','nc','c']
ALU = ['add a,','adc a,','sub','sbc a,','and','xor','or','cp']
ROT = ['rlc','rrc','rl','rr','sla','sra','swap','srl']


def s8(x): return x-256 if x & 0x80 else x

def u16(data, i): return data[i] | (data[i+1] << 8)

def fmt8(v): return f'${v:02X}'
def fmt16(v): return f'${v:04X}'


def decode_cb(op):
    x, y, z = op >> 6, (op >> 3) & 7, op & 7
    if x == 0: return f'{ROT[y]} {R8[z]}'
    if x == 1: return f'bit {y},{R8[z]}'
    if x == 2: return f'res {y},{R8[z]}'
    return f'set {y},{R8[z]}'


def decode(data, off, cpu):
    op = data[off]
    # (text, length, flow, target) flow: next, jmp, cjmp, call, ccall, ret, cret, stop, indirect
    if op == 0xCB:
        if off+1 >= len(data): return ('db $CB',1,'stop',None)
        return (decode_cb(data[off+1]),2,'next',None)

    # LD r,r (except HALT)
    if 0x40 <= op <= 0x7F:
        if op == 0x76: return ('halt',1,'stop',None)
        d,s=(op>>3)&7,op&7
        return (f'ld {R8[d]},{R8[s]}',1,'next',None)
    # ALU A,r
    if 0x80 <= op <= 0xBF:
        y,z=(op>>3)&7,op&7
        return (f'{ALU[y]} {R8[z]}',1,'next',None)
    # INC/DEC/LD r,n patterns
    if op < 0x40:
        if op & 0xC7 == 0x04:
            return (f'inc {R8[(op>>3)&7]}',1,'next',None)
        if op & 0xC7 == 0x05:
            return (f'dec {R8[(op>>3)&7]}',1,'next',None)
        if op & 0xC7 == 0x06:
            if off+1>=len(data): return (f'db {fmt8(op)}',1,'stop',None)
            return (f'ld {R8[(op>>3)&7]},{fmt8(data[off+1])}',2,'next',None)
        if op & 0xCF == 0x01:
            if off+2>=len(data): return (f'db {fmt8(op)}',1,'stop',None)
            return (f'ld {RP[(op>>4)&3]},{fmt16(u16(data,off+1))}',3,'next',None)
        if op & 0xCF == 0x03:
            return (f'inc {RP[(op>>4)&3]}',1,'next',None)
        if op & 0xCF == 0x0B:
            return (f'dec {RP[(op>>4)&3]}',1,'next',None)
        if op & 0xCF == 0x09:
            return (f'add hl,{RP[(op>>4)&3]}',1,'next',None)

    one = {
      0x00:'nop',0x02:'ld [bc],a',0x07:'rlca',0x08:None,0x0A:'ld a,[bc]',0x0F:'rrca',
      0x10:None,0x12:'ld [de],a',0x17:'rla',0x18:None,0x1A:'ld a,[de]',0x1F:'rra',
      0x20:None,0x22:'ld [hl+],a',0x27:'daa',0x28:None,0x2A:'ld a,[hl+]',0x2F:'cpl',
      0x30:None,0x32:'ld [hl-],a',0x37:'scf',0x38:None,0x3A:'ld a,[hl-]',0x3F:'ccf',
      0xC9:'ret',0xD9:'reti',0xE2:'ldh [c],a',0xE9:'jp hl',0xF2:'ldh a,[c]',0xF3:'di',0xFB:'ei'
    }
    if op in one and one[op] is not None:
        txt=one[op]
        if op in (0xC9,0xD9): return (txt,1,'ret',None)
        if op==0xE9: return (txt,1,'indirect',None)
        return (txt,1,'next',None)

    # JR / conditional JR
    if op == 0x18:
        if off+1>=len(data): return ('db $18',1,'stop',None)
        t=(cpu+2+s8(data[off+1])) & 0xFFFF
        return (f'jr {fmt16(t)}',2,'jmp',t)
    if op in (0x20,0x28,0x30,0x38):
        if off+1>=len(data): return (f'db {fmt8(op)}',1,'stop',None)
        t=(cpu+2+s8(data[off+1])) & 0xFFFF
        cc=CC[(op-0x20)//8]
        return (f'jr {cc},{fmt16(t)}',2,'cjmp',t)

    # STOP
    if op == 0x10:
        return ('stop',2 if off+1<len(data) else 1,'stop',None)

    # 16-bit immediate / memory ops
    if op == 0x08:
        if off+2>=len(data): return ('db $08',1,'stop',None)
        return (f'ld [{fmt16(u16(data,off+1))}],sp',3,'next',None)
    if op == 0xEA:
        if off+2>=len(data): return ('db $EA',1,'stop',None)
        return (f'ld [{fmt16(u16(data,off+1))}],a',3,'next',None)
    if op == 0xFA:
        if off+2>=len(data): return ('db $FA',1,'stop',None)
        return (f'ld a,[{fmt16(u16(data,off+1))}]',3,'next',None)
    if op == 0xE0:
        return (f'ldh [{fmt8(data[off+1])}],a',2,'next',None) if off+1<len(data) else ('db $E0',1,'stop',None)
    if op == 0xF0:
        return (f'ldh a,[{fmt8(data[off+1])}]',2,'next',None) if off+1<len(data) else ('db $F0',1,'stop',None)
    if op == 0xE8:
        return (f'add sp,{s8(data[off+1])}',2,'next',None) if off+1<len(data) else ('db $E8',1,'stop',None)
    if op == 0xF8:
        return (f'ld hl,sp+{s8(data[off+1])}',2,'next',None) if off+1<len(data) else ('db $F8',1,'stop',None)
    if op == 0xF9: return ('ld sp,hl',1,'next',None)

    # stack
    if op in (0xC1,0xD1,0xE1,0xF1): return (f'pop {RP2[(op>>4)&3]}',1,'next',None)
    if op in (0xC5,0xD5,0xE5,0xF5): return (f'push {RP2[(op>>4)&3]}',1,'next',None)

    # immediate ALU
    immalu={0xC6:'add a,',0xCE:'adc a,',0xD6:'sub',0xDE:'sbc a,',0xE6:'and',0xEE:'xor',0xF6:'or',0xFE:'cp'}
    if op in immalu:
        return (f'{immalu[op]} {fmt8(data[off+1])}',2,'next',None) if off+1<len(data) else (f'db {fmt8(op)}',1,'stop',None)

    # JP/CALL absolute
    if op == 0xC3:
        if off+2>=len(data): return ('db $C3',1,'stop',None)
        t=u16(data,off+1); return (f'jp {fmt16(t)}',3,'jmp',t)
    if op in (0xC2,0xCA,0xD2,0xDA):
        if off+2>=len(data): return (f'db {fmt8(op)}',1,'stop',None)
        t=u16(data,off+1); cc=CC[(op-0xC2)//8]
        return (f'jp {cc},{fmt16(t)}',3,'cjmp',t)
    if op == 0xCD:
        if off+2>=len(data): return ('db $CD',1,'stop',None)
        t=u16(data,off+1); return (f'call {fmt16(t)}',3,'call',t)
    if op in (0xC4,0xCC,0xD4,0xDC):
        if off+2>=len(data): return (f'db {fmt8(op)}',1,'stop',None)
        t=u16(data,off+1); cc=CC[(op-0xC4)//8]
        return (f'call {cc},{fmt16(t)}',3,'ccall',t)

    # conditional returns
    if op in (0xC0,0xC8,0xD0,0xD8):
        cc=CC[(op-0xC0)//8]; return (f'ret {cc}',1,'cret',None)

    # RST
    if op in (0xC7,0xCF,0xD7,0xDF,0xE7,0xEF,0xF7,0xFF):
        t=op & 0x38; return (f'rst {fmt8(t)}',1,'call',t)

    # undefined opcodes on GB CPU
    if op in (0xD3,0xDB,0xDD,0xE3,0xE4,0xEB,0xEC,0xED,0xF4,0xFC,0xFD):
        return (f'db {fmt8(op)} ; invalid opcode',1,'stop',None)

    # Remaining legal single-byte odds
    misc={0xD9:'reti'}
    if op in misc: return (misc[op],1,'ret',None)
    return (f'db {fmt8(op)} ; undecoded',1,'stop',None)


def in_same_bank(addr, bank):
    if bank == 0: return 0x0000 <= addr <= 0x3FFF
    return 0x4000 <= addr <= 0x7FFF


def bank_offset(addr, bank):
    return addr if bank == 0 else addr - 0x4000


def cpu_addr(off, bank):
    return off if bank == 0 else 0x4000 + off


def trace(bank_bytes, bank, seeds):
    q=collections.deque(seeds)
    seen_starts=set(); code_bytes=set(); insns={}; labels=set(seeds); external=[]
    while q:
        addr=q.popleft()
        if not in_same_bank(addr,bank): continue
        off=bank_offset(addr,bank)
        while 0 <= off < len(bank_bytes):
            addr=cpu_addr(off,bank)
            if addr in seen_starts: break
            seen_starts.add(addr)
            text,ln,flow,target=decode(bank_bytes,off,addr)
            if off+ln>len(bank_bytes): ln=1
            raw=bank_bytes[off:off+ln]
            insns[addr]=(raw,text,flow,target)
            code_bytes.update(range(off,off+ln))
            if target is not None:
                if in_same_bank(target,bank):
                    labels.add(target)
                    if flow in ('call','ccall','jmp','cjmp'): q.append(target)
                else:
                    external.append((addr,flow,target))
            if flow in ('ret','stop','indirect','jmp'):
                break
            # Conditional return has fallthrough; calls and conditional jumps fall through.
            off += ln
    return insns,code_bytes,labels,external


def ranges_from_set(indices, n):
    out=[]; i=0
    while i<n:
        kind=i in indices; j=i+1
        while j<n and ((j in indices)==kind): j+=1
        out.append((i,j-1,'code' if kind else 'unclassified'))
        i=j
    return out


def render(bank, insns, labels, bank_bytes, names):
    lines=[]
    for addr in sorted(insns):
        if addr in labels:
            label=names.get(addr, f'loc_{addr:04X}')
            lines.append(f'\n{label}:')
        raw,text,flow,target=insns[addr]
        bs=' '.join(f'{b:02X}' for b in raw)
        if target in names:
            text=text.replace(fmt16(target), names[target]).replace(fmt8(target), names[target])
        lines.append(f'    {text:<28} ; {addr:04X}: {bs}')
    return '\n'.join(lines).lstrip()+"\n"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom'); ap.add_argument('--bank',type=lambda x:int(x,0),required=True)
    ap.add_argument('--seeds',default=''); ap.add_argument('--names-json'); ap.add_argument('--out-prefix',required=True)
    args=ap.parse_args()
    rom=pathlib.Path(args.rom).read_bytes(); bank=args.bank
    start=bank*0x4000; bb=rom[start:start+0x4000]
    seeds=[int(x,0) for x in args.seeds.split(',') if x.strip()]
    names={}
    if args.names_json:
        obj=json.loads(pathlib.Path(args.names_json).read_text())
        names={int(k,0) if isinstance(k,str) else int(k):v for k,v in obj.items()}
    seeds=sorted(set(seeds)|set(names))
    insns,code_bytes,labels,external=trace(bb,bank,seeds)
    prefix=pathlib.Path(args.out_prefix); prefix.parent.mkdir(parents=True,exist_ok=True)
    prefix.with_suffix('.asm').write_text(render(bank,insns,labels,bb,names))
    report={
      'rom':str(args.rom),'bank':bank,'bank_hex':f'{bank:02X}','seeds':[f'0x{x:04X}' for x in seeds],
      'instruction_count':len(insns),'classified_code_bytes':len(code_bytes),'bank_bytes':len(bb),
      'coverage_percent':round(100*len(code_bytes)/len(bb),3),
      'labels':[{'address':f'0x{x:04X}','name':names.get(x,f'loc_{x:04X}')} for x in sorted(labels)],
      'external_control_flow':[{'from':f'0x{a:04X}','kind':f,'target':f'0x{t:04X}'} for a,f,t in external],
      'ranges':[{'start':f'0x{cpu_addr(a,bank):04X}','end':f'0x{cpu_addr(b,bank):04X}','kind':k} for a,b,k in ranges_from_set(code_bytes,len(bb))]
    }
    prefix.with_suffix('.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:report[k] for k in ('bank_hex','instruction_count','classified_code_bytes','coverage_percent')},indent=2))

if __name__=='__main__': main()
