#!/usr/bin/env python3
from pathlib import Path
import hashlib, subprocess, tempfile, sys
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/'tools/green_romlab.py'
REV0=Path(sys.argv[1]); REVA=Path(sys.argv[2])
def sha(p):return hashlib.sha1(Path(p).read_bytes()).hexdigest()
assert sha(REV0)=='82c0eef40a5e2423699d9fd8ba15dfaa8b51d196'
assert sha(REVA)=='4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b'
with tempfile.TemporaryDirectory() as td:
 td=Path(td); split=td/'banks'; rebuilt=td/'rebuilt.gb'; patched=td/'patched.gb'; reverse=td/'reverse.gb'
 subprocess.run([sys.executable,str(TOOL),'split',str(REV0),str(split)],check=True)
 subprocess.run([sys.executable,str(TOOL),'join',str(split),str(rebuilt)],check=True,stdout=subprocess.DEVNULL)
 assert sha(rebuilt)==sha(REV0)
 subprocess.run([sys.executable,str(TOOL),'apply',str(REV0),str(ROOT/'generated/rev0_to_reva.delta.jsonl'),str(patched)],check=True,stdout=subprocess.DEVNULL)
 assert sha(patched)==sha(REVA)
 subprocess.run([sys.executable,str(TOOL),'apply',str(REVA),str(ROOT/'generated/reva_to_rev0.delta.jsonl'),str(reverse)],check=True,stdout=subprocess.DEVNULL)
 assert sha(reverse)==sha(REV0)
print('8/8 core assertions passed: hashes, split/join, forward delta, reverse delta')
