#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,zlib
from pathlib import Path
def hc(d):
 x=0
 for v in d[0x134:0x14D]: x=(x-v-1)&255
 return x
def gc(d): return (sum(d[:0x14E])+sum(d[0x150:]))&65535
def inspect(p):
 d=p.read_bytes(); s=hashlib.sha256(d).hexdigest(); return {'filename':p.name,'size':len(d),'md5':hashlib.md5(d).hexdigest(),'sha1':hashlib.sha1(d).hexdigest(),'sha256':s,'crc32':f'{zlib.crc32(d)&0xffffffff:08x}','dump_id':f'DUMP-SHA256-{s[:16].upper()}','title':d[0x134:0x144].split(b'\0',1)[0].decode('ascii','replace').rstrip(),'header_version':d[0x14C],'header_checksum_valid':d[0x14D]==hc(d),'global_checksum_valid':int.from_bytes(d[0x14E:0x150],'big')==gc(d)}
def main():
 a=argparse.ArgumentParser();a.add_argument('rom',nargs='+',type=Path);x=a.parse_args();print(json.dumps([inspect(p) for p in x.rom],indent=2))
if __name__=='__main__':main()
