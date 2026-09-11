#!/usr/bin/env python3
"""Build a Gen III-ready battle-sprite pack from the 64x64 Gen IV masters."""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import defaultdict,deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from PIL import Image

SOURCE_ROOTS={
 "DP":Path("GENERATION-IV/DIAMOND-PEARL/USA/REV-UNKNOWN/SPRITES/BATTLE_MASTER_V1/PREVIEWS"),
 "PT":Path("GENERATION-IV/PLATINUM/KOREA/REV-0/SPRITES/BATTLE_MASTER_V1/PREVIEWS"),
 "HGSS":Path("GENERATION-IV/HEARTGOLD-SOULSILVER/KOREA/REV-0/SPRITES/BATTLE_MASTER_V1/PREVIEWS"),
}

def sha256(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def align4(b:bytearray)->None:
 while len(b)&3:b.append(0)
def rgb8_to_bgr555(r:int,g:int,b:int)->int:
 return ((r*31+127)//255)|(((g*31+127)//255)<<5)|(((b*31+127)//255)<<10)

def rgba_to_4bpp_and_palette(path:Path)->tuple[bytes,bytes,int]:
 im=Image.open(path).convert("RGBA")
 if im.size!=(64,64):raise RuntimeError(f"expected 64x64 PNG, got {im.size}: {path}")
 colors=[]; cmap={}; idx=[0]*4096
 for i,(r,g,b,a) in enumerate(im.getdata()):
  if a==0:continue
  c=(r,g,b); n=cmap.get(c)
  if n is None:
   if len(colors)>=15:raise RuntimeError(f">15 opaque colors: {path}")
   colors.append(c); n=len(colors); cmap[c]=n
  idx[i]=n
 raw=bytearray()
 for ty in range(8):
  for tx in range(8):
   for y in range(8):
    base=(ty*8+y)*64+tx*8
    for x in range(0,8,2):raw.append(idx[base+x]|(idx[base+x+1]<<4))
 if len(raw)!=2048:raise AssertionError(len(raw))
 pal=bytearray(32)
 for slot,(r,g,b) in enumerate(colors,1):
  v=rgb8_to_bgr555(r,g,b); pal[slot*2]=v&255; pal[slot*2+1]=v>>8
 return bytes(raw),bytes(pal),len(colors)+1

def gba_lz77(data:bytes)->bytes:
 n=len(data); out=bytearray((0x10,n&255,(n>>8)&255,(n>>16)&255)); pos=0
 chains:dict[bytes,deque[int]]=defaultdict(deque)
 def add(p:int):
  if p+2>=n:return
  q=chains[data[p:p+3]];q.append(p)
  while len(q)>128:q.popleft()
 while pos<n:
  flag_at=len(out);out.append(0);flags=0;payload=bytearray()
  for bit in range(8):
   if pos>=n:break
   best_len=0;best_pos=-1
   if pos+2<n:
    q=chains.get(data[pos:pos+3]);checked=0
    if q:
     for cand in reversed(q):
      disp=pos-cand-1
      if disp>0xFFF:break
      checked+=1;length=3;limit=min(18,n-pos)
      while length<limit and data[cand+length]==data[pos+length]:length+=1
      if length>best_len:
       best_len=length;best_pos=cand
       if length==18:break
      if checked>=64:break
   if best_len>=3:
    flags|=1<<(7-bit);disp=pos-best_pos-1;token=((best_len-3)<<12)|disp
    payload.extend(((token>>8)&255,token&255));old=pos;pos+=best_len
    for p in range(old,pos):add(p)
   else:
    payload.append(data[pos]);add(pos);pos+=1
  out[flag_at]=flags;out.extend(payload)
 align4(out);return bytes(out)

def gba_lz77_decompress(blob:bytes)->bytes:
 if not blob or blob[0]!=0x10:raise ValueError("not type-0x10")
 target=blob[1]|(blob[2]<<8)|(blob[3]<<16);out=bytearray();p=4
 while len(out)<target:
  flags=blob[p];p+=1
  for bit in range(8):
   if len(out)>=target:break
   if flags&(1<<(7-bit)):
    a,b=blob[p],blob[p+1];p+=2;length=(a>>4)+3;disp=((a&15)<<8)|b;src=len(out)-disp-1
    for _ in range(length):out.append(out[src]);src+=1
   else:out.append(blob[p]);p+=1
 return bytes(out[:target])

@dataclass(frozen=True)
class GfxRecord:id:int;sha256:str;raw_size:int;offset:int;compressed_size:int
@dataclass(frozen=True)
class PalRecord:id:int;sha256:str;offset:int;size:int

def source_pngs(root:Path)->Iterable[Path]:
 for p in sorted(root.rglob("*.png")):
  if "GALLERIES" not in p.parts:yield p

def main()->None:
 ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,default=Path("."));ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
 repo=args.repo.resolve();out=args.out if args.out.is_absolute() else repo/args.out;out.mkdir(parents=True,exist_ok=True)
 logical=[];gfx_by_hash={};pal_by_hash={};gfx_raws=[];pal_raws=[];max_pal=0;source_counts={}
 for game,relroot in SOURCE_ROOTS.items():
  root=repo/relroot
  if not root.exists():raise FileNotFoundError(root)
  count=0
  for png in source_pngs(root):
   raw,pal,pentries=rgba_to_4bpp_and_palette(png);max_pal=max(max_pal,pentries);gsha=sha256(raw);psha=sha256(pal)
   if gsha not in gfx_by_hash:gfx_by_hash[gsha]=len(gfx_raws);gfx_raws.append(raw)
   if psha not in pal_by_hash:pal_by_hash[psha]=len(pal_raws);pal_raws.append(pal)
   logical.append({"logical_id":len(logical),"source_game":game,"source_path":png.relative_to(repo).as_posix(),"source_key":png.relative_to(root).as_posix(),"gfx_id":gfx_by_hash[gsha],"palette_id":pal_by_hash[psha],"gfx_sha256":gsha,"palette_sha256":psha,"palette_entries":pentries});count+=1
  source_counts[game]=count
 gfxpack=bytearray();gfxrecords=[];total_raw=0
 for i,raw in enumerate(gfx_raws):
  align4(gfxpack);off=len(gfxpack);comp=gba_lz77(raw)
  if gba_lz77_decompress(comp)!=raw:raise RuntimeError(f"LZ77 round-trip failed: {i}")
  gfxpack.extend(comp);gfxrecords.append(GfxRecord(i,sha256(raw),len(raw),off,len(comp)));total_raw+=len(raw)
 palpack=bytearray();palrecords=[]
 for i,pal in enumerate(pal_raws):
  off=len(palpack);palpack.extend(pal);palrecords.append(PalRecord(i,sha256(pal),off,len(pal)))
 (out/"gen4_battle_gfx_lz.pack").write_bytes(gfxpack);(out/"gen4_battle_palettes.gbapal").write_bytes(palpack)
 with (out/"logical_index.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=list(logical[0]));w.writeheader();w.writerows(logical)
 with (out/"gfx_index.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["id","sha256","raw_size","offset","compressed_size"]);w.writeheader();[w.writerow(r.__dict__) for r in gfxrecords]
 with (out/"palette_index.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["id","sha256","offset","size"]);w.writeheader();[w.writerow(r.__dict__) for r in palrecords]
 summary={"format":"GEN4_BATTLE_TO_GEN3_PACK_V1","source_counts":source_counts,"logical_records":len(logical),"unique_4bpp_graphics":len(gfxrecords),"unique_palettes":len(palrecords),"raw_graphics_bytes_before_dedup":len(logical)*2048,"unique_raw_graphics_bytes":total_raw,"gfx_lz_pack_bytes":len(gfxpack),"palette_pack_bytes":len(palpack),"gfx_compression_ratio_vs_unique_raw":len(gfxpack)/total_raw if total_raw else 0,"max_palette_entries_including_transparent":max_pal,"canvas":"64x64","pixel_format":"GBA OBJ 4bpp tiled","palette_format":"16-color little-endian BGR555; slot 0 transparent","compression":"GBA BIOS LZ77 type 0x10; each unique 2048-byte frame independently compressed and 4-byte aligned","variant_policy":"DP, Platinum and HGSS remain separate logical records; no version difference is discarded","frame_policy":"all master frames retained; f0 is vanilla-Gen-III-compatible default, later frames are reserved for the extended animation table"}
 (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 (out/"README.md").write_text("# Generation IV battle sprites -> Generation III pack v1\n\nGenerated from the existing Tsubaki DP / Platinum / HGSS 64x64 battle masters. Every source-game/gender/side/normal-shiny/form/frame logical variant is retained while identical GBA-ready graphics and palettes are deduplicated internally. Original Gen III graphics are not overwritten by this build step.\n\n`gen4_battle_gfx_lz.pack` contains concatenated GBA BIOS LZ77 type-0x10 64x64 4bpp frames. `gen4_battle_palettes.gbapal` contains concatenated unique 32-byte BGR555 palettes. CSV indices preserve provenance and offsets. ROM patching is a separate local step against read-only uploaded Gen III originals.\n",encoding="utf-8")
 print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
