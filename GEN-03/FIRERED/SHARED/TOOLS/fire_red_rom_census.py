#!/usr/bin/env python3
"""Generate deterministic, non-ROM FireRed research metadata from a local GBA image."""
from pathlib import Path
import argparse, hashlib, json, zlib

def lz10(data, off, max_out=0x40000):
    if off+4 > len(data) or data[off] != 0x10:
        return None
    size=data[off+1] | data[off+2]<<8 | data[off+3]<<16
    if size < 16 or size > max_out:
        return None
    ip=off+4; out=bytearray()
    while len(out) < size:
        if ip >= len(data): return None
        flags=data[ip]; ip += 1
        for bit in range(7,-1,-1):
            if len(out) >= size: break
            if flags & (1<<bit):
                if ip+2 > len(data): return None
                a,c=data[ip],data[ip+1]; ip += 2
                ln=(a>>4)+3; disp=((a&0xF)<<8)|c; src=len(out)-disp-1
                if src < 0: return None
                for _ in range(ln):
                    if len(out) >= size: break
                    out.append(out[src]); src += 1
            else:
                if ip >= len(data): return None
                out.append(data[ip]); ip += 1
    return size, ip-off

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom'); ap.add_argument('--out')
    a=ap.parse_args(); p=Path(a.rom); b=p.read_bytes()
    meta={'filename':p.name,'size':len(b),'sha1':hashlib.sha1(b).hexdigest(),'md5':hashlib.md5(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','header_title':b[0xA0:0xAC].rstrip(b'\0').decode('ascii','replace'),'game_code':b[0xAC:0xB0].decode('ascii','replace'),'maker_code':b[0xB0:0xB2].decode('ascii','replace'),'header_version':b[0xBC],'complement_check':b[0xBD]}
    chunks=[]
    for i,off in enumerate(range(0,len(b),0x10000)):
        c=b[off:off+0x10000]
        chunks.append({'index':i,'start':f'0x{off:08X}','sha1':hashlib.sha1(c).hexdigest(),'crc32':f'{zlib.crc32(c)&0xffffffff:08x}'})
    pointers=[]
    for off in range(0,len(b),0x100000):
        c=b[off:off+0x100000]
        n=sum(0x08000000 <= int.from_bytes(c[j:j+4],'little') < 0x09000000 for j in range(0,len(c)-3,4))
        pointers.append({'start':f'0x{off:08X}','aligned_rom_pointer_words':n})
    filler=[]; i=0
    while i<len(b):
        if b[i] not in (0,255): i+=1; continue
        v=b[i]; j=i+1
        while j<len(b) and b[j]==v: j+=1
        if j-i >= 0x1000:
            filler.append({'start':f'0x{i:08X}','end_exclusive':f'0x{j:08X}','length':j-i,'byte':f'0x{v:02X}','status':'candidate-not-verified-free'})
        i=j
    lz_by={}
    for off,x in enumerate(b):
        if x != 0x10: continue
        q=lz10(b,off)
        if not q: continue
        size,span=q; k=off//0x10000
        d=lz_by.setdefault(k,{'block_index':k,'start':f'0x{k*0x10000:08X}','candidate_count':0,'compressed_bytes_total':0,'decompressed_bytes_total':0})
        d['candidate_count']+=1; d['compressed_bytes_total']+=span; d['decompressed_bytes_total']+=size
    result={'dump':meta,'chunk_map_64k':chunks,'pointer_density_1m':pointers,'filler_candidates':filler,'lz77_summary_64k':[lz_by[k] for k in sorted(lz_by)]}
    text=json.dumps(result,indent=2)+'\n'
    if a.out: Path(a.out).write_text(text,encoding='utf-8')
    else: print(text,end='')
if __name__=='__main__': main()
