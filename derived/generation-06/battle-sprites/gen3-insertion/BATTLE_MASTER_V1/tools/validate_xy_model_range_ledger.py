#!/usr/bin/env python3
"""Validate the public XY Generation VI model-range research ledger.

This validator checks only structural invariants that can be established from the
recorded public list. It deliberately does not promote reported-public labels to
retail-game verification.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_COLUMNS = {
    "archive_path",
    "range_start",
    "range_end",
    "member_count",
    "national_dex",
    "reported_label",
    "evidence_status",
    "verification_status",
    "notes",
    "source_reference",
}

EXPECTED_ARCHIVE = "a/0/0/7"
EXPECTED_FIRST_MEMBER = 6868
EXPECTED_LAST_MEMBER = 7851
EXPECTED_BLOCK_SIZE = 8
EXPECTED_ROW_COUNT = 123
EXPECTED_GAP_ROWS = 4
EXPECTED_DEX = set(range(650, 722))
GAP_LABEL = "UNRESOLVED_PUBLIC_LIST_GAP"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"missing columns: {sorted(missing)}")
        return list(reader)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ledger",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "source-ledgers"
        / "xy_model_ranges_public_gen6.csv",
    )
    args = parser.parse_args()

    rows = load_rows(args.ledger)
    if len(rows) != EXPECTED_ROW_COUNT:
        fail(f"expected {EXPECTED_ROW_COUNT} rows, found {len(rows)}")

    parsed: list[tuple[int, int, int, dict[str, str]]] = []
    dex_seen: set[int] = set()
    gap_count = 0

    for index, row in enumerate(rows, start=2):
        if row["archive_path"] != EXPECTED_ARCHIVE:
            fail(f"line {index}: unexpected archive {row['archive_path']!r}")

        try:
            start = int(row["range_start"])
            end = int(row["range_end"])
            count = int(row["member_count"])
        except ValueError as exc:
            fail(f"line {index}: non-integer range/count: {exc}")

        if start > end:
            fail(f"line {index}: inverted range {start}-{end}")
        if end - start + 1 != count:
            fail(
                f"line {index}: member_count={count} but range contains "
                f"{end - start + 1} members"
            )
        if count != EXPECTED_BLOCK_SIZE:
            fail(f"line {index}: expected 8-member block, found {count}")

        label = row["reported_label"]
        if label == GAP_LABEL:
            gap_count += 1
            if row["evidence_status"] != "observed-public-gap":
                fail(f"line {index}: unresolved gap has wrong evidence status")
            if row["verification_status"] != "unresolved":
                fail(f"line {index}: unresolved gap is not marked unresolved")
        else:
            if row["verification_status"] == "verified":
                fail(
                    f"line {index}: public mapping must not be promoted to verified "
                    "without member-level game evidence"
                )

        dex = row["national_dex"].strip()
        if dex:
            try:
                dex_number = int(dex)
            except ValueError as exc:
                fail(f"line {index}: invalid National Dex number: {exc}")
            if not 650 <= dex_number <= 721:
                fail(f"line {index}: Dex number outside Generation VI new-species range")
            dex_seen.add(dex_number)

        parsed.append((start, end, count, row))

    parsed.sort(key=lambda item: item[0])

    if parsed[0][0] != EXPECTED_FIRST_MEMBER:
        fail(f"first member is {parsed[0][0]}, expected {EXPECTED_FIRST_MEMBER}")
    if parsed[-1][1] != EXPECTED_LAST_MEMBER:
        fail(f"last member is {parsed[-1][1]}, expected {EXPECTED_LAST_MEMBER}")

    for previous, current in zip(parsed, parsed[1:]):
        expected = previous[1] + 1
        if current[0] != expected:
            fail(
                f"non-contiguous ledger between {previous[0]}-{previous[1]} and "
                f"{current[0]}-{current[1]} (expected next start {expected})"
            )

    if gap_count != EXPECTED_GAP_ROWS:
        fail(f"expected {EXPECTED_GAP_ROWS} explicit public-list gaps, found {gap_count}")

    missing_dex = EXPECTED_DEX - dex_seen
    extra_dex = dex_seen - EXPECTED_DEX
    if missing_dex or extra_dex:
        fail(
            "National Dex coverage mismatch: "
            f"missing={sorted(missing_dex)} extra={sorted(extra_dex)}"
        )

    total_members = sum(item[2] for item in parsed)
    expected_span = EXPECTED_LAST_MEMBER - EXPECTED_FIRST_MEMBER + 1
    if total_members != expected_span:
        fail(
            f"member total {total_members} does not match covered span {expected_span}"
        )

    print("PASS: XY Generation VI public model-range ledger")
    print(f"rows={len(rows)}")
    print(f"member_span={EXPECTED_FIRST_MEMBER}-{EXPECTED_LAST_MEMBER}")
    print(f"members={total_members}")
    print(f"block_size={EXPECTED_BLOCK_SIZE}")
    print(f"explicit_unresolved_label_blocks={gap_count}")
    print(f"national_dex_species_covered={len(dex_seen)} (650-721)")
    print("verification=structural-only; member signatures/loading logic still unresolved")


if __name__ == "__main__":
    main()
