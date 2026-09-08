#!/usr/bin/env python3
from pathlib import Path
from itertools import combinations
from collections import Counter, defaultdict
import hashlib, json, csv, math, zlib, shutil, sys

BANK_SIZE = 0x4000
CATALOG = {
    '392ce450d708c8d127aaed7afc20001a48625bd83a5fa5325be82f5c0972ccfa': {'region':'JP','rev':'REV-0','canonical':'Pocket Monsters Aka (Japan) Rev 0','short':'jp_rev0'},
    '751abb1fb2b2d6b91dc631fa10ed36bd07f682cb5c3febe6c8f0e3dabc1fae1c': {'region':'JP','rev':'REV-A','canonical':'Pocket Monsters Aka (Japan) Rev A','short':'jp_reva'},
    '5ca7ba01642a3b27b0cc0b5349b52792795b62d3ed977e98a09390659af96b7b': {'region':'USA-EUROPE','rev':'REV-0','canonical':'Pokemon Red Version (USA, Europe)','short':'en_rev0'},
    '9cd186b288dbcd52413d561ae449f1f700c32b45af56dbf849095d4a0c8637a6': {'region':'DE','rev':'REV-0','canonical':'Pokemon Rote Edition (Germany)','short':'de_rev0'},
    '23766290f3b2347f815f1e8977c3b84047ed880cadda8c4f1a3595a633daa303': {'region':'FR','rev':'REV-0','canonical':'Pokemon Version Rouge (France)','short':'fr_rev0'},
    'e805d00b0002156d38b96efd57c823b0db3a3ef4cd32f98bd9bb4779bda3dd5b': {'region':'IT','rev':'REV-0','canonical':'Pokemon Versione Rossa (Italy)','short':'it_rev0'},
    'a756cf7ad888aa46de4b9699a177a0edf1775e59eb6330014c6f5c139be9c45d': {'region':'ES','rev':'REV-0','canonical':'Pokemon Edicion Roja (Spain)','short':'es_rev0'},
}
CART_TYPES = {0x00:'ROM ONLY',0x01:'MBC1',0x02:'MBC1+RAM',0x03:'MBC1+RAM+BATTERY',0x0f:'MBC3+TIMER+BATTERY',0x10:'MBC3+TIMER+RAM+BATTERY',0x11:'MBC3',0x12:'MBC3+RAM',0x13:'MBC3+RAM+BATTERY',0x19:'MBC5',0x1a:'MBC5+RAM',0x1b:'MBC5+RAM+BATTERY'}
ROM_SIZES = {0x00:32*1024,0x01:64*1024,0x02:128*1024,0x03:256*1024,0x04:512*1024,0x05:1024*1024,0x06:2*1024*1024,0x07:4*1024*1024,0x08:8*1024*1024}
RAM_SIZES = {0x00:0,0x01:2*1024,0x02:8*1024,0x03:32*1024,0x04:128*1024,0x05:64*1024}

def h256(b): return hashlib.sha256(b).hexdigest()
def h1(b): return hashlib.sha1(b).hexdigest()
def hmd5(b): return hashlib.md5(b).hexdigest()
def ent(b):
    c=Counter(b); n=len(b)
    return 0.0 if not n else -sum((v/n)*math.log2(v/n) for v in c.values())
def header_checksum(b):
    x=0
    for v in b[0x134:0x14d]: x=(x-v-1)&0xff
    return x
def global_checksum(b): return (sum(b)-b[0x14e]-b[0x14f])&0xffff
def header_info(b):
    return {
        'title':b[0x134:0x144].split(b'\0',1)[0].decode('ascii','replace'),
        'cgb_flag':b[0x143],'sgb_flag':b[0x146],
        'cartridge_type_code':b[0x147],'cartridge_type':CART_TYPES.get(b[0x147],f'UNKNOWN_0x{b[0x147]:02X}'),
        'rom_size_code':b[0x148],'declared_rom_bytes':ROM_SIZES.get(b[0x148]),
        'ram_size_code':b[0x149],'declared_ram_bytes':RAM_SIZES.get(b[0x149]),
        'destination_code':b[0x14a],'old_licensee_code':b[0x14b],'rom_version':b[0x14c],
        'header_checksum_stored':b[0x14d],'header_checksum_calculated':header_checksum(b),'header_checksum_ok':b[0x14d]==header_checksum(b),
        'global_checksum_stored':int.from_bytes(b[0x14e:0x150],'big'),'global_checksum_calculated':global_checksum(b),'global_checksum_ok':int.from_bytes(b[0x14e:0x150],'big')==global_checksum(b),
    }
def repeated_runs(b,min_len=64):
    out=[]; i=0
    while i<len(b):
        v=b[i]
        if v not in (0,255): i+=1; continue
        j=i+1
        while j<len(b) and b[j]==v: j+=1
        if j-i>=min_len: out.append((i,j,v))
        i=j
    return out
def diff_ranges(a,b):
    n=min(len(a),len(b)); out=[]; i=0
    while i<n:
        if a[i]==b[i]: i+=1; continue
        s=i
        while i<n and a[i]!=b[i]: i+=1
        out.append((s,i))
    if len(a)!=len(b): out.append((n,max(len(a),len(b))))
    return out
def cpu_addr(bank,off): return off if bank==0 else 0x4000+off
def mkdir(p): p.mkdir(parents=True,exist_ok=True); return p
def wc(path,rows,fields):
    mkdir(path.parent)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
def wj(path,obj): mkdir(path.parent); path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def analyze(input_dir, output_dir):
    input_dir=Path(input_dir); out=Path(output_dir)
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    found=[]
    for p in sorted(input_dir.glob('*.gb')):
        b=p.read_bytes(); sh=h256(b)
        if sh in CATALOG: found.append({'name':p.name,'bytes':b,'sha256':sh,'cat':CATALOG[sh]})
    byhash=defaultdict(list)
    for x in found: byhash[x['sha256']].append(x)
    unique=[]
    for sh,items in sorted(byhash.items(),key=lambda kv: CATALOG[kv[0]]['short']):
        x=items[0].copy(); x['input_names']=[i['name'] for i in items]; unique.append(x)
    if not unique: raise SystemExit('no recognized Red ROMs found')

    multi=mkdir(out/'GENERATION-I/RED/MULTI-REGION/REV-MIXED/analysis')
    master=[]
    for x in unique:
        b=x['bytes']; c=x['cat']; hi=header_info(b)
        master.append({'id':c['short'],'canonical':c['canonical'],'region':c['region'],'revision':c['rev'],'input_names':' | '.join(x['input_names']),'duplicate_input_count':len(x['input_names']),'size_bytes':len(b),'bank_count':len(b)//BANK_SIZE,'md5':hmd5(b),'sha1':h1(b),'sha256':x['sha256'],'crc32':f'{zlib.crc32(b)&0xffffffff:08x}',**hi})
    wc(multi/'master-rom-manifest.csv',master,list(master[0]))
    wj(multi/'master-rom-manifest.json',master)
    wj(multi/'duplicate-groups.json',[{'sha256':sh,'canonical':CATALOG[sh]['canonical'],'input_names':[i['name'] for i in items]} for sh,items in sorted(byhash.items()) if len(items)>1])

    bank_hashes=[]; bank_stats=[]; padding=[]; layouts=[]
    for x in unique:
        b=x['bytes']; c=x['cat']; hi=header_info(b); rid=c['short']
        base=mkdir(out/f"GENERATION-I/RED/{c['region']}/{c['rev']}/analysis")
        row=next(r for r in master if r['id']==rid)
        wj(base/'rom-manifest.json',row)
        (base/'rom-manifest.md').write_text('\n'.join([f"# {c['canonical']} — ROM manifest",'',f"- Region: `{c['region']}`",f"- Revision: `{c['rev']}`",f"- Size: `{len(b)}` bytes",f"- Banks: `{len(b)//BANK_SIZE}`",f"- Cartridge: `{hi['cartridge_type']}`",f"- SHA-256: `{x['sha256']}`",f"- SHA-1: `{h1(b)}`",f"- MD5: `{hmd5(b)}`",f"- CRC32: `{zlib.crc32(b)&0xffffffff:08x}`",f"- Header checksum: `{'OK' if hi['header_checksum_ok'] else 'FAIL'}`",f"- Global checksum: `{'OK' if hi['global_checksum_ok'] else 'FAIL'}`",'', 'Input filenames seen:',*[f"- `{n}`" for n in x['input_names']], '']),encoding='utf-8')
        ph=[]; ps=[]; pp=[]; pl=[]; hist=[]
        for bank in range((len(b)+BANK_SIZE-1)//BANK_SIZE):
            s=bank*BANK_SIZE; e=min(s+BANK_SIZE,len(b)); bb=b[s:e]; cnt=Counter(bb)
            hr={'rom_id':rid,'bank':bank,'bank_hex':f'{bank:02X}','file_start':s,'file_end_exclusive':e,'size':len(bb),'sha256':h256(bb),'sha1':h1(bb),'md5':hmd5(bb),'crc32':f'{zlib.crc32(bb)&0xffffffff:08x}'}
            sr={'rom_id':rid,'bank':bank,'bank_hex':f'{bank:02X}','entropy_bits_per_byte':f'{ent(bb):.8f}','unique_byte_values':len(cnt),'zero_bytes':cnt.get(0,0),'ff_bytes':cnt.get(255,0),'nonzero_nonff_bytes':len(bb)-cnt.get(0,0)-cnt.get(255,0)}
            lr={'rom_id':rid,'bank':bank,'bank_hex':f'{bank:02X}','file_start':s,'file_end_exclusive':e,'cpu_window_start':f"0x{(0 if bank==0 else 0x4000):04X}",'cpu_window_end_inclusive':f"0x{(0x3fff if bank==0 else 0x7fff):04X}"}
            ph.append(hr); ps.append(sr); pl.append(lr); bank_hashes.append(hr); bank_stats.append(sr); layouts.append(lr)
            hist.append({'rom_id':rid,'bank':bank,'bank_hex':f'{bank:02X}',**{f'byte_{i:02X}':cnt.get(i,0) for i in range(256)}})
            for rs,re,v in repeated_runs(bb):
                pr={'rom_id':rid,'bank':bank,'bank_hex':f'{bank:02X}','value':f'0x{v:02X}','bank_offset_start':rs,'bank_offset_end_exclusive':re,'file_start':s+rs,'file_end_exclusive':s+re,'length':re-rs,'cpu_addr_start':f'0x{cpu_addr(bank,rs):04X}','cpu_addr_end_inclusive':f'0x{cpu_addr(bank,re-1):04X}','classification':'padding_candidate_only'}
                pp.append(pr); padding.append(pr)
        wc(base/'bank-hashes.csv',ph,list(ph[0])); wc(base/'bank-stats.csv',ps,list(ps[0])); wc(base/'bank-layout.csv',pl,list(pl[0])); wc(base/'byte-histograms.csv',hist,list(hist[0]));
        wc(base/'padding-candidates.csv',pp,list(pp[0]) if pp else ['rom_id','bank','bank_hex','value','bank_offset_start','bank_offset_end_exclusive','file_start','file_end_exclusive','length','cpu_addr_start','cpu_addr_end_inclusive','classification'])
        (base/'checksums.txt').write_text(f"MD5 {hmd5(b)}\nSHA1 {h1(b)}\nSHA256 {x['sha256']}\nCRC32 {zlib.crc32(b)&0xffffffff:08x}\n",encoding='utf-8')

    groups=defaultdict(list)
    for r in bank_hashes: groups[r['sha256']].append((r['rom_id'],r['bank']))
    eq=[]
    for gid,(sh,members) in enumerate([(sh,m) for sh,m in sorted(groups.items()) if len(m)>1],1):
        eq.append({'group_id':gid,'bank_sha256':sh,'member_count':len(members),'members':' | '.join(f'{rid}:bank_{bank:02X}' for rid,bank in sorted(members))})
    wc(multi/'bank-equivalence-groups.csv',eq,['group_id','bank_sha256','member_count','members'])

    pair_summary=[]; pair_bank=[]; diffdir=mkdir(multi/'pairwise-diff-ranges')
    for a,b in combinations(unique,2):
        aid=a['cat']['short']; bid=b['cat']['short']; ab=a['bytes']; bb=b['bytes']; n=min(len(ab),len(bb))
        overlap_diff=sum(x!=y for x,y in zip(ab[:n],bb[:n])); total_diff=overlap_diff+abs(len(ab)-len(bb)); ranges=diff_ranges(ab,bb)
        bank_count=max((len(ab)+BANK_SIZE-1)//BANK_SIZE,(len(bb)+BANK_SIZE-1)//BANK_SIZE); diff_bank_count=0
        for bank in range(bank_count):
            ba=ab[bank*BANK_SIZE:(bank+1)*BANK_SIZE]; bbk=bb[bank*BANK_SIZE:(bank+1)*BANK_SIZE]; m=min(len(ba),len(bbk)); d=sum(x!=y for x,y in zip(ba[:m],bbk[:m]))+abs(len(ba)-len(bbk))
            if d: diff_bank_count+=1
            pair_bank.append({'rom_a':aid,'rom_b':bid,'bank':bank,'bank_hex':f'{bank:02X}','bytes_a':len(ba),'bytes_b':len(bbk),'differing_bytes':d,'identical_bank':len(ba)==len(bbk) and h256(ba)==h256(bbk)})
        pair_summary.append({'rom_a':aid,'rom_b':bid,'bytes_a':len(ab),'bytes_b':len(bb),'overlap_bytes':n,'differing_bytes':total_diff,'same_bytes_in_overlap':n-overlap_diff,'difference_percent_of_max':f'{100*total_diff/max(len(ab),len(bb)):.6f}','diff_range_count':len(ranges),'differing_bank_count':diff_bank_count,'max_bank_count':bank_count})
        rows=[{'rom_a':aid,'rom_b':bid,'file_start':s,'file_end_exclusive':e,'length':e-s,'start_bank':s//BANK_SIZE,'end_bank':(e-1)//BANK_SIZE,'start_bank_offset':s%BANK_SIZE,'end_bank_offset_exclusive':((e-1)%BANK_SIZE)+1} for s,e in ranges]
        wc(diffdir/f'{aid}__vs__{bid}.csv',rows,['rom_a','rom_b','file_start','file_end_exclusive','length','start_bank','end_bank','start_bank_offset','end_bank_offset_exclusive'])
    wc(multi/'pairwise-summary.csv',pair_summary,list(pair_summary[0])); wc(multi/'pairwise-bank-diff.csv',pair_bank,list(pair_bank[0])); wc(multi/'all-bank-hashes.csv',bank_hashes,list(bank_hashes[0])); wc(multi/'all-bank-stats.csv',bank_stats,list(bank_stats[0])); wc(multi/'all-bank-layout.csv',layouts,list(layouts[0])); wc(multi/'all-padding-candidates.csv',padding,list(padding[0]))

    jp=next(r for r in pair_summary if {r['rom_a'],r['rom_b']}=={'jp_rev0','jp_reva'})
    mapper_counts=Counter(r['cartridge_type'] for r in master)
    region_revs=', '.join(r['region']+'/'+r['revision'] for r in master)
    overview='\n'.join(['# Pokémon Red ROM set — structural overview','', '## Scope','',f"- Input `.gb` files found: **{len(found)}** recognized files",f"- Unique recognized ROM images: **{len(unique)}**",f"- Exact duplicate groups: **{sum(1 for v in byhash.values() if len(v)>1)}**",f"- Unique regions/revisions: {region_revs}",'', '## Cartridge families','',*[f'- {k}: {v} ROM(s)' for k,v in sorted(mapper_counts.items())],'','## Japanese revision delta','',f"JP Rev 0 vs Rev A differs in **{jp['differing_bytes']} bytes**, across **{jp['differing_bank_count']} banks**, represented by **{jp['diff_range_count']} contiguous differing ranges**.",'','## Reproducibility boundary','', 'This analysis stores addresses, hashes, statistics, and difference ranges but no replacement byte values. It documents and verifies the ROM set without embedding original ROM data.','','## Next semantic layers','', 'Structural reproducibility is complete at file/header/bank/difference level. Add semantic layers separately: control-flow/code map, pointer map, text map, graphics map, species/move/item tables, maps/events, save structure, and expansion constraints.',''])
    (multi/'OVERVIEW.md').write_text(overview,encoding='utf-8')
    return len(found),len(unique)

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: analyze_roms.py INPUT_ROM_DIR OUTPUT_DIR')
    f,u=analyze(sys.argv[1],sys.argv[2]); print(f'OK: {f} recognized inputs, {u} unique ROMs')
