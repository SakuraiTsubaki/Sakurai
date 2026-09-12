import os,struct,hashlib,json,sys
from collections import defaultdict

def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]

def parse_nds(path):
    with open(path,'rb') as f: data=f.read()
    fnt_off,fnt_size=u32(data,0x40),u32(data,0x44)
    fat_off,fat_size=u32(data,0x48),u32(data,0x4c)
    game_title=data[:12].rstrip(b'\0').decode('ascii','replace')
    game_code=data[12:16].decode('ascii','replace')
    maker=data[16:18].decode('ascii','replace')
    unit=data[0x12]
    device_capacity=data[0x14]
    rom_capacity=1 << (17+device_capacity)
    region=data[0x1d]
    rom_version=data[0x1e]
    arm9_off,arm9_entry,arm9_ram,arm9_size=map(lambda o:u32(data,o),(0x20,0x24,0x28,0x2c))
    arm7_off,arm7_entry,arm7_ram,arm7_size=map(lambda o:u32(data,o),(0x30,0x34,0x38,0x3c))
    overlay9_off,overlay9_size=u32(data,0x50),u32(data,0x54)
    overlay7_off,overlay7_size=u32(data,0x58),u32(data,0x5c)
    banner_off=u32(data,0x68)
    used_size=u32(data,0x80)
    nfiles=fat_size//8
    fat=[]
    for i in range(nfiles):
        s,e=struct.unpack_from('<II',data,fat_off+i*8); fat.append((s,e))
    root_sub=u32(data,fnt_off)
    n_dirs=u16(data,fnt_off+6)
    dirs={0xF000: {'suboff':root_sub,'first':u16(data,fnt_off+4),'parent':u16(data,fnt_off+6)}}
    for i in range(1,n_dirs):
        o=fnt_off+i*8
        dirs[0xF000+i]={'suboff':u32(data,o),'first':u16(data,o+4),'parent':u16(data,o+6)}
    files_by_id={}
    children_dirs=defaultdict(list)
    dir_entries={}
    for did,d in dirs.items():
        p=fnt_off+d['suboff']; fid=d['first']; entries=[]
        while True:
            if p>=fnt_off+fnt_size: break
            x=data[p]; p+=1
            if x==0: break
            isdir=bool(x&0x80); ln=x&0x7f
            name=data[p:p+ln].decode('ascii','replace'); p+=ln
            if isdir:
                cid=u16(data,p); p+=2
                entries.append(('dir',name,cid)); children_dirs[did].append((name,cid))
            else:
                entries.append(('file',name,fid)); fid+=1
        dir_entries[did]=entries
    def walk(did,prefix):
        for typ,name,x in dir_entries.get(did,[]):
            if typ=='file': files_by_id[x]=(prefix+name)
            else: walk(x,prefix+name+'/')
    walk(0xF000,'')
    files=[]
    for i,(s,e) in enumerate(fat):
        name=files_by_id.get(i,f'__file_{i:04d}')
        files.append({'id':i,'path':name,'start':s,'end':e,'size':e-s})
    return data, {
      'path':path,'title':game_title,'game_code':game_code,'maker':maker,'region_byte':region,'rom_version':rom_version,
      'file_size':len(data),'declared_capacity':rom_capacity,'used_size_header':used_size,
      'arm9':{'off':arm9_off,'size':arm9_size,'entry':arm9_entry,'ram':arm9_ram},
      'arm7':{'off':arm7_off,'size':arm7_size,'entry':arm7_entry,'ram':arm7_ram},
      'overlay9':{'off':overlay9_off,'size':overlay9_size},'overlay7':{'off':overlay7_off,'size':overlay7_size},
      'fnt':{'off':fnt_off,'size':fnt_size},'fat':{'off':fat_off,'size':fat_size,'count':nfiles},
      'banner_off':banner_off,'files':files,
    }

def parse_narc(buf):
    if len(buf)<0x20 or buf[:4]!=b'NARC': return None
    p=0x10
    sections=[]
    for _ in range(8):
        if p+8>len(buf): break
        magic=buf[p:p+4]; sz=u32(buf,p+4)
        if sz<8 or p+sz>len(buf): break
        sections.append((magic.decode('ascii','replace'),p,sz))
        p+=sz
    out={'sections':sections}
    for magic,p,sz in sections:
        if magic in ('BTAF','FATB'):
            cnt=u16(buf,p+8); out['members']=cnt
            spans=[]
            base=p+12
            for i in range(cnt):
                if base+i*8+8>p+sz: break
                a,b=struct.unpack_from('<II',buf,base+i*8); spans.append((a,b))
            out['member_spans']=spans
    return out

def sha(path,alg='sha256'):
    h=hashlib.new(alg)
    with open(path,'rb') as f:
      for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def audit(path):
    data,meta=parse_nds(path)
    narcs=[]
    for f in meta['files']:
        b=data[f['start']:f['end']]
        n=parse_narc(b)
        if n:
            narcs.append({'id':f['id'],'path':f['path'],'size':f['size'],'members':n.get('members'), 'sections':[(a,c) for a,_,c in n['sections']]})
    meta2={k:v for k,v in meta.items() if k!='files'}
    max_end=max((f['end'] for f in meta['files']),default=0)
    meta2.update({'sha256':sha(path),'nitro_file_count':len(meta['files']),'nitro_max_end':max_end,
                  'tail_free_bytes':len(data)-max_end,'narc_count':len(narcs),'narcs':narcs})
    return meta2

if __name__=='__main__':
    res=[]
    for p in sys.argv[1:]:
        print('AUDIT',p,file=sys.stderr)
        res.append(audit(p))
    print(json.dumps(res,ensure_ascii=False,indent=2))
