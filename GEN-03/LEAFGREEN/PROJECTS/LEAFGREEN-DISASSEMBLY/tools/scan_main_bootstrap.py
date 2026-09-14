#!/usr/bin/env python3
"""Locate and verify the LeafGreen main/bootstrap module in a reference ROM.

The script never modifies the ROM. It uses a stable InitMainCallbacks signature to
infer the target's post-AgbMain layout delta, then prints the known function map.

Usage:
    python tools/scan_main_bootstrap.py path/to/reference.gba
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

INIT_MAIN_CALLBACKS_SIG = bytes.fromhex("10 b5 0b 48 00 24 04 62")
SEARCH_START = 0x400
SEARCH_END = 0x600
USA_INIT_MAIN_CALLBACKS = 0x4C4
AGB_MAIN = 0x3A4

FUNCTIONS = [
    ("AgbMain", 0x3A4),
    ("UpdateLinkAndCallCallbacks", 0x4B0),
    ("InitMainCallbacks", 0x4C4),
    ("CallCallbacks", 0x510),
    ("SetMainCallback2", 0x544),
    ("StartTimer1", 0x558),
    ("SeedRngAndSetTrainerId", 0x564),
    ("GetGeneratedTrainerIdLower", 0x58C),
    ("EnableVCountIntrAtLine150", 0x598),
    ("InitKeys", 0x5C0),
    ("ReadKeys", 0x5E8),
    ("InitIntrHandlers", 0x688),
    ("SetVBlankCallback", 0x6F4),
    ("SetHBlankCallback", 0x700),
    ("SetVCountCallback", 0x70C),
    ("SetSerialCallback", 0x718),
    ("VBlankIntr", 0x724),
    ("InitFlashTimer", 0x7C8),
    ("HBlankIntr", 0x7DC),
    ("VCountIntr", 0x80C),
    ("SerialIntr", 0x844),
    ("RestoreSerialTimer3IntrHandlers", 0x874),
    ("IntrDummy", 0x88C),
    ("WaitForVBlank", 0x890),
    ("SetVBlankCounter1Ptr", 0x8C0),
    ("DisableVBlankCounter1", 0x8CC),
    ("DoSoftReset", 0x8D8),
    ("ClearPokemonCrySongs", 0x944),
    ("NEXT_MODULE", 0x968),
]


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def find_unique(data: bytes, needle: bytes, start: int, end: int) -> int:
    first = data.find(needle, start, end)
    if first < 0:
        raise SystemExit("stable InitMainCallbacks signature not found")
    second = data.find(needle, first + 1, end)
    if second >= 0:
        raise SystemExit(
            f"signature is not unique in search window: 0x{first:X}, 0x{second:X}"
        )
    return first


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    args = ap.parse_args()

    data = args.rom.read_bytes()
    if len(data) != 0x1000000:
        raise SystemExit(f"expected 16 MiB ROM, got {len(data)} bytes")

    game_code = data[0xAC:0xB0].decode("ascii", errors="replace")
    title = data[0xA0:0xAC].rstrip(b"\0").decode("ascii", errors="replace")
    revision = data[0xBC]

    init_main = find_unique(
        data, INIT_MAIN_CALLBACKS_SIG, SEARCH_START, SEARCH_END
    )
    delta = init_main - USA_INIT_MAIN_CALLBACKS

    print(f"file      : {args.rom}")
    print(f"title     : {title}")
    print(f"game code : {game_code}")
    print(f"revision  : {revision}")
    print(f"sha1      : {sha1(data)}")
    print(f"delta     : {delta:+#x} after AgbMain")
    print()
    print("function,start,end,size,sha1")

    for i, (name, usa_start) in enumerate(FUNCTIONS[:-1]):
        next_name, usa_end = FUNCTIONS[i + 1]
        start = AGB_MAIN if name == "AgbMain" else usa_start + delta
        end = usa_end + delta
        chunk = data[start:end]
        print(
            f"{name},0x{start:06X},0x{end:06X},{len(chunk)},{sha1(chunk)}"
        )


if __name__ == "__main__":
    main()
