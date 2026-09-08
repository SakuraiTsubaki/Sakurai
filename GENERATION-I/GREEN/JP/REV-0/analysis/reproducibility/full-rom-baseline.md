# Pokémon Green JP — Full-ROM reproducibility baseline

## Scope

This package covers both user-supplied 512 KiB Japanese Pokémon Green ROM revisions without embedding either ROM binary.
The originals are treated as read-only inputs. Every generated table can be regenerated using `tools/green_romlab.py`.

## Canonical inputs

| Revision | SHA-1 | SHA-256 | ROM version |
|---|---|---|---:|
| REV-0 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | `6576b4e0979e93d4a6fa02db893c294b7aeab3b841b1acc8658bc10b3554f33c` | 0 |
| REV-A | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` | `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816` | 1 |

Both are 524,288 bytes, 32 banks × 16 KiB. Header checksum and global checksum validate for both ROMs.

## Full-byte coverage

The generated page manifests fingerprint all 2,048 pages of 256 bytes per ROM: 2,048 × 256 = 524,288 bytes. No byte is omitted or duplicated.
The bank manifests independently fingerprint all 32 banks.

## Revision relationship

* Different bytes: **46,168**
* Identical bytes: **478,120 (91.194153%)**
* Contiguous difference runs: **5,436**
* Completely identical banks: **Bank 1B only**
* Largest changed banks: Bank 0F = 15,403 bytes, Bank 00 = 13,109 bytes, Bank 01 = 11,803 bytes.

`generated/rev0_to_reva.delta.jsonl` and its reverse store deterministic contiguous-run deltas. Applying them validates against the canonical target SHA-1.

## Reproduction commands

```sh
python3 tools/green_romlab.py verify "Pocket Monsters - Midori (Japan) (SGB Enhanced).gb"
python3 tools/green_romlab.py verify "Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb"
python3 tests/test_roundtrip.py REV0.gb REVA.gb
```

For local byte-exact bank binaries, run `split`; for a local byte-exact `db` representation, run `emit-db`. Those outputs contain ROM bytes and are intentionally **not** included for publication.

## What is established vs. still semantic work

This package establishes a byte-perfect, reproducible foundation: identity, checksums, full-bank/page coverage, address conversion, revision delta, round-trip reconstruction, and candidate pointer scanning.
It does **not** pretend that every byte has already been semantically named as code, text, map, graphics, music, or tables. Semantic labeling is the next layer and can be added without invalidating this baseline.
