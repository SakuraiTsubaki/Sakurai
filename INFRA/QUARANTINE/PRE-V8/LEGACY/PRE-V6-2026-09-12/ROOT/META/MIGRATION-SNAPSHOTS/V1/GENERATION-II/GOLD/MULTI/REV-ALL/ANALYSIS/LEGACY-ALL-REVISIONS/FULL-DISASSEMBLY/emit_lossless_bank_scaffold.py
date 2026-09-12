#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, re

BANK = 0x4000
p = argparse.ArgumentParser()
p.add_argument('--input', type=Path, required=True, help='directory containing user-supplied .gbc files')
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=True)

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', Path(name).stem.lower()).strip('-')

def bank_source(bank, data):
    if bank == 0:
        section = 'SECTION "ROM Bank $00", ROM0[$0000]'
        base = 0
    else:
        section = f'SECTION "ROM Bank ${bank:02X}", ROMX[$4000], BANK[${bank:02X}]'
        base = 0x4000
    out = [section, f'; SHA1 {hashlib.sha1(data).hexdigest()}']
    if len(set(data)) == 1:
        out.append(f'ds $4000, ${data[0]:02X}')
    else:
        for off in range(0, BANK, 32):
            chunk = data[off:off + 32]
            out.append(f'; ${base + off:04X} file+${bank * BANK + off:06X}')
            out.append('db ' + ', '.join(f'${x:02X}' for x in chunk))
    return '\n'.join(out) + '\n'

for rom in sorted(a.input.glob('*.gbc')):
    raw = rom.read_bytes()
    if len(raw) % BANK:
        raise SystemExit(f'{rom}: size is not a multiple of 16 KiB')
    root = a.output / slug(rom.name)
    banks = root / 'banks'
    banks.mkdir(parents=True, exist_ok=True)
    includes = []
    for bank in range(len(raw) // BANK):
        data = raw[bank * BANK:(bank + 1) * BANK]
        (banks / f'bank_{bank:02X}.asm').write_text(bank_source(bank, data), encoding='utf-8')
        includes.append(f'INCLUDE "banks/bank_{bank:02X}.asm"')
    (root / 'main.asm').write_text('\n'.join(includes) + '\n', encoding='utf-8')
    (root / 'SOURCE_SHA1.txt').write_text(f'{hashlib.sha1(raw).hexdigest()}  {rom.name}\n', encoding='utf-8')
    print(rom.name, len(raw) // BANK, 'banks', hashlib.sha1(raw).hexdigest())
