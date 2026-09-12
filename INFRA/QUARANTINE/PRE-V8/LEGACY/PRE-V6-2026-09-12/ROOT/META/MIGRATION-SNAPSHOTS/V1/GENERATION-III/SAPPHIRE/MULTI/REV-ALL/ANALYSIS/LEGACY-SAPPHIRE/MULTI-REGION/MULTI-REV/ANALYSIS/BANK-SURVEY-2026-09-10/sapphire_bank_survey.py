from pathlib import Path
import hashlib, zlib, math, csv, json, itertools, statistics
from collections import defaultdict, Counter
import numpy as np

BANK=0x10000
BASE=0x08000000
OUT=Path('/mnt/data/sapphire_bank_survey')
OUT.mkdir(exist_ok=True)
ROM_PATHS=sorted(Path('/mnt/data').glob('*.gba'))

def longest_true_run(mask):
    if not mask.any(): return 0
    x=np.concatenate(([False],mask,[False])).astype(np.int8)
    d=np.diff(x)
    starts=np.where(d==1)[0]; ends=np.where(d==-1)[0]
    return int((ends-starts).max()) if len(starts) else 0

def ascii_runs(mask,minlen=4):
    if not mask.any(): return 0,0
    x=np.concatenate(([False],mask,[False])).astype(np.int8)
    d=np.diff(x); starts=np.where(d==1)[0]; ends=np.where(d==-1)[0]
    lens=ends-starts; good=lens>=minlen
    return int(good.sum()), int(lens[good].sum())

def header_info(data):
    title=data[0xA0:0xAC].rstrip(b'\0').decode('ascii','replace')
    code=data[0xAC:0xB0].decode('ascii','replace')
    maker=data[0xB0:0xB2].decode('ascii','replace')
    rev=data[0xBC]; chk=data[0xBD]; calc=(-sum(data[0xA0:0xBD])-0x19)&0xff
    return dict(title=title,game_code=code,maker=maker,revision=rev,fixed_value=data[0xB2],header_checksum=chk,header_checksum_calc=calc,header_checksum_ok=(chk==calc))

def bank_metrics(chunk,rom_size):
    arr=np.frombuffer(chunk,dtype=np.uint8)
    hist=np.bincount(arr,minlength=256)
    nz=hist[hist>0]; probs=nz/arr.size
    ent=float(-(probs*np.log2(probs)).sum())
    zmask=arr==0; fmask=arr==255
    printable=((arr>=0x20)&(arr<=0x7e)) | (arr==9)|(arr==10)|(arr==13)
    aruns, achars=ascii_runs(printable)
    words=np.frombuffer(chunk,dtype='<u4')
    rp=int(((words>=BASE)&(words<BASE+rom_size)).sum())
    ep=int(((words>=0x02000000)&(words<0x02040000)).sum())
    ip=int(((words>=0x03000000)&(words<0x03008000)).sum())
    iop=int(((words>=0x04000000)&(words<0x04000400)).sum())
    if arr.size>=4:
        t=arr[:-3]
        sizes=arr[1:-2].astype(np.uint32) | (arr[2:-1].astype(np.uint32)<<8) | (arr[3:].astype(np.uint32)<<16)
        plausible=(sizes>=1)&(sizes<=0x200000)
        lz=int(((t==0x10)&plausible).sum())
        hf=int((((t==0x20)|(t==0x24))&plausible).sum())
        rle=int(((t==0x30)&plausible).sum())
    else: lz=hf=rle=0
    return ent,int((hist>0).sum()),int(hist[0]),int(hist[255]),longest_true_run(zmask),longest_true_run(fmask),aruns,achars,rp,ep,ip,iop,lz,hf,rle

roms=[]; rows=[]; rom_data={}
for p in ROM_PATHS:
    data=p.read_bytes(); h=header_info(data); rid=f"{h['game_code']}_rev{h['revision']}"
    if rid in rom_data: rid += '_' + hashlib.sha1(data).hexdigest()[:8]
    rom_data[rid]=data
    meta={'id':rid,'file':p.name,'size':len(data),'banks':len(data)//BANK,'sha1':hashlib.sha1(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest(),'crc32':f"{zlib.crc32(data)&0xffffffff:08X}",**h}
    roms.append(meta)
    for bi in range(0,len(data),BANK):
        chunk=data[bi:bi+BANK]; idx=bi//BANK
        (ent,uniq,zc,fc,zrun,frun,aruns,achars,rp,ep,ip,iop,lz,hf,rle)=bank_metrics(chunk,len(data))
        if fc*100/len(chunk)>=99.9: cls='FF_blank'
        elif zc*100/len(chunk)>=99.9: cls='00_blank'
        elif ent<1.0 and ((fc+zc)*100/len(chunk)>90): cls='sparse'
        elif ent>=7.5: cls='high_entropy'
        elif rp>=256: cls='pointer_dense'
        elif lz+hf+rle>=16: cls='compression_candidate_dense'
        else: cls='mixed'
        rows.append({'rom_id':rid,'file':p.name,'game_code':h['game_code'],'revision':h['revision'],'bank_index':idx,'bank_hex':f"{idx:02X}",'file_start':bi,'file_end':bi+len(chunk)-1,'gba_start':f"0x{BASE+bi:08X}",'gba_end':f"0x{BASE+bi+len(chunk)-1:08X}",'size':len(chunk),'crc32':f"{zlib.crc32(chunk)&0xffffffff:08X}",'sha1':hashlib.sha1(chunk).hexdigest(),'sha256':hashlib.sha256(chunk).hexdigest(),'entropy':round(ent,6),'unique_bytes':uniq,'zero_count':zc,'ff_count':fc,'zero_pct':round(zc*100/len(chunk),4),'ff_pct':round(fc*100/len(chunk),4),'longest_zero_run':zrun,'longest_ff_run':frun,'ascii_runs_ge4':aruns,'ascii_chars_in_runs':achars,'rom_pointer_words':rp,'ewram_pointer_words':ep,'iwram_pointer_words':ip,'io_pointer_words':iop,'lz77_header_candidates':lz,'huffman_header_candidates':hf,'rle_header_candidates':rle,'coarse_class':cls})

byrom=defaultdict(list)
for r in rows: byrom[r['rom_id']].append(r)
rom_ids=[m['id'] for m in roms]; lookup={(r['rom_id'],r['bank_index']):r for r in rows}
max_banks=max(m['banks'] for m in roms)
aligned=[]; pairwise=[]
for idx in range(max_banks):
    present=[rid for rid in rom_ids if idx*BANK<len(rom_data[rid])]
    groups=defaultdict(list)
    for rid in present: groups[lookup[(rid,idx)]['sha256']].append(rid)
    aligned.append({'bank_index':idx,'bank_hex':f"{idx:02X}",'gba_start':f"0x{BASE+idx*BANK:08X}",'present_roms':present,'exact_match_groups':[g for g in groups.values() if len(g)>=2],'distinct_hashes':len(groups)})
    for a,b in itertools.combinations(present,2):
        aa=np.frombuffer(rom_data[a][idx*BANK:(idx+1)*BANK],dtype=np.uint8); bb=np.frombuffer(rom_data[b][idx*BANK:(idx+1)*BANK],dtype=np.uint8)
        diff=int((aa!=bb).sum())
        pairwise.append({'bank_index':idx,'bank_hex':f"{idx:02X}",'rom_a':a,'rom_b':b,'different_bytes':diff,'different_pct':round(diff*100/BANK,6),'identical':diff==0})

wanted=[]
for code in ('AXPE','AXPF','AXPI'):
    vs=sorted([m for m in roms if m['game_code']==code],key=lambda x:x['revision'])
    wanted += [(a['id'],b['id']) for a,b in itertools.combinations(vs,2)]
rev_rows=[]
for a,b in wanted:
    n=min(len(rom_data[a]),len(rom_data[b]))//BANK
    for idx in range(n):
        aa=np.frombuffer(rom_data[a][idx*BANK:(idx+1)*BANK],dtype=np.uint8); bb=np.frombuffer(rom_data[b][idx*BANK:(idx+1)*BANK],dtype=np.uint8)
        pos=np.flatnonzero(aa!=bb)
        if pos.size:
            rev_rows.append({'rom_a':a,'rom_b':b,'bank_index':idx,'bank_hex':f"{idx:02X}",'different_bytes':int(pos.size),'first_diff_in_bank':int(pos[0]),'last_diff_in_bank':int(pos[-1]),'first_diff_file_offset':idx*BANK+int(pos[0]),'last_diff_file_offset':idx*BANK+int(pos[-1])})

summaries=[]
for m in roms:
    rr=byrom[m['id']]; blank=[r for r in rr if r['coarse_class'] in ('FF_blank','00_blank')]; used=[r for r in rr if r['coarse_class'] not in ('FF_blank','00_blank')]
    summaries.append({**m,'mean_bank_entropy':round(statistics.mean(r['entropy'] for r in rr),6),'min_bank_entropy':min(r['entropy'] for r in rr),'max_bank_entropy':max(r['entropy'] for r in rr),'blank_banks':len(blank),'nonblank_banks':len(used),'last_nonblank_bank':max((r['bank_index'] for r in used),default=None),'total_rom_pointer_words':sum(r['rom_pointer_words'] for r in rr),'total_lz77_candidates':sum(r['lz77_header_candidates'] for r in rr),'total_huffman_candidates':sum(r['huffman_header_candidates'] for r in rr),'total_rle_candidates':sum(r['rle_header_candidates'] for r in rr)})

def writecsv(path,data,fields=None):
    if fields is None: fields=list(data[0].keys())
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)
writecsv(OUT/'banks.csv',rows)
writecsv(OUT/'pairwise_aligned_bank_diffs.csv',pairwise)
writecsv(OUT/'revision_changed_banks.csv',rev_rows,['rom_a','rom_b','bank_index','bank_hex','different_bytes','first_diff_in_bank','last_diff_in_bank','first_diff_file_offset','last_diff_file_offset'])
writecsv(OUT/'rom_summary.csv',summaries)
(OUT/'manifest.json').write_text(json.dumps({'bank_size':BANK,'base_address':BASE,'roms':roms},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'aligned_exact_groups.json').write_text(json.dumps(aligned,ensure_ascii=False,indent=2),encoding='utf-8')

lines=['# Pokémon Sapphire ROM 64 KiB Logical-Bank Survey','',f'- Logical bank size: `0x{BANK:X}` (64 KiB)',f'- GBA ROM mapping base: `0x{BASE:08X}`',f'- ROMs surveyed: {len(roms)}',f'- Total bank-images surveyed: {len(rows)}','','## ROM summary','','| ROM | Code | Rev | Banks | Blank | Last nonblank | Mean entropy | ROM ptr words | LZ77 candidates |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for s in summaries: lines.append(f"| {s['file']} | {s['game_code']} | {s['revision']} | {s['banks']} | {s['blank_banks']} | {s['last_nonblank_bank']} | {s['mean_bank_entropy']:.4f} | {s['total_rom_pointer_words']} | {s['total_lz77_candidates']} |")
lines += ['','## Coarse bank classes','']
for m in roms:
    cnt=Counter(r['coarse_class'] for r in byrom[m['id']]); lines.append(f"- **{m['id']}**: "+', '.join(f"{k}={v}" for k,v in sorted(cnt.items())))
lines += ['','## Revision-pair changed banks','']
for a,b in wanted:
    x=[r for r in rev_rows if r['rom_a']==a and r['rom_b']==b]; total=sum(r['different_bytes'] for r in x); banks=', '.join(f"0x{r['bank_index']:02X}({r['different_bytes']} B)" for r in x[:40]); banks += (f", … +{len(x)-40} banks" if len(x)>40 else '')
    lines.append(f"- **{a} → {b}**: changed banks={len(x)}, total changed bytes={total:,}. {banks or 'No changes.'}")
lines += ['','## Notes','','- `coarse_class` is heuristic, not a semantic label. It prioritizes deeper disassembly/data analysis.','- Compression counts are plausible BIOS-format header candidates, not confirmed compressed assets.','- Pointer counts inspect 4-byte-aligned little-endian words targeting ROM/EWRAM/IWRAM/I/O ranges.','- Localized builds can relocate data, so aligned-bank difference does not automatically mean semantic difference.']
(OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'roms':len(roms),'bank_images':len(rows),'out':str(OUT),'summaries':summaries},ensure_ascii=False,indent=2))
