#!/usr/bin/env python3
"""Emit a byte-exact RGBDS-compatible bank source tree from a 2 MiB Pokémon Crystal ROM.

This intentionally does *not* guess code vs data. It is the lossless Layer-A skeleton:
all bytes are emitted as `db` so a semantic disassembly can replace regions gradually
without losing rebuildability.
"""
from pathlib import Path
import argparse, hashlib, json, re

BANK_SIZE=0x4000
ROM_SIZE=0x200000

def emit(rom_path: Path, outdir: Path):
    rom=rom_path.read_bytes()
    if len(rom)!=ROM_SIZE:
        raise SystemExit(f'expected {ROM_SIZE} bytes, got {len(rom)}')
    outdir.mkdir(parents=True, exist_ok=True)
    banks=outdir/'banks'; banks.mkdir(exist_ok=True)
    includes=[]
    bank_hashes=[]
    for bank in range(0x80):
        chunk=rom[bank*BANK_SIZE:(bank+1)*BANK_SIZE]
        name=f'bank{bank:02x}.asm'
        p=banks/name
        if bank==0:
            section='SECTION "ROM Bank 00", ROM0[$0000]'
            cpu_base=0x0000
        else:
            section=f'SECTION "ROM Bank {bank:02X}", ROMX[$4000], BANK[${bank:02X}]'
            cpu_base=0x4000
        lines=[f'; Auto-generated from {rom_path.name}',f'; Bank ${bank:02X}; file offset ${bank*BANK_SIZE:06X}; CPU ${cpu_base:04X}-${cpu_base+0x3FFF:04X}',section,'']
        for off in range(0,BANK_SIZE,16):
            vals=', '.join(f'${x:02X}' for x in chunk[off:off+16])
            lines.append(f'    db {vals} ; ${cpu_base+off:04X}')
        p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        includes.append(f'INCLUDE "banks/{name}"')
        bank_hashes.append({'bank':f'{bank:02X}','sha1':hashlib.sha1(chunk).hexdigest()})
    (outdir/'master.asm').write_text('\n'.join(['; Lossless Layer-A Crystal ROM source','; Assemble/link with RGBDS; no rgbfix step is needed because the original header/checksums are included byte-for-byte.','']+includes)+"\n",encoding='utf-8')
    manifest={
        'source_rom_name':rom_path.name,
        'source_sha1':hashlib.sha1(rom).hexdigest(),
        'size':len(rom),'bank_size':BANK_SIZE,'bank_count':0x80,
        'representation':'byte-exact RGBDS db skeleton; not semantic code/data classification',
        'banks':bank_hashes,
    }
    (outdir/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return manifest

def reconstruct_from_source(outdir: Path) -> bytes:
    data=bytearray()
    rx=re.compile(r'\$([0-9A-Fa-f]{2})')
    for bank in range(0x80):
        lines=(outdir/'banks'/f'bank{bank:02x}.asm').read_text(encoding='utf-8').splitlines()
        chunk=bytearray()
        for line in lines:
            code=line.split(';',1)[0]
            if 'db ' not in code: continue
            chunk.extend(int(m.group(1),16) for m in rx.finditer(code))
        if len(chunk)!=BANK_SIZE:
            raise ValueError((bank,len(chunk)))
        data.extend(chunk)
    return bytes(data)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom',type=Path)
    ap.add_argument('outdir',type=Path)
    ap.add_argument('--verify',action='store_true')
    a=ap.parse_args()
    manifest=emit(a.rom,a.outdir)
    print('emitted',a.outdir,'sha1',manifest['source_sha1'])
    if a.verify:
        rebuilt=reconstruct_from_source(a.outdir)
        original=a.rom.read_bytes()
        print('reconstructed sha1',hashlib.sha1(rebuilt).hexdigest())
        if rebuilt!=original: raise SystemExit('verification FAILED')
        print('verification OK: source tree is byte-identical')
if __name__=='__main__': main()
