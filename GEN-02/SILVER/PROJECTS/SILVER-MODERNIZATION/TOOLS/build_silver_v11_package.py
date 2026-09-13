#!/usr/bin/env python3
"""Build GitHub-safe v11 metadata from local Pokemon Silver ROM observations.

ROM images are read-only inputs and are never copied to the output tree.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zlib
from itertools import combinations
from pathlib import Path


RELEASES = {
    "AAXD": ("DE", "de", "Pokémon Silberne Edition", "Pokemon - Silberne Edition (Germany).gbc"),
    "AAXE": ("US-EU", "en", "Pokémon Silver Version", "Pokemon - Silver Version (USA, Europe).gbc"),
    "AAXF": ("FR", "fr", "Pokémon Version Argent", "Pokemon - Version Argent (France).gbc"),
    "AAXI": ("IT", "it", "Pokémon Versione Argento", "Pokemon - Versione Argento (Italy).gbc"),
    "AAXJ": ("JP", "ja", "ポケットモンスター 銀", None),
    "AAXK": ("KR", "ko", "포켓몬스터 은", "Pocket Monsters Eun (Korea).gbc"),
    "AAXS": ("ES", "es", "Pokémon Edición Plata", "Pokemon - Edicion Plata (Spain).gbc"),
}


def digest(data: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_rom(path: Path) -> dict:
    data = path.read_bytes()
    title = data[0x134:0x143].decode("ascii", "replace").rstrip("\0")
    technical_id = title[-4:]
    version = data[0x14C]
    release_id = f"{technical_id}-HV{version}"
    sha256 = digest(data, "sha256")
    header_checksum = 0
    for byte in data[0x134:0x14D]:
        header_checksum = (header_checksum - byte - 1) & 0xFF
    global_checksum = (sum(data) - data[0x14E] - data[0x14F]) & 0xFFFF
    banks = [data[offset:offset + 0x4000] for offset in range(0, len(data), 0x4000)]
    market, language, release_title, observed_filename = RELEASES[technical_id]
    if technical_id == "AAXJ":
        observed_filename = "Pocket Monsters Gin (Japan) (Rev A).gbc" if version else "Pocket Monsters Gin (Japan).gbc"
    return {
        "path": path,
        "data": data,
        "release_id": release_id,
        "technical_id": technical_id,
        "market": market,
        "language": language,
        "release_title": release_title,
        "dump_id": f"DUMP-SHA256-{sha256[:16].upper()}",
        "filename": observed_filename,
        "size_bytes": len(data),
        "bank_count": len(banks),
        "md5": digest(data, "md5"),
        "sha1": digest(data, "sha1"),
        "sha256": sha256,
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "internal_title": title,
        "cgb_flag": data[0x143],
        "new_licensee": data[0x144:0x146].decode("ascii", "replace"),
        "sgb_flag": data[0x146],
        "cartridge_type": data[0x147],
        "rom_size_code": data[0x148],
        "ram_size_code": data[0x149],
        "destination_code": data[0x14A],
        "old_licensee": data[0x14B],
        "header_version": version,
        "header_checksum": data[0x14D],
        "header_checksum_calculated": header_checksum,
        "header_checksum_valid": header_checksum == data[0x14D],
        "global_checksum": int.from_bytes(data[0x14E:0x150], "big"),
        "global_checksum_calculated": global_checksum,
        "global_checksum_valid": global_checksum == int.from_bytes(data[0x14E:0x150], "big"),
        "nintendo_logo_valid": data[0x104:0x134] == bytes.fromhex(
            "CEED6666CC0D000B03730083000C000D0008111F8889000EDCC"
            "C6EE6DDDDD999BBBB67636E0EECCCDDDC999FBBB9333E"
        ),
        "banks": banks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    roms = [parse_rom(path) for path in sorted(args.source_dir.glob("*.gbc"))]
    if len(roms) != 8:
        raise SystemExit(f"expected 8 Silver ROM observations, found {len(roms)}")
    if len({rom["sha256"] for rom in roms}) != 8:
        raise SystemExit("duplicate full-ROM SHA-256 detected")

    sakurai = args.output_dir / "Sakurai"
    tsubaki = args.output_dir / "Tsubaki"
    inventory_rows = []

    for rom in roms:
        coordinate = Path("GEN-02/SILVER/RELEASES/GBC/CART") / rom["release_id"]
        dump_coordinate = coordinate / "DUMPS" / rom["dump_id"]
        release = {
            "schema": "pokemon.release.v11",
            "release_id": rom["release_id"],
            "generation": "GEN-02",
            "game_id": "SILVER",
            "platform_id": "GBC",
            "package_kind": "CART",
            "technical_id": rom["technical_id"],
            "market": rom["market"],
            "language": rom["language"],
            "title": rom["release_title"],
            "header_version": rom["header_version"],
            "rom_binary_committed": False,
        }
        observation = {
            "schema": "pokemon.dump-observation.v11",
            "dump_id": rom["dump_id"],
            "release_id": rom["release_id"],
            "provenance": "user-upload",
            "observed_filename": rom["filename"],
            "size_bytes": rom["size_bytes"],
            "bank_size_bytes": 0x4000,
            "bank_count": rom["bank_count"],
            "hashes": {key: rom[key] for key in ("crc32", "md5", "sha1", "sha256")},
            "checksums": {
                "header_stored": f"0x{rom['header_checksum']:02X}",
                "header_calculated": f"0x{rom['header_checksum_calculated']:02X}",
                "header_valid": rom["header_checksum_valid"],
                "global_stored": f"0x{rom['global_checksum']:04X}",
                "global_calculated": f"0x{rom['global_checksum_calculated']:04X}",
                "global_valid": rom["global_checksum_valid"],
                "nintendo_logo_valid": rom["nintendo_logo_valid"],
            },
            "rom_binary_committed": False,
        }
        header = {
            "schema": "pokemon.gb-header-analysis.v1",
            "dump_id": rom["dump_id"],
            "internal_title": rom["internal_title"],
            "technical_id": rom["technical_id"],
            "cgb_flag": f"0x{rom['cgb_flag']:02X}",
            "new_licensee_code": rom["new_licensee"],
            "sgb_flag": f"0x{rom['sgb_flag']:02X}",
            "cartridge_type": f"0x{rom['cartridge_type']:02X}",
            "rom_size_code": f"0x{rom['rom_size_code']:02X}",
            "ram_size_code": f"0x{rom['ram_size_code']:02X}",
            "destination_code": f"0x{rom['destination_code']:02X}",
            "old_licensee_code": f"0x{rom['old_licensee']:02X}",
            "header_version": rom["header_version"],
        }
        bank_rows = [
            {
                "bank_hex": f"{index:02X}",
                "bank_index": index,
                "offset_start_hex": f"0x{index * 0x4000:06X}",
                "size_bytes": len(bank),
                "sha256": digest(bank, "sha256"),
            }
            for index, bank in enumerate(rom["banks"])
        ]
        for repository in (sakurai, tsubaki):
            write_json(repository / coordinate / "RELEASE.json", release)
            write_json(repository / dump_coordinate / "OBSERVATION.json", observation)
            write_json(repository / dump_coordinate / "ANALYSIS/GB-HEADER.json", header)
            write_csv(repository / dump_coordinate / "TABLES/ROM-BANK-SHA256.csv", bank_rows, list(bank_rows[0]))

        extraction_plan = {
            "schema": "tsubaki.extraction-plan.v11",
            "dump_id": rom["dump_id"],
            "source_release": coordinate.as_posix(),
            "source_sha256": rom["sha256"],
            "scope": "full-non-rom-production-extraction",
            "outputs": ["catalogs", "assets", "normalized", "converted", "implementation", "patches", "build-metadata", "verification"],
            "status": "registered",
            "rom_binary_committed": False,
        }
        write_json(tsubaki / dump_coordinate / "EXTRACTION/PLAN.json", extraction_plan)
        write_csv(tsubaki / dump_coordinate / "CATALOGS/ROM-BANKS.csv", bank_rows, list(bank_rows[0]))

        inventory_rows.append({
            "release_id": rom["release_id"], "dump_id": rom["dump_id"], "market": rom["market"],
            "language": rom["language"], "header_version": rom["header_version"], "size_bytes": rom["size_bytes"],
            "bank_count": rom["bank_count"], "crc32": rom["crc32"], "md5": rom["md5"],
            "sha1": rom["sha1"], "sha256": rom["sha256"], "header_checksum_valid": rom["header_checksum_valid"],
            "global_checksum_valid": rom["global_checksum_valid"], "rom_binary_committed": False,
        })

    compare = Path("GEN-02/SILVER/COMPARES/SUPPLIED-8-DUMP-CORPUS")
    compare_manifest = {
        "schema": "pokemon.compare.v11", "compare_id": "SUPPLIED-8-DUMP-CORPUS",
        "release_count": 7, "dump_count": 8,
        "release_ids": sorted({rom["release_id"] for rom in roms}),
        "dump_ids": [rom["dump_id"] for rom in roms], "rom_binary_committed": False,
    }
    pair_rows = []
    for left, right in combinations(roms, 2):
        common = min(len(left["data"]), len(right["data"]))
        differing = sum(a != b for a, b in zip(left["data"][:common], right["data"][:common]))
        equal_banks = sum(a == b for a, b in zip(left["banks"], right["banks"]))
        pair_rows.append({
            "left_release": left["release_id"], "right_release": right["release_id"],
            "left_dump": left["dump_id"], "right_dump": right["dump_id"],
            "common_bytes": common, "differing_bytes_in_common_span": differing,
            "size_delta_bytes": right["size_bytes"] - left["size_bytes"],
            "common_bank_count": min(left["bank_count"], right["bank_count"]), "byte_identical_banks": equal_banks,
        })
    for repository in (sakurai, tsubaki):
        write_json(repository / compare / "MANIFEST.json", compare_manifest)
        write_csv(repository / compare / "TABLES/INVENTORY.csv", inventory_rows, list(inventory_rows[0]))
        write_csv(repository / compare / "TABLES/PAIRWISE-ROM-COMPARISON.csv", pair_rows, list(pair_rows[0]))

    project = Path("GEN-02/SILVER/PROJECTS/SILVER-MODERNIZATION")
    pins = [{"release_id": rom["release_id"], "dump_id": rom["dump_id"], "sha256": rom["sha256"]} for rom in roms]
    project_manifest = {
        "schema": "pokemon.project.v11", "project_id": "SILVER-MODERNIZATION",
        "game_id": "SILVER", "input_pins": pins, "rom_binary_committed": False,
    }
    write_json(sakurai / project / "PROJECT.json", project_manifest)
    write_json(tsubaki / project / "PROJECT.json", project_manifest)
    print(json.dumps({"roms": len(roms), "sakurai_files": sum(p.is_file() for p in sakurai.rglob('*')),
                      "tsubaki_files": sum(p.is_file() for p in tsubaki.rglob('*'))}))


if __name__ == "__main__":
    main()
