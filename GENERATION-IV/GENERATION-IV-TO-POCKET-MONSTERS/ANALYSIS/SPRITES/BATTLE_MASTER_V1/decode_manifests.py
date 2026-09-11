#!/usr/bin/env python3
from pathlib import Path
import base64, zlib, hashlib

FILES = {
    "logical_slots.csv": ["logical_slots.csv.zlib.b85.part01", "logical_slots.csv.zlib.b85.part02"],
    "asset_index.csv": ["asset_index.csv.zlib.b85"],
    "atlas_map.csv": ["atlas_map.csv.zlib.b85"],
    "otherpoke_member_inventory.csv": ["otherpoke_member_inventory.csv.zlib.b85"],
}
EXPECTED = {
    "logical_slots.csv": "d74ac5170bd634b0012472b5e2ddd9a9936f74d1512c9289a94e145635db28eb",
    "asset_index.csv": "b0ca754e7bb9ad1db605ad83f603ad9ca06f5c50b874f06f07160b18a65f99b6",
    "atlas_map.csv": "35c5e6b5c2c7724f02d1884efba260de935c1c370a11e4a88351255a8f2c97f6",
    "otherpoke_member_inventory.csv": "f5b55491ca04fb88f082674279d5532baba0f3ade520cbcafd28a865fd5ba4c1",
}
base=Path(__file__).resolve().parent
for target, parts in FILES.items():
    encoded=b"".join((base/p).read_bytes() for p in parts)
    raw=zlib.decompress(base64.b85decode(encoded))
    got=hashlib.sha256(raw).hexdigest()
    if got != EXPECTED[target]:
        raise SystemExit(f"SHA-256 mismatch for {target}: {got}")
    (base/target).write_bytes(raw)
    print(target, len(raw), got)
