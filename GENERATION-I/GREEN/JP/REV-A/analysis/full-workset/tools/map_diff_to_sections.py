#!/usr/bin/env python3
"""Attribute ROM revision diff runs to exact RGBDS section boundaries."""
from pathlib import Path
from collections import defaultdict
import argparse,csv
def load_sections(path):
 out=[]
 for r in csv.DictReader(Path(path).open(encoding='utf-8')):
  if r.get('file_offset_start') and r.get('file_offset_end'):out.append({**r,'start':int(r['file_offset_start'],16),'end':int(r['file_offset_end'],16)})
 return sorted(out,key=lambda x:(x['start'],x['end'],x['section']))
def at(ss,o):
 for s in ss:
  if s['start']<=o<=s['end']:return s
def write(path,rows,fields):
 Path(path).parent.mkdir(parents=True,exist_ok=True)
 with Path(path).open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--diff-runs',type=Path,required=True);ap.add_argument('--rev0-sections',type=Path,required=True);ap.add_argument('--reva-sections',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);a=ap.parse_args();s0=load_sections(a.rev0_sections);s1=load_sections(a.reva_sections);pieces=[]
 for rid,r in enumerate(csv.DictReader(a.diff_runs.open(encoding='utf-8')),1):
  lo,hi=int(r['offset_start'],16),int(r['offset_end'],16);cuts={lo,hi+1}
  for s in s0+s1:
   if lo<s['start']<=hi:cuts.add(s['start'])
   if lo<=s['end']<hi:cuts.add(s['end']+1)
  cuts=sorted(cuts)
  for x,y in zip(cuts,cuts[1:]):
   e=y-1;u,v=at(s0,x),at(s1,x);pieces.append({'diff_run_id':rid,'offset_start':f'0x{x:05X}','offset_end':f'0x{e:05X}','length':e-x+1,'bank':f'{x//0x4000:02X}','rev0_section':u['section'] if u else '','reva_section':v['section'] if v else '','rev0_domain':u['domain'] if u else '','reva_domain':v['domain'] if v else ''})
 fields=['diff_run_id','offset_start','offset_end','length','bank','rev0_section','reva_section','rev0_domain','reva_domain'];write(a.outdir/'diff_runs_with_sections.csv',pieces,fields)
 agg=defaultdict(lambda:{'runs':set(),'pieces':0,'changed_bytes':0,'first':None,'last':None})
 for p in pieces:
  k=(p['bank'],p['rev0_section'],p['reva_section']);z=agg[k];z['runs'].add(p['diff_run_id']);z['pieces']+=1;z['changed_bytes']+=int(p['length']);x=int(p['offset_start'],16);y=int(p['offset_end'],16);z['first']=x if z['first'] is None else min(z['first'],x);z['last']=y if z['last'] is None else max(z['last'],y)
 rows=[]
 for (bank,u,v),z in sorted(agg.items()):rows.append({'bank':bank,'rev0_section':u,'reva_section':v,'diff_run_count':len(z['runs']),'piece_count':z['pieces'],'changed_bytes':z['changed_bytes'],'first_offset':f"0x{z['first']:05X}",'last_offset':f"0x{z['last']:05X}"})
 write(a.outdir/'diff_by_section.csv',rows,['bank','rev0_section','reva_section','diff_run_count','piece_count','changed_bytes','first_offset','last_offset']);print(f'{len(pieces)} section-attributed pieces; {sum(int(p["length"]) for p in pieces)} changed bytes')
if __name__=='__main__':main()
