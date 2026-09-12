#!/usr/bin/env python3
"""GBA ROM census helper: identity, 64 KiB banks, and aligned BIOS-LZ77 candidates."""
import argparse,csv,hashlib,json,zlib
from pathlib import Path

def valid_lz(data,off):
    if off+4>len(data) or data[off]!=0x10: return None
    target=data[off+1]|(data[off+2]<<8)|(data[off+3]<<16)
    if target<4 or target>0x400000: return None
    p=off+4; out=0; literals=refs=0
    try:
        while out<target:
            flags=data[p]; p+=1
            for bit in range(7,-1,-1):
                if out>=target: break
                if flags&(1<<bit):
                    x,y=data[p],data[p+1]; p+=2
                    length=(x>>4)+3; disp=((x&15)<<8|y)+1
                    if disp>out: return None
                    out+=length; refs+=1
                else:
                    p+=1; out+=1; literals+=1
                if p>len(data): return None
        return {'decompressed_size':target,'compressed_span':p-off,'literals':literals,'backrefs':refs,'overshoot':out-target}
    except IndexError:
        return None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom'); ap.add_argument('--out',default='census-out'); a=ap.parse_args()
    data=Path(a.rom).read_bytes(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    header={'title':data[0xA0:0xAC].rstrip(b'\0').decode('ascii','replace'),'game_code':data[0xAC:0xB0].decode('ascii','replace'),'maker_code':data[0xB0:0xB2].decode('ascii','replace'),'software_version':data[0xBC],'header_checksum':data[0xBD],'size':len(data),'crc32':f'{zlib.crc32(data)&0xffffffff:08x}','md5':hashlib.md5(data).hexdigest(),'sha1':hashlib.sha1(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest()}
    (out/'identity.json').write_text(json.dumps(header,indent=2)+'\n')
    with (out/'banks-64k.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t'); w.writerow(['bank','rom_start','gba_start','size','crc32','sha1','sha256'])
        for i in range((len(data)+0xffff)//0x10000):
            c=data[i*0x10000:(i+1)*0x10000];w.writerow([i,f'0x{i*0x10000:08X}',f'0x{0x08000000+i*0x10000:08X}',len(c),f'{zlib.crc32(c)&0xffffffff:08x}',hashlib.sha1(c).hexdigest(),hashlib.sha256(c).hexdigest()])
    with (out/'lz77-candidates.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['rom_offset','gba_address','decompressed_size','compressed_span','literal_tokens','backref_tokens','overshoot'])
        for off in range(0,len(data)-4,4):
            if data[off]!=0x10: continue
            r=valid_lz(data,off)
            if r:w.writerow([f'0x{off:08X}',f'0x{0x08000000+off:08X}',r['decompressed_size'],r['compressed_span'],r['literals'],r['backrefs'],r['overshoot']])
if __name__=='__main__': main()
