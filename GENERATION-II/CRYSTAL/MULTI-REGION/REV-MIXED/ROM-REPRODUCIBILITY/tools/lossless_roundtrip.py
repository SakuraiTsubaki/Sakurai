#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib, shutil, tempfile
BANK_SIZE = 0x4000

def h(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def resolve_rom(catalog_path: pathlib.Path, item: dict) -> pathlib.Path:
    p = pathlib.Path(item['path']); return p if p.is_absolute() else (catalog_path.resolve().parent / p).resolve()

def roundtrip_one(label: str, rom: pathlib.Path, scratch_root: pathlib.Path, keep: bool) -> dict:
    original = rom.read_bytes(); work = scratch_root / label
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True); banks_dir = work / 'banks'; banks_dir.mkdir()
    bank_rows=[]; bank_paths=[]
    for bank,start in enumerate(range(0,len(original),BANK_SIZE)):
        chunk=original[start:start+BANK_SIZE]; bp=banks_dir/f'bank_{bank:02X}.bin'; bp.write_bytes(chunk); bank_paths.append(bp)
        bank_rows.append({'bank':bank,'bank_hex':f'{bank:02X}','size':len(chunk),'sha256':h(chunk)})
    rebuilt=b''.join(p.read_bytes() for p in bank_paths); (work/'rebuilt.gbc').write_bytes(rebuilt)
    result={'label':label,'source_filename':rom.name,'source_size':len(original),'bank_size':BANK_SIZE,'bank_count':len(bank_rows),'source_sha256':h(original),'rebuilt_sha256':h(rebuilt),'byte_identical':rebuilt==original,'size_identical':len(rebuilt)==len(original),'banks':bank_rows,'scratch_preserved':keep}
    (work/'roundtrip_report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    if not keep: shutil.rmtree(work)
    return result

def main():
    ap=argparse.ArgumentParser(description='Losslessly split ROMs into 16 KiB banks, reassemble, and verify exact identity.')
    ap.add_argument('--catalog',required=True); ap.add_argument('--scratch',default=None); ap.add_argument('--report',required=True); ap.add_argument('--keep',action='store_true'); a=ap.parse_args()
    cp=pathlib.Path(a.catalog); cat=json.loads(cp.read_text(encoding='utf-8')); rp=pathlib.Path(a.report); rp.parent.mkdir(parents=True,exist_ok=True)
    if a.scratch:
        sr=pathlib.Path(a.scratch); sr.mkdir(parents=True,exist_ok=True); results=[roundtrip_one(i['label'],resolve_rom(cp,i),sr,a.keep) for i in cat['roms']]
    else:
        with tempfile.TemporaryDirectory(prefix='crystal-roundtrip-') as td: results=[roundtrip_one(i['label'],resolve_rom(cp,i),pathlib.Path(td),False) for i in cat['roms']]
    out={'schema_version':1,'method':'split into consecutive 0x4000-byte banks, concatenate in original order','roms':results,'success':all(x['byte_identical'] and x['size_identical'] for x in results),'note':'Scratch bank binaries and rebuilt ROMs are not distributable workpack artifacts.'}
    rp.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'success':out['success'],'verified_roms':len(results),'report':str(rp)},indent=2))
if __name__=='__main__': main()
