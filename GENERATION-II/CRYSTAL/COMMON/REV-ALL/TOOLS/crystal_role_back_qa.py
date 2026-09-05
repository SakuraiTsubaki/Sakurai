#!/usr/bin/env python3
"""QA Crystal-role HGSS back candidates against original Crystal back sprites."""
from __future__ import annotations
import argparse,csv,importlib.util,re
from pathlib import Path

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def names(root):
    text=(Path(root)/'data/pokemon/palettes.asm').read_text(encoding='utf-8')
    a=re.findall(r'INCBIN "gfx/pokemon/([^/]+)/normal\.gbcpal", middle_colors',text)
    if len(a)!=251: raise ValueError(len(a))
    return {i+1:n for i,n in enumerate(a)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--front-qa-tool',required=True); ap.add_argument('--candidate-root',required=True); ap.add_argument('--pokecrystal-root',required=True); ap.add_argument('--output',required=True); ns=ap.parse_args()
    q=load_module('frontqa',ns.front_qa_tool); nmap=names(ns.pokecrystal_root); root=Path(ns.candidate_root); rows=[]
    for sp in list(range(1,201))+list(range(202,252)):
        name=nmap[sp]; f=root/'2BPP'/'BACK'/f'{sp:03d}.6x6.2bpp'
        cand=q.metrics(q.decode_2bpp(f.read_bytes(),6)); orig=q.metrics(q.png_first_frame(Path(ns.pokecrystal_root)/'gfx'/'pokemon'/name/'back.png',48)); area_ratio,light_shift,flags=q.evaluate(orig,cand)
        rows.append({'species':sp,'name':name,'status':'REVIEW' if flags else 'PASS','flags':','.join(flags),'area_ratio':f'{area_ratio:.4f}','light_shift':f'{light_shift:.4f}' if light_shift>=0 else '','orig_highlight':f"{orig['p0']:.4f}",'cand_highlight':f"{cand['p0']:.4f}",'orig_color1':f"{orig['p1']:.4f}",'cand_color1':f"{cand['p1']:.4f}",'orig_color2':f"{orig['p2']:.4f}",'cand_color2':f"{cand['p2']:.4f}",'orig_black':f"{orig['p3']:.4f}",'cand_black':f"{cand['p3']:.4f}",'orig_bbox':f"{orig['bbox_w']}x{orig['bbox_h']}",'cand_bbox':f"{cand['bbox_w']}x{cand['bbox_h']}"})
    out=Path(ns.output); out.parent.mkdir(parents=True,exist_ok=True); fields=list(rows[0])
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); w.writeheader(); w.writerows(rows)
    review=[r for r in rows if r['status']=='REVIEW']; counts={}
    for r in review:
        for x in filter(None,r['flags'].split(',')): counts[x]=counts.get(x,0)+1
    lines=['# Crystal-role back lighting QA','',f'- PASS: {len(rows)-len(review)} / {len(rows)}',f'- REVIEW: {len(review)} / {len(rows)}','','## Flag counts','']
    lines += [f'- {k}: {v}' for k,v in sorted(counts.items(),key=lambda kv:(-kv[1],kv[0]))]
    lines += ['','## Manual-review species','']+[f"- #{r['species']:03d} {r['name']}: {r['flags']}" for r in review]
    out.with_suffix('.summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('PASS',len(rows)-len(review),'REVIEW',len(review),'TOTAL',len(rows)); [print(k,v) for k,v in sorted(counts.items())]
if __name__=='__main__': main()
