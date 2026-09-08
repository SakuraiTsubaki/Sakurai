#!/usr/bin/env python3
"""Compute Git's SHA-1 object id for blob files."""
from pathlib import Path
import argparse,hashlib,sys
def blob_sha(p):
 d=Path(p).read_bytes();return hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('files',nargs='+');ap.add_argument('--expect',action='append',default=[]);a=ap.parse_args();exp=dict(x.split('=',1) for x in a.expect);ok=True
 for raw in a.files:
  p=Path(raw);got=blob_sha(p);print(got,p);want=exp.get(p.name) or exp.get(str(p))
  if want and got.lower()!=want.lower():print(f'ERROR: {p}: expected {want}, got {got}',file=sys.stderr);ok=False
 return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
