#!/usr/bin/env python3
"""Normalize the two known FireRed English tail-byte variants into clean work copies.

The source file is never modified. The output is accepted only if its SHA-1
matches the canonical target for the BPRE revision encoded in the GBA header.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

TARGETS = {
    0: "41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc",
    1: "dd5945db9b930750cb39d00c84da8571feebf417",
}
EXPECTED_TAILS = {
    0: bytes.fromhex("0019"),
    1: bytes.fromhex("0018"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = bytearray(args.source.read_bytes())
    if len(data) != 16 * 1024 * 1024:
        raise SystemExit("expected a 16 MiB FireRed ROM image")
    if data[0xAC:0xB0] != b"BPRE":
        raise SystemExit("expected game code BPRE")

    revision = data[0xBC]
    if revision not in TARGETS:
        raise SystemExit(f"unsupported BPRE revision: {revision}")
    if bytes(data[-2:]) != EXPECTED_TAILS[revision]:
        raise SystemExit(
            f"unexpected source tail {bytes(data[-2:]).hex()}; refusing to guess"
        )

    data[-2:] = b"\xff\xff"
    digest = hashlib.sha1(data).hexdigest()
    if digest != TARGETS[revision]:
        raise SystemExit(
            f"normalization did not reach canonical SHA-1: {digest}"
        )

    args.output.write_bytes(data)
    print(f"wrote {args.output} (SHA-1 {digest})")


if __name__ == "__main__":
    main()
