#!/usr/bin/env python3
"""Build per-ROM IPS data-staging patches for the Silver Generation-III layer.

No ROM bytes are embedded here. The patches only:
- write the deterministic Generation-III parameter block at common free Bank $73,
- update the ROM/global checksum fields,
- and for the two 1-MiB Japanese ROMs, switch the ROM-size header to 2 MiB and
  force the patched file to 2 MiB by writing a final zero byte.

The target ROM identities/checksums were censused from the project's eight clean
Silver ROMs. Original or derivative ROM files are never committed.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path

BLOCK_OFFSET = 0x73 * 0x4000  # file offset $1CC000
FINAL_2M_BYTE = 0x1FFFFF

TARGETS = [
    {
        "key": "kr", "file": "Pocket Monsters Eun (Korea).gbc",
        "sha256": "ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22",
        "size": 0x200000, "rom_size_code": 0x06, "header_checksum": 0xE7, "global_checksum": 0x985B,
    },
    {
        "key": "jp_reva", "file": "Pocket Monsters Gin (Japan) (Rev A).gbc",
        "sha256": "99e5267fbf5a7748d4f3b75ba1990cb5d91348339468607a04bfbc6081c62d71",
        "size": 0x100000, "rom_size_code": 0x05, "header_checksum": 0x26, "expanded_header_checksum": 0x25, "global_checksum": 0x1D34,
    },
    {
        "key": "jp_rev0", "file": "Pocket Monsters Gin (Japan).gbc",
        "sha256": "0a532063a3ff5750a464582aa7bbee2b6d42e1a92a136d9f4590e373487b615c",
        "size": 0x100000, "rom_size_code": 0x05, "header_checksum": 0x27, "expanded_header_checksum": 0x26, "global_checksum": 0x7691,
    },
    {
        "key": "es", "file": "Pokemon - Edicion Plata (Spain).gbc",
        "sha256": "6797010c052e8f9373ea2b9e855ec078b34fda12e5ccf742eb19bb5e8f6947c2",
        "size": 0x200000, "rom_size_code": 0x06, "header_checksum": 0x1C, "global_checksum": 0x064B,
    },
    {
        "key": "de", "file": "Pokemon - Silberne Edition (Germany).gbc",
        "sha256": "c3d1fd0dec1d5fa9aa7f85275e79c52aa9175d191c63cbed7b406c306d946348",
        "size": 0x200000, "rom_size_code": 0x06, "header_checksum": 0x2B, "global_checksum": 0xCD6E,
    },
    {
        "key": "en", "file": "Pokemon - Silver Version (USA, Europe).gbc",
        "sha256": "72b190859a59623cbef6c49d601f8de52c1d2331b4f08a8d2acc17274fc19a8c",
        "size": 0x200000, "rom_size_code": 0x06, "header_checksum": 0x2A, "global_checksum": 0x0DAE,
    },
    {
        "key": "fr", "file": "Pokemon - Version Argent (France).gbc",
        "sha256": "e120c4ddb0dc3e25b95c9c71b3ffd59ff57ce689cf4d79d04913ba59140c18c2",
        "size": 0x200000, "rom_size_code": 0x06, "header_checksum": 0x29, "global_checksum": 0xFB8C,
    },
    {
        "key": "it", "file": "Pokemon - Versione Argento (Italy).gbc",
        "sha256": "04c442246d1ae0ed6bf5e072bb7e3d06376e584b953d6b14047b39e45fbb0cb4",
        "size": 0x200000, "rom_size_code": 0x06, "header_checksum": 0x26, "global_checksum": 0x7350,
    },
]


def ips_record(offset: int, data: bytes) -> bytes:
    if not (0 <= offset <= 0xFFFFFF):
        raise ValueError(offset)
    if not (1 <= len(data) <= 0xFFFF):
        raise ValueError(len(data))
    return offset.to_bytes(3, "big") + len(data).to_bytes(2, "big") + data


def make_patch(target: dict, block: bytes) -> tuple[bytes, int]:
    block_sum = sum(block) & 0xFFFF
    new_global = (target["global_checksum"] + block_sum) & 0xFFFF
    # For JP expansion: ROM-size byte +1 and header checksum -1, so the total
    # byte sum outside the global checksum remains unchanged before block data.
    out = bytearray(b"PATCH")
    if target["size"] == 0x100000:
        out += ips_record(0x148, b"\x06")
        out += ips_record(0x14D, bytes([target["expanded_header_checksum"]]))
    out += ips_record(0x14E, new_global.to_bytes(2, "big"))
    out += ips_record(BLOCK_OFFSET, block)
    if target["size"] == 0x100000:
        out += ips_record(FINAL_2M_BYTE, b"\x00")
    out += b"EOF"
    return bytes(out), new_global


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("block", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("report", type=Path)
    args = ap.parse_args()
    block = args.block.read_bytes()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "block_offset": BLOCK_OFFSET,
        "block_bytes": len(block),
        "block_sha256": hashlib.sha256(block).hexdigest(),
        "block_byte_sum16": sum(block) & 0xFFFF,
        "common_zero_banks_verified_on_clean_2MiB_targets": ["0x73", "0x74"],
        "status": "DATA-STAGED; engine routing not yet active",
        "targets": [],
    }
    for t in TARGETS:
        patch, new_global = make_patch(t, block)
        name = f"silver_gen3_parameters_{t['key']}.ips"
        p = args.out_dir / name
        p.write_bytes(patch)
        (args.out_dir / f"{name}.b64").write_text(base64.encodebytes(patch).decode("ascii"), encoding="ascii")
        result["targets"].append({
            "key": t["key"],
            "source_file": t["file"],
            "source_sha256": t["sha256"],
            "source_bytes": t["size"],
            "output_bytes": 0x200000,
            "old_rom_size_code": t["rom_size_code"],
            "new_rom_size_code": 0x06,
            "old_header_checksum": t["header_checksum"],
            "new_header_checksum": t.get("expanded_header_checksum", t["header_checksum"]),
            "old_global_checksum": t["global_checksum"],
            "new_global_checksum": new_global,
            "patch": name,
            "patch_bytes": len(patch),
            "patch_sha256": hashlib.sha256(patch).hexdigest(),
        })
    args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
