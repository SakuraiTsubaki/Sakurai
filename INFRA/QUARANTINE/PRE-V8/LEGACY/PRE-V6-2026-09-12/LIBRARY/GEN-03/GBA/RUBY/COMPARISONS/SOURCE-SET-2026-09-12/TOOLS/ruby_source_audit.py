#!/usr/bin/env python3
"""Reproducible Pokémon Ruby ROM source-set audit.

This tool never modifies ROMs. It reads a local ROM directory plus Sakurai's
source-set registry, then emits research/production-routing evidence:
- full file hashes and GBA header identity
- coarse ROM layout measurements
- 64 KiB bank fingerprints and cross-release equivalence groups
- validated GBA LZ77 (type 0x10) blocks in the graphics payload
- decompressed-output equality summaries for production deduplication

Original ROM bytes are never written to the output directory.
"""
from __future__ import annotations
import argparse,csv,hashlib,zlib
from collections import Counter,defaultdict
from pathlib import Path

BANK=0x10000

def hashes(data:bytes):
    return (f"{zlib.crc32(data)&0xffffffff:08x}",hashlib.md5(data).hexdigest(),hashlib.sha1(data).hexdigest(),hashlib.sha256(data).hexdigest())

def load_registry(path:Path):
    with path.open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    return {r['source_filename']:r for r in rows}

def ff_layout(data:bytes):
    best=(0,0); i=0
    while i<len(data):
        if data[i]!=0xff: i+=1; continue
        j=i+1
        while j<len(data) and data[j]==0xff: j+=1
        if j-i>best[1]-best[0]: best=(i,j)
        i=j
    end=len(data)
    while end and data[end-1]==0xff: end-=1
    return best[0],best[1],end

def valid_lz10(data:bytes,off:int,max_out:int=2_000_000):
    if off+4>len(data) or data[off]!=0x10:return None
    n=data[off+1]|(data[off+2]<<8)|(data[off+3]<<16)
    if n<=0 or n>max_out:return None
    p=off+4; out=bytearray()
    try:
        while len(out)<n:
            flags=data[p];p+=1
            for bit in range(8):
                if len(out)>=n:break
                if flags&(0x80>>bit):
                    b1,b2=data[p],data[p+1];p+=2
                    ln=(b1>>4)+3;disp=((b1&15)<<8|b2)+1
                    if disp>len(out):return None
                    for _ in range(ln):
                        if len(out)>=n:break
                        out.append(out[-disp])
                else:
                    out.append(data[p]);p+=1
        return bytes(out),p-off
    except IndexError:
        return None

def write_csv(path:Path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(fields);w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom_dir',type=Path);ap.add_argument('registry',type=Path);ap.add_argument('out_dir',type=Path);a=ap.parse_args()
    reg=load_registry(a.registry);header=[];layout=[];banks=[];lz=[];outputs=defaultdict(lambda:{'occ':0,'rels':set()})
    for fn,r in reg.items():
        p=a.rom_dir/fn
        if not p.exists():continue
        data=p.read_bytes(); rid=r['release_id']
        crc,md5,sha1,sha256=hashes(data)
        title=data[0xa0:0xac].decode('ascii','replace').rstrip('\0 '); code=data[0xac:0xb0].decode('ascii','replace');maker=data[0xb0:0xb2].decode('ascii','replace');hv=data[0xbc]
        header.append([rid,fn,len(data),title,code,maker,hv,f"{data[0xbd]:02X}",crc,md5,sha1,sha256])
        ff0,ff1,last=ff_layout(data); graphics=ff1
        layout.append([rid,len(data),f"0x{ff0:08X}",f"0x{ff1:08X}",ff1-ff0,f"0x{graphics:08X}",f"0x{last:08X}"])
        for off in range(0,len(data),BANK):
            chunk=data[off:off+BANK];h=hashlib.sha1(chunk).hexdigest();banks.append([rid,f"{off//BANK:02X}",f"0x{off:08X}",len(chunk),h,round(chunk.count(0xff)/len(chunk),6),round(chunk.count(0)/len(chunk),6)])
        i=graphics
        while i+4<=last:
            if data[i]==0x10:
                v=valid_lz10(data,i)
                if v:
                    dec,clen=v; h=hashlib.sha1(dec).hexdigest();lz.append([rid,f"0x{i:08X}",f"0x{0x08000000+i:08X}",len(dec),clen,'yes' if i%4==0 else 'no',h]);outputs[(h,len(dec))]['occ']+=1;outputs[(h,len(dec))]['rels'].add(rid)
            i+=1
    write_csv(a.out_dir/'header-audit.csv',['release_id','filename','size_bytes','title','game_code','maker','header_version','header_complement','crc32','md5','sha1','sha256'],header)
    write_csv(a.out_dir/'layout-audit.csv',['release_id','size_bytes','largest_ff_start','largest_ff_end','largest_ff_bytes','graphics_payload_start','last_non_ff_plus_one'],layout)
    write_csv(a.out_dir/'bank-fingerprints.csv',['release_id','bank_hex','file_offset','size','sha1','ff_ratio','zero_ratio'],banks)
    bg=defaultdict(list)
    for r in banks:bg[r[4]].append(f"{r[0]}:{r[1]}@{r[2]}")
    eq=[]
    for h,m in bg.items():
        rels=sorted({x.split(':',1)[0] for x in m})
        if len(rels)>=2:eq.append([h,len(m),len(rels),';'.join(rels),';'.join(m)])
    eq.sort(key=lambda x:(-x[2],-x[1],x[0]));write_csv(a.out_dir/'bank-equivalence-groups.csv',['sha1','member_count','release_count','releases','members'],eq)
    write_csv(a.out_dir/'lz10-validated.csv',['release_id','offset','gba_address','declared_size','compressed_bytes','word_aligned','decompressed_sha1'],lz)
    counts=Counter(r[0] for r in lz); write_csv(a.out_dir/'lz10-validation-summary.csv',['release_id','validated_blocks'],sorted(counts.items()))
    relsets=defaultdict(set);coverage=Counter()
    for (h,n),g in outputs.items():
        if len(g['rels'])<2:continue
        coverage[len(g['rels'])]+=1
        for rid in g['rels']:relsets[rid].add(h)
    rids=sorted(relsets)
    write_csv(a.out_dir/'lz10-output-shared-matrix.csv',['release_id']+rids,[[x]+[len(relsets[x]&relsets[y]) for y in rids] for x in rids])
    write_csv(a.out_dir/'lz10-output-release-coverage.csv',['release_count','shared_decompressed_output_groups'],sorted(coverage.items()))
if __name__=='__main__':main()
