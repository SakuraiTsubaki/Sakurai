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
- `tools/lossless_roundtrip.py` — temporary 16 KiB bank split→concatenate roundtrip; proves byte-identical reconstruction without bundling the split binaries.
- `tools/address_map.py` — deterministic file-offset ↔ bank ↔ CPU-address maps.
- `tools/cross_version_equivalence.py` — same-offset bank/page equality groups across all seven targets.
- `tools/pointer_sweep_summary.py` — exhaustive adjacent 16-bit word target-class summaries (heuristic evidence, not pointer proof).
- `tools/run_full_pipeline.py` — orchestration entry point for the complete forensic pipeline.
- `tools/verify_pokecrystal_bridge.py` — verifies source builds from a pinned `pret/pokecrystal` checkout against the two exact English target hashes.
- `rom_catalog.template.json` — expected filenames, SHA-256 identities and repository output paths.

Python 3.10+ is sufficient; only the standard library is used.

## Reproduce

1. Create `roms/` beside this README.
2. Place the seven original ROMs there using the filenames in `rom_catalog.template.json`.
3. Run:

```bash
python tools/run_full_pipeline.py --catalog rom_catalog.template.json --output output
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

## Reproducibility level reached

All seven supplied targets have now passed **L2 lossless structural roundtrip**: each ROM was split into 128 consecutive 16 KiB banks in temporary scratch space, concatenated in order, and reproduced byte-identically with the same SHA-256. The temporary bank binaries and rebuilt ROMs are not bundled.

The two USA/Europe English targets are additionally linked to the pinned public `pret/pokecrystal` source baseline by exact SHA-1 identity; see `SOURCE_BRIDGE.md` and `source_bridge.json`.

This is still not a semantically complete regional source reconstruction. Page classifications, JP/CALL scans and 16-bit word sweeps are heuristic evidence. The next reconstruction layers must convert every region into symbolic code/typed data/assets while retaining exact rebuild tests.

No `.gbc` file or raw bank dump belongs in GitHub.

## Bank/page semantic ownership seeds

The workpack now also creates `bank_ownership_seed.csv` and `page_ownership_seed.csv` for every target. These do **not** pretend that regional reconstruction is finished. They distinguish:

- exact English targets whose bank roles come from the pinned source layout;
- regional chunks that are byte-identical at the same offset to an English target, which can inherit that role with high confidence;
- differing regional chunks, which remain tentative until a typed decoder/symbol alignment proves their contents.

This means all 2 MiB of every target has a reproducible analysis status while still keeping “known” separate from “inferred”.

## External source/symbol bridge

See:

- `SOURCE_BRIDGE.md`
- `UPSTREAM_SYMBOLS.md`
- `source_bridge.json`
- `upstream_bank_roles.csv`
- `tools/bootstrap_pokecrystal.sh`
- `tools/verify_pokecrystal_bridge.py`

The workpack pins the external source reference instead of copying an entire third-party source tree into this package.
