#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, struct, zlib
from pathlib import Path

RUNTIME_OFFSET=0x80000
RUNTIME_SIZE=19403
MAP_OFFSET=0x85000
DESC_OFFSET=0x85200
MAP_HELPER_OFFSET=0x85300
FIXED_STUB_OFFSET=0x0008

REV={
 "rev0":{"tail":0x2FA7,"home":0x3606,"back":0x3617,
         "sha1":"82c0eef40a5e2423699d9fd8ba15dfaa8b51d196"},
 "reva":{"tail":0x2F95,"home":0x35F4,"back":0x3605,
         "sha1":"4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b"},
}

MAP_HELPER=bytes.fromhex("fa92d04f060021005009092a4f7e47c9")
OVERLAY_HELPER=bytes.fromhex(
 "78a7c079a7c8fe98d00d216f5d111e0079a72804193d20fc23231196d00604"
 "2a12130520fa232323232aea9dd0232aea9ed0232323237eeaa8d0c9"
)

def h(b): return hashlib.sha1(b).hexdigest()

def fixed_stub(home,back):
    b=bytearray([0xC5,0xD5,0xE5,0x3E,0x21])
    b += bytes([0xCD,home&255,home>>8, 0xCD,0x00,0x53, 0xCD,back&255,back>>8])
    b += bytes([0x3E,0x20, 0xCD,home&255,home>>8, 0xCD,0x80,0x40, 0xCD,back&255,back>>8])
    b += bytes([0xE1,0xD1,0xC1,0xC9])
    assert len(b)==29
    return bytes(b)

def header_checksum(rom):
    x=0
    for b in rom[0x134:0x14D]: x=(x-b-1)&255
    return x

def global_checksum(rom):
    return (sum(rom[:0x14E])+sum(rom[0x150:]))&0xffff

def checksums(rom):
    rom[0x14D]=header_checksum(rom); rom[0x14E]=rom[0x14F]=0
    g=global_checksum(rom); rom[0x14E]=g>>8; rom[0x14F]=g&255

def make_ips(original,target):
    def rec(off,data):
        out=bytearray()
        while data:
            c=data[:0xffff]; data=data[len(c):]
            out += off.to_bytes(3,"big")+len(c).to_bytes(2,"big")+c; off+=len(c)
        return out
    def rle(off,n,val):
        out=bytearray()
        while n:
            k=min(n,0xffff)
            out += off.to_bytes(3,"big")+b"\0\0"+k.to_bytes(2,"big")+bytes([val]); off+=k; n-=k
        return out
    out=bytearray(b"PATCH"); i=0
    while i<len(original):
        if original[i]==target[i]: i+=1; continue
        s=i; buf=bytearray()
        while i<len(original) and original[i]!=target[i] and len(buf)<0xffff:
            buf.append(target[i]); i+=1
        out+=rec(s,bytes(buf))
    out+=rle(len(original),len(target)-len(original),0xff)
    i=len(original)
    while i<len(target):
        if target[i]==0xff: i+=1; continue
        s=i; buf=bytearray()
        while i<len(target) and target[i]!=0xff and len(buf)<0xffff:
            buf.append(target[i]); i+=1
        out+=rec(s,bytes(buf))
    out+=b"EOF"+len(target).to_bytes(3,"big")
    return bytes(out)

def make_hooked_runtime(runtime):
    r=bytearray(runtime)
    assert len(r)==RUNTIME_SIZE and r[:8]==b"G386F3\0\0"
    r[0x08:0x0A]=struct.pack("<H",3)
    r[0x40:0x60]=b"GREEN 386 + GEN3 KANTO HOOK V3".ljust(32,b"\0")
    r[0x80:0x80+len(OVERLAY_HELPER)]=OVERLAY_HELPER
    r[0x60:0x64]=b"\0"*4
    crc=zlib.crc32(r)&0xffffffff
    r[0x60:0x64]=struct.pack("<I",crc)
    return bytes(r)

def descriptor(runtime,mapping):
    d=bytearray(0x100); d[:8]=b"G386MAP\0"
    struct.pack_into("<HH",d,0x08,2,0x100)
    struct.pack_into("<II",d,0x0C,RUNTIME_OFFSET,len(runtime))
    struct.pack_into("<II",d,0x14,MAP_OFFSET,len(mapping))
    struct.pack_into("<HHH",d,0x1C,386,419,151)
    d[0x22:0x25]=bytes([0x1B,0x05,0x03])
    d[0x28:0x3C]=hashlib.sha1(runtime).digest()
    d[0x3C:0x50]=hashlib.sha1(mapping).digest()
    struct.pack_into("<H",d,0x50,FIXED_STUB_OFFSET)
    d[0x52]=0x21; struct.pack_into("<H",d,0x53,0x5300)
    d[0x55]=0x20; struct.pack_into("<H",d,0x56,0x4080)
    d[0x58]=0x7F
    d[0x60:0x80]=b"GREEN GETMONHEADER HOOK V1".ljust(32,b"\0")
    struct.pack_into("<I",d,0xFC,zlib.crc32(d[:0xFC])&0xffffffff)
    return bytes(d)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original",type=Path,required=True)
    ap.add_argument("--scaffold",type=Path,required=True)
    ap.add_argument("--revision",choices=REV,required=True)
    ap.add_argument("--out-rom",type=Path,required=True)
    ap.add_argument("--out-ips",type=Path,required=True)
    a=ap.parse_args(); meta=REV[a.revision]
    original=a.original.read_bytes(); scaffold=bytearray(a.scaffold.read_bytes())
    assert h(original)==meta["sha1"]; assert len(original)==0x80000 and len(scaffold)==0x100000
    assert scaffold[meta["tail"]:meta["tail"]+4]==bytes.fromhex("ea0020c9")
    runtime=make_hooked_runtime(scaffold[RUNTIME_OFFSET:RUNTIME_OFFSET+RUNTIME_SIZE])
    mapping=bytes(scaffold[MAP_OFFSET:MAP_OFFSET+0x200])
    scaffold[RUNTIME_OFFSET:RUNTIME_OFFSET+RUNTIME_SIZE]=runtime
    scaffold[DESC_OFFSET:DESC_OFFSET+0x100]=descriptor(runtime,mapping)
    scaffold[MAP_HELPER_OFFSET:MAP_HELPER_OFFSET+len(MAP_HELPER)]=MAP_HELPER
    scaffold[FIXED_STUB_OFFSET:FIXED_STUB_OFFSET+29]=fixed_stub(meta["home"],meta["back"])
    scaffold[meta["tail"]:meta["tail"]+4]=bytes.fromhex("c3080000")
    checksums(scaffold)
    target=bytes(scaffold)
    assert target[RUNTIME_OFFSET+0x80:RUNTIME_OFFSET+0x80+len(OVERLAY_HELPER)]==OVERLAY_HELPER
    assert target[MAP_HELPER_OFFSET:MAP_HELPER_OFFSET+len(MAP_HELPER)]==MAP_HELPER
    assert target[0x14D]==header_checksum(target)
    assert ((target[0x14E]<<8)|target[0x14F])==global_checksum(target)
    a.out_rom.write_bytes(target)
    a.out_ips.write_bytes(make_ips(original,target))
    print(a.revision,h(target),h(a.out_ips.read_bytes()))

if __name__=="__main__": main()
