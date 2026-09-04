#!/usr/bin/env python3
"""Metadata-only census for two equal-size Game Boy ROM images.

Does not emit ROM payload bytes. Outputs hashes, header metadata, and aggregate
16 KiB bank-level byte-difference counts.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path

def digest(data: bytes) -> dict[str,str]:
    return {name: getattr(hashlib,name)(data).hexdigest() for name in ("md5","sha1","sha256")}

def parse_rom(path: Path) -> dict:
    b=path.read_bytes()
    chk=0
    for i in range(0x134,0x14D): chk=(chk-b[i]-1)&0xff
    g=(sum(b)-b[0x14E]-b[0x14F])&0xffff
    return {"filename":path.name,"size_bytes":len(b),"rom_banks_16k":len(b)//0x4000,"hashes":digest(b),"header":{
      "entry_point_hex":b[0x100:0x104].hex().upper(),"title":b[0x134:0x144].rstrip(b"\0").decode("ascii","replace"),
      "cgb_flag":b[0x143],"new_licensee_hex":b[0x144:0x146].hex().upper(),"sgb_flag":b[0x146],
      "cartridge_type":b[0x147],"rom_size_code":b[0x148],"ram_size_code":b[0x149],"destination_code":b[0x14A],
      "old_licensee_code":b[0x14B],"mask_rom_version":b[0x14C],"header_checksum":b[0x14D],"header_checksum_valid":chk==b[0x14D],
      "global_checksum":int.from_bytes(b[0x14E:0x150],"big"),"global_checksum_valid":g==int.from_bytes(b[0x14E:0x150],"big")}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("rev0",type=Path); ap.add_argument("reva",type=Path); ap.add_argument("--out",type=Path,default=Path("census-out")); a=ap.parse_args()
    b0=a.rev0.read_bytes(); ba=a.reva.read_bytes()
    if len(b0)!=len(ba): raise SystemExit("ROM sizes differ")
    a.out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for bank in range(len(b0)//0x4000):
      s,e=bank*0x4000,(bank+1)*0x4000; n=sum(x!=y for x,y in zip(b0[s:e],ba[s:e]))
      rows.append({"bank_hex":f"{bank:02X}","start_offset_hex":f"{s:06X}","end_offset_hex":f"{e-1:06X}","different_bytes":n,"difference_percent":round(n/0x4000*100,6),"rev_0_sha256":hashlib.sha256(b0[s:e]).hexdigest(),"rev_a_sha256":hashlib.sha256(ba[s:e]).hexdigest(),"identical":n==0})
    diffs=[i for i,(x,y) in enumerate(zip(b0,ba)) if x!=y]
    data={"rev_0":parse_rom(a.rev0),"rev_a":parse_rom(a.reva),"comparison":{"different_bytes":len(diffs),"different_percent":round(len(diffs)/len(b0)*100,6),"first_difference_offset_hex":f"{diffs[0]:06X}" if diffs else None,"last_difference_offset_hex":f"{diffs[-1]:06X}" if diffs else None,"identical_banks_hex":[r["bank_hex"] for r in rows if r["identical"]],"changed_banks_hex":[r["bank_hex"] for r in rows if not r["identical"]]}}
    (a.out/"rom_inventory.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    with (a.out/"rev_a_diff_by_bank.csv").open("w",newline="",encoding="utf-8") as f:
      w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
if __name__=="__main__": main()
