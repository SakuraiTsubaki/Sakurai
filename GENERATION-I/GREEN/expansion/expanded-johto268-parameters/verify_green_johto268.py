#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, json, struct, zlib
ROOT=Path(__file__).resolve().parent
BASES={
 'rev0':Path('/mnt/data/Pocket Monsters - Midori (Japan) (SGB Enhanced).gb'),
 'reva':Path('/mnt/data/Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb')}
OUTS={
 'rev0':ROOT/'Pocket Monsters - Midori (Japan) - Expanded Johto Dex 268 Parameters (rev0).gb',
 'reva':ROOT/'Pocket Monsters - Midori (Japan) - Expanded Johto Dex 268 Parameters (reva).gb'}
IPS={
 'rev0':ROOT/'green_expanded_johto268_parameters_rev0.ips',
 'reva':ROOT/'green_expanded_johto268_parameters_reva.ips'}
DATA_OFF=0x084000

def sha(b):return hashlib.sha1(b).hexdigest()
def header_ok(b):
 x=0
 for v in b[0x134:0x14d]:x=(x-v-1)&255
 return x==b[0x14d]
def global_ok(b):
 exp=(b[0x14e]<<8)|b[0x14f]
 t=bytearray(b); t[0x14e]=t[0x14f]=0
 return (sum(t)&0xffff)==exp
def apply_ips(src,p):
 assert p[:5]==b'PATCH'; out=bytearray(src); i=5
 while p[i:i+3]!=b'EOF':
  off=int.from_bytes(p[i:i+3],'big'); i+=3; n=int.from_bytes(p[i:i+2],'big'); i+=2
  if n:
   d=p[i:i+n]; i+=n
  else:
   r=int.from_bytes(p[i:i+2],'big'); i+=2; v=p[i]; i+=1; d=bytes([v])*r
  if len(out)<off+len(d):out.extend(b'\x00'*(off+len(d)-len(out)))
  out[off:off+len(d)]=d
 return bytes(out)
with open(ROOT/'expanded_johto268_registry.csv',encoding='utf-8') as f: rows=list(csv.DictReader(f))
assert len(rows)==268
assert [int(x['expanded_johto_dex']) for x in rows]==list(range(1,269))
assert len({int(x['national_dex']) for x in rows})==268
assert sum(x['id_class']=='KANTO_LEGACY' for x in rows)==151
assert sum(x['id_class']=='JOHTO_RECLAIMED_8BIT' for x in rows)==100
assert sum(x['id_class']=='GEN4_EXTENDED_ESCAPE_FC' for x in rows)==17
assert all(int(x['storage_species_byte'])==0xFC for x in rows if x['id_class']=='GEN4_EXTENDED_ESCAPE_FC')
assert sorted(int(x['ext_selector']) for x in rows if x['ext_selector']!='')==list(range(17))
normal=[int(x['storage_species_byte']) for x in rows if x['id_class']!='GEN4_EXTENDED_ESCAPE_FC']
assert len(normal)==251 and len(set(normal))==251
assert not ({0,0xfc,0xfd,0xfe,0xff}&set(normal))
results={}
for tag in BASES:
 b=BASES[tag].read_bytes(); q=OUTS[tag].read_bytes(); p=IPS[tag].read_bytes()
 assert len(b)==0x80000 and len(q)==0x100000
 assert q[0x147]==0x1b and q[0x148]==0x05 and header_ok(q) and global_ok(q)
 dif=[i for i,(a,c) in enumerate(zip(b,q[:len(b)])) if a!=c]
 assert set(dif)<={0x147,0x148,0x14d,0x14e,0x14f}
 assert apply_ips(b,p)==q
 assert q[DATA_OFF:DATA_OFF+8]==b'HGJX268\0'
 hs, count, ext = struct.unpack_from('<HHH',q,DATA_OFF+10)
 assert hs==0x80 and count==268 and ext==17
 results[tag]={'base_sha1':sha(b),'rom_sha1':sha(q),'ips_sha1':sha(p),'header_checksum_ok':True,'global_checksum_ok':True,'ips_roundtrip':True,'original_region_changed_offsets':[hex(x) for x in dif]}
(ROOT/'VERIFICATION.json').write_text(json.dumps({'registry_rows':268,'kanto_legacy':151,'johto_reclaimed_8bit':100,'gen4_extended':17,'escape_id':'0xFC','no_mon':'0x00','terminator':'0xFF','reserved':['0xFD','0xFE'],'builds':results},indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
