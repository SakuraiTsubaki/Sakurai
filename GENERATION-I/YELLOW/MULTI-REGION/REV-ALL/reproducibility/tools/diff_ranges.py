#!/usr/bin/env python3
from pathlib import Path
import sys,csv,hashlib
def sha1(x):return hashlib.sha1(x).hexdigest()
def ranges(a,b):
    s=None
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y and s is None:s=i
        elif x==y and s is not None:yield s,i;s=None
    if s is not None:yield s,min(len(a),len(b))
if len(sys.argv)<3:raise SystemExit('usage: diff_ranges.py A B [OUT.csv]')
a=Path(sys.argv[1]).read_bytes();b=Path(sys.argv[2]).read_bytes();rows=[]
for n,(s,e) in enumerate(ranges(a,b)):rows.append([n,f'0x{s:06X}',f'0x{e:06X}',e-s,sha1(a[s:e]),sha1(b[s:e])])
out=sys.argv[3] if len(sys.argv)>3 else '-'
f=open(out,'w',newline='') if out!='-' else sys.stdout;w=csv.writer(f);w.writerow(['index','start','end_exclusive','length','a_slice_sha1','b_slice_sha1']);w.writerows(rows)
