#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,pathlib,sys
BANK=0x4000;PAGE=0x100

def sha256(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    cat=json.loads(pathlib.Path(a.catalog).read_text());root=pathlib.Path(a.output);fail=[];ok=[]
    for item in cat['roms']:
        rom=pathlib.Path(item['path']); rom=rom if rom.is_absolute() else (pathlib.Path(a.catalog).resolve().parent/rom).resolve()
        data=rom.read_bytes(); od=root/item['output_subdir']
        ident=json.loads((od/'identity.json').read_text())
        if ident['sha256']!=sha256(data):fail.append(f"{item['label']}: identity SHA mismatch")
        banks=list(csv.DictReader((od/'bank_manifest.csv').open()))
        pages=list(csv.DictReader((od/'page_manifest.csv').open()))
        if sum(int(r['size']) for r in banks)!=len(data):fail.append(f"{item['label']}: bank coverage")
        if sum(int(r['size']) for r in pages)!=len(data):fail.append(f"{item['label']}: page coverage")
        if len(banks)!=(len(data)+BANK-1)//BANK:fail.append(f"{item['label']}: bank count")
        if len(pages)!=(len(data)+PAGE-1)//PAGE:fail.append(f"{item['label']}: page count")
        # Verify every listed bank/page digest deterministically; no sampling shortcuts.
        for r in banks:
            off=int(r['file_start_hex'],16); size=int(r['size'])
            if sha256(data[off:off+size])!=r['sha256']:fail.append(f"{item['label']}: bank {r['bank_hex']} hash")
        for r in pages:
            off=int(r['file_offset_hex'],16); size=int(r['size'])
            if sha256(data[off:off+size])!=r['sha256']:fail.append(f"{item['label']}: page {r['file_offset_hex']} hash")
        ok.append(item['label'])
    print(json.dumps({'verified_roms':ok,'failures':fail,'success':not fail},indent=2))
    sys.exit(1 if fail else 0)
if __name__=='__main__':main()
