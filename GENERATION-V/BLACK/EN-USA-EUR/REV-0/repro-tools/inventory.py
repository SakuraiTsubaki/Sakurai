#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,json,zlib
from collections import Counter,defaultdict

def detect(b):
    t={b'NARC':'NARC',b'RGCN':'NCGR',b'RLCN':'NCLR',b'RCSN':'NSCR',b'RECN':'NCER',b'RNAN':'NANR',b'SDAT':'SDAT',b'SSEQ':'SSEQ',b'SBNK':'SBNK',b'SWAR':'SWAR',b'BTX0':'BTX0',b'BMD0':'BMD0',b'BCA0':'BCA0',b'BTA0':'BTA0',b'BTP0':'BTP0',b'BMA0':'BMA0',b'BVA0':'BVA0'}
    if b[:4] in t:return t[b[:4]]
    if b[:1]==b'\x10':return 'LZ10-candidate'
    if b[:1]==b'\x11':return 'LZ11-candidate'
    if not b:return 'empty'
    return 'unknown'

def one(p):
    b=p.read_bytes();return len(b),f'{zlib.crc32(b)&0xffffffff:08X}',hashlib.sha1(b).hexdigest().upper(),hashlib.sha256(b).hexdigest().upper(),detect(b)

def build(root):
    root=Path(root);rows=[]
    for scope,base in [('nitrofs',root/'nitrofs'),('narc_member',root/'narc')]:
        if not base.exists():continue
        for p in sorted(base.rglob('*.bin')):
            size,crc,sha1,sha256,typ=one(p);rows.append({'scope':scope,'path':p.relative_to(base).as_posix(),'size':size,'crc32':crc,'sha1':sha1,'sha256':sha256,'type':typ})
    a=root/'analysis';a.mkdir(exist_ok=True)
    with (a/'payload_inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['scope','path','size','crc32','sha1','sha256','type']);w.writeheader();w.writerows(rows)
    groups=defaultdict(int)
    for r in rows:groups[r['sha256']]+=1
    s={'rows':len(rows),'types':dict(Counter(r['type'] for r in rows)),'unique_sha256':len(groups),'duplicate_hash_groups':sum(1 for n in groups.values() if n>1)}
    (a/'payload_inventory_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))

def compare(a,b,out):
    def load(root):
        with (Path(root)/'analysis/payload_inventory.csv').open(encoding='utf-8',newline='') as f:return {(r['scope'],r['path']):r for r in csv.DictReader(f)}
    A=load(a);B=load(b);keys=sorted(set(A)|set(B));rows=[]
    for k in keys:
        x=A.get(k);y=B.get(k);rows.append({'scope':k[0],'path':k[1],'present_black':bool(x),'present_white':bool(y),'identical':bool(x and y and x['sha256']==y['sha256']),'size_black':x['size'] if x else '','size_white':y['size'] if y else '','sha256_black':x['sha256'] if x else '','sha256_white':y['sha256'] if y else ''})
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    with (out/'black_white_payload_compare.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    s={'keys_total':len(rows),'present_both':sum(r['present_black'] and r['present_white'] for r in rows),'identical':sum(r['identical'] for r in rows),'different_or_missing':sum(not r['identical'] for r in rows)}
    (out/'black_white_payload_compare_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('build');p.add_argument('workspace')
    p=sp.add_parser('compare');p.add_argument('black');p.add_argument('white');p.add_argument('out')
    a=ap.parse_args();build(a.workspace) if a.cmd=='build' else compare(a.black,a.white,a.out)
