#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib
from pathlib import Path

BANK_SIZE = 0x4000

CART_TYPES = {
    0x0F: 'MBC3+TIMER+BATTERY',
    0x10: 'MBC3+TIMER+RAM+BATTERY',
    0x11: 'MBC3',
    0x12: 'MBC3+RAM',
    0x13: 'MBC3+RAM+BATTERY',
}


def header_checksum(data: bytes) -> int:
    x = 0
    for i in range(0x134, 0x14D):
        x = (x - data[i] - 1) & 0xFF
    return x


def global_checksum(data: bytes) -> int:
    return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF


def main() -> None:
    ap = argparse.ArgumentParser(description='Audit a Pokémon Gold Game Boy Color ROM without modifying it.')
    ap.add_argument('rom', type=Path)
    args = ap.parse_args()

    data = args.rom.read_bytes()
    banks = [data[i:i+BANK_SIZE] for i in range(0, len(data), BANK_SIZE)]
    blank_zero = [i for i, bank in enumerate(banks) if bank == bytes(BANK_SIZE)]

    print(f'file: {args.rom.name}')
    print(f'size: {len(data)} bytes ({len(data) / 1024 / 1024:.2f} MiB)')
    print(f'banks: {len(banks)}')
    print(f'md5: {hashlib.md5(data).hexdigest()}')
    print(f'sha1: {hashlib.sha1(data).hexdigest()}')
    print(f'sha256: {hashlib.sha256(data).hexdigest()}')
    print(f'cgb_flag: 0x{data[0x143]:02X}')
    print(f'cart_type: 0x{data[0x147]:02X} ({CART_TYPES.get(data[0x147], "unknown")})')
    print(f'rom_size_code: 0x{data[0x148]:02X}')
    print(f'ram_size_code: 0x{data[0x149]:02X}')
    print(f'destination_code: 0x{data[0x14A]:02X}')
    print(f'version: 0x{data[0x14C]:02X}')
    print(f'header_checksum: stored=0x{data[0x14D]:02X} calculated=0x{header_checksum(data):02X}')
    stored_global = int.from_bytes(data[0x14E:0x150], 'big')
    print(f'global_checksum: stored=0x{stored_global:04X} calculated=0x{global_checksum(data):04X}')
    print(f'fully_zero_banks: {len(blank_zero)}')
    print('fully_zero_bank_ids: ' + ' '.join(f'{i:02X}' for i in blank_zero))
    print(f'fully_zero_capacity: {len(blank_zero) * BANK_SIZE} bytes')

    sig = bytes.fromhex('e0 9f ea 00 20 c9')
    offsets = []
    start = 0
    while True:
        off = data.find(sig, start)
        if off < 0:
            break
        offsets.append(off)
        start = off + 1
    print('bankswitch_signature_offsets: ' + ' '.join(f'0x{x:06X}' for x in offsets))

if __name__ == '__main__':
    main()
