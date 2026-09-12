#!/usr/bin/env python3
import argparse,hashlib,json,struct
from pathlib import Path
SHA1='f94d4578956487c09fee20809a591e858017769e'
u16=lambda b,o=0:struct.unpack_from('<H',b,o)[0]
u32=lambda b,o=0:struct.unpack_from('<I',b,o)[0]
def fnt_paths(f):
 n=u16(f,6); ds={}
 for i in range(n):
  p=u32(f,i*8); fid=u16(f,i*8+4); a=[]
  while p<len(f):
   x=f[p];p+=1
   if not x:break
   d=x&128;l=x&127;s=f[p:p+l].decode();p+=l
   if d:q=u16(f,p);p+=2;a.append((1,s,q))
   else:a.append((0,s,fid));fid+=1
  ds[0xf000+i]=a
 out={}
 def w(di,pre=''):
  for d,n,x in ds.get(di,[]):
   q=f'{pre}/{n}' if pre else n
   w(x,q) if d else out.__setitem__(x,q)
 w(0xf000);return out
def narc(b):
 assert b[:4]==b'NARC';p=0x10;fs=u32(b,p+4);n=u16(b,p+8);e=[struct.unpack_from('<II',b,p+12+i*8) for i in range(n)];p+=fs;p+=u32(b,p+4);d=p+8;return[b[d+s:d+t]for s,t in e]
def main():
 a=argparse.ArgumentParser();a.add_argument('rom');x=a.parse_args();r=Path(x.rom).read_bytes();assert hashlib.sha1(r).hexdigest()==SHA1
 h=r[:0x4000];fo,fs=u32(h,0x40),u32(h,0x44);ao,asz=u32(h,0x48),u32(h,0x4c);paths=fnt_paths(r[fo:fo+fs]);fat=r[ao:ao+asz];files=[]
 for i in range(len(fat)//8):
  s,e=struct.unpack_from('<II',fat,i*8);files.append((paths.get(i,''),r[s:e]))
 D={p:b for p,b in files if p}
 narcs={p:narc(b) for p,b in D.items() if b[:4]==b'NARC'}
 z=narc(D['a/0/1/2'])[0];ent=narc(D['a/1/2/5']);scr=narc(D['a/0/5/7']);enc=narc(D['a/1/2/6'])
 def tail(b):
  fc,nc,wc,tc=b[4:8];p=8+fc*20+nc*36+wc*20+tc*22;return b[p:]
 zones=[]
 for i in range(427):
  q=z[i*48:(i+1)*48];zones.append((u16(q,6),u16(q,8),u16(q,0x14)&0x1fff,u16(q,0x16)))
 def ptr_ok(b):
  p=0
  while p+2<=len(b):
   if u16(b,p)==0xfd13:return True
   if p+4>len(b):return False
   t=p+4+u32(b,p)
   if not 0<=t<len(b):return False
   p+=4
  return False
 mainok=sum(ptr_ok(scr[2*i]) for i in range(427));mirror=sum(scr[2*i+1]==tail(ent[i]) for i in range(427));glob=[i for i in range(854,899)if not ptr_ok(scr[i])]
 out={'sha1':SHA1,'fat_entries':len(files),'named_files':sum(bool(p)for p,_ in files),'narc_archives':len(narcs),'narc_members':sum(map(len,narcs.values())),
 'overlays':u32(h,0x54)//32,'zones':427,'entities':len(ent),'scripts':len(scr),'encounters':len(enc),
 'assertions':{'main_script_formula':all(a==2*i for i,(a,b,c,d)in enumerate(zones)),'init_script_formula':all(b==2*i+1 for i,(a,b,c,d)in enumerate(zones)),
 'zone_id_identity':all(d==i for i,(a,b,c,d)in enumerate(zones)),'encounter_ids_exact':sorted(c for a,b,c,d in zones if c!=0x1fff)==list(range(112)),
 'main_pointer_tables_valid':mainok,'odd_entity_tail_mirrors':mirror,'global_nonpointer_members':glob}}
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
