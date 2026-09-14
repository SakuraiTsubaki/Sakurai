# FireRed ROM Baseline Audit

Audit date: 2026-09-13

This repository does not contain ROM images. The table below records metadata and cryptographic hashes observed from the user-supplied local reference ROMs and compares SHA-1 against public clean-dump references.

## Result

- 8 FireRed ROM images inspected.
- All 8 are exactly 16,777,216 bytes (16 MiB).
- All 8 have valid GBA header checksums.
- 6 of 8 match the public clean-reference SHA-1 exactly.
- The two English BPRE images do **not** match the public clean-reference SHA-1 and are quarantined as non-canonical baselines until reconstructed or otherwise resolved.

| Variant | Game code | Rev | Observed SHA-1 | Reference SHA-1 | Status |
|---|---|---:|---|---|---|
| Japan | BPRJ | 0 | `04139887b6cd8f53269aca098295b006ddba6cfe` | same | verified |
| Japan Rev 1 | BPRJ | 1 | `7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857` | same | verified |
| USA | BPRE | 0 | `d3b806453369b4b086c792eb3c05a02f00057f50` | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | quarantined |
| USA/Europe Rev 1 | BPRE | 1 | `c4d0119d9bcb36687f41a8f7ca72ab7af60558e4` | `dd5945db9b930750cb39d00c84da8571feebf417` | quarantined |
| France | BPRF | 0 | `fc663907256f06a3a09e2d6b967bc9af4919f111` | same | verified |
| Germany | BPRD | 0 | `18a3758ceeef2c77b315144be2c3910d6f1f69fe` | same | verified |
| Italy | BPRI | 0 | `66a9d415205321376b4318534c0dce5f69d28362` | same | verified |
| Spain | BPRS | 0 | `ab8f6bfe0ccdaf41188cd015c8c74c314d02296a` | same | verified |

Complete CRC32, MD5, SHA-1 and SHA-256 values are stored in `checksums/fire_red_baselines.json` and `checksums/fire_red_baselines.csv`.

## Reference sources

Public cross-checks used for the clean-reference SHA-1 values:

- pret/pokefirered (English FireRed / Rev 1 build targets)
- 40Cakes/pokebot-gen3 supported game/language hash table (all FireRed language variants)
- Gekkio Game Boy hardware database physical cartridge dump records (spot verification for regional releases)

The audit records hashes only. No ROM image or ROM payload is committed to this repository.

## Policy

A ROM is eligible to act as a byte-exact reconstruction target only after its reference hash is verified. A header checksum being valid is not sufficient by itself to establish a clean/canonical dump.

Original local files remain read-only. Any normalization or clean reconstruction must be produced as a separate build output and validated against the canonical hash.
