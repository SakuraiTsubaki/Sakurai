#!/usr/bin/env python3
"""Stdlib-only NDS extraction/rebuild tool used for the Gen V reproducibility baseline."""
import argparse,csv,hashlib,json,shutil,struct,sys,zlib
from pathlib import Path,PurePosixPath

def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def p32(v): return struct.pack('<I',v)

def hashfile(p):
    md5=hashlib.md5(); sha1=hashlib.sha1(); sha256=hashlib.sha256(); crc=0; size=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):
            size+=len(b); crc=zlib.crc32(b,crc); md5.update(b); sha1.update(b); sha256.update(b)
    return {'size':size,'crc32':f'{crc&0xffffffff:08X}','md5':md5.hexdigest().upper(),'sha1':sha1.hexdigest().upper(),'sha256':sha256.hexdigest().upper()}

class NDS:
    def __init__(self,p):
        self.path=Path(p); self.data=self.path.read_bytes(); self.h=self.data[:0x4000]
        h=self.h
        self.m={'title':h[:12].rstrip(b'\0').decode('ascii','replace'),'game_code':h[12:16].decode('ascii','replace'),'rom_version':h[0x1e],
        'arm9_offset':u32(h,0x20),'arm9_size':u32(h,0x2c),'arm7_offset':u32(h,0x30),'arm7_size':u32(h,0x3c),
        'fnt_offset':u32(h,0x40),'fnt_size':u32(h,0x44),'fat_offset':u32(h,0x48),'fat_size':u32(h,0x4c),
        'ov9_offset':u32(h,0x50),'ov9_size':u32(h,0x54),'ov7_offset':u32(h,0x58),'ov7_size':u32(h,0x5c),
        'banner_offset':u32(h,0x68),'declared_rom_size':u32(h,0x80),'header_size':u32(h,0x84),'actual_size':len(self.data),
        'arm9i_offset':u32(h,0x1c0),'arm9i_size':u32(h,0x1cc),'arm7i_offset':u32(h,0x1d0),'arm7i_size':u32(h,0x1dc)}
        self.fat=[]; o=self.m['fat_offset']
        for i in range(self.m['fat_size']//8):
            s=u32(self.data,o+i*8); e=u32(self.data,o+i*8+4); self.fat.append((s,e))
        self.paths=self._fnt()
    def _fnt(self):
        f=self.data[self.m['fnt_offset']:self.m['fnt_offset']+self.m['fnt_size']]
        if len(f)<8:return {}
        count=u16(f,6) or 1; dirs={0xF000+i:(u32(f,i*8),u16(f,i*8+4)) for i in range(count) if i*8+8<=len(f)}; out={}; seen=set()
        def walk(d,base):
            if d in seen or d not in dirs:return
            seen.add(d); pos,fid=dirs[d]
            while pos<len(f):
                L=f[pos];pos+=1
                if not L:break
                isdir=L&0x80; n=L&0x7f; name=f[pos:pos+n].decode('ascii','replace');pos+=n
                if isdir:
                    child=u16(f,pos);pos+=2;walk(child,base/name)
                else: out[fid]=str(base/name);fid+=1
        walk(0xF000,PurePosixPath('')); return out
    def capacity(self,i):
        s,e=self.fat[i]; nxt=min((a for a,b in self.fat if a>s),default=self.m['declared_rom_size'] or len(self.data)); return max(e-s,nxt-s)

def narc_members(b):
    if len(b)<16 or b[:4]!=b'NARC':return None
    total=u32(b,8); pos=u16(b,12); blocks=u16(b,14); entries=[]; data0=None; datasz=0
    if total>len(b):return None
    for _ in range(blocks):
        if pos+8>len(b):return None
        magic=b[pos:pos+4]; size=u32(b,pos+4)
        if size<8 or pos+size>len(b):return None
        if magic in (b'BTAF',b'FATB'):
            n=u16(b,pos+8); q=pos+12; entries=[(u32(b,q+i*8),u32(b,q+i*8+4)) for i in range(n) if q+i*8+8<=pos+size]
        if magic in (b'GMIF',b'FIMG'): data0=pos+8; datasz=size-8
        pos+=size
    if data0 is None:return None
    out=[]
    for s,e in entries:
        if s<=e<=datasz:out.append(b[data0+s:data0+e])
    return out

def extract(rom,out):
    n=NDS(rom); out=Path(out); (out/'analysis').mkdir(parents=True,exist_ok=True); (out/'segments').mkdir(exist_ok=True); (out/'nitrofs').mkdir(exist_ok=True)
    (out/'analysis/rom_hashes.json').write_text(json.dumps(hashfile(Path(rom)),indent=2)+'\n'); (out/'analysis/nds_header.json').write_text(json.dumps(n.m,indent=2)+'\n')
    (out/'segments/header_0x4000.bin').write_bytes(n.data[:0x4000])
    for k,name in [('arm9','arm9.bin'),('arm7','arm7.bin'),('arm9i','arm9i.bin'),('arm7i','arm7i.bin')]:
        o=n.m[k+'_offset']; z=n.m[k+'_size']
        if o and z and o<len(n.data):(out/'segments'/name).write_bytes(n.data[o:min(len(n.data),o+z)])
    rows=[]; narcs=0
    for i,(s,e) in enumerate(n.fat):
        rel=n.paths.get(i,f'__unnamed__/file_{i:04d}.bin'); p=out/'nitrofs'/rel; p.parent.mkdir(parents=True,exist_ok=True); b=n.data[s:e]; p.write_bytes(b)
        rows.append({'file_id':i,'start':s,'end':e,'size':e-s,'capacity':n.capacity(i),'path':rel,'sha256':hashlib.sha256(b).hexdigest().upper()})
        mem=narc_members(b)
        if mem is not None:
            narcs+=1; d=out/'narc'/rel; d.mkdir(parents=True,exist_ok=True)
            for j,x in enumerate(mem):(d/f'{j:04d}.bin').write_bytes(x)
    with (out/'analysis/nitrofs_files.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    (out/'analysis/summary.json').write_text(json.dumps({'fat_entries':len(n.fat),'named_files':len(n.paths),'narc_containers':narcs},indent=2)+'\n')

def chunkify(rom,out,size=1048576):
    out=Path(out); d=out/'base_chunks';d.mkdir(parents=True,exist_ok=True); rows=[]
    with Path(rom).open('rb') as f:
        i=0;off=0
        while True:
            b=f.read(size)
            if not b:break
            name=f'{i:04d}.bin';(d/name).write_bytes(b);rows.append({'index':i,'offset':off,'size':len(b),'sha256':hashlib.sha256(b).hexdigest().upper()});i+=1;off+=len(b)
    (out/'base_chunks_manifest.json').write_text(json.dumps({'chunk_size':size,'source_hashes':hashfile(Path(rom)),'chunks':rows},indent=2)+'\n')

def rebuild(source,work,out):
    n=NDS(source); buf=bytearray(n.data); work=Path(work)
    for k,name in [('arm9','arm9.bin'),('arm7','arm7.bin')]:
        p=work/'segments'/name
        if p.exists():
            b=p.read_bytes(); z=n.m[k+'_size']; o=n.m[k+'_offset']
            if len(b)!=z:raise SystemExit(f'{name}: fixed size must remain {z}')
            buf[o:o+z]=b
    fato=n.m['fat_offset']
    for i,(s,e) in enumerate(n.fat):
        rel=n.paths.get(i,f'__unnamed__/file_{i:04d}.bin'); p=work/'nitrofs'/rel
        if not p.exists():raise SystemExit(f'missing {p}')
        b=p.read_bytes(); cap=n.capacity(i)
        if len(b)>cap:raise SystemExit(f'{rel}: {len(b)} > layout capacity {cap}')
        buf[s:s+len(b)]=b;buf[fato+i*8+4:fato+i*8+8]=p32(s+len(b))
    Path(out).write_bytes(buf);return hashfile(Path(out))

def from_chunks(work,out):
    work=Path(work); tmp=Path(out).with_suffix('.base.tmp.nds')
    with tmp.open('wb') as w:
        for p in sorted((work/'base_chunks').glob('*.bin')):shutil.copyfileobj(p.open('rb'),w)
    try:return rebuild(tmp,work,out)
    finally:tmp.unlink(missing_ok=True)

def main():
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('extract');p.add_argument('rom');p.add_argument('out')
    p=sp.add_parser('chunkify');p.add_argument('rom');p.add_argument('out')
    p=sp.add_parser('rebuild');p.add_argument('source');p.add_argument('work');p.add_argument('out')
    p=sp.add_parser('rebuild-from-chunks');p.add_argument('work');p.add_argument('out')
    p=sp.add_parser('verify');p.add_argument('a');p.add_argument('b')
    a=ap.parse_args()
    if a.cmd=='extract':extract(a.rom,a.out)
    elif a.cmd=='chunkify':chunkify(a.rom,a.out)
    elif a.cmd=='rebuild':print(json.dumps(rebuild(a.source,a.work,a.out),indent=2))
    elif a.cmd=='rebuild-from-chunks':print(json.dumps(from_chunks(a.work,a.out),indent=2))
    else:
        x=hashfile(Path(a.a));y=hashfile(Path(a.b));print(json.dumps({'a':x,'b':y,'identical':x['sha256']==y['sha256']},indent=2));sys.exit(0 if x['sha256']==y['sha256'] else 1)
if __name__=='__main__':main()
