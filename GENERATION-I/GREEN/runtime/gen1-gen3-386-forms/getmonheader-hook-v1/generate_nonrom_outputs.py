#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, struct, zlib
from pathlib import Path

RUNTIME_OFFSET=0x80000
MAP_OFFSET=0x85000
DESC_OFFSET=0x85200
MAP_HELPER_OFFSET=0x85300
MAP_HELPER=bytes.fromhex('fa92d04f060021005009092a4f7e47c9')
OVERLAY_HELPER=bytes.fromhex('78a7c079a7c8fe98d00d216f5d111e0079a72804193d20fc23231196d006042a12130520fa232323232aea9dd0232aea9ed0232323237eeaa8d0c9')
REVS={
 'rev0': dict(tail=0x2fa7,home=0x3606,back=0x3617,hdr=131,gchk=0xba8a,ips='d0c1ef38d6e974aeca337e3286eb488c05ef7aa6'),
 'reva': dict(tail=0x2f95,home=0x35f4,back=0x3605,hdr=130,gchk=0xd3b2,ips='435c7c956b8109b7b9ae5b96453031c8252a6e3a'),
}

def sha1(b): return hashlib.sha1(b).hexdigest()

def make_map(csv_path: Path):
    table=[0xffff]*256
    with csv_path.open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            c=r['canonical_species_id'].strip()
            if c: table[int(r['legacy_internal_id'])]=int(c)
    assert sorted(v for v in table if v!=0xffff)==list(range(1,152))
    return b''.join(struct.pack('<H',v) for v in table)

def hook_runtime(base: bytes):
    r=bytearray(base)
    assert len(r)==19403 and r[:8]==b'G386F3\0\0'
    r[0x08:0x0a]=struct.pack('<H',3)
    r[0x40:0x60]=b'GREEN 386 + GEN3 KANTO HOOK V3'.ljust(32,b'\0')
    r[0x80:0x80+len(OVERLAY_HELPER)]=OVERLAY_HELPER
    r[0x60:0x64]=b'\0'*4
    r[0x60:0x64]=struct.pack('<I',zlib.crc32(r)&0xffffffff)
    out=bytes(r)
    assert sha1(out)=='081e9919db0220c0a201ff210d2471ea2fd45ae3'
    return out

def descriptor(runtime,mapping):
    d=bytearray(0x100); d[:8]=b'G386MAP\0'
    struct.pack_into('<HH',d,0x08,2,0x100)
    struct.pack_into('<II',d,0x0c,RUNTIME_OFFSET,len(runtime))
    struct.pack_into('<II',d,0x14,MAP_OFFSET,len(mapping))
    struct.pack_into('<HHH',d,0x1c,386,419,151)
    d[0x22:0x25]=bytes([0x1b,0x05,0x03])
    d[0x28:0x3c]=hashlib.sha1(runtime).digest()
    d[0x3c:0x50]=hashlib.sha1(mapping).digest()
    struct.pack_into('<H',d,0x50,0x0008)
    d[0x52]=0x21; struct.pack_into('<H',d,0x53,0x5300)
    d[0x55]=0x20; struct.pack_into('<H',d,0x56,0x4080)
    d[0x58]=0x7f
    d[0x60:0x80]=b'GREEN GETMONHEADER HOOK V1'.ljust(32,b'\0')
    struct.pack_into('<I',d,0xfc,zlib.crc32(d[:0xfc])&0xffffffff)
    out=bytes(d); assert sha1(out)=='a9fff0c03e9806ab40ebfe106e0d42e87950b444'
    return out

def fixed_stub(home,back):
    b=bytearray([0xc5,0xd5,0xe5,0x3e,0x21])
    b+=bytes([0xcd,home&255,home>>8,0xcd,0,0x53,0xcd,back&255,back>>8])
    b+=bytes([0x3e,0x20,0xcd,home&255,home>>8,0xcd,0x80,0x40,0xcd,back&255,back>>8])
    b+=bytes([0xe1,0xd1,0xc1,0xc9]); assert len(b)==29
    return bytes(b)

def rec(off,data):
    out=bytearray()
    while data:
        c=data[:0xffff]; data=data[len(c):]
        out+=off.to_bytes(3,'big')+len(c).to_bytes(2,'big')+c; off+=len(c)
    return out

def rle(off,n,val):
    out=bytearray()
    while n:
        k=min(n,0xffff); out+=off.to_bytes(3,'big')+b'\0\0'+k.to_bytes(2,'big')+bytes([val]); off+=k; n-=k
    return out

def sparse_ips(runtime,mapping,desc,rev):
    m=REVS[rev]; out=bytearray(b'PATCH')
    s=fixed_stub(m['home'],m['back'])
    old=bytearray(29)
    for i in (0,8,16,24): old[i]=0xff
    i=0
    while i<29:
        if old[i]==s[i]: i+=1; continue
        st=i; buf=bytearray()
        while i<29 and old[i]!=s[i]: buf.append(s[i]); i+=1
        out+=rec(0x8+st,bytes(buf))
    out+=rec(0x147,bytes([0x1b,0x05]))
    out+=rec(0x14d,bytes([m['hdr'],m['gchk']>>8,m['gchk']&255]))
    out+=rec(m['tail'],bytes.fromhex('c3080000'))
    out+=rle(0x80000,0x80000,0xff)
    ext=bytearray([0xff])*0x80000
    ext[0:len(runtime)]=runtime
    ext[MAP_OFFSET-0x80000:MAP_OFFSET-0x80000+len(mapping)]=mapping
    ext[DESC_OFFSET-0x80000:DESC_OFFSET-0x80000+len(desc)]=desc
    ext[MAP_HELPER_OFFSET-0x80000:MAP_HELPER_OFFSET-0x80000+len(MAP_HELPER)]=MAP_HELPER
    i=0
    while i<len(ext):
        if ext[i]==0xff: i+=1; continue
        st=i; buf=bytearray()
        while i<len(ext) and ext[i]!=0xff and len(buf)<0xffff: buf.append(ext[i]); i+=1
        out+=rec(0x80000+st,bytes(buf))
    out+=b'EOF'+(0x100000).to_bytes(3,'big')
    p=bytes(out); assert sha1(p)==m['ips']; return p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-runtime',type=Path,required=True); ap.add_argument('--map-csv',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    mapping=make_map(a.map_csv); assert sha1(mapping)=='e87588031b826c707891061daa5cd38202a2d35c'
    runtime=hook_runtime(a.base_runtime.read_bytes()); desc=descriptor(runtime,mapping)
    outputs={
      'green_386_forms_runtime_parameter_block_v3_hooked.bin':runtime,
      'green_386_forms_getmonheader_hook_descriptor.bin':desc,
      'green_legacy8_to_canonical16_map.bin':mapping,
      'map_helper_bank21_5300.bin':MAP_HELPER,
      'overlay_helper_bank20_4080.bin':OVERLAY_HELPER,
      'green_386_forms_getmonheader_hook_rev0.ips':sparse_ips(runtime,mapping,desc,'rev0'),
      'green_386_forms_getmonheader_hook_reva.ips':sparse_ips(runtime,mapping,desc,'reva'),
    }
    for name,data in outputs.items(): (a.out/name).write_bytes(data); print(name,len(data),sha1(data))

if __name__=='__main__': main()
