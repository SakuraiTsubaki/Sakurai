#!/usr/bin/env python3
"""Normalize the two-byte tail corruption observed in two FireRed BPRE dumps.

The script only accepts the exact known pre-cleanup SHA-1 fingerprints. It writes a
new file, changes bytes 0x00FFFFFE-0x00FFFFFF to FF FF, and verifies the expected
clean SHA-1. It never overwrites the source ROM.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

PROFILES = {
    "D3B806453369B4B086C792EB3C05A02F00057F50": {
        "name": "FireRed English USA Rev 0",
        "tail": bytes.fromhex("0019"),
        "clean_sha1": "41CB23D8DCCC8EBD7C649CD8FBB58EEACE6E2FDC",
    },
    "C4D0119D9BCB36687F41A8F7CA72AB7AF60558E4": {
        "name": "FireRed English USA/Europe Rev 1",
        "tail": bytes.fromhex("0018"),
        "clean_sha1": "DD5945DB9B930750CB39D00C84DA8571FEEBF417",
    },
}

ROM_SIZE = 0x01000000
TAIL_OFFSET = 0x00FFFFFE
CLEAN_TAIL = b"\xFF\xFF"


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    source = args.rom.read_bytes()
    if len(source) != ROM_SIZE:
        raise SystemExit(f"Unexpected ROM size: {len(source)} bytes")

    source_sha1 = sha1(source)
    profile = PROFILES.get(source_sha1)
    if profile is None:
        raise SystemExit(f"Unsupported source SHA-1: {source_sha1}")

    if source[TAIL_OFFSET:] != profile["tail"]:
        raise SystemExit("Known source fingerprint has an unexpected ROM tail")

    cleaned = bytearray(source)
    cleaned[TAIL_OFFSET:] = CLEAN_TAIL
    cleaned = bytes(cleaned)

    clean_sha1 = sha1(cleaned)
    if clean_sha1 != profile["clean_sha1"]:
        raise SystemExit(
            f"Verification failed: got {clean_sha1}, expected {profile['clean_sha1']}"
        )

    output = args.output or args.rom.with_name(args.rom.stem + ".clean.gba")
    if output.resolve() == args.rom.resolve():
        raise SystemExit("Refusing to overwrite the source ROM")

    output.write_bytes(cleaned)
    print(profile["name"])
    print(f"source SHA-1: {source_sha1}")
    print(f"clean  SHA-1: {clean_sha1}")
    print(f"output: {output}")


if __name__ == "__main__":
    main()
