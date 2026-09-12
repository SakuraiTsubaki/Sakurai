#!/usr/bin/env python3
"""Rebuild Pokémon Ruby ROM identity/header audit without committing ROM binaries."""
from pathlib import Path
import hashlib, binascii, csv, sys
FIELDS=["file","size_bytes","title","game_code","maker","header_version","header_complement","crc32","md5","sha1","sha256"]
def audit(p):
    b=p.read_bytes()
    return {"file":p.name,"size_bytes":len(b),"title":b[0xA0:0xAC].rstrip(b"\0").decode("ascii","replace"),"game_code":b[0xAC:0xB0].decode("ascii","replace"),"maker":b[0xB0:0xB2].decode("ascii","replace"),"header_version":b[0xBC],"header_complement":f"{b[0xBD]:02X}","crc32":f"{binascii.crc32(b)&0xffffffff:08x}","md5":hashlib.md5(b).hexdigest(),"sha1":hashlib.sha1(b).hexdigest(),"sha256":hashlib.sha256(b).hexdigest()}
def main():
    ps=[Path(x) for x in sys.argv[1:]]
    w=csv.DictWriter(sys.stdout,fieldnames=FIELDS); w.writeheader(); [w.writerow(audit(p)) for p in ps]
if __name__=="__main__": main()
