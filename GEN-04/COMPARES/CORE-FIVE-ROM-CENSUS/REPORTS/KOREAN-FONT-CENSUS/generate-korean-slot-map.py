#!/usr/bin/env python3
"""Regenerate the inferred Gen IV Korean 3440-slot Unicode map.

The mapping is evidence-driven but remains marked inferred until message-code
correlation confirms the executable/text encoding path.
"""
import csv
import sys


def decode_pair(hi, lo):
    raw = bytes((hi, lo))
    try:
        return raw.decode("euc_kr")
    except UnicodeDecodeError:
        return ""


def rows():
    for slot in range(3440):
        if slot <= 508:
            yield slot, "legacy_base", "", "", ""
        elif slot <= 1023:
            yield slot, "fallback_reserved", "", "", ""
        elif slot <= 3373:
            n = slot - 1024
            hi = 0xB0 + n // 94
            lo = 0xA1 + n % 94
            ch = decode_pair(hi, lo)
            yield slot, "ks_x_1001_hangul_inferred", f"{hi:02X}{lo:02X}", ch, f"U+{ord(ch):04X}" if ch else ""
        elif slot in (3374, 3375):
            yield slot, "fallback_or_unmapped", "", "", ""
        elif slot <= 3426:
            n = slot - 3376
            hi, lo = 0xA4, 0xA1 + n
            ch = decode_pair(hi, lo)
            yield slot, "ks_x_1001_compat_jamo_inferred", f"{hi:02X}{lo:02X}", ch, f"U+{ord(ch):04X}" if ch else ""
        elif slot <= 3428:
            yield slot, "nonfallback_unmapped_requires_message_correlation", "", "", ""
        else:
            yield slot, "fallback_or_unmapped", "", "", ""


w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(("slot", "class", "euc_kr_hex", "character", "unicode"))
w.writerows(rows())
