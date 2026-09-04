#!/usr/bin/env python3
"""Byte-level Pokémon Black/White NDS census.

Usage:
    python3 bw_rom_census.py BLACK.nds WHITE.nds OUTDIR

This script never modifies the ROMs. It emits CSV/JSON inventories and a
Black↔White comparison. Original ROM images must not be committed.
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, struct, sys


def u16(b,o): return struct.unpack_from('<H', b, o)[0]
def u32(b,o): return struct.unpack_from('<I', b, o)[0]
def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()


def header(data):
    h=data[:0x4000]
    cap=(128*1024) << h[0x14]
    return {
        'title':h[:12].rstrip(b'\0').decode('ascii','replace'),
        'game_code':h[0x0c:0x10].decode('ascii','replace'),
        'maker':h[0x10:0x12].decode('ascii','replace'),
        'unit_code':h[0x12], 'revision':h[0x1e],
        'arm9_off':u32(h,0x20), 'arm9_size':u32(h,0x2c),
        'arm7_off':u32(h,0x30), 'arm7_size':u32(h,0x3c),
        'fnt_off':u32(h,0x40), 'fnt_size':u32(h,0x44),
        'fat_off':u32(h,0x48), 'fat_size':u32(h,0x4c),
        'ov9_off':u32(h,0x50), 'ov9_size':u32(h,0x54),
        'used_rom_size':u32(h,0x80), 'declared_capacity':cap,
        'physical_size':len(data), 'trimmed':len(data)<cap,
    }


def fat(data,h):
    return [struct.unpack_from('<II',data,h['fat_off']+i*8)
            for i in range(h['fat_size']//8)]


def fnt_names(data,h):
    f=data[h['fnt_off']:h['fnt_off']+h['fnt_size']]
    count=u16(f,6); dirs=[(u32(f,i*8),u16(f,i*8+4),u16(f,i*8+6)) for i in range(count)]
    names={}; seen=set()
    def walk(did,prefix):
        if did in seen: return
        seen.add(did); idx=did-0xF000
        if not (0<=idx<len(dirs)): return
        pos,fid,_=dirs[idx]
        while pos<len(f):
            n=f[pos]; pos+=1
            if n==0: break
            isdir=n&0x80; ln=n&0x7f
            name=f[pos:pos+ln].decode('ascii','replace'); pos+=ln
            if isdir:
                child=u16(f,pos); pos+=2; walk(child,prefix+name+'/')
            else:
                names[fid]=prefix+name; fid+=1
    walk(0xF000,'/')
    return names, count


def narc_members(blob):
    if blob[:4]!=b'NARC': return None
    pos=16; btaf=gmif=None
    while pos+8<=len(blob):
        magic=blob[pos:pos+4]; size=u32(blob,pos+4)
        if size<8 or pos+size>len(blob): break
        if magic==b'BTAF': btaf=(pos,size)
        elif magic==b'GMIF': gmif=(pos,size)
        pos+=size
    if not btaf or not gmif: return None
    bo,_=btaf; go,_=gmif; count=u16(blob,bo+8); base=go+8
    out=[]
    for i in range(count):
        s,e=struct.unpack_from('<II',blob,bo+12+i*8)
        out.append(blob[base+s:base+e])
    return out


def scan(path):
    data=Path(path).read_bytes(); h=header(data); ft=fat(data,h); names,dir_count=fnt_names(data,h)
    files=[]; narcs=[]; members=[]
    for fid,(s,e) in enumerate(ft):
        present=e<=len(data); blob=data[s:e] if present else b''
        files.append({'file_id':fid,'path':names.get(fid,''),'start':s,'end':e,'size':e-s,
                      'present':present,'sha1':sha1(blob) if present else ''})
        ms=narc_members(blob) if present else None
        if ms is not None:
            narcs.append({'file_id':fid,'path':names.get(fid,''),'size':len(blob),'members':len(ms),'sha1':sha1(blob)})
            for i,m in enumerate(ms):
                members.append({'file_id':fid,'path':names.get(fid,''),'member':i,'size':len(m),'sha1':sha1(m)})
    overlays=[]
    for i in range(h['ov9_size']//32):
        o=h['ov9_off']+i*32; vals=struct.unpack_from('<8I',data,o); fid=vals[6]
        s,e=ft[fid]; blob=data[s:e] if e<=len(data) else b''
        overlays.append({'overlay':i,'overlay_id':vals[0],'file_id':fid,'size':e-s,
                         'present':e<=len(data),'sha1':sha1(blob) if blob else ''})
    return {'path':str(path),'data':data,'h':h,'files':files,'narcs':narcs,'members':members,
            'overlays':overlays,'named':len(names),'dirs':dir_count,'sha1':sha1(data),'sha256':sha256(data)}


def write_csv(path,rows):
    if not rows: Path(path).write_text('',encoding='utf-8'); return
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    if len(sys.argv)!=4: raise SystemExit('usage: bw_rom_census.py BLACK.nds WHITE.nds OUTDIR')
    B,W=scan(sys.argv[1]),scan(sys.argv[2]); out=Path(sys.argv[3]); out.mkdir(parents=True,exist_ok=True)
    ids=[]
    for version,X in [('Black',B),('White',W)]:
        h=X['h']; ids.append({'version':version,'filename':Path(X['path']).name,'physical_size':h['physical_size'],
          'declared_capacity':h['declared_capacity'],'used_rom_size':h['used_rom_size'],'trimmed':h['trimmed'],
          'title':h['title'],'game_code':h['game_code'],'unit_code':h['unit_code'],'revision':h['revision'],
          'sha1':X['sha1'],'sha256':X['sha256']})
    write_csv(out/'rom_identity.csv',ids)
    fc=[]
    for b,w in zip(B['files'],W['files']):
        fc.append({'file_id':b['file_id'],'path':b['path'] or w['path'],'size_black':b['size'],'size_white':w['size'],
                   'present_black':b['present'],'present_white':w['present'],'same':b['sha1']==w['sha1'] and b['present'] and w['present']})
    write_csv(out/'file_comparison.csv',fc)
    oc=[]
    for b,w in zip(B['overlays'],W['overlays']):
        oc.append({'overlay':b['overlay'],'file_id_black':b['file_id'],'file_id_white':w['file_id'],
                   'size_black':b['size'],'size_white':w['size'],'same':b['sha1']==w['sha1'] and b['present'] and w['present']})
    write_csv(out/'overlay_comparison.csv',oc)
    bn={r['file_id']:r for r in B['narcs']}; wn={r['file_id']:r for r in W['narcs']}; nc=[]
    for fid in sorted(set(bn)|set(wn)):
        b=bn.get(fid,{}); w=wn.get(fid,{})
        nc.append({'file_id':fid,'path':b.get('path') or w.get('path',''),'members_black':b.get('members',''),
                   'members_white':w.get('members',''),'size_black':b.get('size',''),'size_white':w.get('size',''),
                   'same':bool(b and w and b['sha1']==w['sha1'])})
    write_csv(out/'narc_summary.csv',nc)
    bm={(r['file_id'],r['member']):r for r in B['members']}; wm={(r['file_id'],r['member']):r for r in W['members']}
    mc=[]
    for k in sorted(set(bm)|set(wm)):
        b= bm.get(k,{}); w=wm.get(k,{})
        mc.append({'file_id':k[0],'path':b.get('path') or w.get('path',''),'member':k[1],
                   'size_black':b.get('size',''),'size_white':w.get('size',''),'same':bool(b and w and b['sha1']==w['sha1'])})
    write_csv(out/'all_narc_member_comparison.csv',mc)
    write_csv(out/'differing_narc_members.csv',[r for r in mc if not r['same']])
    summary={'roms':ids,'fat_files':len(B['files']),'named_files':B['named'],'directories':B['dirs'],
      'overlays':len(B['overlays']),'narcs':len(B['narcs']),'narc_members':len(B['members']),
      'same_fat_files':sum(r['same'] for r in fc),'different_fat_files':sum(not r['same'] for r in fc),
      'same_overlays':sum(r['same'] for r in oc),'different_overlays':sum(not r['same'] for r in oc),
      'same_narc_members':sum(r['same'] for r in mc),'different_narc_members':sum(not r['same'] for r in mc),
      'different_narcs':[r['path'] for r in nc if not r['same']]}
    (out/'census_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
