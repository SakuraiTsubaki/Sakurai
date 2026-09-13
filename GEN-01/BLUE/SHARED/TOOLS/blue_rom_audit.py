#!/usr/bin/env python3
"""Generate Pokémon Blue GB identity and per-bank hash reports without committing ROM data."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

BANK_SIZE = 0x4000

def digest(data: bytes, name: str) -> str:
    return hashlib.new(name, data).hexdigest()

def inspect(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) % BANK_SIZE:
        raise ValueError(f"{path}: size is not a multiple of 16 KiB")
    title = data[0x134:0x144].split(b"\0", 1)[0].decode("latin1", errors="replace")
    header = 0
    for value in data[0x134:0x14D]:
        header = (header - value - 1) & 0xFF
    global_sum = (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF
    banks = []
    for bank_index in range(len(data) // BANK_SIZE):
        bank = data[bank_index * BANK_SIZE:(bank_index + 1) * BANK_SIZE]
        banks.append({"bank_dec":bank_index,"bank_hex":f"0x{bank_index:02X}","sha256":digest(bank,"sha256"),"non_ff_bytes":sum(value != 0xFF for value in bank),"non_00_bytes":sum(value != 0x00 for value in bank),"unique_byte_values":len(set(bank))})
    return {"filename":path.name,"size_bytes":len(data),"bank_count":len(data)//BANK_SIZE,"title":title,"header_version":data[0x14C],"cgb_flag":f"0x{data[0x143]:02X}","sgb_flag":f"0x{data[0x146]:02X}","cartridge_type":f"0x{data[0x147]:02X}","rom_size_code":f"0x{data[0x148]:02X}","ram_size_code":f"0x{data[0x149]:02X}","destination_code":f"0x{data[0x14A]:02X}","header_checksum_valid":header==data[0x14D],"global_checksum_valid":global_sum==int.from_bytes(data[0x14E:0x150],"big"),"md5":digest(data,"md5"),"sha1":digest(data,"sha1"),"sha256":digest(data,"sha256"),"banks":banks}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=Path("blue-audit"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    reports = [inspect(path) for path in args.rom]
    identity = [{key:value for key,value in report.items() if key != "banks"} for report in reports]
    (args.out/"identity.json").write_text(json.dumps(identity,indent=2)+"\n",encoding="utf-8")
    with (args.out/"bank-sha256.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.writer(handle)
        writer.writerow(["filename","bank_dec","bank_hex","sha256","non_ff_bytes","non_00_bytes","unique_byte_values"])
        for report in reports:
            for bank in report["banks"]:
                writer.writerow([report["filename"],bank["bank_dec"],bank["bank_hex"],bank["sha256"],bank["non_ff_bytes"],bank["non_00_bytes"],bank["unique_byte_values"]])

if __name__ == "__main__":
    main()
