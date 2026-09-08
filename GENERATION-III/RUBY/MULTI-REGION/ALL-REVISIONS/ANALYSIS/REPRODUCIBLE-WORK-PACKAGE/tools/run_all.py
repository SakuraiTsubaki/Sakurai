#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,hashlib,os,sys
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import hashes,gba_header,shannon_entropy,trailing_run,pointer_count,parse_lz77

PAGE=0x10000

def rid(path, h):
    suffix=h['game_code'][-1]
    base={'J':'JP','E':'EN','D':'DE','F':'FR','I':'IT','S':'ES'}.get(suffix,suffix)
    rev=f"REV-{h['software_version']}"
    if 'Debug Version' in path.name: rev += '-DEBUG'
    return f'RUBY-{base}-{rev}'

def write_csv(path, rows, fields):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def diff_ranges(a,b):
    n=min(len(a),len(b)); ranges=[]; block=0x10000; active=None
    for bs in range(0,n,block):
        be=min(bs+block,n)
        aa=a[bs:be]; bb=b[bs:be]
        if aa==bb:
            if active is not None:
                ranges.append((active,bs)); active=None
            continue
        i=0
        while i<len(aa):
            if aa[i]==bb[i]:
                if active is not None:
                    ranges.append((active,bs+i)); active=None
                i+=1; continue
            if active is None: active=bs+i
            i+=1
    if active is not None: ranges.append((active,n))
    if len(a)!=len(b): ranges.append((n,max(len(a),len(b))))
    return ranges

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom_dir');ap.add_argument('out_dir');ap.add_argument('--exhaustive-ranges',action='store_true');args=ap.parse_args()
    rom_dir=Path(args.rom_dir); out=Path(args.out_dir); (out/'manifests').mkdir(parents=True,exist_ok=True); (out/'reports').mkdir(parents=True,exist_ok=True)
    roms=[]; blobs={}; page_rows=[]; lz_rows=[]
    for p in sorted(rom_dir.glob('*.gba')):
        data=p.read_bytes(); h=gba_header(data); id_=rid(p,h); hs=hashes(data); blobs[id_]=data
        row={'id':id_,'filename':p.name,'size_bytes':len(data),**hs,**h,
             'trailing_ff_bytes':trailing_run(data,0xFF),'trailing_00_bytes':trailing_run(data,0x00)}
        roms.append(row)
        for page_off in range(0,len(data),PAGE):
            block=data[page_off:page_off+PAGE]
            page_rows.append({'id':id_,'page_index':page_off//PAGE,'offset_hex':f'0x{page_off:08X}','length':len(block),
                'sha256':hashlib.sha256(block).hexdigest(),
                'zero_pct':f'{block.count(0)/len(block)*100:.4f}','ff_pct':f'{block.count(0xFF)/len(block)*100:.4f}'})
        # Generated report uses 4-byte-aligned candidates; bytes.find keeps the scan fast.
        pos=0
        while True:
            pos=data.find(b'\x10', pos)
            if pos < 0:
                break
            if (pos & 3) == 0:
                parsed=parse_lz77(data,pos)
                if parsed:
                    dec,span=parsed; comp=data[pos:pos+span]
                    lz_rows.append({'id':id_,'offset_hex':f'0x{pos:08X}','decompressed_size':dec,'compressed_span':span,'compressed_sha256':hashlib.sha256(comp).hexdigest()})
            pos += 1
    roms.sort(key=lambda r:r['id'])
    (out/'manifests'/'roms.json').write_text(json.dumps(roms,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fields=list(roms[0].keys()); write_csv(out/'manifests'/'roms.csv',roms,fields)
    write_csv(out/'reports'/'page_fingerprints_64k.csv',page_rows,list(page_rows[0].keys()))
    if lz_rows: write_csv(out/'reports'/'lz77_candidates.csv',lz_rows,list(lz_rows[0].keys()))

    # page equivalence at same offset
    eq=defaultdict(list)
    for r in page_rows: eq[(r['page_index'],r['sha256'])].append(r['id'])
    eq_rows=[]
    for (pi,sha),ids in sorted(eq.items()):
        if len(ids)>=2:
            eq_rows.append({'page_index':pi,'offset_hex':f'0x{pi*PAGE:08X}','sha256':sha,'rom_count':len(ids),'rom_ids':'|'.join(sorted(ids))})
    if eq_rows: write_csv(out/'reports'/'page_equivalence_groups.csv',eq_rows,list(eq_rows[0].keys()))

    # revision diffs within same language/game code, and debug vs retail
    by_code=defaultdict(list)
    for r in roms: by_code[r['game_code']].append(r)
    sum_rows=[]; range_rows=[]; changed_page_rows=[]
    for code,rs in sorted(by_code.items()):
        rs=sorted(rs,key=lambda x:(x['software_version'],'DEBUG' in x['id']))
        for i in range(len(rs)):
            for j in range(i+1,len(rs)):
                a,b=rs[i],rs[j]; A=blobs[a['id']];B=blobs[b['id']]
                rr=diff_ranges(A,B); diffbytes=sum(e-s for s,e in rr)
                store_ranges = args.exhaustive_ranges or len(rr) <= 10000
                sum_rows.append({'game_code':code,'base_id':a['id'],'target_id':b['id'],'base_size':len(A),'target_size':len(B),'diff_bytes':diffbytes,'diff_pct':f'{diffbytes/max(len(A),len(B))*100:.6f}','range_count':len(rr),'range_details_stored':store_ranges,'first_diff_hex':f'0x{rr[0][0]:08X}' if rr else '','last_diff_exclusive_hex':f'0x{rr[-1][1]:08X}' if rr else ''})
                if store_ranges:
                    for k,(s,e) in enumerate(rr):
                        aa=A[s:min(e,len(A))]; bb=B[s:min(e,len(B))]
                        range_rows.append({'game_code':code,'base_id':a['id'],'target_id':b['id'],'range_index':k,'start_hex':f'0x{s:08X}','end_exclusive_hex':f'0x{e:08X}','length':e-s,'base_range_sha256':hashlib.sha256(aa).hexdigest(),'target_range_sha256':hashlib.sha256(bb).hexdigest()})
                # Always persist a compact 64 KiB changed-page map, including large rebuilds.
                maxn=max(len(A),len(B))
                for po in range(0,maxn,PAGE):
                    aa=A[po:po+PAGE]; bb=B[po:po+PAGE]
                    if aa==bb: continue
                    n=min(len(aa),len(bb)); db=sum(1 for x,y in zip(aa[:n],bb[:n]) if x!=y)+abs(len(aa)-len(bb))
                    changed_page_rows.append({'game_code':code,'base_id':a['id'],'target_id':b['id'],'page_index':po//PAGE,'offset_hex':f'0x{po:08X}','different_bytes':db,'base_page_sha256':hashlib.sha256(aa).hexdigest(),'target_page_sha256':hashlib.sha256(bb).hexdigest()})
    if sum_rows: write_csv(out/'reports'/'revision_diff_summary.csv',sum_rows,list(sum_rows[0].keys()))
    if range_rows: write_csv(out/'reports'/'revision_diff_ranges_small.csv',range_rows,list(range_rows[0].keys()))
    if changed_page_rows: write_csv(out/'reports'/'revision_changed_pages_64k.csv',changed_page_rows,list(changed_page_rows[0].keys()))

    # Compact Markdown reports
    lines=['# Pokémon Ruby ROM Identity Matrix','',f'ROM count: **{len(roms)}**','', '| ID | Size | Game code | Rev | Header checksum | SHA-256 |','|---|---:|---|---:|---|---|']
    for r in roms:
        lines.append(f"| {r['id']} | {r['size_bytes']} | {r['game_code']} | {r['software_version']} | {'OK' if r['header_checksum_ok'] else 'FAIL'} | `{r['sha256']}` |")
    (out/'reports'/'identity_matrix.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

    lines=['# Revision Difference Summary','', '| Code | Base | Target | Different bytes | Percent | Ranges |','|---|---|---|---:|---:|---:|']
    for r in sum_rows:
        lines.append(f"| {r['game_code']} | {r['base_id']} | {r['target_id']} | {r['diff_bytes']} | {r['diff_pct']}% | {r['range_count']} |")
    (out/'reports'/'revision_diff_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

    stats=defaultdict(int)
    for r in lz_rows: stats[r['id']]+=1
    lines=['# Validated GBA LZ77 Candidate Counts','', '| ROM | Candidates |','|---|---:|']
    for r in roms: lines.append(f"| {r['id']} | {stats[r['id']]} |")
    (out/'reports'/'lz77_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

    print(f'Generated {len(roms)} ROM records, {len(page_rows)} pages, {len(lz_rows)} validated LZ77 candidates, {len(range_rows)} stored diff ranges, {len(changed_page_rows)} changed-page records.')
if __name__=='__main__':main()
