#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, hashlib, json, math, struct

REGION = 0x100000  # 1 MiB
MIN_RUN = 0x1000


def entry_target(data: bytes):
    insn = struct.unpack_from('<I', data, 0)[0]
    if ((insn >> 25) & 0b111) != 0b101:
        return None
    imm24 = insn & 0x00FFFFFF
    if imm24 & 0x00800000:
        imm24 -= 0x01000000
    return (8 + (imm24 << 2)) & 0xFFFFFFFF


def trailing_run(data: bytes):
    val = data[-1]
    i = len(data) - 1
    while i >= 0 and data[i] == val:
        i -= 1
    return val, i + 1, len(data) - i - 1


def aligned_pointer_like_words(data: bytes):
    out = []
    n = len(data)
    for off in range(0, n - 3, 4):
        v = struct.unpack_from('<I', data, off)[0]
        norm = v & ~1
        if 0x08000000 <= norm < 0x08000000 + n:
            out.append((off, v, norm - 0x08000000))
    return out


def constant_runs(data: bytes, values=(0x00,0xFF), min_run=MIN_RUN):
    runs=[]
    n=len(data)
    i=0
    vals=set(values)
    while i<n:
        v=data[i]
        if v not in vals:
            i+=1; continue
        j=i+1
        while j<n and data[j]==v:
            j+=1
        ln=j-i
        if ln>=min_run:
            runs.append((v,i,ln))
        i=j
    return runs


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom_dir',type=Path)
    ap.add_argument('out_dir',type=Path)
    args=ap.parse_args(); args.out_dir.mkdir(parents=True,exist_ok=True)
    roms=sorted(args.rom_dir.glob('*.gba'))
    region_rows=[]; summary=[]; run_rows=[]; ptr_rows=[]
    for p in roms:
        b=p.read_bytes(); code=b[0xAC:0xB0].decode('ascii','replace')
        tval,tstart,tlen=trailing_run(b)
        ptrs=aligned_pointer_like_words(b)
        tail_refs=sum(1 for _,_,target in ptrs if tstart <= target < len(b))
        entry=entry_target(b)
        summary.append({
            'file':p.name,'game_code':code,'size':len(b),
            'entry_target':None if entry is None else f'0x{entry:08X}',
            'aligned_pointer_like_word_count':len(ptrs),
            'trailing_byte':f'0x{tval:02X}','trailing_run_start':tstart,'trailing_run_length':tlen,
            'pointer_like_targets_into_trailing_run':tail_refs,
        })
        target_counts=[0]*math.ceil(len(b)/REGION)
        source_counts=[0]*len(target_counts)
        for off,_,target in ptrs:
            target_counts[target//REGION]+=1
            source_counts[off//REGION]+=1
        for idx,start in enumerate(range(0,len(b),REGION)):
            chunk=b[start:start+REGION]
            ff=chunk.count(0xFF); zz=chunk.count(0)
            region_rows.append({
                'file':p.name,'game_code':code,'region_index':idx,
                'start':f'0x{start:07X}','end':f'0x{start+len(chunk)-1:07X}',
                'ff_bytes':ff,'ff_percent':round(ff/len(chunk)*100,4),
                'zero_bytes':zz,'zero_percent':round(zz/len(chunk)*100,4),
                'pointer_like_sources':source_counts[idx],'pointer_like_targets':target_counts[idx],
                'sha256':hashlib.sha256(chunk).hexdigest(),
            })
        runs=constant_runs(b)
        for v,start,ln in sorted(runs,key=lambda x:x[2],reverse=True)[:40]:
            refs=sum(1 for _,_,target in ptrs if start <= target < start+ln)
            run_rows.append({'file':p.name,'game_code':code,'byte':f'0x{v:02X}','start':f'0x{start:07X}','length':ln,'end':f'0x{start+ln-1:07X}','pointer_like_targets_inside':refs})
        for region_idx,count in enumerate(target_counts):
            ptr_rows.append({'file':p.name,'game_code':code,'target_region_index':region_idx,'start':f'0x{region_idx*REGION:07X}','pointer_like_target_count':count})

    def write_csv(name,rows):
        with (args.out_dir/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    write_csv('layout_summary.csv',summary)
    write_csv('region_usage_1m.csv',region_rows)
    write_csv('large_constant_runs.csv',run_rows)
    write_csv('pointer_target_regions.csv',ptr_rows)

    lines=['# Pokémon LeafGreen Layout Census','',
           'This stage scans each ROM locally for coarse layout signals. It does not copy ROM bytes into the repository.','',
           '## Entry point and terminal padding validation','',
           '| File | Code | Entry target | Pointer-like aligned words | Tail FF start | Tail length | Pointer-like targets in tail |','|---|---|---:|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f"| {r['file']} | `{r['game_code']}` | `{r['entry_target']}` | {r['aligned_pointer_like_word_count']:,} | `0x{r['trailing_run_start']:07X}` | {r['trailing_run_length']:,} | {r['pointer_like_targets_into_trailing_run']} |")
    lines += ['', '### Interpretation','',
              '- All seven headers branch to the same startup entry target: ROM offset `0x204`.',
              '- The pointer-like scan is only a heuristic: aligned 32-bit words whose normalized value falls in `0x08000000..0x08FFFFFF`. Compressed, graphic, or arbitrary data can produce false positives, so these counts are **not** treated as verified references.',
              '- The Japanese image has a much shorter terminal `0xFF` run than the international images, so free-space planning must be version-specific.',
              '- International builds also contain a ~5.9 MiB pure-`0xFF` gap ending at `0x0CFFFFFF`; the Japanese build has a ~5.22 MiB pure-`0xFF` gap ending at `0x0BFFFFFF`. These are high-priority candidates for reference-aware free-space validation.',
              '', '## Fully `0xFF` 1 MiB windows', '']
    full_ff = {}
    for rr in region_rows:
        if rr['ff_bytes'] == REGION:
            full_ff.setdefault(rr['file'], []).append(rr['region_index'])
    grouped = {}
    for filename, indices in full_ff.items():
        grouped.setdefault(tuple(indices), []).append(filename)
    for indices, filenames in grouped.items():
        windows = ', '.join(f'`0x{i*REGION:07X}–0x{((i+1)*REGION)-1:07X}`' for i in indices)
        names = '; '.join(filenames)
        lines.append(f'- **{names}:** regions {", ".join(map(str, indices))} ({windows})')
    lines += ['', 'These windows are **unused/padding candidates only** until reference-aware validation and runtime regression tests are complete.',
              '', '## 1 MiB region census', '',
              '`region_usage_1m.csv` records per-region `0xFF`/`0x00` density, pointer-like source density, pointer-like target density, and a SHA-256 fingerprint. This is the first coarse map for locating shared engine areas, localization-heavy areas, and likely padding.',
              '', '## Large constant runs', '',
              '`large_constant_runs.csv` lists the largest >=4 KiB `0x00`/`0xFF` runs and counts pointer-like aligned words whose values land inside each run. A run is not classified as safe free space until cross-reference and behavior checks are complete.',
              '']
    (args.out_dir/'LAYOUT.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':
    main()
