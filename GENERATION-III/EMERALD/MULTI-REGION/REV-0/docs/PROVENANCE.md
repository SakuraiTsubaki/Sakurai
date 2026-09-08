# Provenance and reproducibility

This package is generated from the locally supplied Pokémon Emerald ROM files. Original ROM bytes are not included.

## Evidence chain
1. `manifest/rom_manifest.json` records exact source filenames, sizes, hashes, GBA header fields and duplicate relationships.
2. `analysis/chunks_16k.csv` covers every source byte range using deterministic 16 KiB boundaries and cryptographic checksums.
3. `analysis/pointer_index_*.csv.gz` records every 4-byte-aligned value recognized as a GBA ROM/RAM/I/O pointer candidate for each unique ROM.
4. `analysis/baseline_delta_16k.csv` records per-chunk difference density against the canonical English image.
5. `manifest/generated_artifacts_manifest.csv` records hashes of every generated work file so regenerated results can be compared byte-for-byte.
6. `tools/audit_emerald.py` regenerates the forensic tables from locally supplied originals; `tools/verify_roms.py` validates source identity first.

## Semantic decomposition status
The forensic layer is byte-complete, but it intentionally does not guess that every byte is code or data. ARM/Thumb code, scripts, text, graphics, audio, maps, tables and free-space classification will be layered on top with source offsets and evidence, so incorrect automatic disassembly cannot contaminate the base map.
