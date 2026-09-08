# Pokémon Sapphire multi-region ROM reproducibility substrate

This directory contains a deterministic, byte-complete analysis harness for the nine supplied Pokémon Sapphire ROM images. **No ROM image, raw chunk, extracted text, graphics, audio, or other copyrighted binary payload is stored here.**

## Scope

- GBA header parsing and complement validation.
- MD5, SHA-1, and SHA-256 identity manifests.
- SHA-256 coverage for every 64 KiB of every ROM.
- 64 KiB entropy maps.
- byte-frequency histograms.
- long 0x00 / 0xFF fill-run maps (>= 256 bytes).
- aligned in-ROM GBA pointer-density maps aggregated by 1 MiB source/target bins.
- same-offset pairwise similarity for every supplied version.
- revision-oriented coalesced difference-region maps for matching game codes.
- local byte-complete split/rebuild tool: every ROM can be split into deterministic binary chunks and reassembled to the exact original SHA-256.

## Reproduce

Place the original ROMs in a local directory and run:

```bash
python3 -m pip install -r requirements.txt
./reproduce.sh /path/to/roms generated-local
```

Validate only:

```bash
python3 tools/verify_manifest.py /path/to/roms data/source_manifest.json
```

Byte-complete local split/rebuild example:

```bash
python3 tools/materialize_rom.py split "/path/to/rom.gba" materialized/example
python3 tools/materialize_rom.py rebuild materialized/example rebuilt/example.gba
```

The split output and rebuilt ROM are deliberately ignored by Git. This lets the repository preserve the full method, identity, and structure of the source ROMs without redistributing the ROM bytes.

## Canonical hierarchy

`GENERATION-III/SAPPHIRE/MULTI-REGION/REV-MULTI/REPRODUCIBILITY`

The manifest records the logical language/region and revision for each ROM. Future region-specific analysis can be placed under the corresponding `LANGUAGE-REGION/REV-N/WORK-TYPE` branch of the hierarchy.

## Determinism

The analysis script uses the pinned NumPy version in `requirements.txt`; split/rebuild and manifest verification use the Python standard library. Generated rows are produced in stable filename / offset / byte order. A clean run against inputs matching `data/source_manifest.json` must reproduce the same datasets byte-for-byte; `tools/verify_generated.py` checks them against `data/generated_dataset_manifest.json`.

## Verified baseline

The committed `data/rebuild_verification.csv` records a successful byte-exact split/rebuild check for all nine supplied ROMs. Every rebuilt SHA-256 matches its source SHA-256.
