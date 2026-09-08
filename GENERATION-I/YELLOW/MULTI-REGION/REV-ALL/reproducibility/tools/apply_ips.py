#!/usr/bin/env python3
from pathlib import Path
import sys,hashlib
def apply(base,p):
    if not p.startswith(b'PATCH'):raise ValueError('bad IPS')
    o=bytearray(base); i=5
    while p[i:i+3]!=b'EOF':
        off=int.from_bytes(p[i:i+3],'big');i+=3; n=int.from_bytes(p[i:i+2],'big');i+=2
        if n==0:
            r=int.from_bytes(p[i:i+2],'big');i+=2; data=bytes([p[i]])*r;i+=1
        else:data=p[i:i+n];i+=n
        if off+len(data)>len(o):o.extend(b'\0'*(off+len(data)-len(o)))
        o[off:off+len(data)]=data
    return bytes(o)
if len(sys.argv)!=4:raise SystemExit('usage: apply_ips.py BASE PATCH OUT')
b=apply(Path(sys.argv[1]).read_bytes(),Path(sys.argv[2]).read_bytes());Path(sys.argv[3]).write_bytes(b);print(hashlib.sha1(b).hexdigest())
