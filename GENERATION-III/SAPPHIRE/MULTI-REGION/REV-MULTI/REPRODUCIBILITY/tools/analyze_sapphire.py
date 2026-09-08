#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math
from pathlib import Path
import numpy as np

CHUNK = 64 * 1024
ROM_MAP = {
    'Pocket Monsters - Sapphire (Japan).gba': ('JAPANESE-JAPAN','REV-0'),
    'Pokemon - Saphir-Edition (Germany) (Rev 1).gba': ('GERMAN-GERMANY','REV-1'),
    'Pokemon - Sapphire Version (USA).gba': ('ENGLISH-USA','REV-0'),
    'Pokemon - Sapphire Version (Europe) (Rev 1).gba': ('ENGLISH-EUROPE','REV-1'),
    'Pokemon - Sapphire Version (USA, Europe) (Rev 2).gba': ('ENGLISH-USA-EUROPE','REV-2'),
    'Pokemon - Version Saphir (France).gba': ('FRENCH-FRANCE','REV-0'),
    'Pokemon - Version Saphir (France) (Rev 1).gba': ('FRENCH-FRANCE','REV-1'),
    'Pokemon - Versione Zaffiro (Italy).gba': ('ITALIAN-ITALY','REV-0'),
    'Pokemon - Versione Zaffiro (Italy) (Rev 1).gba': ('ITALIAN-ITALY','REV-1'),
}

def h(data: bytes, algo: str) -> str:
    x=hashlib.new(algo); x.update(data); return x.hexdigest()

def entropy(data: bytes) -> float:
    if not data: return 0.0
    a=np.frombuffer(data,dtype=np.uint8)
    c=np.bincount(a,minlength=256)
    p=c[c>0]/a.size
    return float(-(p*np.log2(p)).sum())

def header(data: bytes) -> dict:
    if len(data) < 0xC0: raise ValueError('too small for GBA header')
    title=data[0xA0:0xAC].decode('ascii','replace').rstrip('\0')
    game=data[0xAC:0xB0].decode('ascii','replace')
    maker=data[0xB0:0xB2].decode('ascii','replace')
    stored=data[0xBD]
    calc=(-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
    return {
        'title': title, 'game_code': game, 'maker_code': maker,
        'fixed_value_0x96': data[0xB2], 'unit_code': data[0xB3],
        'device_type': data[0xB4], 'software_version': data[0xBC],
        'header_complement_stored': stored, 'header_complement_calculated': calc,
        'header_complement_valid': stored == calc,
    }

def scan_fill_runs(data: bytes, min_len: int=256):
    a=np.frombuffer(data,dtype=np.uint8)
    if a.size == 0: return []
    cuts=np.flatnonzero(a[1:] != a[:-1]) + 1
    starts=np.concatenate(([0],cuts)); ends=np.concatenate((cuts,[a.size]))
    out=[]
    vals=a[starts]
    lens=ends-starts
    mask=((vals==0)|(vals==255)) & (lens>=min_len)
    for st,en,v in zip(starts[mask],ends[mask],vals[mask]):
        out.append((int(st),int(en-1),int(en-st),int(v)))
    return out

def pointer_bins(data: bytes, bin_size: int=1024*1024):
    n=len(data); words=np.frombuffer(data[:n-(n%4)],dtype='<u4')
    mask=(words>=0x08000000)&(words<0x08000000+n)
    idx=np.flatnonzero(mask)
    if idx.size==0: return {}
    vals=words[idx]
    src=((idx*4)//bin_size).astype(np.int64)
    dst=((vals.astype(np.uint64)-0x08000000)//bin_size).astype(np.int64)
    bins=(n+bin_size-1)//bin_size
    codes=src*bins+dst
    counts=np.bincount(codes,minlength=bins*bins)
    out={}
    nz=np.flatnonzero(counts)
    for code in nz:
        out[(int(code//bins),int(code%bins))]=int(counts[code])
    return out

def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom_dir',type=Path)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    found=[]
    for name,(region,rev) in ROM_MAP.items():
        p=args.rom_dir/name
        if not p.exists(): continue
        data=p.read_bytes(); hdr=header(data)
        rec={'filename':name,'language_region':region,'revision':rev,'size_bytes':len(data),
             'md5':h(data,'md5'),'sha1':h(data,'sha1'),'sha256':h(data,'sha256'), **hdr}
        found.append((p,data,rec))
    if not found: raise SystemExit('No known Sapphire ROMs found.')

    inv=[]; chunks=[]; ents=[]; fills=[]; ptrs=[]; hist=[]
    for p,data,rec in found:
        inv.append(rec)
        for i,start in enumerate(range(0,len(data),CHUNK)):
            c=data[start:start+CHUNK]
            chunks.append({'filename':p.name,'language_region':rec['language_region'],'revision':rec['revision'],
                           'chunk_index':i,'offset_start':f'0x{start:08X}','offset_end':f'0x{start+len(c)-1:08X}',
                           'size':len(c),'sha256':h(c,'sha256')})
            ents.append({'filename':p.name,'language_region':rec['language_region'],'revision':rec['revision'],
                         'chunk_index':i,'offset_start':f'0x{start:08X}','size':len(c),'entropy_bits_per_byte':f'{entropy(c):.6f}'})
        for start,end,length,b in scan_fill_runs(data):
            fills.append({'filename':p.name,'language_region':rec['language_region'],'revision':rec['revision'],
                          'offset_start':f'0x{start:08X}','offset_end':f'0x{end:08X}','length':length,'byte':f'0x{b:02X}'})
        for (src,dst),count in sorted(pointer_bins(data).items()):
            ptrs.append({'filename':p.name,'language_region':rec['language_region'],'revision':rec['revision'],
                         'source_1mib_bin':src,'target_1mib_bin':dst,'aligned_pointer_count':count})
        bc=np.bincount(np.frombuffer(data,dtype=np.uint8),minlength=256)
        for b in range(256):
            hist.append({'filename':p.name,'language_region':rec['language_region'],'revision':rec['revision'],
                         'byte':f'0x{b:02X}','count':int(bc[b])})

    pair=[]
    for i in range(len(found)):
        for j in range(i+1,len(found)):
            p1,d1,r1=found[i]; p2,d2,r2=found[j]
            n=min(len(d1),len(d2)); a1=np.frombuffer(d1[:n],dtype=np.uint8); a2=np.frombuffer(d2[:n],dtype=np.uint8); eq=int(np.count_nonzero(a1==a2))
            cc=min((len(d1)+CHUNK-1)//CHUNK,(len(d2)+CHUNK-1)//CHUNK)
            same_chunks=0
            for k in range(cc):
                a=d1[k*CHUNK:(k+1)*CHUNK]; b=d2[k*CHUNK:(k+1)*CHUNK]
                if a==b: same_chunks+=1
            pair.append({'a':p1.name,'b':p2.name,'bytes_compared':n,'equal_bytes':eq,
                         'equal_byte_ratio':f'{eq/n:.9f}','equal_64k_chunks':same_chunks,'chunks_compared':cc,
                         'size_delta':len(d2)-len(d1)})

    diffrows=[]
    groups={}
    for p,d,r in found: groups.setdefault(r['game_code'],[]).append((p,d,r))
    for game,items in groups.items():
        items=sorted(items,key=lambda x:x[2]['software_version'])
        for idx in range(len(items)-1):
            p1,d1,r1=items[idx]; p2,d2,r2=items[idx+1]
            n=min(len(d1),len(d2)); diffs=[]
            a1=np.frombuffer(d1[:n],dtype=np.uint8); a2=np.frombuffer(d2[:n],dtype=np.uint8)
            pos=np.flatnonzero(a1!=a2)
            if pos.size:
                breaks=np.flatnonzero(np.diff(pos)>16)+1
                groups=np.split(pos,breaks)
                diffs=[(int(g[0]),int(g[-1]),int(g.size)) for g in groups if g.size]
            for k,(s,e,local) in enumerate(diffs):
                diffrows.append({'game_code':game,'from_file':p1.name,'to_file':p2.name,
                                 'from_version':r1['software_version'],'to_version':r2['software_version'],
                                 'region_index':k,'offset_start':f'0x{s:08X}','offset_end':f'0x{e:08X}',
                                 'span_length':e-s+1,'changed_bytes_in_span':local})
            if len(d1)!=len(d2):
                diffrows.append({'game_code':game,'from_file':p1.name,'to_file':p2.name,
                                 'from_version':r1['software_version'],'to_version':r2['software_version'],
                                 'region_index':'TAIL','offset_start':f'0x{n:08X}','offset_end':f'0x{max(len(d1),len(d2))-1:08X}',
                                 'span_length':abs(len(d2)-len(d1)),'changed_bytes_in_span':abs(len(d2)-len(d1))})

    manifest={'schema_version':1,'chunk_size':CHUNK,'rom_count':len(inv),'roms':inv,
              'notes':['No ROM bytes are stored in this package.','All generated datasets are deterministic from the listed input ROMs.']}
    (args.out/'rom_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    write_csv(args.out/'rom_inventory.csv', list(inv[0].keys()), inv)
    write_csv(args.out/'chunk_hashes_64k.csv', list(chunks[0].keys()), chunks)
    write_csv(args.out/'entropy_map_64k.csv', list(ents[0].keys()), ents)
    write_csv(args.out/'fill_runs.csv', list(fills[0].keys()) if fills else ['filename'], fills)
    write_csv(args.out/'pointer_bins_1mib.csv', list(ptrs[0].keys()) if ptrs else ['filename'], ptrs)
    write_csv(args.out/'byte_histogram.csv', list(hist[0].keys()), hist)
    write_csv(args.out/'pairwise_similarity.csv', list(pair[0].keys()) if pair else ['a'], pair)
    write_csv(args.out/'revision_diff_regions.csv', list(diffrows[0].keys()) if diffrows else ['game_code'], diffrows)
    print(json.dumps({'roms':len(inv),'chunks':len(chunks),'fill_runs':len(fills),'pointer_bins':len(ptrs),'pairs':len(pair),'diff_regions':len(diffrows)},indent=2))
if __name__=='__main__': main()
