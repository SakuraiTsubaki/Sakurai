#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
root=Path(__file__).resolve().parents[1]
errors=[]
rows=list(csv.DictReader(open(root/'data/semantic/bank_summary_64.csv',encoding='utf-8')))
if len(rows)!=64: errors.append(f'bank summary rows {len(rows)} != 64')
sec=list(csv.DictReader(open(root/'data/semantic/section_layout.csv',encoding='utf-8')))
if len(sec)!=148: errors.append(f'section rows {len(sec)} != 148')
if not any(r['section']=='Pokédex Text' and r['bank_hex']=='2E' for r in sec): errors.append('missing Pokédex Text bank 2E')
if not any(r['section']=='Move Names' and r['bank_hex']=='2F' for r in sec): errors.append('missing Move Names bank 2F')
if any(r['bank_hex']=='3B' for r in sec): errors.append('bank 3B should have no EN layout sections')
lock=json.load(open(root/'reference/pret_semantic_reference.lock.json',encoding='utf-8'))
if lock['semantic_commit']!='e89ead154b9968aa50eed9328ff2b38b6c194382': errors.append('pret commit drift')
# Large generated caches are optional in Git; when present, validate their cardinality.
atlas_path=root/'data/semantic/bank_atlas.csv'
if atlas_path.exists():
 atlas=list(csv.DictReader(open(atlas_path,encoding='utf-8')))
 if len(atlas)!=576: errors.append(f'atlas rows {len(atlas)} != 576')
rels_path=root/'data/semantic/relationship_bank_diffs.csv'
if rels_path.exists():
 rels=list(csv.DictReader(open(rels_path,encoding='utf-8')))
 if len(rels)!=512: errors.append(f'relationship bank rows {len(rels)} != 512')
if errors:
 print('FAIL'); [print('-',e) for e in errors]; sys.exit(1)
print('PASS semantic core:',len(rows),'banks,',len(sec),'EN layout sections')
