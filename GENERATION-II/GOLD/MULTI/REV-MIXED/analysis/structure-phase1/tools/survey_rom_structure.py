#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,math
from collections import Counter,deque
from pathlib import Path

BANK=0x4000
R=['b','c','d','e','h','l','[hl]','a']
RP=['bc','de','hl','sp']
RP2=['bc','de','hl','af']
CC=['nz','z','nc','c']
ALU=['add a,','adc a,','sub','sbc a,','and','xor','or','cp']
ROT=['rlc','rrc','rl','rr','sla','sra','swap','srl']

# Return (len, mnemonic, flow_kind, target)
def decode(d,pc):
    op=d[pc]
    def b(i=1): return d[pc+i] if pc+i<len(d) else 0
    def w(): return b(1)|(b(2)<<8)
    def rel():
        n=b(1); n=n-256 if n>=128 else n
        return (pc+2+n)&0xffff
    if op==0xcb:
        if pc+1>=len(d): return 1,'db $cb','fall',None
        q=b(1); x=q>>6;y=(q>>3)&7;z=q&7
        if x==0:m=f'{ROT[y]} {R[z]}'
        elif x==1:m=f'bit {y},{R[z]}'
        elif x==2:m=f'res {y},{R[z]}'
        else:m=f'set {y},{R[z]}'
        return 2,m,'fall',None
    x=op>>6;y=(op>>3)&7;z=op&7;p=y>>1;q=y&1
    if x==0:
        if z==0:
            if y==0:return 1,'nop','fall',None
            if y==1:return 3,f'ld [${w():04x}],sp','fall',None
            if y==2:return 2,'stop','fall',None
            if y==3:return 2,f'jr ${rel():04x}','jump',rel()
            return 2,f'jr {CC[y-4]},${rel():04x}','cond',rel()
        if z==1:
            return (3,f'ld {RP[p]},${w():04x}','fall',None) if q==0 else (1,f'add hl,{RP[p]}','fall',None)
        if z==2:
            rp=['bc','de','hli','hld'][p]
            return 1,(f'ld [{rp}],a' if q==0 else f'ld a,[{rp}]'),'fall',None
        if z==3:return 1,(f'inc {RP[p]}' if q==0 else f'dec {RP[p]}'),'fall',None
        if z==4:return 1,f'inc {R[y]}','fall',None
        if z==5:return 1,f'dec {R[y]}','fall',None
        if z==6:return 2,f'ld {R[y]},${b():02x}','fall',None
        return 1,['rlca','rrca','rla','rra','daa','cpl','scf','ccf'][y],'fall',None
    if x==1:
        if y==6 and z==6:return 1,'halt','fall',None
        return 1,f'ld {R[y]},{R[z]}','fall',None
    if x==2:return 1,f'{ALU[y]} {R[z]}','fall',None
    # x=3
    if z==0:
        if y<4:return 1,f'ret {CC[y]}','condret',None
        if y==4:return 2,f'ldh [$ff00+${b():02x}],a','fall',None
        if y==5:return 2,f'add sp,{(b()-256 if b()>=128 else b())}','fall',None
        if y==6:return 2,f'ldh a,[$ff00+${b():02x}]','fall',None
        return 2,f'ld hl,sp+{(b()-256 if b()>=128 else b())}','fall',None
    if z==1:
        if q==0:return 1,f'pop {RP2[p]}','fall',None
        if p==0:return 1,'ret','ret',None
        if p==1:return 1,'reti','ret',None
        if p==2:return 1,'jp hl','indirect',None
        return 1,'ld sp,hl','fall',None
    if z==2:
        if y<4:return 3,f'jp {CC[y]},${w():04x}','cond',w()
        if y==4:return 1,'ld [$ff00+c],a','fall',None
        if y==5:return 3,f'ld [${w():04x}],a','fall',None
        if y==6:return 1,'ld a,[$ff00+c]','fall',None
        return 3,f'ld a,[${w():04x}]','fall',None
    if z==3:
        if y==0:return 3,f'jp ${w():04x}','jump',w()
        if y==1:return 1,'prefix cb','fall',None
        if y==6:return 1,'di','fall',None
        if y==7:return 1,'ei','fall',None
        return 1,f'db ${op:02x} ; invalid','invalid',None
    if z==4:
        if y<4:return 3,f'call {CC[y]},${w():04x}','condcall',w()
        return 1,f'db ${op:02x} ; invalid','invalid',None
    if z==5:
        if q==0:return 1,f'push {RP2[p]}','fall',None
        if p==0:return 3,f'call ${w():04x}','call',w()
        return 1,f'db ${op:02x} ; invalid','invalid',None
    if z==6:return 2,f'{ALU[y]} ${b():02x}','fall',None
    return 1,f'rst ${y*8:02x}','rst',y*8

def cfg_bank0(d):
    seeds={0x0000:'ResetVector',0x0008:'FarCall',0x0010:'Bankswitch',0x0018:'Rst18Trap',0x0020:'Rst20Trap',0x0028:'JumpTable',0x0038:'Rst38Trap',0x0040:'VBlankVector',0x0048:'LCDVector',0x0050:'TimerVector',0x0058:'SerialVector',0x0060:'JoypadVector',0x0100:'Start'}
    q=deque(seeds); visited={}; labels=dict(seeds); edges=[]
    # Semantic names that can be inferred from the standard Gen II vector layout.
    for vec,name in [(0x0008,'FarCall_hl'),(0x0040,'VBlank'),(0x0048,'LCD'),(0x0058,'Serial'),(0x0060,'Joypad'),(0x0101,'_Start')]:
        ln,mn,flow,tgt=decode(d,vec)
        if tgt is not None and 0<=tgt<0x4000:
            labels[tgt]=name
    while q:
        pc=q.popleft()
        if not (0<=pc<0x4000): continue
        # walk basic block
        while 0<=pc<0x4000 and pc not in visited:
            ln,mn,flow,tgt=decode(d,pc)
            raw=d[pc:pc+ln]
            visited[pc]={'len':ln,'mnemonic':mn,'bytes':raw.hex(),'flow':flow,'target':tgt}
            nxt=pc+ln
            if tgt is not None and 0<=tgt<0x4000:
                labels.setdefault(tgt,f'loc_{tgt:04x}')
                edges.append((pc,tgt,flow))
                q.append(tgt)
            if flow in ('jump','ret','indirect'):
                break
            if flow in ('cond','condcall','call','rst'):
                # fall-through continues; target queued above
                pass
            if flow=='invalid':
                break
            pc=nxt
    return seeds,labels,visited,edges

def long_runs(d,minlen=32):
    out=[];i=0
    while i<len(d):
        v=d[i];j=i+1
        while j<len(d) and d[j]==v:j+=1
        n=j-i
        if n>=minlen and v in (0,0xff):out.append((i,j-1,n,v,i//BANK))
        i=j
    return out

def entropy(block):
    if not block:return 0.0
    c=Counter(block); n=len(block)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def pointer_table_candidates(d,min_words=4):
    # Unaligned scan; contiguous LE words that all point into a ROM CPU window.
    # To reduce false positives, keep sequences where >=75% target the same 16K window class.
    outs=[]
    for parity in (0,1):
        i=parity
        while i+1<len(d):
            start=i; vals=[]
            while i+1<len(d):
                v=d[i]|(d[i+1]<<8)
                if 0x0100<=v<=0x7fff:
                    vals.append(v);i+=2
                else: break
            if len(vals)>=min_words:
                lo=sum(v<0x4000 for v in vals); hi=len(vals)-lo
                dominant=max(lo,hi)/len(vals)
                if dominant>=.75:
                    outs.append((start,len(vals),lo,hi,vals[:12]))
            i=max(i+2,start+2)
    # remove massive false-positive noise by top useful runs, sorted offset; caller writes all up to 1000
    return outs[:1000]

IMM16_OPS={0x08,0x01,0x11,0x21,0x31,0xc2,0xca,0xd2,0xda,0xc3,0xc4,0xcc,0xd4,0xdc,0xcd,0xea,0xfa}
def opcode_addr_candidates(d):
    out=[]
    for i in range(min(len(d),0x4000)-2):
        op=d[i]
        if op in IMM16_OPS:
            v=d[i+1]|(d[i+2]<<8)
            if 0x0100<=v<=0x7fff:
                out.append((i,op,v,i//BANK))
    return out

def write_csv(path,header,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)

def asm_cfg(d,labels,vis):
    lines=['; Candidate control-flow disassembly for fixed ROM Bank 00.', '; Only addresses reachable from reset/RST/interrupt vectors are emitted as instructions.', '; Unvisited bytes are intentionally omitted from this file and remain unclassified.', 'SECTION "Fixed Bank CFG Candidates", ROM0[$0000]']
    for pc in sorted(vis):
        if pc in labels: lines.append(f'\n{labels[pc]}::')
        ins=vis[pc]
        b=' '.join(f'{x:02X}' for x in d[pc:pc+ins['len']])
        lines.append(f'    {ins["mnemonic"]:<24} ; ${pc:04X}: {b}')
    lines.append('')
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--label',required=True)
    a=ap.parse_args(); d=a.rom.read_bytes(); o=a.out;o.mkdir(parents=True,exist_ok=True)
    seeds,labels,vis,edges=cfg_bank0(d)
    # outputs
    (o/'fixed_bank_cfg.asm').write_text(asm_cfg(d,labels,vis),encoding='utf-8')
    (o/'fixed_bank_symbols.sym').write_text('\n'.join(f'00:{addr:04X} {name}' for addr,name in sorted(labels.items()))+'\n',encoding='utf-8')
    (o/'fixed_bank_cfg.json').write_text(json.dumps({'label':a.label,'seeds':seeds,'labels':{f'{k:04X}':v for k,v in labels.items()},'instructions':{f'{k:04X}':v for k,v in vis.items()},'edges':[{'from':f'{x:04X}','to':f'{y:04X}','kind':z} for x,y,z in edges]},indent=2),encoding='utf-8')
    # Merge visited instruction bytes into coverage ranges.
    covered=set()
    for pc,ins in vis.items(): covered.update(range(pc,pc+ins['len']))
    ranges=[]
    for x in sorted(covered):
        if not ranges or x!=ranges[-1][1]+1: ranges.append([x,x])
        else: ranges[-1][1]=x
    write_csv(o/'fixed_bank_coverage_ranges.csv',['start','end','length'],((f'0x{s:04X}',f'0x{e:04X}',e-s+1) for s,e in ranges))
    title=d[0x134:0x143].rstrip(b'\0').decode('ascii','replace')
    hinc=f'''\n; Declarative cartridge-header metadata. No ROM payload bytes are embedded.\nDEF ROM_TITLE EQUS "{title}"\nDEF CGB_FLAG EQU ${d[0x143]:02X}\nDEF CARTRIDGE_TYPE EQU ${d[0x147]:02X}\nDEF ROM_SIZE_CODE EQU ${d[0x148]:02X}\nDEF RAM_SIZE_CODE EQU ${d[0x149]:02X}\nDEF DESTINATION_CODE EQU ${d[0x14A]:02X}\nDEF MASK_ROM_VERSION EQU ${d[0x14C]:02X}\nDEF HEADER_CHECKSUM EQU ${d[0x14D]:02X}\nDEF GLOBAL_CHECKSUM EQU ${int.from_bytes(d[0x14E:0x150],'big'):04X}\n'''
    (o/'header_constants.inc').write_text(hinc.lstrip(),encoding='utf-8')
    runs=long_runs(d)
    write_csv(o/'long_zero_ff_runs.csv',['start','end','length','value','bank'],((f'0x{s:06X}',f'0x{e:06X}',n,f'0x{v:02X}',f'0x{b:02X}') for s,e,n,v,b in runs))
    erows=[]
    for off in range(0,len(d),0x400):
        blk=d[off:off+0x400]; erows.append((f'0x{off:06X}',f'0x{off//BANK:02X}',len(blk),f'{entropy(blk):.6f}'))
    write_csv(o/'entropy_1k.csv',['offset','bank','size','entropy_bits_per_byte'],erows)
    pts=pointer_table_candidates(d)
    write_csv(o/'pointer_table_candidates.csv',['offset','word_count','rom0_targets','romx_targets','sample_targets'],((f'0x{s:06X}',n,lo,hi,' '.join(f'{v:04X}' for v in vals)) for s,n,lo,hi,vals in pts))
    ops=opcode_addr_candidates(d)
    write_csv(o/'opcode_address_candidates.csv',['offset','opcode','target_cpu_addr','bank'],((f'0x{s:06X}',f'0x{op:02X}',f'0x{v:04X}',f'0x{b:02X}') for s,op,v,b in ops))
    code_bytes=sum(x['len'] for x in vis.values())
    summary=f'''# Structural Survey Phase 1 — {a.label}\n\n- Source: `{a.rom.name}` (external/read-only; not part of generated corpus)\n- Size: {len(d):,} bytes; banks: {len(d)//BANK}\n- SHA-256: `{hashlib.sha256(d).hexdigest()}`\n- Bank 00 reachable instruction starts: {len(vis):,}\n- Bank 00 reachable instruction bytes: {code_bytes:,} / 16,384 ({code_bytes/16384:.2%})\n- Discovered fixed-bank labels: {len(labels):,}\n- CFG edges within Bank 00: {len(edges):,}\n- Long `00`/`FF` runs (>=32 bytes): {len(runs):,}\n- Pointer-table candidates (heuristic): {len(pts):,}\n- Immediate-address opcode candidates: {len(ops):,}\n\n## Interpretation\n\n`fixed_bank_cfg.asm` is a **control-flow candidate disassembly**, not a declaration that every emitted byte has already been semantically named. It follows reset, RST and interrupt entry points and direct in-bank branches/calls. The other tables are heuristic maps intended for the next classification pass.\n'''
    (o/'STRUCTURE-SUMMARY.md').write_text(summary,encoding='utf-8')
    # Compact, human-browsable map: summary + stable/derived symbols + header + CFG coverage.
    symbol_text=(o/'fixed_bank_symbols.sym').read_text(encoding='utf-8').rstrip()
    header_text=(o/'header_constants.inc').read_text(encoding='utf-8').rstrip()
    coverage_text=(o/'fixed_bank_coverage_ranges.csv').read_text(encoding='utf-8').rstrip()
    key_map=(
        f'# Phase 1 Key Map — {a.label}\n\n'
        + summary.split('## Interpretation')[0].rstrip() + '\n\n'
        + '## Fixed Bank 00 symbols\n\n```text\n' + symbol_text + '\n```\n\n'
        + '## Header constants\n\n```asm\n' + header_text + '\n```\n\n'
        + '## Reachable CFG coverage ranges\n\n```csv\n' + coverage_text + '\n```\n\n'
        + 'The symbol map contains stable vector semantics plus ROM-local CFG-derived labels. '
          'Unknown targets remain `loc_XXXX`; they are not force-named from another localization.\n'
    )
    (o/'PHASE1-KEY-MAP.md').write_text(key_map,encoding='utf-8')
    manifest=[]
    for p in sorted(o.iterdir()):
        if p.is_file(): manifest.append({'file':p.name,'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (o/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'label':a.label,'files':len(manifest)+1,'visited':len(vis),'code_bytes':code_bytes,'labels':len(labels),'runs':len(runs),'ptr_tables':len(pts),'op_addr':len(ops)}))
if __name__=='__main__': main()
