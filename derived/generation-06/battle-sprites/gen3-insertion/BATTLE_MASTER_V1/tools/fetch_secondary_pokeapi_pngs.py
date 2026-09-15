#!/usr/bin/env python3
"""Fetch small batches of secondary Generation VI PNG evidence from PokeAPI/sprites.

These files are *not* the Generation VI model-based battle master source. They are
stored/used only as secondary visual evidence under SECONDARY_PNG_POLICY.md.

The script has no Pillow dependency. PNG width/height are read directly from IHDR.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import struct
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


BASE = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
    "sprites/pokemon/versions/generation-vi"
)

VARIANT_PATHS = {
    "default": "{species}.png",
    "female": "female/{species}.png",
    "shiny": "shiny/{species}.png",
    "shiny-female": "shiny/female/{species}.png",
}

GAME_VARIANTS = {
    "x-y": "x-y",
    "omegaruby-alphasapphire": "omegaruby-alphasapphire",
}

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass(frozen=True)
class FetchResult:
    species: int
    variant: str
    url: str
    status: str
    byte_size: int | None = None
    width: int | None = None
    height: int | None = None
    sha256: str | None = None
    output_path: str | None = None
    note: str = ""


def parse_species_range(value: str) -> list[int]:
    result: list[int] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if end < start:
                raise ValueError(f"inverted species range: {part}")
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    if not result:
        raise ValueError("no species specified")
    if any(not 1 <= species <= 721 for species in result):
        raise ValueError("Generation VI evidence fetch only accepts species 1..721")
    return sorted(set(result))


def png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG")
    if data[12:16] != b"IHDR":
        raise ValueError("PNG IHDR is not first chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width <= 0 or height <= 0:
        raise ValueError("invalid PNG dimensions")
    return width, height


def build_url(game_variant: str, species: int, variant: str) -> str:
    relative = VARIANT_PATHS[variant].format(species=species)
    return f"{BASE}/{GAME_VARIANTS[game_variant]}/{relative}"


def build_destination(root: Path, species: int, variant: str) -> Path:
    if variant == "default":
        return root / f"{species}.png"
    if variant == "female":
        return root / "female" / f"{species}.png"
    if variant == "shiny":
        return root / "shiny" / f"{species}.png"
    if variant == "shiny-female":
        return root / "shiny" / "female" / f"{species}.png"
    raise ValueError(f"unknown variant: {variant}")


def fetch_one(
    game_variant: str,
    species: int,
    variant: str,
    output_root: Path,
    overwrite: bool,
    timeout: float,
) -> FetchResult:
    url = build_url(game_variant, species, variant)
    destination = build_destination(output_root, species, variant)

    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return FetchResult(
                species=species,
                variant=variant,
                url=url,
                status="missing-public-source",
                note="HTTP 404; variant may be not applicable or absent upstream",
            )
        return FetchResult(
            species=species,
            variant=variant,
            url=url,
            status="fetch-error",
            note=f"HTTP {exc.code}: {exc.reason}",
        )
    except (urllib.error.URLError, TimeoutError) as exc:
        return FetchResult(
            species=species,
            variant=variant,
            url=url,
            status="fetch-error",
            note=str(exc),
        )

    try:
        width, height = png_dimensions(data)
    except ValueError as exc:
        return FetchResult(
            species=species,
            variant=variant,
            url=url,
            status="invalid-source",
            byte_size=len(data),
            sha256=hashlib.sha256(data).hexdigest(),
            note=str(exc),
        )

    sha256 = hashlib.sha256(data).hexdigest()

    if destination.exists() and not overwrite:
        existing = destination.read_bytes()
        existing_sha = hashlib.sha256(existing).hexdigest()
        if existing_sha == sha256:
            return FetchResult(
                species=species,
                variant=variant,
                url=url,
                status="already-present-identical",
                byte_size=len(data),
                width=width,
                height=height,
                sha256=sha256,
                output_path=destination.as_posix(),
            )
        return FetchResult(
            species=species,
            variant=variant,
            url=url,
            status="existing-conflict",
            byte_size=len(data),
            width=width,
            height=height,
            sha256=sha256,
            output_path=destination.as_posix(),
            note=(
                f"destination exists with different SHA-256 {existing_sha}; "
                "refusing silent replacement"
            ),
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return FetchResult(
        species=species,
        variant=variant,
        url=url,
        status="fetched",
        byte_size=len(data),
        width=width,
        height=height,
        sha256=sha256,
        output_path=destination.as_posix(),
    )


def write_manifest(path: Path, game_variant: str, rows: list[FetchResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    collected_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(
            [
                "game_variant",
                "species",
                "variant",
                "source_url",
                "status",
                "byte_size",
                "width",
                "height",
                "sha256",
                "output_path",
                "evidence_class",
                "collected_at_utc",
                "note",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    game_variant,
                    row.species,
                    row.variant,
                    row.url,
                    row.status,
                    "" if row.byte_size is None else row.byte_size,
                    "" if row.width is None else row.width,
                    "" if row.height is None else row.height,
                    row.sha256 or "",
                    row.output_path or "",
                    "secondary-provisional-visual-evidence",
                    collected_at,
                    row.note,
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-variant", choices=sorted(GAME_VARIANTS), required=True)
    parser.add_argument(
        "--species",
        required=True,
        help="comma/range syntax, e.g. 650-659 or 3,6,25",
    )
    parser.add_argument(
        "--variants",
        default="default,shiny,female,shiny-female",
        help="comma-separated: default, female, shiny, shiny-female",
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    try:
        species_ids = parse_species_range(args.species)
    except ValueError as exc:
        parser.error(str(exc))

    variants = [value.strip() for value in args.variants.split(",") if value.strip()]
    invalid_variants = sorted(set(variants) - set(VARIANT_PATHS))
    if invalid_variants:
        parser.error(f"unknown variants: {invalid_variants}")

    rows: list[FetchResult] = []
    for species in species_ids:
        for variant in variants:
            result = fetch_one(
                game_variant=args.game_variant,
                species=species,
                variant=variant,
                output_root=args.output_root,
                overwrite=args.overwrite,
                timeout=args.timeout,
            )
            rows.append(result)
            print(
                f"{species:04d} {variant:13s} {result.status:25s} "
                f"{result.sha256 or '-'}"
            )

    write_manifest(args.manifest, args.game_variant, rows)

    hard_failures = {
        "fetch-error",
        "invalid-source",
        "existing-conflict",
    }
    failed = [row for row in rows if row.status in hard_failures]
    print(f"records={len(rows)} hard_failures={len(failed)} manifest={args.manifest}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
