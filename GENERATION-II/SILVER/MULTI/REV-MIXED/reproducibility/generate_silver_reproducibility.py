#!/usr/bin/env python3
"""Generate a byte-exact, ROM-free reproducibility corpus for Pokémon Silver targets.

The source ROMs stay local. This script identifies them by SHA-256 and writes only
metadata, CSV maps, RGBDS INCBIN scaffolds, and verification/generation scripts.
Generated bank binaries and rebuilt ROMs are intentionally git-ignored.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import zlib
from collections import Counter, defaultdict
from pathlib import Path

BANK_SIZE = 0x4000
PREFIX = Path("GENERATION-II") / "SILVER"
TARGETS = [
    {"language_region":"JP", "revision":"REV-0", "sha256":"0a532063a3ff5750a464582aa7bbee2b6d42e1a92a136d9f4590e373487b615c", "size":1048576, "reference_filename":"Pocket Monsters Gin (Japan).gbc"},
    {"language_region":"JP", "revision":"REV-A", "sha256":"99e5267fbf5a7748d4f3b75ba1990cb5d91348339468607a04bfbc6081c62d71", "size":1048576, "reference_filename":"Pocket Monsters Gin (Japan) (Rev A).gbc"},
    {"language_region":"USA-EUROPE", "revision":"REV-0", "sha256":"72b190859a59623cbef6c49d601f8de52c1d2331b4f08a8d2acc17274fc19a8c", "size":2097152, "reference_filename":"Pokemon - Silver Version (USA, Europe).gbc"},
    {"language_region":"DE", "revision":"REV-0", "sha256":"c3d1fd0dec1d5fa9aa7f85275e79c52aa9175d191c63cbed7b406c306d946348", "size":2097152, "reference_filename":"Pokemon - Silberne Edition (Germany).gbc"},
    {"language_region":"FR", "revision":"REV-0", "sha256":"e120c4ddb0dc3e25b95c9c71b3ffd59ff57ce689cf4d79d04913ba59140c18c2", "size":2097152, "reference_filename":"Pokemon - Version Argent (France).gbc"},
    {"language_region":"IT", "revision":"REV-0", "sha256":"04c442246d1ae0ed6bf5e072bb7e3d06376e584b953d6b14047b39e45fbb0cb4", "size":2097152, "reference_filename":"Pokemon - Versione Argento (Italy).gbc"},
    {"language_region":"ES", "revision":"REV-0", "sha256":"6797010c052e8f9373ea2b9e855ec078b34fda12e5ccf742eb19bb5e8f6947c2", "size":2097152, "reference_filename":"Pokemon - Edicion Plata (Spain).gbc"},
    {"language_region":"KR", "revision":"REV-0", "sha256":"ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22", "size":2097152, "reference_filename":"Pocket Monsters Eun (Korea).gbc"},
]


def digest(data: bytes, name: str) -> str:
    return hashlib.new(name, data).hexdigest()


def entropy(data: bytes) -> float:
    counts = Counter(data)
    n = len(data)
    return -sum((v / n) * math.log2(v / n) for v in counts.values()) if n else 0.0


def header_checksum(data: bytes) -> int:
    x = 0
    for v in data[0x134:0x14D]:
        x = (x - v - 1) & 0xFF
    return x


def global_checksum(data: bytes) -> int:
    return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF


def parse_header(data: bytes) -> dict:
    title_raw = data[0x134:0x144]
    title = ''.join(chr(x) if 32 <= x < 127 else f'\\x{x:02X}' for x in title_raw).rstrip('\\x00')
    return {
        "entry_point_hex": data[0x100:0x104].hex(),
        "title_raw_hex": title_raw.hex(),
        "title_ascii_escaped": title,
        "cgb_flag": f"0x{data[0x143]:02X}",
        "new_licensee_raw_hex": data[0x144:0x146].hex(),
        "sgb_flag": f"0x{data[0x146]:02X}",
        "cartridge_type": f"0x{data[0x147]:02X}",
        "rom_size_code": f"0x{data[0x148]:02X}",
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
    }


def fill_runs(data: bytes, minimum: int = 64):
    i = 0
    while i < len(data):
        value = data[i]
        if value not in (0x00, 0xFF):
            i += 1
            continue
        j = i + 1
        while j < len(data) and data[j] == value:
            j += 1
        if j - i >= minimum:
            yield i, j - i, value
        i = j


def discover_sources(rom_dir: Path) -> dict[str, Path]:
    expected = {t["sha256"]: t for t in TARGETS}
    found: dict[str, Path] = {}
    candidates = [p for p in rom_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".gbc", ".gb"}]
    for path in candidates:
        data = path.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        if h in expected:
            found[h] = path
    missing = [t for t in TARGETS if t["sha256"] not in found]
    if missing:
        names = '\n'.join(f"  - {t['language_region']} {t['revision']} {t['sha256']}" for t in missing)
        raise SystemExit(f"Missing {len(missing)} required ROM(s) in {rom_dir}:\n{names}")
    return found


def make_layout(bank_count: int) -> str:
    lines = [
        "; Pokémon Silver byte-exact physical-bank scaffold",
        "; Requires local baserom.gbc. This file stores no ROM bytes.",
        "",
    ]
    for bank in range(bank_count):
        offset = bank * BANK_SIZE
        if bank == 0:
            lines += [f'SECTION "bank {bank:02X}", ROM0[$0000]', f'    INCBIN "baserom.gbc", ${offset:06X}, $4000', '']
        else:
            lines += [f'SECTION "bank {bank:02X}", ROMX[$4000], BANK[${bank:02X}]', f'    INCBIN "baserom.gbc", ${offset:06X}, $4000', '']
    return '\n'.join(lines)


def make_verify(expected_sha: str, expected_size: int) -> str:
    return f'''#!/usr/bin/env python3\nfrom pathlib import Path\nimport hashlib, sys\nEXPECTED_SHA256={expected_sha!r}\nEXPECTED_SIZE={expected_size}\n\ndef hc(d):\n    x=0\n    for v in d[0x134:0x14D]: x=(x-v-1)&0xff\n    return x\n\ndef gc(d): return (sum(d[:0x14E])+sum(d[0x150:]))&0xffff\n\np=Path(sys.argv[1] if len(sys.argv)>1 else 'baserom.gbc')\nd=p.read_bytes(); h=hashlib.sha256(d).hexdigest(); ok=True\nif len(d)!=EXPECTED_SIZE: print('FAIL size',len(d),EXPECTED_SIZE); ok=False\nif h!=EXPECTED_SHA256: print('FAIL sha256',h,EXPECTED_SHA256); ok=False\nhs,hh=d[0x14D],hc(d); gs=int.from_bytes(d[0x14E:0x150],'big'); gg=gc(d)\nprint(f'size={{len(d)}} sha256={{h}}')\nprint(f'header checksum stored={{hs:02X}} computed={{hh:02X}} valid={{hs==hh}}')\nprint(f'global checksum stored={{gs:04X}} computed={{gg:04X}} valid={{gs==gg}}')\nok &= hs==hh and gs==gg\nraise SystemExit(0 if ok else 1)\n'''


def make_reproduce(expected_sha: str, bank_count: int) -> str:
    return f'''#!/usr/bin/env python3\nfrom pathlib import Path\nimport hashlib, sys\nBANK_SIZE=0x4000\nEXPECTED_SHA256={expected_sha!r}\nEXPECTED_BANKS={bank_count}\n\ndef split():\n    d=Path('baserom.gbc').read_bytes(); out=Path('generated/banks'); out.mkdir(parents=True,exist_ok=True)\n    if len(d)!=EXPECTED_BANKS*BANK_SIZE: raise SystemExit('unexpected ROM size')\n    for n in range(EXPECTED_BANKS): (out/f'bank_{{n:02X}}.bin').write_bytes(d[n*BANK_SIZE:(n+1)*BANK_SIZE])\n    print('wrote',EXPECTED_BANKS,'banks')\n\ndef join():\n    src=Path('generated/banks'); out=Path('build/rejoined.gbc'); out.parent.mkdir(parents=True,exist_ok=True)\n    d=b''.join((src/f'bank_{{n:02X}}.bin').read_bytes() for n in range(EXPECTED_BANKS)); out.write_bytes(d)\n    h=hashlib.sha256(d).hexdigest(); print('sha256',h,'match',h==EXPECTED_SHA256)\n    raise SystemExit(0 if h==EXPECTED_SHA256 else 1)\n\ncmd=sys.argv[1] if len(sys.argv)>1 else 'split'\nif cmd=='split': split()\nelif cmd=='join': join()\nelse: raise SystemExit('usage: reproduce.py split|join')\n'''


def make_makefile() -> str:
    return '''PYTHON ?= python3\nRGBASM ?= rgbasm\nRGBLINK ?= rgblink\n.PHONY: verify split join rgbds clean\nverify:\n\t$(PYTHON) verify_rom.py baserom.gbc\nsplit:\n\t$(PYTHON) reproduce.py split\njoin:\n\t$(PYTHON) reproduce.py join\nrgbds: verify\n\tmkdir -p build\n\t$(RGBASM) -o build/layout.o layout.asm\n\t$(RGBLINK) -o build/rebuilt.gbc build/layout.o\n\t$(PYTHON) verify_rom.py build/rebuilt.gbc\nclean:\n\trm -rf build generated\n'''


def write_target(out_root: Path, target: dict, source: Path, data: bytes) -> tuple[dict, list[str]]:
    lang, rev = target["language_region"], target["revision"]
    target_dir = out_root / PREFIX / lang / rev / "reproducibility"
    target_dir.mkdir(parents=True, exist_ok=True)
    header = parse_header(data)
    bank_count = len(data) // BANK_SIZE
    manifest = {
        "project": "Pokémon Silver reproducibility baseline",
        "language_region": lang,
        "revision": rev,
        "source_filename_reference": target["reference_filename"],
        "matched_local_filename": source.name,
        "rom_binary_included": False,
        "size_bytes": len(data),
        "bank_size_bytes": BANK_SIZE,
        "bank_count": bank_count,
        "hashes": {
            "sha256": digest(data, "sha256"),
            "sha1": digest(data, "sha1"),
            "md5": digest(data, "md5"),
            "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        },
        "header": header,
        "policy": "ROM stays local; generated binary banks/build outputs are ignored.",
    }
    (target_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding="utf-8")
    (target_dir / "header.json").write_text(json.dumps(header, indent=2, ensure_ascii=False) + '\n', encoding="utf-8")
    (target_dir / "expected.sha256").write_text(f"{target['sha256']}  baserom.gbc\n", encoding="utf-8")

    rows = []
    bank_hashes = []
    zero_banks = []
    for bank in range(bank_count):
        chunk = data[bank * BANK_SIZE:(bank + 1) * BANK_SIZE]
        counts = Counter(chunk)
        bh = digest(chunk, "sha256")
        bank_hashes.append(bh)
        if counts[0] == BANK_SIZE:
            zero_banks.append(f"{bank:02X}")
        rows.append({
            "bank_hex": f"{bank:02X}",
            "file_offset_start": f"0x{bank * BANK_SIZE:06X}",
            "file_offset_end": f"0x{(bank + 1) * BANK_SIZE - 1:06X}",
            "cpu_addr_start": "$0000" if bank == 0 else "$4000",
            "cpu_addr_end": "$3FFF" if bank == 0 else "$7FFF",
            "sha256": bh,
            "crc32": f"{zlib.crc32(chunk) & 0xFFFFFFFF:08x}",
            "entropy_bits_per_byte": f"{entropy(chunk):.6f}",
            "zero_bytes": counts[0],
            "ff_bytes": counts[255],
            "non_00_ff_bytes": BANK_SIZE - counts[0] - counts[255],
            "full_zero": counts[0] == BANK_SIZE,
            "full_ff": counts[255] == BANK_SIZE,
        })
    with (target_dir / "banks.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

    fill_rows = [{
        "value": f"0x{value:02X}", "start_offset": f"0x{offset:06X}",
        "end_offset": f"0x{offset + length - 1:06X}", "length": length,
        "start_bank": f"{offset // BANK_SIZE:02X}", "end_bank": f"{(offset + length - 1) // BANK_SIZE:02X}",
    } for offset, length, value in fill_runs(data)]
    with (target_dir / "fill_runs_ge64.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["value", "start_offset", "end_offset", "length", "start_bank", "end_bank"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(fill_rows)

    (target_dir / "layout.asm").write_text(make_layout(bank_count), encoding="utf-8")
    (target_dir / "verify_rom.py").write_text(make_verify(target["sha256"], len(data)), encoding="utf-8")
    (target_dir / "reproduce.py").write_text(make_reproduce(target["sha256"], bank_count), encoding="utf-8")
    (target_dir / "Makefile").write_text(make_makefile(), encoding="utf-8")
    (target_dir / ".gitignore").write_text("baserom.gbc\nbuild/\ngenerated/\n*.gbc\n*.gb\n*.bin\n*.o\n", encoding="utf-8")
    (target_dir / "README.md").write_text(
        f"# Pokémon Silver {lang} {rev} reproducibility baseline\n\n"
        f"Exact SHA-256: `{target['sha256']}`  \n"
        f"Size: {len(data)} bytes / {bank_count} physical 16 KiB banks.  \n"
        f"Fully-zero bank candidates: {', '.join(zero_banks) if zero_banks else 'none'}.\n\n"
        "This directory contains no ROM bytes. Copy the matching local ROM here as `baserom.gbc`, then run `make verify`, `make split`, `make join`, or (with RGBDS installed) `make rgbds`. `banks.csv` covers every physical ROM bank. `fill_runs_ge64.csv` is only a fill-space candidate list; a separate reference analysis is required before reusing any range.\n",
        encoding="utf-8",
    )
    return manifest, bank_hashes


def write_cross_version(out_root: Path, records: list[dict], data_by_label: dict[str, bytes], bank_hashes: dict[str, list[str]]):
    d = out_root / PREFIX / "MULTI" / "REV-MIXED" / "reproducibility"
    d.mkdir(parents=True, exist_ok=True)
    (d / "rom_set_manifest.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + '\n', encoding="utf-8")
    labels = list(data_by_label)

    pair_rows = []
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            da, db = data_by_label[a], data_by_label[b]
            shared = min(len(da), len(db))
            shared_banks = shared // BANK_SIZE
            pair_rows.append({
                "a": a, "b": b, "size_a": len(da), "size_b": len(db), "compared_bytes": shared,
                "differing_bytes_in_overlap": sum(x != y for x, y in zip(da[:shared], db[:shared])),
                "identical_16k_banks_in_overlap": sum(bank_hashes[a][n] == bank_hashes[b][n] for n in range(shared_banks)),
                "overlap_bank_count": shared_banks,
            })
    with (d / "pairwise_diff_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=pair_rows[0].keys()); w.writeheader(); w.writerows(pair_rows)

    eq_rows = []
    for bank in range(max(map(len, bank_hashes.values()))):
        groups = defaultdict(list)
        for label, hashes in bank_hashes.items():
            if bank < len(hashes): groups[hashes[bank]].append(label)
        for h, members in groups.items():
            eq_rows.append({"bank_hex": f"{bank:02X}", "sha256": h, "members": ";".join(members), "member_count": len(members)})
    with (d / "bank_equivalence.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["bank_hex", "sha256", "members", "member_count"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(eq_rows)

    a, b = data_by_label["JP_REV-0"], data_by_label["JP_REV-A"]
    ranges = []
    i = 0
    while i < len(a):
        if a[i] == b[i]: i += 1; continue
        j = i + 1
        while j < len(a) and a[j] != b[j]: j += 1
        ranges.append({"start_offset": f"0x{i:06X}", "end_offset": f"0x{j - 1:06X}", "length": j - i, "start_bank": f"{i // BANK_SIZE:02X}", "end_bank": f"{(j - 1) // BANK_SIZE:02X}"})
        i = j
    with (d / "jp_rev0_vs_reva_diff_ranges.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["start_offset", "end_offset", "length", "start_bank", "end_bank"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(ranges)

    cohorts = {
        "all_8_within_first_64": labels,
        "western_5": ["USA-EUROPE_REV-0", "DE_REV-0", "FR_REV-0", "IT_REV-0", "ES_REV-0"],
        "international_6_plus_kr": ["USA-EUROPE_REV-0", "DE_REV-0", "FR_REV-0", "IT_REV-0", "ES_REV-0", "KR_REV-0"],
    }
    common = {}
    for name, members in cohorts.items():
        nbank = min(len(data_by_label[x]) // BANK_SIZE for x in members)
        free = [f"{bank:02X}" for bank in range(nbank) if all(data_by_label[x][bank * BANK_SIZE:(bank + 1) * BANK_SIZE] == bytes(BANK_SIZE) for x in members)]
        common[name] = {"bank_count": len(free), "banks_hex": free, "bytes": len(free) * BANK_SIZE}
    (d / "common_full_zero_banks.json").write_text(json.dumps(common, indent=2) + '\n', encoding="utf-8")
    (d / "README.md").write_text(
        "# Pokémon Silver multi-ROM reproducibility layer\n\n"
        "Cross-version bank hashes, pairwise byte differences, JP revision change ranges, and shared full-zero bank candidates. No ROM bytes are stored. The byte-exact layer is intentionally semantic-free: code/text/graphics/data labels are added later without changing source identities.\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True, help="directory containing the 8 source ROMs (names may differ; SHA-256 is authoritative)")
    ap.add_argument("--out-root", type=Path, default=Path("."), help="repository/work root; GENERATION-II/SILVER/... is created below it")
    ap.add_argument("--clean", action="store_true", help="remove the existing SILVER reproducibility output paths before regenerating")
    args = ap.parse_args()
    sources = discover_sources(args.rom_dir)
    if args.clean:
        for t in TARGETS:
            shutil.rmtree(args.out_root / PREFIX / t["language_region"] / t["revision"] / "reproducibility", ignore_errors=True)
        shutil.rmtree(args.out_root / PREFIX / "MULTI" / "REV-MIXED" / "reproducibility", ignore_errors=True)

    records, data_by_label, hashes_by_label = [], {}, {}
    for t in TARGETS:
        src = sources[t["sha256"]]
        data = src.read_bytes()
        if len(data) != t["size"] or hashlib.sha256(data).hexdigest() != t["sha256"]:
            raise SystemExit(f"identity changed while reading {src}")
        manifest, hashes = write_target(args.out_root, t, src, data)
        records.append(manifest)
        label = f"{t['language_region']}_{t['revision']}"
        data_by_label[label] = data
        hashes_by_label[label] = hashes
    write_cross_version(args.out_root, records, data_by_label, hashes_by_label)
    print(f"Generated reproducibility corpus under {args.out_root / PREFIX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
