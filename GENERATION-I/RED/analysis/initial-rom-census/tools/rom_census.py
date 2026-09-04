#!/usr/bin/env python3
"""ROM-safe census helper for Pokémon Red-family Game Boy ROMs.

Records hashes, Game Boy cartridge-header metadata, checksum validation,
pairwise byte-difference counts, and 16 KiB bank statistics. It never emits
ROM payload bytes.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path

BANK_SIZE = 0x4000
ROM_SIZE = {
    0x00: 32 << 10,
    0x01: 64 << 10,
    0x02: 128 << 10,
    0x03: 256 << 10,
    0x04: 512 << 10,
    0x05: 1024 << 10,
    0x06: 2048 << 10,
    0x07: 4096 << 10,
    0x08: 8192 << 10,
}
RAM_SIZE = {
    0x00: 0,
    0x01: 2 << 10,
    0x02: 8 << 10,
    0x03: 32 << 10,
    0x04: 128 << 10,
    0x05: 64 << 10,
}
CART = {
    0x00: "ROM ONLY",
    0x01: "MBC1",
    0x02: "MBC1+RAM",
    0x03: "MBC1+RAM+BATTERY",
    0x0F: "MBC3+TIMER+BATTERY",
    0x10: "MBC3+TIMER+RAM+BATTERY",
    0x11: "MBC3",
    0x12: "MBC3+RAM",
    0x13: "MBC3+RAM+BATTERY",
    0x19: "MBC5",
    0x1A: "MBC5+RAM",
    0x1B: "MBC5+RAM+BATTERY",
}


def digest(name: str, data: bytes) -> str:
    return hashlib.new(name, data).hexdigest()


def entropy(data: bytes) -> float:
    counts = collections.Counter(data)
    total = len(data)
    if not total:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def header_row(path: Path) -> dict:
    data = path.read_bytes()
    title = data[0x134:0x144].split(b"\0", 1)[0].decode("ascii", "replace")

    header_checksum = 0
    for value in data[0x134:0x14D]:
        header_checksum = (header_checksum - value - 1) & 0xFF

    global_checksum = (sum(data) - data[0x14E] - data[0x14F]) & 0xFFFF

    return {
        "file": path.name,
        "size_bytes": len(data),
        "md5": digest("md5", data),
        "sha1": digest("sha1", data),
        "sha256": digest("sha256", data),
        "title": title,
        "cgb_flag": f"0x{data[0x143]:02X}",
        "new_licensee": data[0x144:0x146].decode("ascii", "replace"),
        "sgb_flag": f"0x{data[0x146]:02X}",
        "cartridge_type": f"0x{data[0x147]:02X} {CART.get(data[0x147], 'UNKNOWN')}",
        "rom_size_code": f"0x{data[0x148]:02X}",
        "declared_rom_size": ROM_SIZE.get(data[0x148]),
        "ram_size_code": f"0x{data[0x149]:02X}",
        "declared_ram_size": RAM_SIZE.get(data[0x149]),
        "destination_code": f"0x{data[0x14A]:02X}",
        "old_licensee": f"0x{data[0x14B]:02X}",
        "version": data[0x14C],
        "header_checksum": f"0x{data[0x14D]:02X}",
        "global_checksum": f"0x{int.from_bytes(data[0x14E:0x150], 'big'):04X}",
        "header_checksum_valid": header_checksum == data[0x14D],
        "global_checksum_valid": global_checksum == int.from_bytes(data[0x14E:0x150], "big"),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()

    files = sorted(args.rom_dir.glob("*.gb"))
    if not files:
        raise SystemExit("No .gb files found")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    inventory = [header_row(path) for path in files]
    (args.out_dir / "rom_inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_csv(args.out_dir / "rom_inventory.csv", inventory)

    pairs: list[dict] = []
    for index, left in enumerate(files):
        left_data = left.read_bytes()
        for right in files[index + 1 :]:
            right_data = right.read_bytes()
            shared = min(len(left_data), len(right_data))
            diff = sum(a != b for a, b in zip(left_data[:shared], right_data[:shared]))
            diff += abs(len(left_data) - len(right_data))
            pairs.append(
                {
                    "a": left.name,
                    "b": right.name,
                    "same_size": len(left_data) == len(right_data),
                    "byte_differences": diff,
                    "identical": left_data == right_data,
                }
            )
    write_csv(args.out_dir / "pairwise_diff_counts.csv", pairs)

    bank_rows: list[dict] = []
    for path in files:
        data = path.read_bytes()
        for offset in range(0, len(data), BANK_SIZE):
            bank = data[offset : offset + BANK_SIZE]
            bank_rows.append(
                {
                    "file": path.name,
                    "bank": offset // BANK_SIZE,
                    "offset_start": f"0x{offset:06X}",
                    "offset_end": f"0x{offset + len(bank) - 1:06X}",
                    "sha1": digest("sha1", bank),
                    "entropy": round(entropy(bank), 6),
                    "zero_bytes": bank.count(0),
                    "ff_bytes": bank.count(0xFF),
                    "unique_byte_values": len(set(bank)),
                }
            )
    write_csv(args.out_dir / "bank_census.csv", bank_rows)


if __name__ == "__main__":
    main()
