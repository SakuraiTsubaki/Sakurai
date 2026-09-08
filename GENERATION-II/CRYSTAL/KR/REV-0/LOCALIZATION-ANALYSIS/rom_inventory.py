#!/usr/bin/env python3
"""Fresh ROM inventory for GS Korean -> Crystal Korean.

This script deliberately does not contain localization offsets. It reads only
standard Game Boy header fields plus fixed-size 16 KiB ROM banks, hashes the
actual inputs, validates checksums, and emits a machine-readable baseline.

ROM binaries remain local/read-only and are never written to the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

BANK_SIZE = 0x4000
HEADER_START = 0x100
HEADER_END = 0x150

EXPECTED = {
    "gold_kr": {
        "sha1": "c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65",
        "size": 2_097_152,
    },
    "silver_kr": {
        "sha1": "cb22d7e03a74dc3a563fde6be8626626b2b392e7",
        "size": 2_097_152,
    },
    "crystal_jp": {
        "sha1": "95127b901bbce2407daf43cce9f45d4c27ef635d",
        "size": 2_097_152,
    },
}


def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()


def header_checksum(data: bytes) -> int:
    value = 0
    for b in data[0x134:0x14D]:
        value = (value - b - 1) & 0xFF
    return value


def global_checksum(data: bytes) -> int:
    return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF


def printable_title(raw: bytes) -> str:
    return raw.rstrip(b"\x00").decode("ascii", errors="replace")


def bank_record(index: int, bank: bytes) -> dict[str, Any]:
    counts = [0] * 256
    for b in bank:
        counts[b] += 1
    unique = sum(1 for n in counts if n)
    most_common_byte = max(range(256), key=lambda b: counts[b])
    return {
        "bank": index,
        "rom_offset": index * BANK_SIZE,
        "size": len(bank),
        "sha256": digest(bank, "sha256"),
        "unique_byte_values": unique,
        "ff_bytes": counts[0xFF],
        "zero_bytes": counts[0x00],
        "most_common_byte": most_common_byte,
        "most_common_count": counts[most_common_byte],
    }


def inventory(label: str, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    sha1 = digest(data, "sha1")
    expected = EXPECTED[label]

    if len(data) < HEADER_END:
        raise ValueError(f"{path}: file is too small to contain a Game Boy header")

    stored_global = int.from_bytes(data[0x14E:0x150], "big")
    record = {
        "label": label,
        "filename": path.name,
        "size": len(data),
        "identity": {
            "md5": digest(data, "md5"),
            "sha1": sha1,
            "sha256": digest(data, "sha256"),
            "expected_sha1": expected["sha1"],
            "expected_size": expected["size"],
            "matches_expected_sha1": sha1 == expected["sha1"],
            "matches_expected_size": len(data) == expected["size"],
        },
        "header": {
            "title": printable_title(data[0x134:0x143]),
            "cgb_flag": data[0x143],
            "new_licensee": data[0x144:0x146].hex(),
            "sgb_flag": data[0x146],
            "cartridge_type": data[0x147],
            "rom_size_code": data[0x148],
            "ram_size_code": data[0x149],
            "destination_code": data[0x14A],
            "old_licensee": data[0x14B],
            "version": data[0x14C],
            "header_checksum_stored": data[0x14D],
            "header_checksum_computed": header_checksum(data),
            "header_checksum_valid": data[0x14D] == header_checksum(data),
            "global_checksum_stored": stored_global,
            "global_checksum_computed": global_checksum(data),
            "global_checksum_valid": stored_global == global_checksum(data),
        },
        "bank_size": BANK_SIZE,
        "bank_count": (len(data) + BANK_SIZE - 1) // BANK_SIZE,
        "banks": [],
    }

    for index, start in enumerate(range(0, len(data), BANK_SIZE)):
        record["banks"].append(bank_record(index, data[start:start + BANK_SIZE]))

    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, required=True, help="Korean Gold ROM")
    parser.add_argument("--silver", type=Path, required=True, help="Korean Silver ROM")
    parser.add_argument("--crystal", type=Path, required=True, help="Japanese Crystal ROM")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON inventory")
    args = parser.parse_args()

    result = {
        "schema": 1,
        "project": "GS Korean -> Crystal Korean",
        "offset_policy": "fresh-discovery-only",
        "roms": [
            inventory("gold_kr", args.gold),
            inventory("silver_kr", args.silver),
            inventory("crystal_jp", args.crystal),
        ],
    }

    mismatches = [
        rom["label"]
        for rom in result["roms"]
        if not rom["identity"]["matches_expected_sha1"]
        or not rom["identity"]["matches_expected_size"]
        or not rom["header"]["header_checksum_valid"]
        or not rom["header"]["global_checksum_valid"]
    ]
    result["all_inputs_verified"] = not mismatches
    result["mismatched_inputs"] = mismatches

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if mismatches:
        raise SystemExit("input verification failed: " + ", ".join(mismatches))


if __name__ == "__main__":
    main()
