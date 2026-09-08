#!/usr/bin/env python3
from pathlib import Path
import sys
def ranges(a,b):
    s=None
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y and s is None:s=i
        elif x==y and s is not None: yield s,i; s=None
    if s is not None: yield s,min(len(a),len(b))
def make(a,b):
    o=bytearray(b'PATCH')
    for s,e in ranges(a,b):
        i=s
        while i<e:
            n=min(65535,e-i); o+=i.to_bytes(3,'big')+n.to_bytes(2,'big')+b[i:i+n]; i+=n
    o+=b'EOF'; return bytes(o)
if len(sys.argv)!=4:raise SystemExit('usage: make_ips.py BASE TARGET PATCH')
a=Path(sys.argv[1]).read_bytes(); b=Path(sys.argv[2]).read_bytes(); Path(sys.argv[3]).write_bytes(make(a,b))
