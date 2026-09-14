#!/usr/bin/env python3
"""Fingerprint the first affine-animation core block in a local Pokémon Sapphire ROM."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path
ROM_BASE=0x08000000
AXPE=[
("BeginAffineAnim",0x194C,0x19C8),("ContinueAffineAnim",0x19C8,0x1A60),("AffineAnimDelay",0x1A60,0x1A94),("AffineAnimCmd_loop",0x1A94,0x1AC8),("BeginAffineAnimLoop",0x1AC8,0x1B04),("ContinueAffineAnimLoop",0x1B04,0x1B34),("JumpToTopOfAffineAnimLoop",0x1B34,0x1BA0),("AffineAnimCmd_jump",0x1BA0,0x1BEC),("AffineAnimCmd_end",0x1BEC,0x1C28),("AffineAnimCmd_frame",0x1C28,0x1C60),("CopyOamMatrix",0x1C60,0x1C80),("GetSpriteMatrixNum",0x1C80,0x1CA0),("SetSpriteOamFlipBits",0x1CA0,0x1D14),("AffineAnimStateRestartAnim",0x1D14,0x1D30),("AffineAnimStateStartAnim",0x1D30,0x1D58),("AffineAnimStateReset",0x1D58,0x1D80),("ApplyAffineAnimFrameAbsolute",0x1D80,0x1DA4),("DecrementAnimDelayCounter",0x1DA4,0x1DCC),("DecrementAffineAnimDelayCounter",0x1DCC,0x1DFC),]
FAMILY={"AXPJ":("jp",-0xE4),"AXPE":("axpe",0),"AXPD":("extended_european",0x134),"AXPF":("extended_european",0x134),"AXPI":("extended_european",0x134)}
TARGET_ID={("AXPJ",0):"JPN-AXPJ-v0",("AXPE",0):"USA-AXPE-v0",("AXPE",1):"EUR-AXPE-v1",("AXPE",2):"USA-EUR-AXPE-v2",("AXPD",1):"DEU-AXPD-v1",("AXPF",0):"FRA-AXPF-v0",("AXPF",1):"FRA-AXPF-v1",("AXPI",0):"ITA-AXPI-v0",("AXPI",1):"ITA-AXPI-v1"}
def analyze(path:Path):
 data=path.read_bytes(); code=data[0xAC:0xB0].decode('ascii',errors='replace'); version=data[0xBC]
 if code not in FAMILY: raise ValueError(f"unsupported game code: {code!r}")
 if (code,version) not in TARGET_ID: raise ValueError(f"unsupported Sapphire revision: {code} v{version}")
 family,delta=FAMILY[code]; funcs=[]
 for name,start,end in AXPE:
  start+=delta; end+=delta; chunk=data[start:end]
  funcs.append({"name":name,"file_offset":f"0x{start:08X}","runtime_address":f"0x{ROM_BASE+start:08X}","size":end-start,"sha256":hashlib.sha256(chunk).hexdigest()})
 return {"file":path.name,"target_id":TARGET_ID[(code,version)],"game_code":code,"software_version":version,"family":family,"functions":funcs}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('rom',type=Path); ap.add_argument('--format',choices=('json','csv'),default='json'); a=ap.parse_args(); r=analyze(a.rom)
 if a.format=='json': json.dump(r,sys.stdout,indent=2); print()
 else:
  w=csv.writer(sys.stdout); w.writerow(['file','target_id','game_code','software_version','family','function','file_offset','runtime_address','size','sha256'])
  for f in r['functions']: w.writerow([r['file'],r['target_id'],r['game_code'],r['software_version'],r['family'],f['name'],f['file_offset'],f['runtime_address'],f['size'],f['sha256']])
if __name__=='__main__': main()
