#!/usr/bin/env python3
"""Generate non-ROM audit artifacts for the six Pokémon Blue source dumps.

Usage:
  python blue_rom_audit.py --rom JP-JA-HV0=path/to/ao.gb ... --out outdir

The script never writes ROM bytes into its outputs. It emits hashes, header facts,
bank fingerprints, duplicate-bank groups and pairwise byte-similarity summaries.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, itertools, math
from pathlib import Path

BANK=0x4000

def entropy(buf: bytes) -> float:
    n=len(buf); c=collections.Counter(buf)
    return -sum((v/n)*math.log2(v/n) for v in c.values()) if n else 0.0

def checks(buf: bytes):
    x=0
    for v in buf[0x134:0x14D]: x=(x-v-1)&0xff
    g=(sum(buf[:0x14E])+sum(buf[0x150:]))&0xffff
    stored=(buf[0x14E]<<8)|buf[0x14F]
    return x==buf[0x14D], g==stored

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rom', action='append', required=True, help='RELEASE-ID=PATH')
    ap.add_argument('--out', required=True)
    ns=ap.parse_args(); out=Path(ns.out); out.mkdir(parents=True,exist_ok=True)
    roms={}
    for item in ns.rom:
        rid,p=item.split('=',1); roms[rid]=Path(p)
    data={rid:p.read_bytes() for rid,p in roms.items()}
    releases=[]; hashes={}
    for rid,b in data.items():
        h,g=checks(b)
        releases.append(dict(release_id=rid,source_filename=roms[rid].name,size_bytes=len(b),bank_count_16k=len(b)//BANK,
            md5=hashlib.md5(b).hexdigest(),sha1=hashlib.sha1(b).hexdigest(),sha256=hashlib.sha256(b).hexdigest(),
            header_title=b[0x134:0x144].split(b'\0',1)[0].decode('ascii','replace'),cgb_flag=f'0x{b[0x143]:02X}',
            sgb_flag=f'0x{b[0x146]:02X}',cartridge_type=f'0x{b[0x147]:02X}',rom_size_code=f'0x{b[0x148]:02X}',
            ram_size_code=f'0x{b[0x149]:02X}',destination_code=f'0x{b[0x14A]:02X}',header_version=b[0x14C],
            header_checksum_valid=h,global_checksum_valid=g))
        hashes[rid]=[]
    with (out/'release-inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=releases[0]); w.writeheader(); w.writerows(releases)
    bankrows=[]
    for rid,b in data.items():
        for i in range(len(b)//BANK):
            bk=b[i*BANK:(i+1)*BANK]; s=hashlib.sha1(bk).hexdigest(); hashes[rid].append(s)
            mc,n=collections.Counter(bk).most_common(1)[0]
            bankrows.append(dict(release_id=rid,bank_hex=f'{i:02X}',offset_start=f'0x{i*BANK:06X}',
                sha1=s,sha256=hashlib.sha256(bk).hexdigest(),entropy_bits_per_byte=f'{entropy(bk):.6f}',
                zero_fraction=f'{bk.count(0)/BANK:.6f}',ff_fraction=f'{bk.count(255)/BANK:.6f}',
                most_common_byte=f'0x{mc:02X}',most_common_fraction=f'{n/BANK:.6f}',all_zero=all(v==0 for v in bk)))
    with (out/'bank-fingerprints.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=bankrows[0]); w.writeheader(); w.writerows(bankrows)
    ids=list(data); pairs=[]
    for a,b in itertools.combinations(ids,2):
        n=min(len(data[a]),len(data[b])); eq=sum(x==y for x,y in zip(data[a][:n],data[b][:n])); bc=n//BANK
        pairs.append(dict(release_a=a,release_b=b,common_bytes=n,equal_bytes=eq,common_prefix_similarity=f'{eq/n:.9f}',
                          common_bank_count=bc,identical_same_index_banks=sum(hashes[a][i]==hashes[b][i] for i in range(bc))))
    with (out/'pairwise-similarity.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=pairs[0]); w.writeheader(); w.writerows(pairs)
    dup=[]
    for rid,hs in hashes.items():
        groups=collections.defaultdict(list)
        for i,h in enumerate(hs): groups[h].append(i)
        for h,idx in groups.items():
            if len(idx)>1: dup.append(dict(release_id=rid,sha1=h,bank_count=len(idx),banks=';'.join(f'{i:02X}' for i in idx)))
    with (out/'within-rom-duplicate-banks.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['release_id','sha1','bank_count','banks']); w.writeheader(); w.writerows(dup)
if __name__=='__main__': main()
