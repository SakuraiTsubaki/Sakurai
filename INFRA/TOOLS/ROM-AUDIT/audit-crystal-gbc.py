#!/usr/bin/env python3
"""Emit hashes/header/bank fingerprints for local Pokémon Crystal GBC images."""
import argparse,hashlib,json
from pathlib import Path
def audit(p):
 d=p.read_bytes(); hc=0
 for b in d[0x134:0x14D]: hc=(hc-b-1)&255
 sg=(d[0x14E]<<8)|d[0x14F]; cg=(sum(d)-d[0x14E]-d[0x14F])&65535
 return {"filename":p.name,"size_bytes":len(d),"banks_16k":len(d)//0x4000,"title":d[0x134:0x144].split(b"\0")[0].decode("ascii","replace"),"header_version":d[0x14C],"header_checksum_valid":hc==d[0x14D],"global_checksum_valid":cg==sg,"md5":hashlib.md5(d).hexdigest(),"sha1":hashlib.sha1(d).hexdigest(),"sha256":hashlib.sha256(d).hexdigest(),"bank_sha256":[hashlib.sha256(d[i:i+0x4000]).hexdigest() for i in range(0,len(d),0x4000)]}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("rom",nargs="+"); ap.add_argument("-o","--output"); ns=ap.parse_args(); text=json.dumps([audit(Path(x)) for x in ns.rom],indent=2,ensure_ascii=False)+"\n"; Path(ns.output).write_text(text) if ns.output else print(text,end="")
if __name__=="__main__": main()
