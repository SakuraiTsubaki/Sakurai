#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from collections import deque, defaultdict
import argparse, csv, hashlib, json

REGS = ['b','c','d','e','h','l','[hl]','a']
ALU = ['add a','adc a','sub','sbc a','and','xor','or','cp']
COND = ['nz','z','nc','c']

BASE = {
0x00:('nop',1),0x01:('ld bc,{d16}',3),0x02:('ld [bc],a',1),0x03:('inc bc',1),
0x04:('inc b',1),0x05:('dec b',1),0x06:('ld b,{d8}',2),0x07:('rlca',1),
0x08:('ld [{a16}],sp',3),0x09:('add hl,bc',1),0x0A:('ld a,[bc]',1),0x0B:('dec bc',1),
0x0C:('inc c',1),0x0D:('dec c',1),0x0E:('ld c,{d8}',2),0x0F:('rrca',1),
0x10:('stop {d8}',2),0x11:('ld de,{d16}',3),0x12:('ld [de],a',1),0x13:('inc de',1),
0x14:('inc d',1),0x15:('dec d',1),0x16:('ld d,{d8}',2),0x17:('rla',1),
0x18:('jr {r8}',2),0x19:('add hl,de',1),0x1A:('ld a,[de]',1),0x1B:('dec de',1),
0x1C:('inc e',1),0x1D:('dec e',1),0x1E:('ld e,{d8}',2),0x1F:('rra',1),
0x20:('jr nz,{r8}',2),0x21:('ld hl,{d16}',3),0x22:('ld [hli],a',1),0x23:('inc hl',1),
0x24:('inc h',1),0x25:('dec h',1),0x26:('ld h,{d8}',2),0x27:('daa',1),
0x28:('jr z,{r8}',2),0x29:('add hl,hl',1),0x2A:('ld a,[hli]',1),0x2B:('dec hl',1),
0x2C:('inc l',1),0x2D:('dec l',1),0x2E:('ld l,{d8}',2),0x2F:('cpl',1),
0x30:('jr nc,{r8}',2),0x31:('ld sp,{d16}',3),0x32:('ld [hld],a',1),0x33:('inc sp',1),
0x34:('inc [hl]',1),0x35:('dec [hl]',1),0x36:('ld [hl],{d8}',2),0x37:('scf',1),
0x38:('jr c,{r8}',2),0x39:('add hl,sp',1),0x3A:('ld a,[hld]',1),0x3B:('dec sp',1),
0x3C:('inc a',1),0x3D:('dec a',1),0x3E:('ld a,{d8}',2),0x3F:('ccf',1),
0xC0:('ret nz',1),0xC1:('pop bc',1),0xC2:('jp nz,{a16}',3),0xC3:('jp {a16}',3),
0xC4:('call nz,{a16}',3),0xC5:('push bc',1),0xC6:('add a,{d8}',2),0xC7:('rst $00',1),
0xC8:('ret z',1),0xC9:('ret',1),0xCA:('jp z,{a16}',3),0xCB:('cb',2),
0xCC:('call z,{a16}',3),0xCD:('call {a16}',3),0xCE:('adc a,{d8}',2),0xCF:('rst $08',1),
0xD0:('ret nc',1),0xD1:('pop de',1),0xD2:('jp nc,{a16}',3),0xD3:('db $d3 ; undefined',1),
0xD4:('call nc,{a16}',3),0xD5:('push de',1),0xD6:('sub {d8}',2),0xD7:('rst $10',1),
0xD8:('ret c',1),0xD9:('reti',1),0xDA:('jp c,{a16}',3),0xDB:('db $db ; undefined',1),
0xDC:('call c,{a16}',3),0xDD:('db $dd ; undefined',1),0xDE:('sbc a,{d8}',2),0xDF:('rst $18',1),
0xE0:('ldh [{a8}],a',2),0xE1:('pop hl',1),0xE2:('ldh [c],a',1),0xE3:('db $e3 ; undefined',1),
0xE4:('db $e4 ; undefined',1),0xE5:('push hl',1),0xE6:('and {d8}',2),0xE7:('rst $20',1),
0xE8:('add sp,{s8}',2),0xE9:('jp hl',1),0xEA:('ld [{a16}],a',3),0xEB:('db $eb ; undefined',1),
0xEC:('db $ec ; undefined',1),0xED:('db $ed ; undefined',1),0xEE:('xor {d8}',2),0xEF:('rst $28',1),
0xF0:('ldh a,[{a8}]',2),0xF1:('pop af',1),0xF2:('ldh a,[c]',1),0xF3:('di',1),
0xF4:('db $f4 ; undefined',1),0xF5:('push af',1),0xF6:('or {d8}',2),0xF7:('rst $30',1),
0xF8:('ld hl,sp+{s8}',2),0xF9:('ld sp,hl',1),0xFA:('ld a,[{a16}]',3),0xFB:('ei',1),
0xFC:('db $fc ; undefined',1),0xFD:('db $fd ; undefined',1),0xFE:('cp {d8}',2),0xFF:('rst $38',1),
}
for op in range(0x40,0x80):
    if op == 0x76: BASE[op] = ('halt',1)
    else: BASE[op] = (f'ld {REGS[(op>>3)&7]},{REGS[op&7]}',1)
for op in range(0x80,0xC0): BASE[op]=(f'{ALU[(op>>3)&7]} {REGS[op&7]}',1)
UNDEF={0xD3,0xDB,0xDD,0xE3,0xE4,0xEB,0xEC,0xED,0xF4,0xFC,0xFD}

def cb_mnemonic(op:int)->str:
    r=REGS[op&7]; group=op>>6
    if group==0:
        ops=['rlc','rrc','rl','rr','sla','sra','swap','srl']; return f'{ops[(op>>3)&7]} {r}'
    bit=(op>>3)&7; return f'{["bit","res","set"][group-1]} {bit},{r}'
def s8(x:int)->int: return x-256 if x>=128 else x
def fmt8(x:int)->str: return f'${x:02X}'
def fmt16(x:int)->str: return f'${x:04X}'

class Insn:
    __slots__=('addr','op','size','raw','text','kind','target','conditional','undefined')
    def __init__(self,addr,op,size,raw,text,kind='normal',target=None,conditional=False,undefined=False):
        self.addr=addr; self.op=op; self.size=size; self.raw=raw; self.text=text; self.kind=kind; self.target=target; self.conditional=conditional; self.undefined=undefined

def decode(buf:bytes, pos:int, cpu_addr:int)->Insn|None:
    if pos>=len(buf): return None
    op=buf[pos]
    if op==0xCB:
        if pos+1>=len(buf): return None
        return Insn(cpu_addr,op,2,buf[pos:pos+2],cb_mnemonic(buf[pos+1]))
    tpl,size=BASE.get(op,(f'db ${op:02x} ; unknown',1))
    if pos+size>len(buf): return None
    raw=buf[pos:pos+size]; d8=raw[1] if size>=2 else 0; d16=(raw[1]|(raw[2]<<8)) if size>=3 else 0; rel=(cpu_addr+2+s8(d8))&0xFFFF
    text=tpl.replace('{d8}',fmt8(d8)).replace('{d16}',fmt16(d16)).replace('{a16}',fmt16(d16)).replace('{a8}',f'$FF{d8:02X}').replace('{s8}',f'{s8(d8):+d}').replace('{r8}',fmt16(rel))
    kind='normal'; target=None; cond=False
    if op in (0x18,0x20,0x28,0x30,0x38): kind='jr'; target=rel; cond=(op!=0x18)
    elif op in (0xC2,0xC3,0xCA,0xD2,0xDA): kind='jp'; target=d16; cond=(op!=0xC3)
    elif op in (0xC4,0xCC,0xCD,0xD4,0xDC): kind='call'; target=d16; cond=(op!=0xCD)
    elif op in (0xC0,0xC8,0xC9,0xD0,0xD8,0xD9): kind='ret'; cond=(op not in (0xC9,0xD9))
    elif op==0xE9: kind='jp_indirect'
    elif op in (0xC7,0xCF,0xD7,0xDF,0xE7,0xEF,0xF7,0xFF): kind='rst'; target=op&0x38
    elif op==0x10: kind='stop'
    return Insn(cpu_addr,op,size,raw,text,kind,target,cond,op in UNDEF)

def scan_farcall_seeds(data:bytes):
    out=defaultdict(set); n=len(data)
    for i in range(n-5):
        if data[i]==0x3E and data[i+2]==0x21 and data[i+5]==0xCF:
            bank=data[i+1]; addr=data[i+3]|(data[i+4]<<8)
            if 0x4000<=addr<0x8000 and bank < n//0x4000: out[bank].add(addr)
        if data[i]==0x21 and data[i+3]==0x3E and data[i+5]==0xCF:
            addr=data[i+1]|(data[i+2]<<8); bank=data[i+4]
            if 0x4000<=addr<0x8000 and bank < n//0x4000: out[bank].add(addr)
    return out

KNOWN_SEEDS = {0x21:[0x4000],0x23:[0x4000],0x24:[0x4000],0x25:[0x65F9],0x2E:[0x6300]}
KNOWN_NONCPU = {
    'EN': {0x20,0x22,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D,0x2F},
    'KR': {0x20,0x22,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D,0x2F},
    'EU': {0x20,0x22,0x26,0x28,0x29,0x2A,0x2B,0x2C,0x2D,0x2F},
    'JP': {0x20,0x22,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D,0x2F},
}
def region_of(name:str)->str:
    if 'Korea' in name: return 'KR'
    if 'Japan' in name: return 'JP'
    if 'USA, Europe' in name: return 'EN'
    return 'EU'

def recursive_disasm(data:bytes, bank:int, seeds:set[int], max_insns=50000):
    bankbuf=data[bank*0x4000:(bank+1)*0x4000]; todo=deque(sorted(a for a in seeds if 0x4000<=a<0x8000)); decoded={}; block_starts=set(todo)
    while todo and len(decoded)<max_insns:
        pc=todo.popleft()
        if pc in decoded or not (0x4000<=pc<0x8000): continue
        while 0x4000<=pc<0x8000 and pc not in decoded and len(decoded)<max_insns:
            ins=decode(bankbuf,pc-0x4000,pc)
            if ins is None: break
            decoded[pc]=ins; nxt=pc+ins.size
            if ins.undefined: break
            if ins.kind in ('jr','jp') and ins.target is not None:
                if 0x4000<=ins.target<0x8000: todo.append(ins.target); block_starts.add(ins.target)
                if not ins.conditional: break
            elif ins.kind=='call' and ins.target is not None:
                if 0x4000<=ins.target<0x8000: todo.append(ins.target); block_starts.add(ins.target)
            elif ins.kind=='rst' and ins.target==0x28:
                prev_pc=max((cand for cand in decoded if cand<pc),default=None)
                if prev_pc is not None:
                    prev=decoded[prev_pc]
                    if prev.op==0x21 and prev.size==3:
                        table=prev.raw[1]|(prev.raw[2]<<8)
                        if 0x4000<=table<0x8000:
                            tpos=table-0x4000
                            for j in range(64):
                                q=tpos+2*j
                                if q+1>=len(bankbuf): break
                                ptr=bankbuf[q]|(bankbuf[q+1]<<8)
                                if not (0x4000<=ptr<0x8000): break
                                todo.append(ptr); block_starts.add(ptr)
            elif ins.kind=='ret' and not ins.conditional: break
            elif ins.kind in ('jp_indirect','stop'): break
            pc=nxt
    return decoded,block_starts

def label_for(bank,addr,seedset,block_starts):
    if addr in seedset: return f'Bank{bank:02X}_Entry_{addr:04X}'
    if addr in block_starts: return f'.L_{addr:04X}'
    return None

def emit_asm(path:Path, romname:str, bank:int, decoded, block_starts, seeds):
    path.parent.mkdir(parents=True,exist_ok=True); lines=[f'; Auto recursive LR35902 disassembly candidate',f'; ROM: {romname}',f'; Bank: ${bank:02X}','; IMPORTANT: only control-flow-reachable CPU code is emitted.','; Unreached bytes are deliberately not decoded as CPU instructions.','']
    for addr in sorted(decoded):
        lab=label_for(bank,addr,seeds,block_starts)
        if lab: lines.append(lab+'::' if not lab.startswith('.') else lab+':')
        ins=decoded[addr]; raw=' '.join(f'{b:02X}' for b in ins.raw); lines.append(f'    {ins.text:<24} ; {bank:02X}:{addr:04X}  {raw}')
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',type=Path,default=Path('/mnt/data')); ap.add_argument('--output',type=Path,default=Path('/mnt/data/gold_full_disassembly/semantic_disasm')); ap.add_argument('--banks',default='20-2F'); args=ap.parse_args()
    if '-' in args.banks: a,b=args.banks.split('-',1); banks=range(int(a,16),int(b,16)+1)
    else: banks=[int(x,16) for x in args.banks.split(',')]
    rows=[]
    for rom in sorted(args.input.glob('*.gbc')):
        data=rom.read_bytes(); region=region_of(rom.name); far=scan_farcall_seeds(data); slug=''.join(c.lower() if c.isalnum() else '-' for c in rom.stem).strip('-')
        while '--' in slug: slug=slug.replace('--','-')
        for bank in banks:
            if bank>=len(data)//0x4000: continue
            seeds=set(far.get(bank,set()))
            if bank in KNOWN_SEEDS: seeds.update(KNOWN_SEEDS[bank])
            if region=='EU' and bank==0x27 and far.get(bank): seeds.update(far[bank])
            if bank in KNOWN_NONCPU.get(region,set()) and not (region=='EU' and bank==0x27): decoded={}; blocks=set()
            else: decoded,blocks=recursive_disasm(data,bank,seeds)
            out=args.output/slug/f'bank_{bank:02X}_code.asm'
            if decoded: emit_asm(out,rom.name,bank,decoded,blocks,seeds)
            covered=sum(i.size for i in decoded.values()); rows.append({'rom':rom.name,'region':region,'bank':f'{bank:02X}','farcall_seed_count':len(far.get(bank,set())),'seed_count_total':len(seeds),'decoded_instruction_count':len(decoded),'decoded_byte_count':covered,'bank_coverage_percent':f'{100*covered/0x4000:.3f}','asm_file':str(out.relative_to(args.output)) if decoded else '','status':'cpu-code-partial' if decoded else 'noncpu-or-no-reachable-code'})
    args.output.mkdir(parents=True,exist_ok=True)
    with (args.output/'coverage.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    summary={'roms':len({r['rom'] for r in rows}),'rows':len(rows),'decoded_bytes':sum(r['decoded_byte_count'] for r in rows),'decoded_instructions':sum(r['decoded_instruction_count'] for r in rows),'method':'recursive LR35902 traversal from farcall targets and verified section starts; non-CPU script/data banks excluded'}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
