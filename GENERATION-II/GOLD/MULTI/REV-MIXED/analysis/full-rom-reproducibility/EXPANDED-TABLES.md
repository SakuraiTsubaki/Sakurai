# Expanded Table Inventory

The complete downloadable workset contains large deterministic derivative tables such as per-ROM `page_hashes_256.csv`, `pointer_windows_16le.csv`, and the multi-version `shared_exact_256b_pages.csv`. They are not required as inputs: `tools/build_full_rom_atlas.py` regenerates them exactly from the verified source ROMs.

Largest generated tables are covered by `FULL-ROM-MANIFEST.json`; selected examples:

- KR `pointer_windows_16le.csv`: 2,326,022 bytes — SHA-256 `788bac2b9ecd37c5b1cdfc9d73fa2c08c426c24e38eda028e64addefbc2a66fe`
- USA/EU `pointer_windows_16le.csv`: 1,280,648 bytes — SHA-256 `b2d3c8ba751b12b0edb8c524c659d8426ddcfd9111d5f3691edbef82a8e7f7b8`
- KR `page_hashes_256.csv`: 799,289 bytes — SHA-256 `7caf16043ffcc9420af8e562cdcaa713ef4cf7b4ffbdae110e546c38b9577102`
- `shared_exact_256b_pages.csv`: 863,462 bytes — SHA-256 `3246618ddb341b8e47ce4f3a554a5de769dddbbf8154fdd85ccacf0541283480`

Regenerate the expanded tables with:

```sh
python tools/build_full_rom_atlas.py <rom-directory> <output-directory>
```

The complete 360-file expanded workset is also preserved in the project-delivered archive; no ROM payload bytes are included.
