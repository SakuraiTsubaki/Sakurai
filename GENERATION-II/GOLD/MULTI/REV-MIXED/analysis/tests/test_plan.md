# Reproducibility test plan

1. Verify all eight source ROM filenames exist locally.
2. Verify file size and SHA-256 against `rom_inventory.csv`.
3. Recompute Game Boy header checksum and global checksum.
4. Recompute every 16 KiB bank SHA-256 and statistics.
5. Recompute every 4 KiB chunk SHA-256.
6. Regenerate pairwise bank/chunk similarity tables.
7. Regenerate the JP REV-0 ↔ REV-A exact diff-range table.
8. Ensure no `.gbc`, `.gb`, or `.bin` is present in the distributable corpus.
9. Regenerate the complete corpus a second time and require identical path sets and SHA-256 for every generated file.
10. Keep the RGBDS INCBIN rebuild scaffold external-input-only: `source.gbc` and built ROMs stay gitignored.
