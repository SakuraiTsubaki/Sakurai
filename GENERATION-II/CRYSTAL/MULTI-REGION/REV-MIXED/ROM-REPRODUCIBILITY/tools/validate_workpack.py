#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, pathlib, py_compile, sys

BANNED_SUFFIXES={'.gb','.gbc','.gba','.nds','.3ds','.bin'}

def sha1(path):
    h=hashlib.sha1()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--catalog',required=True);ap.add_argument('--output',required=True);ap.add_argument('--report',required=True);a=ap.parse_args()
    root=pathlib.Path(a.root);out=pathlib.Path(a.output);cp=pathlib.Path(a.catalog);cat=json.loads(cp.read_text());fail=[];checks=[]
    banned=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.suffix.lower() in BANNED_SUFFIXES]
    checks.append({'check':'no ROM/binary redistributables in workpack','pass':not banned,'detail':banned})
    if banned: fail.append('banned binary files present')
    pyfiles=list((root/'tools').glob('*.py'));bad=[]
    for p in pyfiles:
        try: py_compile.compile(str(p),doraise=True)
        except Exception as e: bad.append(f'{p.name}: {e}')
    checks.append({'check':'all Python tools compile','pass':not bad,'detail':bad or f'{len(pyfiles)} scripts'})
    if bad: fail.append('python compile failure')
    rr=out/'MULTI-REGION'/'REV-MIXED'/'ROM-REPRODUCIBILITY'/'lossless_roundtrip_report.json'
    rj=json.loads(rr.read_text()) if rr.exists() else {'success':False}
    checks.append({'check':'lossless roundtrip all targets','pass':bool(rj.get('success')),'detail':f"{len(rj.get('roms',[]))} ROMs"})
    if not rj.get('success'): fail.append('roundtrip failed')
    for item in cat['roms']:
        od=out/item['output_subdir']
        for name,count in [('bank_manifest.csv',128),('page_manifest.csv',8192),('address_map_banks.csv',128),('address_map_pages.csv',8192),('bank_ownership_seed.csv',128),('page_ownership_seed.csv',8192)]:
            p=od/name
            if not p.exists(): fail.append(f"{item['label']}: missing {name}"); continue
            with p.open(encoding='utf-8',newline='') as f: n=sum(1 for _ in csv.DictReader(f))
            if n!=count: fail.append(f"{item['label']}: {name} rows {n} != {count}")
    checks.append({'check':'required per-ROM ledgers have exact row counts','pass':not any('rows ' in x or 'missing ' in x for x in fail),'detail':'128 bank rows and 8192 page rows per target'})
    bridge=json.loads((root/'source_bridge.json').read_text())
    by={i['label']:i for i in cat['roms']};bm=[]
    for t in bridge['exact_source_build_targets']:
        item=by[t['workpack_label']];p=pathlib.Path(item['path']);p=p if p.is_absolute() else (cp.resolve().parent/p).resolve();actual=sha1(p);bm.append({'label':t['workpack_label'],'expected':t['expected_sha1'],'actual':actual,'match':actual==t['expected_sha1']})
    checks.append({'check':'English local ROM identities match pinned source-build SHA-1s','pass':all(x['match'] for x in bm),'detail':bm})
    if not all(x['match'] for x in bm):fail.append('source bridge hash mismatch')
    report={'schema_version':1,'success':not fail,'failures':fail,'checks':checks}
    pathlib.Path(a.report).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));sys.exit(0 if not fail else 1)
if __name__=='__main__':main()
