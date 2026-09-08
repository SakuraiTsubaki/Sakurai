# Reproducibility scope

The project treats the uploaded ROMs as immutable, read-only source inputs.

A reproducible LeafGreen work package must let a collaborator who independently possesses the same source ROM:

1. identify the exact language/region/revision by header + MD5/SHA-1/SHA-256;
2. verify every 64 KiB and 1 MiB region against a full-ROM fingerprint map;
3. derive address-space coordinates (`file offset` ↔ `0x08000000 + offset`);
4. split the ROM into deterministic chunks without modifying bytes;
5. rebuild those chunks byte-for-byte into the original 16 MiB image;
6. verify the rebuilt image against the canonical hashes;
7. generate cross-region and cross-revision byte-difference reports;
8. scan the full image for aligned ROM pointers and validated GBA LZ77 streams;
9. regenerate all derived CSV/JSON reports from the source ROMs;
10. keep all ROM binaries and locally extracted binary chunks outside Git.

This is the baseline layer. Higher-level reverse-engineering artifacts (symbols, functions, data tables, scripts, text, graphics, maps, battle data, species data, etc.) should be added on top of this layer without weakening exact byte-level reproducibility.
