#!/usr/bin/env python3
"""Reproducible structural auditor for Pokémon White IRAO-HV0.

Reads a user-supplied ROM. It never modifies the ROM and never exports ROM
payloads; output is metadata/profile TSV/JSON only.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, json, struct
from pathlib import Path

CORE = {
    'a/0/1/6':'personal', 'a/0/1/7':'growth', 'a/0/1/8':'learnsets',
    'a/0/1/9':'evolution', 'a/0/2/0':'base_species', 'a/0/2/1':'moves',
    'a/0/2/4':'items', 'a/0/9/2':'trdata', 'a/0/9/3':'trpoke',
    'a/1/2/3':'egg_moves', 'a/1/2/6':'encounters', 'a/0/1/2':'zone_data'
}

def u16(b,o=0): return struct.unpack_from('<H',b,o)[0]
def u32(b,o=0): return struct.unpack_from('<I',b,o)[0]
def digest(b): return hashlib.sha256(b).hexdigest()

def narc_members(blob: bytes):
    if blob[:4] != b'NARC': return None
    p=0x10
    fat_sz=u32(blob,p+4); n=u16(blob,p+8)
    ents=[struct.unpack_from('<II',blob,p+12+i*8) for i in range(n)]
    p += fat_sz
    p += u32(blob,p+4)  # FNTB/BTNF
    data0=p+8           # FIMG/GMIF payload
    return [blob[data0+s:data0+e] for s,e in ents]

def parse_fnt(fnt: bytes):
    ndir=u16(fnt,6); dirs={}
    for i in range(ndir):
        p=u32(fnt,i*8); fid=u16(fnt,i*8+4); out=[]
        while True:
            n=fnt[p]; p+=1
            if n==0: break
            isdir=bool(n&0x80); ln=n&0x7f
            name=fnt[p:p+ln].decode('ascii','replace'); p+=ln
            if isdir:
                did=u16(fnt,p); p+=2; out.append(('d',name,did))
            else:
                out.append(('f',name,fid)); fid+=1
        dirs[0xf000+i]=out
    paths={}
    def walk(did,prefix=''):
        for typ,name,x in dirs.get(did,[]):
            q=f'{prefix}/{name}' if prefix else name
            if typ=='f': paths[x]=q
            else: walk(x,q)
    walk(0xf000)
    return paths, ndir

def load_rom(path: Path):
    d=path.read_bytes(); h=d[:0x200]
    hdr={
      'internal_title':h[:12].rstrip(b'\0').decode('ascii','replace'),
      'game_code':h[0x0c:0x10].decode('ascii','replace'),
      'maker_code':h[0x10:0x12].decode('ascii','replace'),
      'unit_code':h[0x12], 'capacity_code':h[0x14], 'rom_version':h[0x1e],
      'arm9_offset':u32(h,0x20),'arm9_size':u32(h,0x2c),
      'arm7_offset':u32(h,0x30),'arm7_size':u32(h,0x3c),
      'fnt_offset':u32(h,0x40),'fnt_size':u32(h,0x44),
      'fat_offset':u32(h,0x48),'fat_size':u32(h,0x4c),
      'overlay9_offset':u32(h,0x50),'overlay9_size':u32(h,0x54),
      'header_rom_size':u32(h,0x80),'header_size':u32(h,0x84)
    }
    fnt=d[hdr['fnt_offset']:hdr['fnt_offset']+hdr['fnt_size']]
    paths,ndir=parse_fnt(fnt)
    fat=d[hdr['fat_offset']:hdr['fat_offset']+hdr['fat_size']]
    files=[]
    for fid in range(len(fat)//8):
        s,e=struct.unpack_from('<II',fat,fid*8); b=d[s:e]
        files.append({'file_id':fid,'path':paths.get(fid,f'__overlay9__/{fid:03d}'),
                      'start':s,'size':e-s,'magic':b[:4].hex()})
    return d,hdr,ndir,files

def get_members(d, files, path):
    f=next(x for x in files if x['path']==path)
    b=d[f['start']:f['start']+f['size']]
    m=narc_members(b)
    if m is None: raise ValueError(f'{path} is not NARC')
    return m

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom'); ap.add_argument('-o','--out',default='white-irao-audit')
    a=ap.parse_args(); p=Path(a.rom); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    d,h,ndir,files=load_rom(p)
    ident={'file':p.name,'size':len(d),'md5':hashlib.md5(d).hexdigest(),
           'sha1':hashlib.sha1(d).hexdigest(),'sha256':hashlib.sha256(d).hexdigest(),
           'header':h,'fnt_directories':ndir,'fat_entries':len(files)}
    (out/'identity.json').write_text(json.dumps(ident,indent=2),encoding='utf-8')

    with (out/'named_files.tsv').open('w',newline='',encoding='utf-8') as fp:
        w=csv.DictWriter(fp,fieldnames=['file_id','path','start','size','magic'],delimiter='\t'); w.writeheader()
        w.writerows(x for x in files if not x['path'].startswith('__overlay9__'))

    profiles=[]
    for path,role in CORE.items():
        m=get_members(d,files,path); sizes=collections.Counter(map(len,m))
        profiles.append({'path':path,'role':role,'members':len(m),
                         'size_distribution':','.join(f'{k}:{v}' for k,v in sorted(sizes.items()))})
    with (out/'core_profiles.tsv').open('w',newline='',encoding='utf-8') as fp:
        w=csv.DictWriter(fp,fieldnames=profiles[0].keys(),delimiter='\t'); w.writeheader(); w.writerows(profiles)

    # Personal archive special layout and Unova-Dex lookup.
    personal=get_members(d,files,'a/0/1/6')
    dex=list(struct.unpack('<650H',personal[668]))
    assert dex[:494] == [999]*494 and dex[494:] == list(range(156))
    form_links=[]
    for species,m in enumerate(personal[1:650],1):
        formid=u16(m,28); form=u16(m,30); nforms=m[32]
        if formid or nforms>1:
            form_links.append({'species':species,'formid':formid,'form_index':form,'numforms':nforms})
    with (out/'personal_form_links.tsv').open('w',newline='',encoding='utf-8') as fp:
        w=csv.DictWriter(fp,fieldnames=form_links[0].keys(),delimiter='\t');w.writeheader();w.writerows(form_links)

    # Trainer width proof.
    td=get_members(d,files,'a/0/9/2'); tp=get_members(d,files,'a/0/9/3')
    fmt='<BBBBHHHHIB3x'; expected={0:8,1:16,2:10,3:18}; dist=collections.Counter(); mism=[]
    for i in range(1,616):
        flag,_,_,count,*_=struct.unpack(fmt,td[i]); dist[flag]+=1
        if count and len(tp[i]) != count*expected[flag]: mism.append(i)
    assert not mism
    (out/'trainer_width_proof.json').write_text(json.dumps({'flag_counts':dict(dist),'bytes_per_pokemon':expected,'mismatches':mism},indent=2),encoding='utf-8')

    # Encounter member/season-block profile.
    enc=get_members(d,files,'a/1/2/6')
    seasonal=[i for i,m in enumerate(enc) if len(m)==928]
    assert all(len(m) in (232,928) for m in enc)
    (out/'encounter_profile.json').write_text(json.dumps({'members':len(enc),'size_counts':dict(collections.Counter(map(len,enc))),
        'seasonal_four_block_member_ids':seasonal,'base_block_size':232},indent=2),encoding='utf-8')

    print(json.dumps({'sha1':ident['sha1'],'named_files':sum(not x['path'].startswith('__overlay9__') for x in files),
        'personal_members':len(personal),'trainer_mismatches':len(mism),'seasonal_encounter_members':seasonal},indent=2))
if __name__=='__main__': main()
