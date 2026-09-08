#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math, shutil, zlib
from collections import Counter, defaultdict
from pathlib import Path

BANK_SIZE = 0x4000
PAGE_SIZE = 0x100
MATCH_CHUNK = 0x40
MIN_FILL = 64

TARGETS = [
    dict(label='KR-REV-0', filename='Pocket Monsters Geum (Korea).gbc', region='KR', rev='REV-0', sha256='9c273e86e6120c6a038160ccb0153b8b20425b84fc08a496281c1d1bcac492f6'),
    dict(label='JP-REV-0', filename='Pocket Monsters Kin (Japan).gbc', region='JP', rev='REV-0', sha256='7cfeceae00737a1f0713c9ab0b3a9e6eb8d05ff6002eb81308072a6f85e385e7'),
    dict(label='JP-REV-A', filename='Pocket Monsters Kin (Japan) (Rev A).gbc', region='JP', rev='REV-A', sha256='27a07a1d3faf9c6a0b1b60d5e88ee3a4159a751a47b4c46ab09f1202d52bac3e'),
    dict(label='USA-EUROPE-REV-0', filename='Pokemon - Gold Version (USA, Europe).gbc', region='USA-EUROPE', rev='REV-0', sha256='fb0016d27b1e5374e1ec9fcad60e6628d8646103b5313ca683417f52b97e7e4e'),
    dict(label='DE-REV-0', filename='Pokemon - Goldene Edition (Germany).gbc', region='DE', rev='REV-0', sha256='542f275f8632ef5265e5cde80a8ba1f0ec11ce714ef9d773088a92680bd17d73'),
    dict(label='FR-REV-0', filename='Pokemon - Version Or (France).gbc', region='FR', rev='REV-0', sha256='6103cadf2ae505f4b489a8a414c8db27a2307d797ddf8a3a848659b591dd4023'),
    dict(label='IT-REV-0', filename='Pokemon - Versione Oro (Italy).gbc', region='IT', rev='REV-0', sha256='367e606f82b9e2e16d0cc8011c5ba2df1862da574e57ffd66e786a82af5b6e22'),
    dict(label='ES-REV-0', filename='Pokemon - Edicion Oro (Spain).gbc', region='ES', rev='REV-0', sha256='7b78e33a348a0729e38ee0fd778cf49b3e07c35d2175ebc74d8f9be41f41455b'),
]

def sha256_bytes(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str: return sha256_bytes(path.read_bytes())
def entropy(data: bytes) -> float:
    if not data: return 0.0
    n=len(data); c=Counter(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
def wr_csv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)
def cpu_addr(bank:int, local:int)->int: return local if bank==0 else 0x4000+local

def fill_runs(data: bytes, min_len=MIN_FILL):
    i=0
    while i<len(data):
        v=data[i]
        if v not in (0x00,0xFF): i+=1; continue
        j=i+1
        while j<len(data) and data[j]==v: j+=1
        if j-i>=min_len: yield i,j,v
        i=j

def all_runs(data:bytes, value:int):
    best=0; i=0
    while i<len(data):
        if data[i]!=value: i+=1; continue
        j=i+1
        while j<len(data) and data[j]==value: j+=1
        best=max(best,j-i); i=j
    return best

def segment_bank(bank_data:bytes, bank:int):
    runs=list(fill_runs(bank_data)); rows=[]; pos=0
    for s,e,v in runs:
        if pos<s: rows.append((pos,s,'payload',None))
        rows.append((s,e,'fill',v)); pos=e
    if pos<len(bank_data): rows.append((pos,len(bank_data),'payload',None))
    assert rows and rows[0][0]==0 and rows[-1][1]==len(bank_data)
    for a,b,_,_ in zip(rows,rows[1:],rows[1:],rows[2:]): pass
    return rows

def valid_ptr(v:int)->bool: return 0x0100 <= v < 0x8000

def pointer_windows(bank_data:bytes, bank:int):
    out=[]
    for parity in (0,1):
        i=parity
        while i+1<len(bank_data):
            s=i; vals=[]
            while i+1<len(bank_data):
                v=bank_data[i] | (bank_data[i+1]<<8)
                if not valid_ptr(v): break
                vals.append(v); i+=2
            if len(vals)>=4:
                zones={'ROM0' if v<0x4000 else 'ROMX' for v in vals}
                out.append((bank,s,len(vals),min(vals),max(vals),'+'.join(sorted(zones)),parity))
            if i==s: i+=2
    return out

def valid_far(bank_byte:int, addr:int, bank_count:int)->bool:
    if bank_byte>=bank_count: return False
    if bank_byte==0: return 0x0100 <= addr < 0x4000
    return 0x4000 <= addr < 0x8000

def far_pointer_windows(bank_data:bytes, bank:int, bank_count:int):
    out=[]
    for phase in (0,1,2):
        i=phase
        while i+2<len(bank_data):
            s=i; vals=[]
            while i+2<len(bank_data):
                b=bank_data[i]; a=bank_data[i+1] | (bank_data[i+2]<<8)
                if not valid_far(b,a,bank_count): break
                vals.append((b,a)); i+=3
            if len(vals)>=3:
                out.append((bank,s,len(vals),min(b for b,_ in vals),max(b for b,_ in vals),phase))
            if i==s: i+=3
    return out

def class_bank(ent:float, fill_ratio:float, data:bytes)->str:
    if data==bytes(len(data)): return 'blank-00'
    if data==bytes([0xff])*len(data): return 'blank-ff'
    if fill_ratio>=0.75: return 'sparse-fill-dominant'
    if ent>=7.5: return 'dense-high-entropy'
    if ent>=6.0: return 'dense-medium-entropy'
    return 'dense-low-entropy'

def nonfill_chunk_set(bank_data:bytes, chunk=MATCH_CHUNK):
    s=set()
    for i in range(0,len(bank_data),chunk):
        q=bank_data[i:i+chunk]
        if q==bytes(len(q)) or q==bytes([0xff])*len(q): continue
        s.add(hashlib.sha1(q).digest())
    return s

def header_md(t, data, bank_count, features):
    fill=sum(r['fill_bytes'] for r in features); size=len(data)
    blank=sum(1 for r in features if r['classification'].startswith('blank-'))
    return f'''# Full-ROM Reproducibility Atlas — {t['label']}\n\n- Source filename: `{t['filename']}` (external/read-only; not committed)\n- SHA-256: `{sha256_bytes(data)}`\n- ROM bytes: {size:,}\n- 16 KiB banks: {bank_count}\n- Every byte covered by source-segment manifest: **YES (100%)**\n- Long `00`/`FF` fill threshold: {MIN_FILL} bytes\n- Bytes promoted from opaque payload to explicit fill directives: {fill:,} ({fill/size:.2%})\n- Completely blank banks: {blank}\n\nThe segmented rebuild scaffold stores no ROM payload bytes. Non-fill regions are referenced from a local verified `baserom.gbc` with `INCBIN`; long fill runs are reproduced with `ds`. This preserves byte-exact rebuilding while making the physical ROM layout directly editable and auditable.\n\nPointer/far-pointer tables and cross-version bank correspondences are **heuristics**, not semantic claims.\n'''

def build_one(t, src:Path, outroot:Path):
    p=src/t['filename']; data=p.read_bytes(); got=sha256_bytes(data)
    if got!=t['sha256']: raise SystemExit(f"SHA-256 mismatch for {p}: {got}")
    if len(data)%BANK_SIZE: raise SystemExit(f'not bank aligned: {p}')
    bank_count=len(data)//BANK_SIZE
    dest=outroot/f"GENERATION-II/GOLD/{t['region']}/{t['rev']}/analysis/full-rom-reproducibility"
    dest.mkdir(parents=True,exist_ok=True)
    coverage=[]; features=[]; page_rows=[]; ptr_rows=[]; far_rows=[]; asm=[]
    asm.append('; Generated whole-ROM segmented scaffold. No ROM payload bytes embedded.')
    asm.append('; Put the verified source ROM beside this file as baserom.gbc.')
    asm.append('')
    chunk_sets=[]
    pages_for_groups=[]
    for bank in range(bank_count):
        off=bank*BANK_SIZE; bd=data[off:off+BANK_SIZE]
        segs=segment_bank(bd,bank)
        fill_bytes=sum(e-s for s,e,k,v in segs if k=='fill')
        ent=entropy(bd); pw=pointer_windows(bd,bank); fw=far_pointer_windows(bd,bank,bank_count)
        ptr_rows.extend(pw); far_rows.extend(fw)
        cls=class_bank(ent,fill_bytes/BANK_SIZE,bd)
        feat=dict(bank=bank,rom_offset=off,sha256=sha256_bytes(bd),crc32=f'{zlib.crc32(bd)&0xffffffff:08x}',entropy=round(ent,6),zero_ratio=round(bd.count(0)/BANK_SIZE,6),ff_ratio=round(bd.count(255)/BANK_SIZE,6),unique_bytes=len(set(bd)),fill_segments=sum(1 for *_,k,v in segs if k=='fill'),fill_bytes=fill_bytes,payload_bytes=BANK_SIZE-fill_bytes,longest_00=all_runs(bd,0),longest_ff=all_runs(bd,255),pointer_windows=len(pw),far_pointer_windows=len(fw),classification=cls)
        features.append(feat)
        chunk_sets.append(nonfill_chunk_set(bd))
        asm.append(f'SECTION "Bank {bank:02X}", ' + (f'ROM0[$0000]' if bank==0 else f'ROMX[$4000], BANK[${bank:02X}]'))
        for idx,(s,e,k,v) in enumerate(segs):
            goff=off+s; ln=e-s
            row=[bank,idx,f'0x{goff:06X}',f'0x{goff+ln-1:06X}',ln,f'0x{cpu_addr(bank,s):04X}',f'0x{cpu_addr(bank,e-1):04X}',k,'' if v is None else f'0x{v:02X}']
            coverage.append(row)
            if k=='fill': asm.append(f'    ds ${ln:X}, ${v:02X} ; ROM ${goff:06X}-${goff+ln-1:06X}')
            else: asm.append(f'    INCBIN "baserom.gbc", ${goff:06X}, ${ln:X}')
        asm.append('')
        for pi in range(BANK_SIZE//PAGE_SIZE):
            s=pi*PAGE_SIZE; pg=bd[s:s+PAGE_SIZE]; ph=sha256_bytes(pg)
            pure='00' if pg==bytes(PAGE_SIZE) else ('FF' if pg==bytes([255])*PAGE_SIZE else '')
            page_rows.append([bank,pi,f'0x{off+s:06X}',ph,f'{entropy(pg):.6f}',pg.count(0),pg.count(255),pure])
            if not pure: pages_for_groups.append((ph,bank,pi))
    wr_csv(dest/'source_segments.csv',['bank','segment','rom_start','rom_end','length','cpu_start','cpu_end','kind','fill_value'],coverage)
    (dest/'source_segments.json').write_text(json.dumps([dict(zip(['bank','segment','rom_start','rom_end','length','cpu_start','cpu_end','kind','fill_value'],r)) for r in coverage],indent=2),encoding='utf-8')
    wr_csv(dest/'bank_features.csv',list(features[0]),[[r[k] for k in features[0]] for r in features])
    (dest/'bank_features.json').write_text(json.dumps(features,indent=2),encoding='utf-8')
    wr_csv(dest/'page_hashes_256.csv',['bank','page','rom_offset','sha256','entropy','zero_bytes','ff_bytes','pure_fill'],page_rows)
    wr_csv(dest/'pointer_windows_16le.csv',['bank','bank_offset','entry_count','min_value','max_value','zones','alignment_parity'],[[b,f'0x{o:04X}',n,f'0x{lo:04X}',f'0x{hi:04X}',z,p] for b,o,n,lo,hi,z,p in ptr_rows])
    wr_csv(dest/'far_pointer_windows.csv',['bank','bank_offset','entry_count','min_bank','max_bank','alignment_phase'],[[b,f'0x{o:04X}',n,lo,hi,p] for b,o,n,lo,hi,p in far_rows])
    (dest/'rebuild_segmented.asm').write_text('\n'.join(asm)+'\n',encoding='utf-8')
    cov_bytes=sum(r[4] for r in coverage); assert cov_bytes==len(data)
    summary={'label':t['label'],'source_filename':t['filename'],'sha256':got,'size':len(data),'bank_count':bank_count,'segment_count':len(coverage),'coverage_bytes':cov_bytes,'coverage_percent':100.0,'fill_bytes':sum(r['fill_bytes'] for r in features),'payload_bytes':sum(r['payload_bytes'] for r in features),'pointer_windows':len(ptr_rows),'far_pointer_windows':len(far_rows),'page_count':len(page_rows)}
    (dest/'coverage_contract.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (dest/'README.md').write_text(header_md(t,data,bank_count,features),encoding='utf-8')
    entries=[]
    for q in sorted(dest.iterdir()):
        if q.is_file() and q.name!='MANIFEST.json': entries.append({'file':q.name,'size':q.stat().st_size,'sha256':sha256_file(q)})
    (dest/'MANIFEST.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
    return {'target':t,'data':data,'bank_count':bank_count,'chunk_sets':chunk_sets,'pages':pages_for_groups,'features':features,'dest':dest,'summary':summary}

def build_cross(results,outroot:Path):
    multi=outroot/'GENERATION-II/GOLD/MULTI/REV-MIXED/analysis/full-rom-reproducibility'
    cross=multi/'cross-version'; cross.mkdir(parents=True,exist_ok=True)
    by={r['target']['label']:r for r in results}; usa=by['USA-EUROPE-REV-0']
    rows=[]
    for r in results:
        for sb,sset in enumerate(r['chunk_sets']):
            best=None
            if not sset:
                rows.append([r['target']['label'],sb,'','','',0,len(sset),0,'no-nonfill-chunks']); continue
            for ub,uset in enumerate(usa['chunk_sets']):
                inter=len(sset & uset); union=len(sset | uset); jac=(inter/union if union else 0.0)
                score=(inter,jac,-abs(sb-ub),-ub)
                if best is None or score>best[0]: best=(score,ub,inter,jac,len(uset))
            _,ub,inter,jac,uc=best
            ev='strong' if inter>=32 and jac>=0.20 else ('moderate' if inter>=8 else ('weak' if inter else 'none'))
            rows.append([r['target']['label'],sb,'USA-EUROPE-REV-0',ub,f'{jac:.6f}',inter,len(sset),uc,ev])
    wr_csv(cross/'bank_correspondence_to_usa.csv',['source_version','source_bank','reference_version','reference_bank','jaccard_nonfill_64b','shared_exact_64b_chunks','source_nonfill_chunks','reference_nonfill_chunks','evidence'],rows)
    same=[]
    for i,a in enumerate(results):
        for b in results[i+1:]:
            n=min(a['bank_count'],b['bank_count'])
            for bank in range(n):
                aa=a['data'][bank*BANK_SIZE:(bank+1)*BANK_SIZE]; bb=b['data'][bank*BANK_SIZE:(bank+1)*BANK_SIZE]
                diff=sum(x!=y for x,y in zip(aa,bb)); same.append([a['target']['label'],b['target']['label'],bank,diff,BANK_SIZE-diff,f'{(BANK_SIZE-diff)/BANK_SIZE:.6f}'])
    wr_csv(cross/'same_index_bank_identity.csv',['a','b','bank','different_bytes','equal_bytes','identity'],same)
    groups=defaultdict(list)
    for r in results:
        for ph,b,p in r['pages']: groups[ph].append((r['target']['label'],b,p))
    grows=[]
    for h,locs in sorted(groups.items()):
        vers=sorted({v for v,_,_ in locs})
        if len(vers)<2: continue
        grows.append([h,len(locs),len(vers),' '.join(vers),';'.join(f'{v}:{b:02X}:{p:02X}' for v,b,p in locs)])
    wr_csv(cross/'shared_exact_256b_pages.csv',['sha256','occurrences','version_count','versions','locations'],grows)
    ja, jb=by['JP-REV-0'], by['JP-REV-A']; jrows=[]
    for bank in range(min(ja['bank_count'],jb['bank_count'])):
        aa=ja['data'][bank*BANK_SIZE:(bank+1)*BANK_SIZE]; bb=jb['data'][bank*BANK_SIZE:(bank+1)*BANK_SIZE]
        diff=sum(x!=y for x,y in zip(aa,bb));
        if diff: jrows.append([bank,diff,BANK_SIZE-diff,f'{(BANK_SIZE-diff)/BANK_SIZE:.6f}'])
    wr_csv(cross/'jp_rev0_vs_reva_bank_diffs.csv',['bank','different_bytes','equal_bytes','identity'],jrows)
    maxbanks=max(r['bank_count'] for r in results); matrix=[]
    for bank in range(maxbanks):
        row=[bank]
        for r in results:
            row.append(r['features'][bank]['classification'] if bank<r['bank_count'] else '')
        matrix.append(row)
    wr_csv(cross/'bank_classification_matrix.csv',['bank']+[r['target']['label'] for r in results],matrix)
    (multi/'README.md').write_text(f'''# Gold Full-ROM Reproducibility Atlas\n\nThis phase expands the reproducibility project from fixed Bank 00 to **every byte in every uploaded Gold ROM**.\n\n- Source ROMs: {len(results)}\n- Total source bytes audited: {sum(len(r['data']) for r in results):,}\n- Total 16 KiB banks audited: {sum(r['bank_count'] for r in results):,}\n- Byte coverage: 100% for every ROM\n- Shared exact non-fill 256-byte page groups across multiple versions: {len(grows):,}\n- Bank correspondences are heuristic and based on exact non-fill 64-byte chunk overlap.\n\nNo ROM payload bytes are committed. The source ROMs are external inputs identified by SHA-256.\n''',encoding='utf-8')
    (multi/'ROM-SET.json').write_text(json.dumps([{k:t[k] for k in ('label','filename','region','rev','sha256')} for t in TARGETS],indent=2),encoding='utf-8')
    return multi

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source_dir',type=Path); ap.add_argument('out_dir',type=Path); a=ap.parse_args()
    a.out_dir.mkdir(parents=True,exist_ok=True)
    results=[build_one(t,a.source_dir,a.out_dir) for t in TARGETS]
    multi=build_cross(results,a.out_dir)
    tools=multi/'tools'; tools.mkdir(exist_ok=True)
    shutil.copy2(Path(__file__),tools/'build_full_rom_atlas.py')
    verifier=Path(__file__).with_name('verify_full_rom_atlas.py')
    if verifier.exists(): shutil.copy2(verifier,tools/'verify_full_rom_atlas.py')
    manifest=[]
    for p in sorted(a.out_dir.rglob('*')):
        if not p.is_file() or p.name=='FULL-ROM-MANIFEST.json':
            continue
        rel=p.relative_to(a.out_dir).as_posix()
        if '/full-rom-reproducibility/' not in ('/'+rel):
            continue
        manifest.append({'path':rel,'size':p.stat().st_size,'sha256':sha256_file(p)})
    (multi/'FULL-ROM-MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    h=hashlib.sha256()
    for e in manifest: h.update(f"{e['path']}\t{e['size']}\t{e['sha256']}\n".encode())
    (multi/'SNAPSHOT.md').write_text(f'''# Full-ROM Atlas Snapshot\n\n- Generated files before this snapshot: {len(manifest)}\n- Canonical manifest-record SHA-256: `{h.hexdigest()}`\n- Source ROMs: {len(TARGETS)}\n- ROM payload files committed: 0\n- Coverage contract: 100% of every source ROM byte\n''',encoding='utf-8')
    print(json.dumps({'roms':len(results),'banks':sum(r['bank_count'] for r in results),'files':sum(1 for p in a.out_dir.rglob('*') if p.is_file()),'tree_digest':h.hexdigest()},indent=2))
if __name__=='__main__': main()
