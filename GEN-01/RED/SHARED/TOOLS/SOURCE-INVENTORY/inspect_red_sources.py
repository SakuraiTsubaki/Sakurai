#!/usr/bin/env python3
"""Inventory supplied Game Boy ROMs without copying ROM bytes into outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROM_SIZE_CODES = {
    0x00: 32 * 1024,
    0x01: 64 * 1024,
    0x02: 128 * 1024,
    0x03: 256 * 1024,
    0x04: 512 * 1024,
    0x05: 1024 * 1024,
    0x06: 2 * 1024 * 1024,
    0x07: 4 * 1024 * 1024,
    0x08: 8 * 1024 * 1024,
    0x52: 1152 * 1024,
    0x53: 1280 * 1024,
    0x54: 1536 * 1024,
}


def digest(data: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, data).hexdigest()


def header_checksum(data: bytes) -> int:
    value = 0
    for byte in data[0x134:0x14D]:
        value = (value - byte - 1) & 0xFF
    return value


def global_checksum(data: bytes) -> int:
    return (sum(data) - data[0x14E] - data[0x14F]) & 0xFFFF


def printable_title(raw: bytes) -> str:
    return raw.split(b"\0", 1)[0].decode("ascii", errors="replace").rstrip()


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    banks = []
    for index in range((len(data) + 0x3FFF) // 0x4000):
        chunk = data[index * 0x4000:(index + 1) * 0x4000]
        banks.append({
            "index": index,
            "offset_start": f"0x{index * 0x4000:06X}",
            "size": len(chunk),
            "sha256": digest(chunk, "sha256"),
        })
    declared_size = ROM_SIZE_CODES.get(data[0x148])
    return {
        "source_label": path.name,
        "size_bytes": len(data),
        "sha1": digest(data, "sha1"),
        "sha256": digest(data, "sha256"),
        "header": {
            "title": printable_title(data[0x134:0x144]),
            "cgb_flag": f"0x{data[0x143]:02X}",
            "new_licensee_code": data[0x144:0x146].decode("ascii", errors="replace"),
            "sgb_flag": f"0x{data[0x146]:02X}",
            "cartridge_type": f"0x{data[0x147]:02X}",
            "rom_size_code": f"0x{data[0x148]:02X}",
            "declared_rom_size_bytes": declared_size,
            "ram_size_code": f"0x{data[0x149]:02X}",
            "destination_code": f"0x{data[0x14A]:02X}",
            "old_licensee_code": f"0x{data[0x14B]:02X}",
            "mask_rom_version": data[0x14C],
            "header_checksum_stored": f"0x{data[0x14D]:02X}",
            "header_checksum_computed": f"0x{header_checksum(data):02X}",
            "header_checksum_valid": data[0x14D] == header_checksum(data),
            "global_checksum_stored": f"0x{int.from_bytes(data[0x14E:0x150], 'big'):04X}",
            "global_checksum_computed": f"0x{global_checksum(data):04X}",
            "global_checksum_valid": int.from_bytes(data[0x14E:0x150], "big") == global_checksum(data),
        },
        "bank_size_bytes": 0x4000,
        "bank_count": len(banks),
        "banks": banks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records = [inspect(path) for path in sorted(args.source_dir.glob("*.gb"))]
    by_sha256: dict[str, list[str]] = defaultdict(list)
    for record in records:
        by_sha256[record["sha256"]].append(record["source_label"])
    duplicates = [
        {"sha256": key, "source_labels": labels}
        for key, labels in sorted(by_sha256.items()) if len(labels) > 1
    ]
    inventory = {
        "schema_version": 1,
        "generated_from": "locally supplied read-only ROMs",
        "rom_binary_included": False,
        "input_count": len(records),
        "unique_content_count": len(by_sha256),
        "duplicates": duplicates,
        "sources": records,
    }
    (args.output_dir / "source_inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (args.output_dir / "source_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["source_label", "size_bytes", "sha1", "sha256", "title", "sgb_flag", "cartridge_type", "rom_size_code", "destination_code", "mask_rom_version", "header_checksum_valid", "global_checksum_valid"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            header = record["header"]
            writer.writerow({
                "source_label": record["source_label"],
                "size_bytes": record["size_bytes"],
                "sha1": record["sha1"],
                "sha256": record["sha256"],
                "title": header["title"],
                "sgb_flag": header["sgb_flag"],
                "cartridge_type": header["cartridge_type"],
                "rom_size_code": header["rom_size_code"],
                "destination_code": header["destination_code"],
                "mask_rom_version": header["mask_rom_version"],
                "header_checksum_valid": header["header_checksum_valid"],
                "global_checksum_valid": header["global_checksum_valid"],
            })


if __name__ == "__main__":
    main()
