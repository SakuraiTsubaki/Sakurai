#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,re
from difflib import SequenceMatcher
from pathlib import Path

VERSIONS=[
 ('KR-REV-0','KR','REV-0'),('JP-REV-0','JP','REV-0'),('JP-REV-A','JP','REV-A'),
 ('USA-EUROPE-REV-0','USA-EUROPE','REV-0'),('DE-REV-0','DE','REV-0'),
 ('FR-REV-0','FR','REV-0'),('IT-REV-0','IT','REV-0'),('ES-REV-0','ES','REV-0')]
FLOW_END={'jump','ret','indirect','invalid','condret'}

HEX_RE=re.compile(r'\$[0-9a-fA-F]{2,4}')
DEC_RE=re.compile(r'(?<![A-Za-z_])[-+]?\d+(?![A-Za-z_])')

def norm(mn:str)->str:
    # Preserve opcode/register structure while abstracting localization-dependent targets/constants.
    s=HEX_RE.sub('$IMM',mn.lower())
    # Keep bit numbers/rst vectors meaningful; decimal immediates are rare in emitted syntax.
    return ' '.join(s.split())

def load_cfg(root:Path,region:str,rev:str):
    p=root/f'GENERATION-II/GOLD/{region}/{rev}/analysis/structure-phase1/fixed_bank_cfg.json'
    j=json.loads(p.read_text())
    labels={int(k,16):v for k,v in j['labels'].items()}
    ins={int(k,16):v for k,v in j['instructions'].items()}
    return labels,ins

def blocks(labels,ins):
    addrs=sorted(labels)
    out=[]
    for a in addrs:
        if a not in ins: continue
        seq=[]; rawbytes=0; pc=a
        seen=set()
        while pc in ins and pc not in seen:
            seen.add(pc); x=ins[pc]
            seq.append(norm(x['mnemonic'])); rawbytes+=x['len']
            nxt=pc+x['len']
            if x['flow'] in FLOW_END: break
            # A branch/call target is a boundary only for the target, not current fallthrough.
            if nxt in labels and nxt!=a: break
            pc=nxt
        sig='\n'.join(seq)
        out.append({'address':a,'label':labels[a],'seq':seq,'sig':sig,'hash':hashlib.sha256(sig.encode()).hexdigest()[:16],'insns':len(seq),'bytes':rawbytes})
    return out

def wr_csv(path,head,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase1_root',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args()
    by={}
    for label,reg,rev in VERSIONS:
        labs,ins=load_cfg(a.phase1_root,reg,rev);by[label]=blocks(labs,ins)
    # Exact normalized basic-block families.
    groups={}
    for ver,bs in by.items():
        for b in bs: groups.setdefault(b['sig'],[]).append((ver,b))
    family_signatures=[]; family_members=[];gid=0
    for sig,members in sorted(groups.items(), key=lambda kv:(-len(kv[1]),kv[0])):
        versions=sorted({v for v,_ in members})
        if len(versions)<2: continue
        gid+=1
        family=f'F{gid:03d}'
        exemplar=members[0][1]
        family_signatures.append((family,exemplar['hash'],exemplar['insns'],sig.replace('\n',' | '),len(versions),' '.join(versions)))
        for ver,b in sorted(members,key=lambda x:(x[0],x[1]['address'])):
            family_members.append((family,ver,f"0x{b['address']:04X}",b['label'],b['insns'],b['bytes']))
    out=a.out;out.mkdir(parents=True,exist_ok=True)
    wr_csv(out/'basic_block_family_signatures.csv',['family','normalized_sha256_16','instruction_count','normalized_sequence','version_count','versions'],family_signatures)
    wr_csv(out/'basic_block_family_members.csv',['family','version','address','label','instruction_count','byte_count'],family_members)

    # KR -> USA exact/fuzzy alignment. Prefer exact normalized blocks; then best sequence match.
    kr=by['KR-REV-0']; us=by['USA-EUROPE-REV-0']; rows=[]
    semantic_names={'ResetVector','FarCall','Bankswitch','Rst18Trap','Rst20Trap','JumpTable','Rst38Trap','VBlankVector','LCDVector','TimerVector','SerialVector','JoypadVector','Start','VBlank','LCD','_Start','Serial','Joypad','FarCall_hl'}
    for kb in kr:
        # Known semantic anchors are aligned by independently established label semantics first.
        if kb['label'] in semantic_names:
            same=next((u for u in us if u['label']==kb['label']),None)
        else:
            same=None
        if same is not None:
            u=same
            score=SequenceMatcher(None,kb['seq'],u['seq']).ratio()
            if max(len(kb['seq']),len(u['seq'])):
                score*=min(len(kb['seq']),len(u['seq']))/max(len(kb['seq']),len(u['seq']))
            kind='semantic-anchor'
        else:
            exact=[u for u in us if u['sig']==kb['sig']]
            if exact:
                exact.sort(key=lambda u:(u['label']!=kb['label'],abs(u['address']-kb['address'])))
                u=exact[0]; score=1.0; kind='exact-normalized'
            else:
                scored=[]
                for u0 in us:
                    score0=SequenceMatcher(None,kb['seq'],u0['seq']).ratio()
                    if max(len(kb['seq']),len(u0['seq'])):
                        score0*=min(len(kb['seq']),len(u0['seq']))/max(len(kb['seq']),len(u0['seq']))
                    scored.append((score0,u0))
                score,u=max(scored,key=lambda x:x[0])
                if score>=0.65:
                    kind='fuzzy-normalized'
                else:
                    kind='unmatched'
        if kind=='unmatched':
            rows.append((f"0x{kb['address']:04X}",kb['label'],'','',kind,f'{score:.6f}',kb['insns'],'',''))
        else:
            rows.append((f"0x{kb['address']:04X}",kb['label'],f"0x{u['address']:04X}",u['label'],kind,f'{score:.6f}',kb['insns'],u['insns'],f'{u["address"]-kb["address"]:+d}'))
    wr_csv(out/'kr_to_usa_alignment.csv',['kr_address','kr_label','usa_address','usa_label','match_kind','score','kr_insns','usa_insns','address_delta'],rows)

    # Stable semantic anchors and per-version address matrix.
    semantic=['ResetVector','FarCall','Bankswitch','JumpTable','VBlankVector','LCDVector','TimerVector','SerialVector','JoypadVector','Start','VBlank','LCD','_Start','Serial','Joypad','FarCall_hl']
    matrix=[]
    for name in semantic:
        row=[name]
        for ver,_,_ in VERSIONS:
            hit=next((b for b in by[ver] if b['label']==name),None)
            row.append('' if hit is None else f"0x{hit['address']:04X}")
        matrix.append(row)
    wr_csv(out/'semantic_anchor_matrix.csv',['symbol']+[v[0] for v in VERSIONS],matrix)

    exact_kr=sum(1 for r in rows if r[4]=='exact-normalized')
    anchored=sum(1 for r in rows if r[4]=='semantic-anchor')
    fuzzy=sum(1 for r in rows if r[4]=='fuzzy-normalized')
    unmatched=sum(1 for r in rows if r[4]=='unmatched')
    strong=sum(1 for r in rows if r[4] != 'unmatched' and float(r[5])>=0.80)
    summary=f'''# Gold Fixed Bank Alignment — Phase 2\n\n- Versions compared: {len(VERSIONS)}\n- KR Bank 00 labeled entry blocks: {len(kr)}\n- USA/Europe Bank 00 labeled entry blocks: {len(us)}\n- KR semantic anchors aligned by established meaning: {anchored}\n- KR anonymous blocks with an exact normalized USA match: {exact_kr}\n- KR anonymous blocks with a high-confidence fuzzy match: {fuzzy}\n- KR blocks left unmatched: {unmatched}\n- KR blocks with alignment score >= 0.80: {strong} / {len(kr)}\n- Multi-version exact normalized block families: {gid}\n\n## Method\n\nThe Phase 1 control-flow output is split at labeled entry points. Instruction mnemonics are normalized by replacing hexadecimal immediates/targets with `$IMM`, then hashed. This lets structurally identical blocks align even when localization moves code or changes addresses. Fuzzy matches use normalized instruction-sequence similarity and are explicitly marked as heuristic.\n\nThis phase **does not assign upstream semantic names to anonymous Korean labels**. It establishes cross-version equivalence first; semantic promotion happens only when an aligned upstream routine can be independently verified.\n'''
    (out/'README.md').write_text(summary,encoding='utf-8')
    manifest=[]
    for p in sorted(out.iterdir()):
        if p.is_file():manifest.append({'file':p.name,'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'exact_families':gid,'kr_blocks':len(kr),'semantic_anchors':anchored,'exact_kr_to_usa':exact_kr,'fuzzy_kr_to_usa':fuzzy,'unmatched':unmatched,'strong_kr_to_usa':strong,'files':len(manifest)+1},indent=2))
if __name__=='__main__':main()
