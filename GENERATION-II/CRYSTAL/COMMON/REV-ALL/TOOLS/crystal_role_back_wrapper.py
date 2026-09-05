#!/usr/bin/env python3
"""Use crystal_role_palette_converter.py to build Crystal-role HGSS back sprites (fixed 6x6)."""
import argparse,csv,importlib.util
from pathlib import Path

def load_module(path):
    spec=importlib.util.spec_from_file_location('role_converter',path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def parse_species(s):
    out=[]
    for part in s.split(','):
        part=part.strip()
        if '-' in part:
            a,b=map(int,part.split('-',1)); out.extend(range(a,b+1))
        else: out.append(int(part))
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--converter',required=True); ap.add_argument('--source-root',required=True); ap.add_argument('--pokecrystal-root',required=True); ap.add_argument('--output-root',required=True); ap.add_argument('--species',required=True); ns=ap.parse_args()
    m=load_module(ns.converter); names=m.build_name_map(ns.pokecrystal_root); root=Path(ns.output_root); rows=[]
    for sp in parse_species(ns.species):
        name=names[sp]
        src=Path(ns.source_root)/'BACK'/f'{sp:03d}.png'
        ref=Path(ns.pokecrystal_root)/'gfx'/'pokemon'/name/'back.png'
        row=m.convert_one(sp,src,ref,6,root); row['side']='back'; rows.append(row)
        print(f'#{sp:03d} {name} back: 6x6 done')
    # The shared converter writes FRONT-named folders; rename them for the back candidate set.
    for parent in ('2BPP','PREVIEW'):
        a=root/parent/'FRONT'; b=root/parent/'BACK'
        if b.exists():
            import shutil; shutil.rmtree(b)
        if a.exists(): a.rename(b)
    out=root/'ROLE_MAPPING_REPORT_BACK.tsv'; fields=list(rows[0]) if rows else []
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); w.writeheader(); w.writerows(rows)
if __name__=='__main__': main()
