#!/usr/bin/env python3
from pathlib import Path
import struct, hashlib, zlib, csv, json

U16=lambda b,o: struct.unpack_from('<H',b,o)[0]
U32=lambda b,o: struct.unpack_from('<I',b,o)[0]

def h(data, alg='sha256'):
    x=hashlib.new(alg); x.update(data); return x.hexdigest()

def parse_fnt(rom, off, size):
    fnt=rom[off:off+size]
    if len(fnt)<8: return {}
    dir_count=U16(fnt,6)
    entries=[]
    for i in range(dir_count):
        base=i*8
        if base+8>len(fnt): break
        entries.append((U32(fnt,base),U16(fnt,base+4),U16(fnt,base+6)))
    out={}; seen=set()
    def walk(dir_id,prefix):
        idx=dir_id-0xF000
        if idx<0 or idx>=len(entries) or dir_id in seen: return
        seen.add(dir_id)
        sub_off, first_id, _parent=entries[idx]
        pos=sub_off; fid=first_id
        while pos<len(fnt):
            n=fnt[pos]; pos+=1
            if n==0: break
            is_dir=bool(n&0x80); ln=n&0x7f
            name=fnt[pos:pos+ln].decode('ascii','replace'); pos+=ln
            if is_dir:
                if pos+2>len(fnt): break
                child=U16(fnt,pos); pos+=2
                walk(child, prefix+name+'/')
            else:
                out[fid]=prefix+name; fid+=1
    walk(0xF000,'')
    return out

def parse_overlay_table(rom, off, size, fat):
    rows=[]
    if not off or not size: return rows
    for pos in range(off, off+size, 32):
        if pos+32>len(rom): break
        overlay_id, ram_addr, ram_size, bss_size, sinit_start, sinit_end, file_id, reserved=struct.unpack_from('<8I',rom,pos)
        start=end=fsz=None; sha1=sha256=None
        if 0<=file_id<len(fat):
            start,end=fat[file_id]; data=rom[start:end]; fsz=end-start
            sha1=h(data,'sha1'); sha256=h(data,'sha256')
        rows.append(dict(overlay_id=overlay_id,ram_address=f'0x{ram_addr:08X}',ram_size=ram_size,bss_size=bss_size,
                         static_init_start=f'0x{sinit_start:08X}',static_init_end=f'0x{sinit_end:08X}',file_id=file_id,
                         flags_reserved=f'0x{reserved:08X}',rom_start=(f'0x{start:08X}' if start is not None else ''),
                         rom_end=(f'0x{end:08X}' if end is not None else ''),file_size=(fsz if fsz is not None else ''),sha1=sha1 or '',sha256=sha256 or ''))
    return rows

def narc_info(data):
    if len(data)<16 or data[:4]!=b'NARC': return None
    info={'magic':'NARC'}
    try:
        info['bom']=f'0x{U16(data,4):04X}'; info['version']=f'0x{U16(data,6):04X}'; info['file_size_field']=U32(data,8)
        hdr=U16(data,12); info['header_size']=hdr; info['section_count']=U16(data,14)
        info['subfile_count']=U16(data,hdr+8) if hdr+12<=len(data) and data[hdr:hdr+4] in (b'BTAF',b'FATB') else ''
    except Exception:
        info['subfile_count']=''
    return info

def parse_rom(path, outdir):
    rom=Path(path).read_bytes(); outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    title=rom[0:12].rstrip(b'\0').decode('ascii','replace'); game=rom[12:16].decode('ascii','replace'); maker=rom[16:18].decode('ascii','replace')
    unit=rom[0x12]; cap=rom[0x14]; hv=rom[0x1e]
    hdr={'source_file':Path(path).name,'size_bytes':len(rom),'crc32':f'{zlib.crc32(rom)&0xffffffff:08X}',
      'md5':h(rom,'md5'),'sha1':h(rom,'sha1'),'sha256':h(rom,'sha256'),'internal_title':title,'game_code':game,'maker_code':maker,
      'unit_code':f'0x{unit:02X}','device_capacity_code':f'0x{cap:02X}','header_version':hv,
      'arm9':{'rom_offset':U32(rom,0x20),'entry_address':U32(rom,0x24),'ram_address':U32(rom,0x28),'size':U32(rom,0x2c)},
      'arm7':{'rom_offset':U32(rom,0x30),'entry_address':U32(rom,0x34),'ram_address':U32(rom,0x38),'size':U32(rom,0x3c)},
      'fnt':{'offset':U32(rom,0x40),'size':U32(rom,0x44)},'fat':{'offset':U32(rom,0x48),'size':U32(rom,0x4c)},
      'overlay9':{'offset':U32(rom,0x50),'size':U32(rom,0x54)},'overlay7':{'offset':U32(rom,0x58),'size':U32(rom,0x5c)},
      'banner_offset':U32(rom,0x68),'used_rom_size_field':U32(rom,0x80),'header_size':U32(rom,0x84),
      'header_crc16_field':f'0x{U16(rom,0x15e):04X}','logo_crc16_field':f'0x{U16(rom,0x15c):04X}','dsi_extended_header_present':bool(unit&0x02)}
    hdr['twl_extended_words_0x180_0x200']=[{'offset':f'0x{o:03X}','u32':f'0x{U32(rom,o):08X}'} for o in range(0x180,0x200,4)]
    json.dump(hdr,open(outdir/'header.json','w'),indent=2)
    fat=[]
    for p in range(hdr['fat']['offset'],hdr['fat']['offset']+hdr['fat']['size'],8):
        if p+8>len(rom): break
        fat.append((U32(rom,p),U32(rom,p+4)))
    names=parse_fnt(rom,hdr['fnt']['offset'],hdr['fnt']['size']); fat_rows=[]; nitro_rows=[]; narc_rows=[]
    for fid,(s,e) in enumerate(fat):
        data=rom[s:e]; row={'file_id':fid,'rom_start':f'0x{s:08X}','rom_end':f'0x{e:08X}','size':e-s,'sha1':h(data,'sha1'),'sha256':h(data,'sha256')}; fat_rows.append(row)
        if fid in names:
            pth=names[fid]; nr={'file_id':fid,'path':pth,**{k:v for k,v in row.items() if k!='file_id'}}; nitro_rows.append(nr)
            ni=narc_info(data)
            if ni: narc_rows.append({'file_id':fid,'path':pth,'size':e-s,'sha1':row['sha1'],'sha256':row['sha256'],**ni})
    def wcsv(name,rows):
        if not rows:return
        with open(outdir/name,'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    wcsv('fat.csv',fat_rows); wcsv('nitrofs.csv',nitro_rows); wcsv('narc.csv',narc_rows)
    ov9=parse_overlay_table(rom,hdr['overlay9']['offset'],hdr['overlay9']['size'],fat); ov7=parse_overlay_table(rom,hdr['overlay7']['offset'],hdr['overlay7']['size'],fat)
    wcsv('overlay9.csv',ov9); wcsv('overlay7.csv',ov7)
    summary={'fat_entries':len(fat),'named_nitrofs_files':len(nitro_rows),'overlay9_entries':len(ov9),'overlay7_entries':len(ov7),'narc_files':len(narc_rows),'fnt_named_file_ids_minmax':[min(names) if names else None,max(names) if names else None]}
    json.dump(summary,open(outdir/'summary.json','w'),indent=2)
    return {'header':hdr,'fat':fat_rows,'nitro':nitro_rows,'ov9':ov9,'ov7':ov7,'narc':narc_rows,'summary':summary}

def compare(a,b,outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    def by(rows,key):return {str(r[key]):r for r in rows}
    mappings={'nitrofs':'nitro','overlay9':'ov9','fat':'fat','narc':'narc'}; comparisons={}
    for label,key in [('nitrofs','path'),('overlay9','overlay_id'),('fat','file_id'),('narc','path')]:
        ar=by(a[mappings[label]],key); br=by(b[mappings[label]],key); rows=[]
        for k in sorted(set(ar)|set(br),key=lambda x:(int(x) if x.isdigit() else x)):
            x,y=ar.get(k),br.get(k); status='only-black' if y is None else 'only-white' if x is None else 'same' if x['sha256']==y['sha256'] else 'different'
            rows.append({'identity':k,'status':status,'black_size':x.get('size',x.get('file_size','')) if x else '','white_size':y.get('size',y.get('file_size','')) if y else '','black_sha256':x['sha256'] if x else '','white_sha256':y['sha256'] if y else ''})
        comparisons[label]=rows
        with open(outdir/f'{label}_compare.csv','w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    summ={label:{s:sum(1 for r in rows if r['status']==s) for s in ['same','different','only-black','only-white']} for label,rows in comparisons.items()}
    json.dump(summ,open(outdir/'summary.json','w'),indent=2); return summ

if __name__=='__main__':
    raise SystemExit('Import parse_rom/compare from this module and provide local ROM paths explicitly; ROM binaries are never repository inputs.')
