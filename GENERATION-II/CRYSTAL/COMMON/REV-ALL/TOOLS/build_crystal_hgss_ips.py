#!/usr/bin/env python3
"""Build Pokémon Crystal HGSS-static sprite IPS patches without requiring ROM images.

Inputs are converted LZ/palette assets plus analysis manifests generated from verified
Crystal ROMs. Main Pokémon #201 (Unown) is intentionally left untouched because
Crystal selects Unown graphics through a separate form pointer table.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from dataclasses import dataclass
from pathlib import Path

PICS_FIX = 0x36
PIC_TABLE = 0x48 * 0x4000
SKIP_SPECIES = {201}

OUT_LAYOUT = {
    "JP": ("JP", "REV-0"),
    "EN": ("EN", "REV-0"),
    "EN_REVA": ("EN", "REV-A"),
    "DE": ("DE", "REV-0"),
    "FR": ("FR", "REV-0"),
    "IT": ("IT", "REV-0"),
    "ES": ("ES", "REV-0"),
}

@dataclass
class Segment:
    bank: int
    start: int
    end: int
    cursor: int

    @property
    def remaining(self) -> int:
        return self.end - self.cursor

@dataclass
class Asset:
    species: int
    side: str
    path: Path
    data: bytes


def ihex(s: str) -> int:
    s=s.strip()
    return int(s, 16)


def load_pool(path: Path, pool_variant: str) -> list[Segment]:
    segs=[]
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["variant"] != pool_variant:
                continue
            start=ihex(r["start"]); end=ihex(r["end"]); bank=ihex(r["bank"])
            if not (start < end): raise ValueError(r)
            if start // 0x4000 != bank or (end-1) // 0x4000 != bank:
                raise ValueError(f"pool segment crosses bank: {r}")
            if end-start != int(r["bytes"]): raise ValueError(f"pool size mismatch: {r}")
            segs.append(Segment(bank,start,end,start))
    if not segs: raise ValueError(f"no pool segments for {pool_variant}")
    return sorted(segs, key=lambda x:(x.bank,x.start))


def load_offsets(path: Path) -> dict[str,dict]:
    out={}
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            out[r["variant"]] = {
                "sha1": r["sha1"],
                "palette_base": ihex(r["palette_base"]),
                "disable_extra_front_tiles": ihex(r["disable_extra_front_tiles"]),
                "disable_animate_frontpic": ihex(r["disable_animate_frontpic"]),
                "disable_hof_after_static": ihex(r["disable_hof_after_static"]),
            }
    missing=set(OUT_LAYOUT)-set(out)
    if missing: raise ValueError(f"missing patch offsets: {sorted(missing)}")
    return out


def find_assets(root: Path) -> list[Asset]:
    assets=[]
    for species in range(1,252):
        if species in SKIP_SPECIES:
            continue
        fronts=list((root/"LZ"/"FRONT").glob(f"{species:03d}.*.2bpp.lz"))
        backs=list((root/"LZ"/"BACK").glob(f"{species:03d}.6x6.2bpp.lz"))
        if len(fronts)!=1 or len(backs)!=1:
            raise FileNotFoundError(f"#{species:03d}: front={fronts}, back={backs}")
        for side,p in (("front",fronts[0]),("back",backs[0])):
            data=p.read_bytes()
            if not data or data[-1] != 0xFF:
                raise ValueError(f"invalid LZ terminator: {p}")
            assets.append(Asset(species,side,p,data))
    if len(assets)!=500:
        raise AssertionError(len(assets))
    return assets


def allocate(assets: list[Asset], pool: list[Segment]):
    # Best-fit decreasing gives deterministic compact placement while ensuring no
    # compressed sprite crosses a bank or an analyzed safe segment boundary.
    alloc={}
    for a in sorted(assets,key=lambda x:(-len(x.data),x.species,0 if x.side=="front" else 1)):
        choices=[s for s in pool if s.remaining >= len(a.data)]
        if not choices:
            need=sum(len(x.data) for x in assets)
            free=sum(s.end-s.start for s in pool)
            raise RuntimeError(f"allocation failed for #{a.species:03d} {a.side} {len(a.data)}B; total {need}/{free}")
        s=min(choices,key=lambda x:(s.remaining if False else x.remaining, x.bank, x.cursor))
        off=s.cursor; s.cursor += len(a.data)
        alloc[(a.species,a.side)] = (off,s.bank,a)
    return alloc


def pic_ptr(file_off: int, bank: int) -> bytes:
    if file_off // 0x4000 != bank:
        raise ValueError((file_off,bank))
    addr=0x4000 + (file_off % 0x4000)
    if not (0x4000 <= addr <= 0x7FFF): raise ValueError(addr)
    return bytes(((bank-PICS_FIX)&0xFF, addr&0xFF, (addr>>8)&0xFF))


def merge_records(records: list[tuple[int,bytes]]) -> list[tuple[int,bytes]]:
    # Last write wins for exact overlaps; then coalesce directly adjacent writes.
    byte_map={}
    for off,data in records:
        if off < 0 or off+len(data) > 0x1000000:
            raise ValueError(f"IPS offset out of range {off:#x}")
        for i,b in enumerate(data):
            key=off+i
            if key in byte_map and byte_map[key] != b:
                raise ValueError(f"conflicting patch byte at {key:#x}")
            byte_map[key]=b
    if not byte_map: return []
    out=[]; keys=sorted(byte_map); start=prev=keys[0]; buf=bytearray([byte_map[start]])
    for k in keys[1:]:
        if k==prev+1 and len(buf)<0xFFFF:
            buf.append(byte_map[k])
        else:
            out.append((start,bytes(buf))); start=k; buf=bytearray([byte_map[k]])
        prev=k
    out.append((start,bytes(buf)))
    return out


def ips(records: list[tuple[int,bytes]]) -> bytes:
    out=bytearray(b"PATCH")
    for off,data in merge_records(records):
        pos=0
        while pos<len(data):
            chunk=data[pos:pos+0xFFFF]
            o=off+pos
            out.extend(((o>>16)&255,(o>>8)&255,o&255))
            out.extend((len(chunk)>>8,len(chunk)&255))
            out.extend(chunk); pos+=len(chunk)
    out.extend(b"EOF")
    return bytes(out)


def palette_bytes(converted: Path, species: int) -> bytes:
    p=converted/"PALETTES"/"NORMAL_MIDDLE"/f"{species:03d}.gbcpal"
    d=p.read_bytes()
    if len(d)!=4: raise ValueError(f"palette must be 4 bytes: {p} ({len(d)})")
    return d


def build_for_variant(variant: str, converted: Path, assets: list[Asset], pool_file: Path, offsets: dict, outroot: Path):
    pool_variant="JP" if variant=="JP" else "INTL"
    pool=load_pool(pool_file,pool_variant)
    pool_capacity=sum(s.end-s.start for s in pool)
    alloc=allocate(assets,pool)
    rec=[]; packing=[]
    for species in range(1,252):
        if species in SKIP_SPECIES: continue
        for side in ("front","back"):
            off,bank,a=alloc[(species,side)]
            rec.append((off,a.data))
            ptr_off=PIC_TABLE+(species-1)*6+(0 if side=="front" else 3)
            rec.append((ptr_off,pic_ptr(off,bank)))
            packing.append({
                "species":f"{species:03d}","side":side,"offset":f"0x{off:06X}",
                "bank":f"0x{bank:02X}","cpu_addr":f"0x{0x4000+(off%0x4000):04X}",
                "bytes":len(a.data),"sha256":hashlib.sha256(a.data).hexdigest(),
                "asset":str(a.path),
            })
    o=offsets[variant]
    rec.extend([
        (o["disable_extra_front_tiles"],b"\x00\x00\x00"),
        (o["disable_animate_frontpic"],b"\xC9"),
        (o["disable_hof_after_static"],b"\xC9"),
    ])
    for species in range(1,252):
        if species in SKIP_SPECIES: continue
        rec.append((o["palette_base"]+species*8,palette_bytes(converted,species)))
    patch=ips(rec)
    lang,rev=OUT_LAYOUT[variant]
    dest=outroot/lang/rev/"SPRITES"/"HGSS_STATIC"
    dest.mkdir(parents=True,exist_ok=True)
    patch_name=f"Pokemon-Crystal-{variant}-HGSS-static-main-pokemon.ips"
    (dest/patch_name).write_bytes(patch)
    fields=["species","side","offset","bank","cpu_addr","bytes","sha256","asset"]
    with (dest/"packing.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t"); w.writeheader(); w.writerows(sorted(packing,key=lambda r:(int(r['species']),r['side'])))
    used=sum(len(a.data) for a in assets)
    meta={
        "variant":variant,"expected_source_sha1":o["sha1"],"pool_variant":pool_variant,
        "main_species_patched":250,"main_sprite_files_patched":500,
        "unown_201_skipped":True,"palette_species_patched":250,
        "pool_capacity":pool_capacity,"packed_lz_bytes":used,"pool_free_after_pack":pool_capacity-used,
        "ips_bytes":len(patch),"ips_sha256":hashlib.sha256(patch).hexdigest(),
        "notes":[
            "Static HGSS front/back sprites; original Crystal front animation paths disabled.",
            "Species #201 is intentionally deferred to the separate Unown A-Z form patch.",
            "Normal palettes are replaced; original Crystal shiny palettes are preserved.",
            "IPS does not rewrite the ROM global checksum; use the supplied apply/repair utility after patching when checksum normalization is desired."
        ]
    }
    (dest/"metadata.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return meta


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--converted-root",required=True)
    ap.add_argument("--pool",required=True)
    ap.add_argument("--offsets",required=True)
    ap.add_argument("--output-root",required=True)
    ns=ap.parse_args()
    converted=Path(ns.converted_root); pool=Path(ns.pool); offsets=load_offsets(Path(ns.offsets)); out=Path(ns.output_root)
    assets=find_assets(converted)
    summaries=[]
    for variant in OUT_LAYOUT:
        summaries.append(build_for_variant(variant,converted,assets,pool,offsets,out))
    print(json.dumps(summaries,indent=2))

if __name__=="__main__": main()
