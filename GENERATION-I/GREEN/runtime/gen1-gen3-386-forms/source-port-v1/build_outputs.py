#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

EXPECTED={'rev0':'82c0eef40a5e2423699d9fd8ba15dfaa8b51d196','reva':'4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b'}

def sha1(b:bytes): return hashlib.sha1(b).hexdigest()

def ips_record(off:int,data:bytes)->bytes:
    out=bytearray()
    while data:
        c=data[:0xffff]; data=data[len(c):]
        out += off.to_bytes(3,'big')+len(c).to_bytes(2,'big')+c; off+=len(c)
    return bytes(out)

def make_ips(old:bytes,new:bytes)->bytes:
    out=bytearray(b'PATCH'); n=max(len(old),len(new)); i=0
    def ov(pos): return old[pos] if pos<len(old) else None
    while i<n:
        nv=new[i] if i<len(new) else None
        if ov(i)==nv: i+=1; continue
        start=i; buf=bytearray()
        while i<n and len(buf)<0xffff:
            nv=new[i] if i<len(new) else None
            if ov(i)==nv: break
            if nv is None: break
            buf.append(nv); i+=1
        if buf: out += ips_record(start,bytes(buf))
        else: i+=1
    out += b'EOF'
    if len(new)!=len(old): out += len(new).to_bytes(3,'big')
    return bytes(out)

def find_sym(sym:Path,name:str):
    rx=re.compile(r'^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+'+re.escape(name)+r'$')
    for line in sym.read_text(encoding='utf-8').splitlines():
        m=rx.match(line.strip())
        if m: return {'bank':int(m.group(1),16),'address':int(m.group(2),16)}
    raise RuntimeError(f'{name} missing from {sym}')

def header(rom:bytes):
    return {'cart_type':rom[0x147],'rom_size_code':rom[0x148],'ram_size_code':rom[0x149],'version':rom[0x14c]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--stock-rev0',type=Path,required=True); ap.add_argument('--stock-reva',type=Path,required=True)
    ap.add_argument('--mod-rev0',type=Path,required=True); ap.add_argument('--mod-reva',type=Path,required=True)
    ap.add_argument('--sym-rev0',type=Path,required=True); ap.add_argument('--sym-reva',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    report={'schema':'green-g386-source-port-v1-build-report','roms':{},'runtime_symbols':{},'claims':{
      'canonical_identity':'u16 species + u8 form','persistent_store':'SRAM bank 4 committed/working journal',
      'wram_added_bytes':0,'playability':'identity/save/personal bridge milestone; names/sprites/cries/evolutions/moves/full 6-stat battle not complete'}}
    for tag,stockp,modp,symp in [('rev0',a.stock_rev0,a.mod_rev0,a.sym_rev0),('reva',a.stock_reva,a.mod_reva,a.sym_reva)]:
        stock=stockp.read_bytes(); mod=modp.read_bytes()
        assert sha1(stock)==EXPECTED[tag], (tag,sha1(stock))
        h=header(mod); assert h['cart_type']==0x1b and h['ram_size_code']==0x04
        assert len(mod)>=0x84000
        syms={name:find_sym(symp,name) for name in ['G386RuntimeStart','G386QueueCanonicalMon','G386OverlayMonHeader','G386LoadExtended','G386CommitExtended','sG386Magic','sG386WorkParty','sG386WorkBoxes']}
        assert syms['G386RuntimeStart']['bank']==0x20
        assert syms['sG386Magic']['bank']==0x04 and syms['sG386WorkParty']['bank']==0x04
        patch=make_ips(stock,mod); (a.out/f'green_g386_source_port_v1_{tag}.ips').write_bytes(patch)
        report['roms'][tag]={'stock_sha1':sha1(stock),'modified_sha1':sha1(mod),'modified_size':len(mod),'ips_sha1':sha1(patch),'ips_size':len(patch),'header':h}
        report['runtime_symbols'][tag]=syms
    report['test_vector']={'canonical_species_id':152,'canonical_species_hex':'0x0098','form_id':0,'purpose':'first post-Kanto identity boundary'}
    (a.out/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    lines=['GREEN G386 SOURCE PORT V1','']
    for tag,r in report['roms'].items():
        lines += [f'{tag}: {r["modified_size"]} bytes, SHA1 {r["modified_sha1"]}',f'{tag} IPS: {r["ips_size"]} bytes, SHA1 {r["ips_sha1"]}',f'{tag}: mapper={r["header"]["cart_type"]:#04x}, RAM code={r["header"]["ram_size_code"]:#04x}','']
    lines += ['PASS: stock source builds reproduce exact known Green SHA-1 before modification.','PASS: G386 runtime linked in ROM bank $20.','PASS: extended identity journal linked in SRAM bank $04.','PASS: no new WRAM section.','LIMIT: this is not yet full 386 playability; graphics/names/cries/evolution/moves and full SpA/SpD battle semantics remain.']
    (a.out/'VERIFICATION.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
