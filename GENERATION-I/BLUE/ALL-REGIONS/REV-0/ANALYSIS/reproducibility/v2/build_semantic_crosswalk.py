#!/usr/bin/env python3
"""Build evidence-based bank semantic crosswalks from exact alignment runs."""
from pathlib import Path
import csv, collections
ROOT=Path(__file__).resolve().parents[0]
BANK=0x4000
LABELS={0:'ROM0 / Header / Home',1:'bank1',2:'Audio 1',3:'bank3',4:'NPC Sprites 1 / Font / Battle Engine 1',5:'NPC Sprites 2 / Battle Engine 2',6:'Maps 1-2 / Play Time / Doors and Ledges',7:'Maps 3-4 / Pokemon Names / Hidden Events 1',8:'Audio 2 / Bills PC',9:'Pics 1 / Battle Engine 3',10:'Pics 2 / Battle Engine 4',11:'Pics 3 / Battle Engine 5',12:'Pics 4 / Battle Engine 6',13:'Pics 5 / Slot Machines',14:'Battle Engine 7',15:'Battle Core',16:'bank10',17:'Maps 5-6 / Pokedex Rating / Hidden Events Core',18:'Maps 7-8 / Screen Effects',19:'Trainer Pics / Maps 9 / Predefs',20:'Maps 10 / Battle Engine 8 / Hidden Events 2',21:'Maps 11-12 / Battle Engine 9 / Diploma / Trainer Sight',22:'Maps 13-14 / Battle Engine 10 / Saffron Guards',23:'Maps 15-16 / Starter Dex / Hidden Events 3',24:'Maps 17-18 / Cinnabar Lab Fossils / Hidden Events 4',25:'Tilesets 1',26:'Battle Engine 11 / Tilesets 2',27:'Tilesets 3',28:'bank1C',29:'Maps 19-21 / Itemfinder / Vending Machine',30:'bank1E',31:'Audio 3',32:'Text 1',33:'Text 2',34:'Text 3',35:'Text 4',36:'Text 5',37:'Text 6',38:'Text 7',39:'Text 8',40:'Text 9',41:'Text 10',42:'Text 11',43:'Pokedex Text',44:'Move Names'}

def main():
    src=ROOT.parent/'exact_alignment_runs.csv'
    if not src.exists(): raise SystemExit('Place exact_alignment_runs.csv beside the v2 directory or regenerate it locally.')
    acc=collections.Counter()
    for r in csv.DictReader(src.open(encoding='utf-8')):
        tgt=r['target']; s=int(r['source_start'],16); t=int(r['target_start'],16); n=int(r['length']); pos=0
        while pos<n:
            sb=(s+pos)//BANK; tb=(t+pos)//BANK; k=min(n-pos,BANK-((s+pos)%BANK),BANK-((t+pos)%BANK)); acc[(tgt,tb,sb)]+=k; pos+=k
    groups=collections.defaultdict(list)
    for (tgt,tb,sb),n in acc.items(): groups[(tgt,tb)].append((n,sb))
    out=ROOT/'semantic_bank_crosswalk_best.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['target','target_bank_hex','best_en_bank_hex','exact_aligned_bytes','target_bank_fraction','confidence','en_semantic_sections'])
        for (tgt,tb),vals in sorted(groups.items()):
            n,sb=max(vals); frac=n/BANK; conf='HIGH' if frac>=.75 else 'MEDIUM' if frac>=.35 else 'LOW'; w.writerow([tgt,f'{tb:02X}',f'{sb:02X}',n,f'{frac:.6f}',conf,LABELS.get(sb,'outside canonical EN semantic banks')])
    print('wrote',out)
if __name__=='__main__': main()
