#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, json, struct, zlib, argparse, shutil

BANK=0x4000; OLD=0x80000; NEW=0x100000
DATA_BANK=0x21; DATA_OFF=DATA_BANK*BANK
MAGIC=b'HGJX268\0'
SHA={0:'82c0eef40a5e2423699d9fd8ba15dfaa8b51d196',1:'4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b'}
T={'NORMAL':0,'FIGHTING':1,'FLYING':2,'POISON':3,'GROUND':4,'ROCK':5,'BUG':6,'GHOST':7,'STEEL':8,'FIRE':9,'WATER':10,'GRASS':11,'ELECTRIC':12,'PSYCHIC':13,'ICE':14,'DRAGON':15,'DARK':16}
EXTRA = {
 'TOGETIC': [('TOGEKISS',468,'NORMAL','FLYING')],
 'MAGNETON': [('MAGNEZONE',462,'ELECTRIC','STEEL')],
 'MAGMAR': [('MAGMORTAR',467,'FIRE','FIRE')],
 'ELECTABUZZ': [('ELECTIVIRE',466,'ELECTRIC','ELECTRIC')],
 'UMBREON': [('LEAFEON',470,'GRASS','GRASS'),('GLACEON',471,'ICE','ICE')],
 'GLIGAR': [('GLISCOR',472,'GROUND','FLYING')],
 'RHYDON': [('RHYPERIOR',464,'GROUND','ROCK')],
 'MURKROW': [('HONCHKROW',430,'DARK','FLYING')],
 'SNEASEL': [('WEAVILE',461,'DARK','ICE')],
 'MISDREAVUS': [('MISMAGIUS',429,'GHOST','GHOST')],
 'PORYGON2': [('PORYGON_Z',474,'NORMAL','NORMAL')],
}
GEN4_EVOS_NAT=[429,430,461,462,463,464,465,466,467,468,469,470,471,472,473,474]
GEN4_EVOS_NAT=[424]+GEN4_EVOS_NAT

def sha1(b): return hashlib.sha1(b).hexdigest()

def load_base_registry(p):
    with open(p,encoding='utf-8') as f:r=list(csv.DictReader(f))
    assert len(r)==256
    for x in r:
        x['johto_dex']=int(x['johto_dex']); x['national_dex']=int(x['national_dex']); x['generation_source']=int(x['generation_source'])
        x['legacy_green_internal_id']=int(x['legacy_green_internal_id']) if x['legacy_green_internal_id'] else None
    return r

def build_expanded(base):
    out=[]
    for x in base:
        y=dict(x); y['hgss_johto_dex']=y.pop('johto_dex'); y['source']='HGSS_JOHTO_256'; out.append(y)
        for ident,nd,t1,t2 in EXTRA.get(x['identifier'],[]):
            out.append({'hgss_johto_dex':None,'national_dex':nd,'identifier':ident,'type1':t1,'type2':t2,'legacy_green_internal_id':None,
                        'required_for_hgss_completion':'','generation_source':4,'base_stats_status':'pending_exact_hgss_personal_import',
                        'evolution_status':'pending_exact_hgss_evo_import','learnset_status':'pending_exact_hgss_wotbl_import','source':'DPPt_EVOLUTION_INSERT'})
    assert len(out)==268
    nats={x['national_dex'] for x in out if x['generation_source']==4}
    assert nats==set(GEN4_EVOS_NAT), (sorted(nats),GEN4_EVOS_NAT)
    for i,x in enumerate(out,1): x['expanded_johto_dex']=i
    return out

def assign_ids(rows):
    kanto={x['national_dex']:x['legacy_green_internal_id'] for x in rows if x['generation_source']==1}
    assert len(kanto)==151 and all(v is not None for v in kanto.values())
    real=set(kanto.values())
    reclaim=[i for i in range(1,191) if i not in real] + list(range(191,255))
    assert len(reclaim)==103
    usable=[i for i in reclaim if i<=0xFB]
    assert len(usable)==100
    gen2=sorted([x for x in rows if x['generation_source']==2], key=lambda x:x['national_dex'])
    assert len(gen2)==100
    gen2_ids={x['national_dex']:i for x,i in zip(gen2,usable)}
    gen4=sorted([x for x in rows if x['generation_source']==4], key=lambda x:x['national_dex'])
    assert len(gen4)==17
    gen4_ext={x['national_dex']:0x100+i for i,x in enumerate(gen4)}
    gen4_sel={x['national_dex']:i for i,x in enumerate(gen4)}
    for x in rows:
        nd=x['national_dex']
        if x['generation_source']==1:
            iid=kanto[nd]; x['internal_id']=iid; x['storage_species_byte']=iid; x['ext_selector']=None; x['id_class']='KANTO_LEGACY'
        elif x['generation_source']==2:
            iid=gen2_ids[nd]; x['internal_id']=iid; x['storage_species_byte']=iid; x['ext_selector']=None; x['id_class']='JOHTO_RECLAIMED_8BIT'
        else:
            iid=gen4_ext[nd]; x['internal_id']=iid; x['storage_species_byte']=0xFC; x['ext_selector']=gen4_sel[nd]; x['id_class']='GEN4_EXTENDED_ESCAPE_FC'
        x['internal_id_hex']=f'0x{x["internal_id"]:03X}' if x['internal_id']>255 else f'0x{x["internal_id"]:02X}'
        x['storage_species_byte_hex']=f'0x{x["storage_species_byte"]:02X}'
    return {'reclaimable_total':103,'gen2_used':100,'escape_id':0xFC,'reserved_future':[0xFD,0xFE],'no_mon':0x00,'terminator':0xFF,'gen4_extended':17}

def write_csv(rows,path):
    fields=['expanded_johto_dex','hgss_johto_dex','national_dex','identifier','generation_source','source','type1','type2','id_class','internal_id','internal_id_hex','storage_species_byte','storage_species_byte_hex','ext_selector','legacy_green_internal_id','base_stats_status','evolution_status','learnset_status']
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in rows:w.writerow({k:'' if x.get(k) is None else x.get(k,'') for k in fields})

def build_block(rows,plan):
    hs=0x80; rs=0x14; rec_off=hs; names_off=rec_off+len(rows)*rs
    names=bytearray(); nameoffs=[]
    for x in rows:
        nameoffs.append(len(names)); names+=x['identifier'].encode('ascii')+b'\0'
    rec=bytearray()
    for x,no in zip(rows,nameoffs):
        hg=x['hgss_johto_dex'] or 0
        flags=(1 if x['generation_source']==1 else 0)|(2 if x['generation_source']==2 else 0)|(4 if x['generation_source']==4 else 0)|(8 if x['source']=='DPPt_EVOLUTION_INSERT' else 0)
        ext=0xFF if x['ext_selector'] is None else x['ext_selector']
        rec += struct.pack('<HHHHBBBBBBHH', x['expanded_johto_dex'], hg, x['national_dex'], x['internal_id'], T[x['type1']], T[x['type2']], x['storage_species_byte'], ext, flags, 0, no, 0xFFFF)
    h=bytearray(hs); h[:8]=MAGIC
    struct.pack_into('<HHHHHHHH',h,8,3,hs,len(rows),17,rs,plan['reclaimable_total'],plan['gen2_used'],0xFC)
    struct.pack_into('<IIII',h,0x18,rec_off,names_off,DATA_OFF,0)
    h[0x28]=0x00; h[0x29]=0xFF; h[0x2A]=0xFD; h[0x2B]=0xFE
    h[0x30:0x50]=b'8BIT_LEGACY+FC_ESCAPE_EXT17'.ljust(32,b'\0')
    payload=h+rec+names
    struct.pack_into('<I',payload,0x24,zlib.crc32(payload)&0xffffffff)
    assert len(payload)<BANK
    return bytes(payload)

def fix_checksums(q):
    x=0
    for b in q[0x134:0x14d]:x=(x-b-1)&0xff
    q[0x14d]=x; q[0x14e]=q[0x14f]=0
    s=sum(q)&0xffff; q[0x14e]=s>>8; q[0x14f]=s&0xff

def ips(src,dst):
    o=bytearray(b'PATCH')
    def raw(a,d):
        for p in range(0,len(d),0xffff):
            c=d[p:p+0xffff]; o.extend((a+p).to_bytes(3,'big')); o.extend(len(c).to_bytes(2,'big')); o.extend(c)
    def rle(a,n,v):
        while n:
            q=min(n,0xffff); o.extend(a.to_bytes(3,'big')+b'\0\0'+q.to_bytes(2,'big')+bytes([v])); a+=q; n-=q
    i=0
    while i<len(src):
        if src[i]==dst[i]:i+=1;continue
        j=i+1
        while j<len(src) and src[j]!=dst[j] and j-i<0xffff:j+=1
        raw(i,dst[i:j]); i=j
    rle(len(src),len(dst)-len(src),0xff)
    i=len(src)
    while i<len(dst):
        if dst[i]==0xff:i+=1;continue
        j=i+1
        while j<len(dst) and dst[j]!=0xff and j-i<0xffff:j+=1
        raw(i,dst[i:j]); i=j
    return bytes(o+b'EOF')

def build_rom(basepath,outdir,block):
    b=basepath.read_bytes(); rev=b[0x14c]
    assert len(b)==OLD and rev in SHA and sha1(b)==SHA[rev]
    q=bytearray(b+b'\xff'*(NEW-OLD))
    q[0x147]=0x1B
    q[0x148]=0x05
    q[DATA_OFF:DATA_OFF+len(block)]=block
    fix_checksums(q)
    tag='rev0' if rev==0 else 'reva'
    rn=f'Pocket Monsters - Midori (Japan) - Expanded Johto Dex 268 Parameters ({tag}).gb'
    pn=f'green_expanded_johto268_parameters_{tag}.ips'
    (outdir/rn).write_bytes(q); p=ips(b,q); (outdir/pn).write_bytes(p)
    dif=[i for i,(a,c) in enumerate(zip(b,q[:OLD])) if a!=c]
    allowed={0x147,0x148,0x14d,0x14e,0x14f}
    assert set(dif)<=allowed
    return {'revision':rev,'input_sha1':sha1(b),'output':rn,'output_sha1':sha1(q),'ips':pn,'ips_sha1':sha1(p),'original_region_changed_offsets':[hex(x) for x in dif]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-registry',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); ap.add_argument('roms',nargs='+',type=Path)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    rows=build_expanded(load_base_registry(a.base_registry)); plan=assign_ids(rows)
    write_csv(rows,a.out/'expanded_johto268_registry.csv')
    block=build_block(rows,plan); (a.out/'expanded_johto268_parameter_block.bin').write_bytes(block)
    builds=[build_rom(p,a.out,block) for p in a.roms]
    manifest={'schema':'green-expanded-johto268-v3','count':268,'base_hgss_count':256,'dppt_inserted':12,'gen4_evolution_total':17,'id_plan':plan,'data_bank':'0x21','data_offset':'0x084000','parameter_block_sha1':sha1(block),'builds':builds}
    (a.out/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
