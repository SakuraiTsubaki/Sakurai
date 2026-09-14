#!/usr/bin/env python3
"""Extract the byte-identical Emerald BattleMove table from verified reference ROMs."""
from __future__ import annotations
import argparse, csv, hashlib, json, struct
from pathlib import Path

COUNT = 355
STRIDE = 12
SEMANTIC_SIZE = 9
SEGMENTS = [(0, 176), (177, 354)]

def sha1(b: bytes) -> str: return hashlib.sha1(b).hexdigest()

def load(ref: dict, rom_dir: Path) -> bytes:
    d=(rom_dir/ref['source_filename']).read_bytes()
    if sha1(d) != ref['sha1']: raise ValueError(f"SHA-1 mismatch: {ref['id']}")
    return d

def parse(i: int, b: bytes) -> dict[str, object]:
    return {'move_id':i,'effect':b[0],'power':b[1],'type':b[2],'accuracy':b[3],'pp':b[4],
            'secondary_effect_chance':b[5],'target':b[6],'priority':struct.unpack('b',b[7:8])[0],
            'flags':b[8],'padding_hex':b[9:12].hex().upper(),'raw_hex':b.hex().upper()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom_dir',type=Path)
    ap.add_argument('--manifest',type=Path,default=Path('manifests/roms.json'))
    ap.add_argument('--headers',type=Path,default=Path('analysis/gf_rom_headers.json'))
    ap.add_argument('--out-dir',type=Path,default=Path('data/battle_moves')); a=ap.parse_args()
    refs={r['id']:r for r in json.loads(a.manifest.read_text())['references']}
    headers=json.loads(a.headers.read_text())['records']; a.out_dir.mkdir(parents=True,exist_ok=True)
    canonical=None; roots=[]
    for h in headers:
        d=load(refs[h['id']],a.rom_dir); root=h['moves_rom_offset']; table=d[root:root+COUNT*STRIDE]
        if canonical is None: canonical=table
        elif table != canonical: raise ValueError(f"BattleMove differs: {h['id']}")
        roots.append({'release':h['id'],'root_rom_offset':f'0x{root:08X}','sha1':sha1(table)})
    rows=[parse(i,canonical[i*STRIDE:(i+1)*STRIDE]) for i in range(COUNT)]
    if any(r['padding_hex'] != '000000' for r in rows): raise ValueError('nonzero BattleMove padding found')
    for start,end in SEGMENTS:
        with (a.out_dir/f'battle_moves_{start:03d}_{end:03d}.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows[start:end+1])
    (a.out_dir/'manifest.json').write_text(json.dumps({'schema_version':1,'record_count':COUNT,'record_stride':STRIDE,
        'semantic_size':SEMANTIC_SIZE,'byte_length':len(canonical),'shared_table_sha1':sha1(canonical),'all_unique_releases_byte_identical':True,
        'segments':[f'{a:03d}-{b:03d}' for a,b in SEGMENTS],'release_roots':roots},indent=2)+'\n')
if __name__=='__main__': main()
