#!/usr/bin/env python3
from pathlib import Path
import json, struct, zlib, hashlib
ROOT=Path('/mnt/data/silver_hgss_johto256_stage1')
BANK=0x7e*0x4000
MAGIC=b'SJ256P1\0'
report=json.loads((ROOT/'build_report.json').read_text())
expected_positions={102:(252,469),124:(253,424),181:(254,463),183:(255,465),197:(256,473),256:(251,251)}
for ent in report['roms']:
 p=ROOT/'roms'/ent['output_file']; d=p.read_bytes(); assert len(d)==0x200000
 q=d[BANK:BANK+0x4000]; assert q[:8]==MAGIC
 version,hdr,nsp,njohto,recsz,flags,nat_off,order_off,base_off,evo_off=struct.unpack_from('<HHHHHHHHHH',q,8)
 move_off,end_off,crc=struct.unpack_from('<HHI',q,28)
 assert zlib.crc32(q[64:end_off]) & 0xffffffff == crc
 nat=struct.unpack_from('<256H',q,nat_off); order=struct.unpack_from('<256H',q,order_off)
 assert sorted(order)==list(range(1,257))
 for pos,(sid,nno) in expected_positions.items(): assert order[pos-1]==sid and nat[sid-1]==nno
 for sid in range(252,257):
  rec=q[base_off+(sid-1)*recsz:base_off+sid*recsz]
  assert struct.unpack_from('<H',rec,0)[0]==sid
 assert all(b==0 for b in q[end_off:])
 x=0
 for i in range(0x134,0x14d): x=(x-d[i]-1)&0xff
 assert x==d[0x14d]
 print('OK',p.name,'payload',end_off,'crc',f'{crc:08x}','sha256',hashlib.sha256(d).hexdigest())
