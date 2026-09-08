# Pokémon Crystal full-ROM reproducibility workpack

This package turns the seven supplied Pokémon Crystal ROM revisions/regions into deterministic analysis artifacts **without modifying or redistributing the ROMs**.

## What “full ROM” means in this baseline

Every source ROM byte is covered twice by deterministic manifests:

- 128 × 16 KiB ROM-bank records (`bank_manifest.csv`)
- 8,192 × 256-byte page records (`page_manifest.csv`)

The verifier recomputes every bank and every page SHA-256 and checks that their byte totals equal the ROM size. No sampling is used.

## Included tools

- `tools/crystal_rom_audit.py` — header decode, ROM identity, bank/page manifests, entropy/fill maps, pairwise comparisons, Rev0↔Rev1 byte-change map.
- `tools/scan_candidates.py` — exhaustive byte-pattern scan for LR35902 immediate JP/CALL candidates. These are **candidates**, not proven code boundaries.
- `tools/verify_outputs.py` — re-hashes every bank/page and verifies total byte coverage.
- `rom_catalog.template.json` — expected filenames, SHA-256 identities and repository output paths.

Python 3.10+ is sufficient; only the standard library is used.

## Reproduce

1. Create `roms/` beside this README.
2. Place the seven original ROMs there using the filenames in `rom_catalog.template.json`.
3. Run:

```bash
python tools/crystal_rom_audit.py --catalog rom_catalog.template.json --output output
python tools/scan_candidates.py --catalog rom_catalog.template.json --output output
python tools/verify_outputs.py --catalog rom_catalog.template.json --output output
```

The audit aborts if any configured source SHA-256 does not match.

## Repository hierarchy

Artifacts follow:

`GENERATION-II / CRYSTAL / LANGUAGE-REGION / REV / ROM-REPRODUCIBILITY`

Cross-region comparison material uses:

`GENERATION-II / CRYSTAL / MULTI-REGION / REV-MIXED / ROM-REPRODUCIBILITY`

## Current verified facts

- All seven ROMs are exactly 2,097,152 bytes (128 banks).
- All seven pass both header and global Game Boy checksum verification.
- Japan Rev 0 has RAM-size header code `05` (64 KiB); the other supplied versions use `03` (32 KiB).
- Japan Rev 0 has banks `60`–`7C` completely zero-filled.
- USA/Europe Rev 0 and Rev 1 have banks `75`, `76`, `79`, `7A` completely zero-filled.
- ES/DE/FR/IT Rev 0 each have bank `7A` completely zero-filled.
- USA/Europe Rev 0 ↔ Rev 1 differs in 584 byte positions across banks `00 10 11 3E 47 5C 7E 7F`; 120 of 128 banks are byte-identical.

## Important boundary

This is the **full-byte forensic/reproducibility baseline**, not yet a semantically complete source-code disassembly. Page classifications and JP/CALL scans are heuristic. The next reconstruction layers should convert identified regions into symbolic code/data while retaining lossless rebuild tests.

No `.gbc` file or raw bank dump belongs in GitHub.
