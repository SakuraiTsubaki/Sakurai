#!/usr/bin/env python3
from pathlib import Path
import urllib.request, hashlib, json, sys
root=Path(__file__).resolve().parents[1]
lock=json.load(open(root/'reference/pret_semantic_reference.lock.json',encoding='utf-8'))
out=Path(sys.argv[1]) if len(sys.argv)>1 else root/'reference'/'pret_cache'
out.mkdir(parents=True,exist_ok=True)
def git_blob_sha(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for group in ('semantic_files','symbol_branch_files'):
    for x in lock[group]:
        ref=x['ref']; path=x['path']; url=f'https://raw.githubusercontent.com/pret/pokeyellow/{ref}/{path}'
        data=urllib.request.urlopen(url,timeout=60).read()
        got=git_blob_sha(data)
        if got!=x['git_blob_sha1']: raise SystemExit(f'hash mismatch {path}: {got} != {x["git_blob_sha1"]}')
        dst=out/ref/path; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(data)
        print('OK',ref,path,got)
