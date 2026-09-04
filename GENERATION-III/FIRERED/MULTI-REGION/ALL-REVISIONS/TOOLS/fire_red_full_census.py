#!/usr/bin/env python3
"""
FireRed multi-region full static census.

Input: a directory containing the FireRed .gba files.
Output: only non-ROM analysis artifacts. The ROM binaries are never copied,
embedded, or emitted.

Census layers:
- GBA header / hashes / build & SDK ASCII signatures
- 4 KiB block statistics and 64 KiB bank statistics
- 00/FF runs
- aligned pointer-like 32-bit words (ROM/EWRAM/IWRAM/etc.)
- validated aligned GBA LZ77 streams
- 64 KiB bank identity matrix
- revision-pair per-bank differences
- fixed-width species/move names and item-table anchors
"""
from __future__ import annotations
import argparse, collections, csv, gzip, hashlib, itertools, json, math, re, zlib
from pathlib import Path
import numpy as np
import pandas as pd

BANK = 0x10000
BLOCK = 0x1000

def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    c = collections.Counter(data)
    n = len(data)
    return -sum((v/n) * math.log2(v/n) for v in c.values())

def ascii_strings(data: bytes, minlen: int = 6):
    start = None
    for i, b in enumerate(data):
        if 0x20 <= b <= 0x7E:
            if start is None:
                start = i
        else:
            if start is not None and i - start >= minlen:
                yield start, data[start:i].decode("ascii", "replace")
            start = None
    if start is not None and len(data) - start >= minlen:
        yield start, data[start:].decode("ascii", "replace")

def fill_runs(data: bytes, min_len=0x100):
    i = 0
    n = len(data)
    while i < n:
        b = data[i]
        if b in (0x00, 0xFF):
            j = i + 1
            while j < n and data[j] == b:
                j += 1
            if j - i >= min_len:
                yield i, j - 1, b, j - i
            i = j
        else:
            i += 1

def parse_lz77(data: bytes, off: int, max_out=0x400000):
    n = len(data)
    if off + 4 > n or data[off] != 0x10:
        return None
    out_len = data[off+1] | (data[off+2] << 8) | (data[off+3] << 16)
    if not (0 < out_len <= max_out):
        return None
    src = off + 4
    produced = 0
    while produced < out_len:
        if src >= n:
            return None
        flags = data[src]
        src += 1
        for bit in range(7, -1, -1):
            if produced >= out_len:
                break
            if flags & (1 << bit):
                if src + 2 > n:
                    return None
                b1, b2 = data[src], data[src+1]
                src += 2
                length = (b1 >> 4) + 3
                disp = (((b1 & 0xF) << 8) | b2) + 1
                if disp > produced:
                    return None
                produced += length
                if produced > out_len + 18:
                    return None
            else:
                if src >= n:
                    return None
                src += 1
                produced += 1
    return src - off, out_len

def scan_lz77(data: bytes):
    start = 0
    out = []
    while True:
        off = data.find(b"\x10", start)
        if off < 0:
            break
        start = off + 1
        if off & 3:
            continue
        parsed = parse_lz77(data, off)
        if parsed:
            comp, unc = parsed
            if unc >= 32 and comp < unc:
                out.append((off, comp, unc))
    return out

def pointer_summary(data: bytes):
    u = np.frombuffer(data[:len(data)//4*4], dtype="<u4")
    ranges = {
        "ROM": (0x08000000, 0x09000000),
        "EWRAM": (0x02000000, 0x02040000),
        "IWRAM": (0x03000000, 0x03008000),
        "IO": (0x04000000, 0x04000400),
        "PAL": (0x05000000, 0x05000400),
        "VRAM": (0x06000000, 0x06018000),
        "OAM": (0x07000000, 0x07000400),
        "SRAM": (0x0E000000, 0x0E010000),
    }
    counts = {}
    for key, (lo, hi) in ranges.items():
        counts[key] = int(((u >= lo) & (u < hi)).sum())
    mask = (u >= 0x08000000) & (u < 0x09000000)
    return counts, np.nonzero(mask)[0] * 4, (u[mask] - 0x08000000).astype(np.uint32)

def sha256_banks(data: bytes):
    return [hashlib.sha256(data[i:i+BANK]).hexdigest()
            for i in range(0, len(data), BANK)]

# Known table anchors discovered structurally in the 8-ROM project set.
# They are intentionally data-only addresses; no ROM content is embedded.
TABLES = {
    "Pocket Monsters - Fire Red (Japan) (Rev 1).gba": (0x1FF4D0, 6, 8, 0x39BEB8, 40, 10),
    "Pocket Monsters - Fire Red (Japan).gba":         (0x203CB8, 6, 8, 0x3A06F8, 40, 10),
    "Pokemon - Edicion Rojo Fuego (Spain).gba":      (0x24164C,11,13,0x3D4F50,44,14),
    "Pokemon - Feuerrote Edition (Germany).gba":     (0x245DB0,11,13,0x3DA518,44,14),
    "Pokemon - Fire Red Version (USA).gba":           (0x245EE0,11,13,0x3DB028,44,14),
    "Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba": (0x245F50,11,13,0x3DB098,44,14),
    "Pokemon - Version Rouge Feu (France).gba":       (0x2402EC,11,13,0x3D3324,44,14),
    "Pokemon - Versione Rosso Fuoco (Italy).gba":     (0x23EF84,11,13,0x3D1EE8,44,14),
}

def western_map():
    m = {0x00:" "}
    for i,ch in enumerate("0123456789", 0xA1): m[i]=ch
    for i,ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0xBB): m[i]=ch
    for i,ch in enumerate("abcdefghijklmnopqrstuvwxyz", 0xD5): m[i]=ch
    m.update({
        0x01:"À",0x02:"Á",0x03:"Â",0x04:"Ç",0x05:"È",0x06:"É",0x07:"Ê",0x08:"Ë",0x09:"Ì",
        0x0B:"Î",0x0C:"Ï",0x0D:"Ò",0x0E:"Ó",0x0F:"Ô",0x10:"Œ",0x11:"Ù",0x12:"Ú",0x13:"Û",0x14:"Ñ",0x15:"ß",
        0x16:"à",0x17:"á",0x19:"ç",0x1A:"è",0x1B:"é",0x1C:"ê",0x1D:"ë",0x1E:"ì",0x20:"î",0x21:"ï",0x22:"ò",0x23:"ó",0x24:"ô",0x25:"œ",0x26:"ù",0x27:"ú",0x28:"û",0x29:"ñ",
        0x2A:"º",0x2B:"ª",0x2D:"&",0x2E:"+",0x35:"=",0x36:";",0x51:"¿",0x52:"¡",0x5A:"Í",0x5B:"%",0x5C:"(",0x5D:")",0x68:"â",0x6F:"í",
        0x79:"↑",0x7A:"↓",0x7B:"←",0x7C:"→",0x85:"<",0x86:">",
        0xAB:"!",0xAC:"?",0xAD:".",0xAE:"-",0xAF:"·",0xB0:"…",0xB1:"“",0xB2:"”",0xB3:"‘",0xB4:"’",0xB5:"♂",0xB6:"♀",0xB7:"¥",0xB8:",",0xB9:"×",0xBA:"/",
        0xEF:"▶",0xF0:":",0xF1:"Ä",0xF2:"Ö",0xF3:"Ü",0xF4:"ä",0xF5:"ö",0xF6:"ü"
    })
    return m

def japanese_map():
    m={0x00:"　"}
    hira="あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっ"
    kata="アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ"
    for i,ch in enumerate(hira,1): m[i]=ch
    for i,ch in enumerate(kata,0x51): m[i]=ch
    for i,ch in enumerate("0123456789",0xA1): m[i]=ch
    for i,ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ",0xBB): m[i]=ch
    for i,ch in enumerate("abcdefghijklmnopqrstuvwxyz",0xD5): m[i]=ch
    m.update({0xAB:"！",0xAC:"？",0xAD:"。",0xAE:"ー",0xB0:"‥"})
    return m

def decode_fixed(data: bytes, cmap):
    out=[]
    for b in data:
        if b == 0xFF:
            break
        out.append(cmap.get(b, f"<{b:02X}>"))
    return "".join(out).rstrip(" \u3000")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("rom_dir")
    ap.add_argument("-o","--out",default="fire_red_full_census")
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    paths=sorted(Path(args.rom_dir).glob("*.gba"))
    roms={p.name:p.read_bytes() for p in paths}
    lz={n:scan_lz77(d) for n,d in roms.items()}
    ptr={n:pointer_summary(d) for n,d in roms.items()}
    banks={n:sha256_banks(d) for n,d in roms.items()}

    rows4=[]; rows64=[]
    for name,d in roms.items():
        lz4=collections.Counter(o//BLOCK for o,_,_ in lz[name])
        lz64=collections.Counter(o//BANK for o,_,_ in lz[name])
        for size, target in ((BLOCK, rows4),(BANK,rows64)):
            for bi in range(len(d)//size):
                st=bi*size; b=d[st:st+size]
                a=np.frombuffer(b,dtype=np.uint8)
                u=np.frombuffer(b,dtype="<u4")
                h=np.frombuffer(b,dtype="<u2")
                target.append({
                    "rom":name,"index":bi,"start":f"0x{st:08X}","end":f"0x{st+size-1:08X}",
                    "entropy":round(entropy(b),6),
                    "ff_pct":round(float((a==0xFF).sum())/len(b)*100,6),
                    "zero_pct":round(float((a==0).sum())/len(b)*100,6),
                    "rom_ptr_words":int(((u>=0x08000000)&(u<0x09000000)).sum()),
                    "ewram_ptr_words":int(((u>=0x02000000)&(u<0x02040000)).sum()),
                    "iwram_ptr_words":int(((u>=0x03000000)&(u<0x03008000)).sum()),
                    "thumb_push_lr_halfwords":int(((h&0xFF00)==0xB500).sum()),
                    "thumb_bx_lr_halfwords":int((h==0x4770).sum()),
                    "thumb_pop_pc_halfwords":int(((h&0xFF00)==0xBD00).sum()),
                    "lz77_objects":(lz4 if size==BLOCK else lz64).get(bi,0),
                })
    pd.DataFrame(rows4).to_csv(out/"whole_rom_block_census_4k.csv.gz",index=False,compression="gzip")
    pd.DataFrame(rows64).to_csv(out/"bank_census_64k.csv",index=False)

    lzrows=[]
    for name,xs in lz.items():
        for o,c,u in xs:
            lzrows.append({"rom":name,"offset":f"0x{o:08X}","compressed_size":c,
                           "uncompressed_size":u,"ratio":round(c/u,6),"bank_64k":o//BANK})
    pd.DataFrame(lzrows).to_csv(out/"lz77_objects.csv.gz",index=False,compression="gzip")

    pad=[]; ps=[]
    for name,d in roms.items():
        counts,src,targets=ptr[name]
        ps.append({"rom":name,**counts})
        for s,e,b,l in fill_runs(d):
            refs=int(((targets>=s)&(targets<=e)).sum())
            pad.append({"rom":name,"start":f"0x{s:08X}","end":f"0x{e:08X}",
                        "length":l,"fill":f"{b:02X}","aligned_pointerlike_rom_targets":refs})
    pd.DataFrame(ps).to_csv(out/"pointer_summary.csv",index=False)
    pd.DataFrame(pad).to_csv(out/"padding_runs_ge_0x100.csv",index=False)

    pbank=[]
    for name,(counts,src,targets) in ptr.items():
        c=collections.Counter(int(v)//BANK for v in targets if int(v)<0x1000000)
        for b in range(256):
            pbank.append({"rom":name,"target_bank":b,"target_start":f"0x{b*BANK:08X}",
                          "pointerlike_refs":c.get(b,0)})
    pd.DataFrame(pbank).to_csv(out/"rom_pointer_target_banks.csv",index=False)

    ident=[]
    names=list(roms)
    for b in range(256):
        hs={n:banks[n][b] for n in names}
        ident.append({"bank":b,"start":f"0x{b*BANK:08X}",
                      "distinct_hashes":len(set(hs.values())),
                      "all_8_identical":len(set(hs.values()))==1,
                      **{n:hs[n][:16] for n in names}})
    pd.DataFrame(ident).to_csv(out/"bank_identity_matrix.csv",index=False)
    pairs=[]
    for a,b in itertools.combinations(names,2):
        eq=[i for i,(x,y) in enumerate(zip(banks[a],banks[b])) if x==y]
        pairs.append({"a":a,"b":b,"equal_64k_banks":len(eq),
                      "different_64k_banks":256-len(eq),
                      "equal_bank_indices":" ".join(f"{i:02X}" for i in eq)})
    pd.DataFrame(pairs).to_csv(out/"pairwise_bank_identity.csv",index=False)

    astr=[]; build=[]
    for name,d in roms.items():
        strings=list(ascii_strings(d,6))
        for off,s in strings:
            astr.append({"rom":name,"offset":f"0x{off:08X}","length":len(s),"text":s})
        stamps=[(o,s) for o,s in strings if re.fullmatch(r"20\d\d \d\d \d\d \d\d:\d\d",s)]
        row={"rom":name,"build_stamp":stamps[0][1] if stamps else "",
             "build_stamp_offset":f"0x{stamps[0][0]:08X}" if stamps else ""}
        for key in ("FLASH1M_V103","NINTENDOSio32ID_030820","PokemonSioInfo","AGBJ01"):
            pos=d.find(key.encode())
            row[key]="" if pos<0 else f"0x{pos:08X}"
        build.append(row)
    pd.DataFrame(astr).to_csv(out/"ascii_strings_ge6.csv.gz",index=False,compression="gzip")
    pd.DataFrame(build).to_csv(out/"build_and_sdk_signatures.csv",index=False)

    cto=[]; namesout=[]
    wm=western_map(); jm=japanese_map()
    for name,d in roms.items():
        if name not in TABLES: continue
        species,ss,ms,item_base,item_stride,item_name_len=TABLES[name]
        move=species+412*ss
        jp="Japan" in name
        cmap=jm if jp else wm
        cto.append({"rom":name,"species_names_offset":f"0x{species:08X}",
                    "species_entries":412,"species_stride":ss,
                    "move_names_offset":f"0x{move:08X}","move_entries":355,"move_stride":ms,
                    "items_table_offset":f"0x{item_base:08X}","items_entries":375,
                    "item_struct_stride":item_stride,"item_name_field":item_name_len})
        for i in range(412):
            o=species+i*ss
            namesout.append({"rom":name,"category":"species_name","id":i,
                             "offset":f"0x{o:08X}","stride":ss,
                             "decoded":decode_fixed(d[o:o+ss],cmap)})
        for i in range(355):
            o=move+i*ms
            namesout.append({"rom":name,"category":"move_name","id":i,
                             "offset":f"0x{o:08X}","stride":ms,
                             "decoded":decode_fixed(d[o:o+ms],cmap)})
        for i in range(375):
            o=item_base+i*item_stride
            namesout.append({"rom":name,"category":"item_name","id":i,
                             "offset":f"0x{o:08X}","stride":item_stride,
                             "decoded":decode_fixed(d[o:o+item_name_len],cmap)})
    pd.DataFrame(cto).to_csv(out/"core_table_offsets.csv",index=False)
    pd.DataFrame(namesout).to_csv(out/"core_names_species_moves_items.csv.gz",index=False,compression="gzip")

    revisions=[
        ("JP Rev0→Rev1","Pocket Monsters - Fire Red (Japan).gba",
         "Pocket Monsters - Fire Red (Japan) (Rev 1).gba"),
        ("EN Rev0→Rev1","Pokemon - Fire Red Version (USA).gba",
         "Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba"),
    ]
    rrows=[]
    for label,a,b in revisions:
        if a not in roms or b not in roms: continue
        for bank in range(256):
            x=np.frombuffer(roms[a][bank*BANK:(bank+1)*BANK],dtype=np.uint8)
            y=np.frombuffer(roms[b][bank*BANK:(bank+1)*BANK],dtype=np.uint8)
            dc=int((x!=y).sum())
            rrows.append({"pair":label,"bank":bank,"start":f"0x{bank*BANK:08X}",
                          "diff_bytes":dc,"diff_pct":round(dc/BANK*100,6)})
    pd.DataFrame(rrows).to_csv(out/"revision_diff_by_bank.csv",index=False)

if __name__ == "__main__":
    main()
