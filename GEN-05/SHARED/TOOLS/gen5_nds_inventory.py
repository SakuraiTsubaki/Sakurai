#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, struct, csv

def u16(b,o): return struct.unpack_from('<H', b, o)[0]
def u32(b,o): return struct.unpack_from('<I', b, o)[0]
def digest(data): return hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()

def parse_fnt(rom, fnt_off, fnt_size):
    fnt=rom[fnt_off:fnt_off+fnt_size]
    if len(fnt)<8: return {}
    dirs=[]
    for i in range(u16(fnt,6)):
        o=i*8
        if o+8>len(fnt): break
        dirs.append((u32(fnt,o),u16(fnt,o+4),u16(fnt,o+6)))
    children={}; files={}
    for i,(sub,first,parent) in enumerate(dirs):
        pos=sub; fid=first; entries=[]
        while pos<len(fnt):
            n=fnt[pos]; pos+=1
            if n==0: break
            isdir=bool(n&0x80); ln=n&0x7f; name=fnt[pos:pos+ln].decode('ascii','replace'); pos+=ln
            if isdir:
                did=u16(fnt,pos); pos+=2; entries.append(('dir',name,did))
            else: entries.append(('file',name,fid)); fid+=1
        children[0xF000+i]=entries
    seen=set()
    def walk(did,prefix):
        if did in seen: return
        seen.add(did)
        for typ,name,val in children.get(did,[]):
            p=f'{prefix}/{name}' if prefix else name
            if typ=='file': files[val]=p
            else: walk(val,p)
    walk(0xF000,''); return files

def parse_rom(path,out):
    data=Path(path).read_bytes(); out.mkdir(parents=True,exist_ok=True)
    vals={'arm9_offset':u32(data,0x20),'arm9_entry':u32(data,0x24),'arm9_ram':u32(data,0x28),'arm9_size':u32(data,0x2c),'arm7_offset':u32(data,0x30),'arm7_entry':u32(data,0x34),'arm7_ram':u32(data,0x38),'arm7_size':u32(data,0x3c),'fnt_offset':u32(data,0x40),'fnt_size':u32(data,0x44),'fat_offset':u32(data,0x48),'fat_size':u32(data,0x4c),'ov9_offset':u32(data,0x50),'ov9_size':u32(data,0x54),'ov7_offset':u32(data,0x58),'ov7_size':u32(data,0x5c),'banner_offset':u32(data,0x68),'used_rom_size':u32(data,0x80),'header_size':u32(data,0x84)}
    fntmap=parse_fnt(data,vals['fnt_offset'],vals['fnt_size']); fat=[]
    for i in range(vals['fat_size']//8):
        s=u32(data,vals['fat_offset']+i*8); e=u32(data,vals['fat_offset']+i*8+4); blob=data[s:e]; a,b=digest(blob)
        fat.append({'file_id':i,'path':fntmap.get(i,''),'start':s,'end':e,'size':e-s,'sha1':a,'sha256':b,'magic':blob[:4].hex()})
    def overlays(off,size):
        rows=[]
        for i in range(size//32):
            o=off+i*32; oid,ram,rsz,bss,si0,si1,fid,flags=struct.unpack_from('<8I',data,o); f=fat[fid] if fid<len(fat) else None
            rows.append({'table_index':i,'overlay_id':oid,'ram_address':ram,'ram_size':rsz,'bss_size':bss,'static_init_start':si0,'static_init_end':si1,'file_id':fid,'flags':flags,'file_size':f['size'] if f else '','sha1':f['sha1'] if f else '','sha256':f['sha256'] if f else ''})
        return rows
    ov9=overlays(vals['ov9_offset'],vals['ov9_size']); ov7=overlays(vals['ov7_offset'],vals['ov7_size'])
    comp=[]
    for name,off,size in [('header',0,vals['header_size']),('arm9',vals['arm9_offset'],vals['arm9_size']),('arm7',vals['arm7_offset'],vals['arm7_size']),('fnt',vals['fnt_offset'],vals['fnt_size']),('fat',vals['fat_offset'],vals['fat_size']),('overlay9_table',vals['ov9_offset'],vals['ov9_size']),('overlay7_table',vals['ov7_offset'],vals['ov7_size'])]:
        a,b=digest(data[off:off+size]); comp.append({'component':name,'offset':off,'size':size,'sha1':a,'sha256':b})
    narc=[]
    for r in fat:
        if not r['path']: continue
        blob=data[r['start']:r['end']]
        if blob[:4]==b'NARC' and len(blob)>=16:
            members=u16(blob,24) if len(blob)>=28 and blob[16:20] in (b'BTAF',b'FATB') else ''
            narc.append({'file_id':r['file_id'],'path':r['path'],'size':r['size'],'members':members,'sha1':r['sha1'],'sha256':r['sha256']})
    nitro=[r for r in fat if r['path']]
    def write_tsv(name,rows):
        p=out/name
        if not rows: p.write_text('',encoding='utf-8'); return
        with p.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t'); w.writeheader(); w.writerows(rows)
    for name,rows in [('fat.tsv',fat),('nitrofs.tsv',nitro),('overlay9.tsv',ov9),('overlay7.tsv',ov7),('narc.tsv',narc),('components.tsv',comp)]: write_tsv(name,rows)
    sha1,sha256=digest(data); meta={'schema':'gen5.nds-inventory.v1','source_filename':Path(path).name,'rom_size':len(data),'sha1':sha1,'sha256':sha256,'internal_title':data[:12].rstrip(b'\0').decode('ascii','replace'),'game_code':data[0x0c:0x10].decode('ascii','replace'),'maker_code':data[0x10:0x12].decode('ascii','replace'),'unit_code':data[0x12],'rom_version':data[0x1e],**vals,'counts':{'fat_entries':len(fat),'named_nitrofs_files':len(nitro),'overlay9_entries':len(ov9),'overlay7_entries':len(ov7),'narc_files':len(narc),'fnt_named_file_ids_minmax':[min(fntmap),max(fntmap)]}}
    (out/'inventory.json').write_text(json.dumps(meta,indent=2)+'\n'); return {'meta':meta,'fat':fat,'nitro':nitro,'ov9':ov9,'components':comp}

def compare(a,b,out):
    out.mkdir(parents=True,exist_ok=True)
    def rows(left,right,key,fields,name):
        L={r[key]:r for r in left}; R={r[key]:r for r in right}; z=[]
        for k in sorted(set(L)|set(R),key=str):
            l=L.get(k); r=R.get(k); same=bool(l and r and l.get('sha256')==r.get('sha256')); row={key:k,'status':'identical' if same else 'different'}
            for f in fields: row['black_'+f]=l.get(f,'') if l else ''; row['white_'+f]=r.get(f,'') if r else ''
            z.append(row)
        with (out/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(z[0]),delimiter='\t'); w.writeheader(); w.writerows(z)
        return z
    n=rows(a['nitro'],b['nitro'],'path',['file_id','size','sha256'],'nitrofs-compare.tsv'); f=rows(a['fat'],b['fat'],'file_id',['path','size','sha256'],'fat-compare.tsv'); o=rows(a['ov9'],b['ov9'],'overlay_id',['file_id','file_size','sha256'],'overlay9-compare.tsv'); c=rows(a['components'],b['components'],'component',['offset','size','sha256'],'components-compare.tsv')
    s={'schema':'gen5.bw-compare.v1','nitrofs':{'total':len(n),'identical':sum(x['status']=='identical' for x in n),'different':sum(x['status']=='different' for x in n),'differing_paths':[x['path'] for x in n if x['status']=='different']},'fat':{'total':len(f),'identical':sum(x['status']=='identical' for x in f),'different':sum(x['status']=='different' for x in f)},'overlay9':{'total':len(o),'identical':sum(x['status']=='identical' for x in o),'different':sum(x['status']=='different' for x in o)},'components':{x['component']:x['status'] for x in c}}
    (out/'summary.json').write_text(json.dumps(s,indent=2)+'\n'); return s

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('black'); p.add_argument('white'); p.add_argument('out'); a=p.parse_args(); root=Path(a.out); A=parse_rom(a.black,root/'BLACK'); B=parse_rom(a.white,root/'WHITE'); print(json.dumps(compare(A,B,root/'COMPARE'),indent=2))
