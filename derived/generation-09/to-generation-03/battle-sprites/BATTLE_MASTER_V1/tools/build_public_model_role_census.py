#!/usr/bin/env python3
"""Build a deterministic Generation IX public model-role census.

This parser consumes the generated config trees from freedom12/PokemonModelViewer.
It deliberately preserves that project's neutral `formIndex` / `variantIndex`
field names. It does NOT reinterpret them as game-native `form` / `gender`
until a resource-catalog cross-check proves that mapping.

The output is research/control data only. It is not a game-native catalog and
is not sufficient by itself to declare a Generation III battle sprite final.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SOURCE_REPO = "freedom12/PokemonModelViewer"
RESOURCE_ID_RE = re.compile(r"^pm(?P<species>\d{4})_(?P<form>\d{2})_(?P<variant>\d{2})$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def classify_animation_names(names: list[str]) -> dict[str, bool]:
    low = [x.lower() for x in names]
    return {
        "has_default_wait": any("defaultwait" in x for x in low),
        "has_battle_wait": any("battlewait" in x for x in low),
        "has_attack": any("attack" in x for x in low),
        "has_damage": any("damage" in x for x in low),
        "has_eye_track": any("eye" in x for x in low),
        "has_mouth_track": any("mouth" in x for x in low),
    }


def load_json(path: Path) -> tuple[object, str]:
    data = path.read_bytes()
    return json.loads(data.decode("utf-8")), sha256_bytes(data)


def int_or_none(value: object) -> int | None:
    return value if isinstance(value, int) else None


def build(config_root: Path, family: str, source_commit: str, out_dir: Path) -> None:
    index_path = config_root / "index.json"
    index, index_sha = load_json(index_path)
    if not isinstance(index, dict) or not isinstance(index.get("pokemonIds"), list):
        raise ValueError(f"unexpected index schema: {index_path}")

    rows: list[dict[str, object]] = []
    missing_configs: list[str] = []
    source_config_hashes: list[tuple[str, str]] = []

    for pokemon_id in index["pokemonIds"]:
        if not isinstance(pokemon_id, str):
            continue
        cfg_path = config_root / f"{pokemon_id}.json"
        if not cfg_path.is_file():
            missing_configs.append(pokemon_id)
            continue

        cfg, cfg_sha = load_json(cfg_path)
        source_config_hashes.append((cfg_path.name, cfg_sha))
        if not isinstance(cfg, dict):
            raise ValueError(f"unexpected config schema: {cfg_path}")

        species_number = cfg.get("number")
        forms = cfg.get("forms") or []
        if not isinstance(forms, list):
            raise ValueError(f"forms is not a list: {cfg_path}")

        for entry in forms:
            if not isinstance(entry, dict):
                continue
            resource_id = str(entry.get("id", ""))
            parsed = RESOURCE_ID_RE.match(resource_id)
            id_species = int(parsed.group("species")) if parsed else None
            id_form = int(parsed.group("form")) if parsed else None
            id_variant = int(parsed.group("variant")) if parsed else None

            form_index = entry.get("formIndex")
            variant_index = entry.get("variantIndex")
            animations = entry.get("animations") or {}
            if not isinstance(animations, dict):
                animations = {}
            animation_names = sorted(str(k) for k in animations.keys())
            animation_file_count = sum(len(v) for v in animations.values() if isinstance(v, list))
            flags = classify_animation_names(animation_names)

            consistency: list[str] = []
            if isinstance(species_number, int) and id_species is not None and species_number != id_species:
                consistency.append("species_number!=resource_id")
            if isinstance(form_index, int) and id_form is not None and form_index != id_form:
                consistency.append("formIndex!=resource_id")
            if isinstance(variant_index, int) and id_variant is not None and variant_index != id_variant:
                consistency.append("variantIndex!=resource_id")

            row: dict[str, object] = {
                "family": family,
                "pokemon_id": pokemon_id,
                "species_number": species_number,
                "resource_id": resource_id,
                "config_form_index": form_index,
                "config_variant_index": variant_index,
                "game_form": "UNRESOLVED",
                "game_gender": "UNRESOLVED",
                "normal_shiny_role": "UNRESOLVED",
                "icon_path": entry.get("icon", ""),
                "animation_name_count": len(animation_names),
                "animation_file_count": animation_file_count,
                "animation_names_sha256": canonical_json_sha256(animation_names),
                "has_default_wait": flags["has_default_wait"],
                "has_battle_wait": flags["has_battle_wait"],
                "has_attack": flags["has_attack"],
                "has_damage": flags["has_damage"],
                "has_eye_track": flags["has_eye_track"],
                "has_mouth_track": flags["has_mouth_track"],
                "source_config_path": f"assets/local/configs/{family}/{cfg_path.name}",
                "source_config_sha256": cfg_sha,
                "source_repo": SOURCE_REPO,
                "source_commit": source_commit,
                "source_status": "public-derived-model-viewer-config-not-game-native-catalog",
                "canonical_source_status": "CROSSCHECK_PENDING",
                "consistency_flags": ";".join(consistency),
            }
            rows.append(row)

    rows.sort(key=lambda r: (
        int(r["species_number"]) if isinstance(r["species_number"], int) else 99999,
        int(r["config_form_index"]) if isinstance(r["config_form_index"], int) else 99999,
        int(r["config_variant_index"]) if isinstance(r["config_variant_index"], int) else 99999,
        str(r["resource_id"]),
    ))

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{family}_PUBLIC_MODEL_ROLE_CENSUS.csv"
    fieldnames = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)

    species_with_rows = sorted({int(r["species_number"]) for r in rows if isinstance(r["species_number"], int)})
    duplicate_resource_ids: dict[str, int] = {}
    for row in rows:
        rid = str(row["resource_id"])
        duplicate_resource_ids[rid] = duplicate_resource_ids.get(rid, 0) + 1
    duplicate_resource_ids = {k: v for k, v in duplicate_resource_ids.items() if v > 1}

    form_index_counts = Counter(str(r["config_form_index"]) for r in rows)
    variant_index_counts = Counter(str(r["config_variant_index"]) for r in rows)
    roles_per_species = Counter(
        int(r["species_number"]) for r in rows if isinstance(r["species_number"], int)
    )
    multi_resource_species = {str(k): v for k, v in sorted(roles_per_species.items()) if v > 1}
    top_species_by_resource_roles = [
        {"species_number": species, "resource_roles": count}
        for species, count in sorted(roles_per_species.items(), key=lambda kv: (-kv[1], kv[0]))[:25]
    ]
    consistency_issue_rows = [str(r["resource_id"]) for r in rows if r["consistency_flags"]]
    nonzero_form_rows = [r for r in rows if int_or_none(r["config_form_index"]) not in (None, 0)]
    nonzero_variant_rows = [r for r in rows if int_or_none(r["config_variant_index"]) not in (None, 0)]

    form_values = [x for x in (int_or_none(r["config_form_index"]) for r in rows) if x is not None]
    variant_values = [x for x in (int_or_none(r["config_variant_index"]) for r in rows) if x is not None]

    tree_material = "\n".join(f"{name}\t{digest}" for name, digest in sorted(source_config_hashes)).encode("utf-8")
    summary = {
        "schema_version": 2,
        "family": family,
        "source_repo": SOURCE_REPO,
        "source_commit": source_commit,
        "source_index_path": f"assets/local/configs/{family}/index.json",
        "source_index_sha256": index_sha,
        "source_config_tree_sha256": sha256_bytes(tree_material),
        "pokemon_ids_in_index": len(index["pokemonIds"]),
        "pokemon_ids_with_config": len(source_config_hashes),
        "missing_config_count": len(missing_configs),
        "missing_configs": missing_configs,
        "species_with_resource_rows": len(species_with_rows),
        "resource_role_rows": len(rows),
        "unique_resource_ids": len({str(r["resource_id"]) for r in rows}),
        "duplicate_resource_ids": duplicate_resource_ids,
        "species_with_multiple_resource_roles": len(multi_resource_species),
        "multi_resource_species": multi_resource_species,
        "top_species_by_resource_roles": top_species_by_resource_roles,
        "config_form_index_counts": dict(sorted(form_index_counts.items(), key=lambda kv: int(kv[0]))),
        "config_variant_index_counts": dict(sorted(variant_index_counts.items(), key=lambda kv: int(kv[0]))),
        "rows_with_nonzero_config_form_index": len(nonzero_form_rows),
        "rows_with_nonzero_config_variant_index": len(nonzero_variant_rows),
        "max_config_form_index": max(form_values) if form_values else None,
        "max_config_variant_index": max(variant_values) if variant_values else None,
        "consistency_issue_count": len(consistency_issue_rows),
        "consistency_issue_resource_ids": consistency_issue_rows,
        "rows_with_icons": sum(bool(r["icon_path"]) for r in rows),
        "rows_with_default_wait": sum(bool(r["has_default_wait"]) for r in rows),
        "rows_with_battle_wait": sum(bool(r["has_battle_wait"]) for r in rows),
        "rows_with_attack": sum(bool(r["has_attack"]) for r in rows),
        "rows_with_damage": sum(bool(r["has_damage"]) for r in rows),
        "rows_with_eye_track": sum(bool(r["has_eye_track"]) for r in rows),
        "rows_with_mouth_track": sum(bool(r["has_mouth_track"]) for r in rows),
        "total_animation_names": sum(int(r["animation_name_count"]) for r in rows),
        "total_animation_files": sum(int(r["animation_file_count"]) for r in rows),
        "semantic_warning": (
            "config_form_index/config_variant_index are preserved exactly as named by the public source. "
            "Do not relabel them as game form/gender until poke_resource_table cross-checking proves the mapping."
        ),
        "authority_warning": (
            "This census is derived from a public model-viewer configuration tree, not from the retail game catalog. "
            "It is secondary evidence for exhaustive role discovery and animation inventory."
        ),
    }
    (out_dir / f"{family}_PUBLIC_MODEL_ROLE_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    provenance = {
        "schema_version": 1,
        "generated_from": SOURCE_REPO,
        "source_commit": source_commit,
        "family": family,
        "index_sha256": index_sha,
        "config_files": [
            {"path": f"assets/local/configs/{family}/{name}", "sha256": digest}
            for name, digest in sorted(source_config_hashes)
        ],
    }
    (out_dir / f"{family}_PUBLIC_MODEL_ROLE_PROVENANCE.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-root", required=True, type=Path)
    parser.add_argument("--family", required=True, choices=["SCVI", "LZA"])
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    build(args.config_root, args.family, args.source_commit, args.out_dir)


if __name__ == "__main__":
    main()
