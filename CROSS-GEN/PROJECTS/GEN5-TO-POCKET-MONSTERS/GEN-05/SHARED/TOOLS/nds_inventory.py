#!/usr/bin/env python3
import sys, struct, hashlib, json, csv
from pathlib import Path

def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def sha(data, alg='sha256'):
    h=getattr(hashlib,alg)(); h.update(data); return h.hexdigest()

def parse_fnt(rom, fnt_off, fnt_size, fat_off, fat_size):
    fnt=rom[fnt_off:fnt_off+fnt_size]; fat=rom[fat_off:fat_off+fat_size]
    nfiles=fat_size//8; dir_count=u16(fnt,6); dirs={}
    for i in range(dir_count):
        off=i*8
        dirs[0xF000+i]={'sub_off':u32(fnt,off),'first_id':u16(fnt,off+4),'parent':u16(fnt,off+6),'children':[],'files':[]}
    for did,d in dirs.items():
        p=d['sub_off']; fid=d['first_id']
        while p<len(fnt):
            n=fnt[p]; p+=1
            if n==0: break
            isdir=bool(n&0x80); ln=n&0x7f
            name=fnt[p:p+ln].decode('ascii','replace'); p+=ln
            if isdir:
                subid=u16(fnt,p); p+=2; d['children'].append((name,subid))
            else:
                d['files'].append((name,fid)); fid+=1
    paths={}
    def walk(did,prefix=''):
        d=dirs[did]
        for name,fid in d['files']: paths[fid]=prefix+name
        for name,subid in d['children']: walk(subid,prefix+name+'/')
    walk(0xF000)
    out=[]
    for fid in range(nfiles):
        st=u32(fat,fid*8); en=u32(fat,fid*8+4); data=rom[st:en]; sig=data[:4]
        out.append({'file_id':fid,'path':paths.get(fid,f'__UNNAMED__/{fid:04d}'),'start':st,'end':en,'size':en-st,
                    'sha1':sha(data,'sha1'),'sha256':sha(data),'magic_hex':sig.hex(),
                    'magic_ascii':''.join(chr(x) if 32<=x<127 else '.' for x in sig)})
    return out,dirs

def parse_overlays(rom,off,size):
    out=[]
    for i in range(size//32):
        vals=struct.unpack('<8I',rom[off+i*32:off+(i+1)*32])
        ov_id,ram,ram_size,bss,si_s,si_e,file_id,comp_flags=vals
        out.append({'table_index':i,'overlay_id':ov_id,'ram_address':ram,'ram_size':ram_size,'bss_size':bss,
                    'static_init_start':si_s,'static_init_end':si_e,'file_id':file_id,
                    'compressed_size_flags_raw':comp_flags,'compressed_size':comp_flags&0x00FFFFFF,'flags':(comp_flags>>24)&0xFF})
    return out

def inspect(path):
    rom=Path(path).read_bytes(); h=rom[:0x200]
    hdr={'filename':Path(path).name,'file_size':len(rom),'title':h[:12].rstrip(b'\0').decode('ascii','replace'),
         'game_code':h[0x0c:0x10].decode('ascii','replace'),'maker_code':h[0x10:0x12].decode('ascii','replace'),
         'unit_code':h[0x12],'device_type':h[0x13],'device_capacity_code':h[0x14],'rom_version':h[0x1e],
         'arm9_offset':u32(h,0x20),'arm9_entry':u32(h,0x24),'arm9_ram':u32(h,0x28),'arm9_size':u32(h,0x2c),
         'arm7_offset':u32(h,0x30),'arm7_entry':u32(h,0x34),'arm7_ram':u32(h,0x38),'arm7_size':u32(h,0x3c),
         'fnt_offset':u32(h,0x40),'fnt_size':u32(h,0x44),'fat_offset':u32(h,0x48),'fat_size':u32(h,0x4c),
         'arm9_overlay_offset':u32(h,0x50),'arm9_overlay_size':u32(h,0x54),'arm7_overlay_offset':u32(h,0x58),
         'arm7_overlay_size':u32(h,0x5c),'banner_offset':u32(h,0x68),'rom_size_header':u32(h,0x80),
         'header_size':u32(h,0x84),'logo_crc16':u16(h,0x15c),'header_crc16':u16(h,0x15e),
         'md5':sha(rom,'md5'),'sha1':sha(rom,'sha1'),'sha256':sha(rom)}
    files,dirs=parse_fnt(rom,hdr['fnt_offset'],hdr['fnt_size'],hdr['fat_offset'],hdr['fat_size'])
    ovs=parse_overlays(rom,hdr['arm9_overlay_offset'],hdr['arm9_overlay_size'])
    arm9=rom[hdr['arm9_offset']:hdr['arm9_offset']+hdr['arm9_size']]
    arm7=rom[hdr['arm7_offset']:hdr['arm7_offset']+hdr['arm7_size']]
    return {'header':hdr,'files':files,'overlays':ovs,'exec':{'arm9_sha256':sha(arm9),'arm7_sha256':sha(arm7),'arm9_sha1':sha(arm9,'sha1'),'arm7_sha1':sha(arm7,'sha1')},'directory_count':len(dirs)}

def write_tsv(path,rows):
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),delimiter='\t'); w.writeheader(); w.writerows(rows)

def main(a,b,outdir):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True); A=inspect(a); B=inspect(b)
    for label,obj in [('black',A),('white',B)]:
        (out/f'{label}-header.json').write_text(json.dumps(obj['header'],indent=2)+'\n',encoding='utf-8')
        (out/f'{label}-summary.json').write_text(json.dumps({'header':obj['header'],'exec':obj['exec'],'directory_count':obj['directory_count'],'fat_entries':len(obj['files']),'overlay9_entries':len(obj['overlays'])},indent=2)+'\n',encoding='utf-8')
        write_tsv(out/f'{label}-nitrofs.tsv',obj['files']); write_tsv(out/f'{label}-overlay9.tsv',obj['overlays'])
    deltas=[]; same=0
    for i,(x,y) in enumerate(zip(A['files'],B['files'])):
        eq=x['sha256']==y['sha256']; same+=int(eq)
        deltas.append({'file_id':i,'black_path':x['path'],'white_path':y['path'],'same_sha256':str(eq).lower(),
                       'black_size':x['size'],'white_size':y['size'],'black_sha256':x['sha256'],'white_sha256':y['sha256']})
    write_tsv(out/'black-white-nitrofs-delta.tsv',deltas)
    (out/'black-white-comparison.json').write_text(json.dumps({'counts':{'black_files':len(A['files']),'white_files':len(B['files']),'same_file_ids_sha256':same,'different_file_ids':len(deltas)-same,'black_overlays':len(A['overlays']),'white_overlays':len(B['overlays'])}},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main(sys.argv[1],sys.argv[2],sys.argv[3])
