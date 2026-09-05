#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,struct,zlib,json
BANK=0x4000; OLD=0x80000; NEW=0x100000; DBANK=0x21; DOFF=DBANK*BANK
POFF=0x4279A; PCOUNT=190; MAGIC=b'HGJD256\0'
SHA={0:'82c0eef40a5e2423699d9fd8ba15dfaa8b51d196',1:'4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b'}
T={'NORMAL':0,'FIGHTING':1,'FLYING':2,'POISON':3,'GROUND':4,'ROCK':5,'BUG':6,'GHOST':7,'STEEL':8,'FIRE':9,'WATER':10,'GRASS':11,'ELECTRIC':12,'PSYCHIC':13,'ICE':14,'DRAGON':15,'DARK':16}
def sh(b): return hashlib.sha1(b).hexdigest()
def rows(path):
    r=list(csv.DictReader(path.open(encoding='utf-8'))); assert len(r)==256
    for i,x in enumerate(r,1):
        assert int(x['johto_dex'])==i
        x['national_dex']=int(x['national_dex']); x['legacy_green_internal_id']=int(x['legacy_green_internal_id'] or 0)
        x['required_for_hgss_completion']=x['required_for_hgss_completion'].lower()=='true'; x['generation_source']=int(x['generation_source'])
    assert len({x['national_dex'] for x in r})==256
    return r
def block(base,r):
    dex=base[POFF:POFF+PCOUNT]; assert len(dex)==PCOUNT and sum(bool(x) for x in dex)==151 and max(dex)==151
    ndslot={x['national_dex']:i for i,x in enumerate(r,1)}
    l2s=[ndslot.get(n,0) if n else 0 for n in dex]
    n2l={n:i+1 for i,n in enumerate(dex) if n}; s2l=[n2l.get(x['national_dex'],0) for x in r]
    assert sum(bool(x) for x in s2l)==151
    for x,l in zip(r,s2l): assert x['legacy_green_internal_id']==l
    names=bytearray(); no=[]
    for x in r: no.append(len(names)); names+=x['identifier'].encode('ascii')+b'\0'
    hs=0x60; rs=0x10; ro=hs; lo=ro+256*rs; so=lo+PCOUNT*2; noff=so+256
    rec=bytearray()
    for slot,x in enumerate(r,1):
        nd=x['national_dex']; flags=(1 if nd<=151 else 0)|(2 if 152<=nd<=251 else 0)|(4 if x['generation_source']==4 else 0)|(8 if x['required_for_hgss_completion'] else 16)
        rec+=struct.pack('<HHBBBBHHHH',slot,nd,T[x['type1']],T[x['type2']],x['legacy_green_internal_id'],flags,no[slot-1],0xffff,0xffff,0xffff)
    h=bytearray(hs); h[:8]=MAGIC
    struct.pack_into('<HHHHHHHH',h,8,1,hs,256,254,rs,PCOUNT,32,7)
    struct.pack_into('<IIIIII',h,0x18,ro,lo,so,noff,POFF,DOFF)
    struct.pack_into('<BBBB',h,0x30,2,2,2,17); h[0x34:0x44]=b'PREFAIRY_GEN4\0\0\0'
    p=bytearray(h)+rec+b''.join(struct.pack('<H',x) for x in l2s)+bytes(s2l)+names
    struct.pack_into('<I',p,0x44,zlib.crc32(p)&0xffffffff); return bytes(p)
def checks(rom):
    x=0
    for b in rom[0x134:0x14d]: x=(x-b-1)&255
    rom[0x14d]=x; rom[0x14e]=rom[0x14f]=0; s=sum(rom)&0xffff; rom[0x14e]=s>>8; rom[0x14f]=s&255
def ips(src,dst):
    o=bytearray(b'PATCH')
    def raw(a,d):
        for p in range(0,len(d),0xffff):
            c=d[p:p+0xffff]; o.extend((a+p).to_bytes(3,'big')); o.extend(len(c).to_bytes(2,'big')); o.extend(c)
    def rle(a,n,v):
        while n: q=min(n,0xffff); o.extend(a.to_bytes(3,'big')+b'\0\0'+q.to_bytes(2,'big')+bytes([v])); a+=q;n-=q
    i=0
    while i<len(src):
        if src[i]==dst[i]: i+=1; continue
        j=i+1
        while j<len(src) and src[j]!=dst[j] and j-i<0xffff: j+=1
        raw(i,dst[i:j]); i=j
    rle(OLD,NEW-OLD,0xff); i=OLD
    while i<NEW:
        if dst[i]==0xff: i+=1; continue
        j=i+1
        while j<NEW and dst[j]!=0xff and j-i<0xffff: j+=1
        raw(i,dst[i:j]); i=j
    return bytes(o+b'EOF')
def one(p,out,r):
    b=p.read_bytes(); assert len(b)==OLD; rev=b[0x14c]; assert rev in SHA and sh(b)==SHA[rev] and b[0x147]==3 and b[0x148]==4
    q=bytearray(b+b'\xff'*(NEW-OLD)); q[0x148]=5; bl=block(b,r); assert len(bl)<=BANK; q[DOFF:DOFF+len(bl)]=bl; checks(q)
    tag='rev0' if rev==0 else 'reva'; rn=f'Pocket Monsters - Midori (Japan) - HGSS Johto 256 Parameters ({tag}).gb'; pn=f'green_hgss_johto256_parameters_{tag}.ips'
    (out/rn).write_bytes(q); pa=ips(b,q); (out/pn).write_bytes(pa)
    return {'revision':rev,'input_sha1':sh(b),'output':rn,'output_sha1':sh(q),'ips':pn,'ips_sha1':sh(pa),'parameter_size':len(bl)}
def main():
    a=argparse.ArgumentParser(); a.add_argument('roms',nargs='+',type=Path); a.add_argument('-r','--registry',type=Path,default=Path(__file__).with_name('hgss_johto256_registry.csv')); a.add_argument('-o','--output-dir',type=Path,default=Path('.')); x=a.parse_args(); x.output_dir.mkdir(parents=True,exist_ok=True)
    print(json.dumps([one(p,x.output_dir,rows(x.registry)) for p in x.roms],indent=2))
if __name__=='__main__': main()
