# Pokémon Sapphire — 64 KiB logical-bank survey

Date: 2026-09-10

## Scope

- 9 supplied Pokémon Sapphire ROM images
- Originals treated as read-only inputs; ROM binaries are not included in this repository
- Logical bank size: `0x10000` (64 KiB)
- GBA ROM mapping base: `0x08000000`
- Total logical bank-images surveyed: **2,176**
- Japanese AXPJ Rev0: 128 banks (8 MiB)
- International AXPD/AXPE/AXPF/AXPI builds: 256 banks each (16 MiB)

## Checks performed per bank

- CRC32 / SHA-1 / SHA-256
- entropy and byte diversity
- `00` / `FF` fill ratios and longest fill runs
- aligned ROM/EWRAM/IWRAM/I/O pointer-word candidates
- aggregated bank-to-bank ROM pointer graph
- BIOS-style compression header candidates
- fully parsed, aligned GBA LZ77 (`0x10`) streams
- exact aligned-bank equality and byte-difference counts across ROMs
- revision-pair change maps

## Key findings

1. **All 2,176 bank-images were scanned.**
2. The 16 MiB international builds share a large internal `FF` allocation gap at banks **`0x6C–0xCF`** (6.25 MiB), followed by a late data/asset island beginning at **`0xD0`**.
3. English AXPE uses content through bank **`0xEA`** and has `0xEB–0xFF` blank; German/French/Italian builds extend through **`0xEB`** and have `0xEC–0xFF` blank.
4. Japanese AXPJ is structurally different: bank **`0x66`** is blank, but banks `0x67–0x7F` contain substantial data. It is not simply the first half of an international 16 MiB image.
5. Minor revisions AXPE Rev1→Rev2, AXPF Rev0→Rev1 and AXPI Rev0→Rev1 each alter exactly **4 bytes**, all inside logical bank `0x00`.
6. AXPE Rev0→Rev1 is a broad rebuild: **109 logical banks** change, with **5,638,997 differing bytes** in aligned comparison.
7. Fully validated aligned LZ77 streams across all nine images: **28,396**. International builds are especially LZ77-heavy around banks `0xD0–0xD2` and `0xE5–0xE7`.
8. English AXPE Rev0 SHA-1 is `3ccbbd45f8553c36463f13b938e833f652b793e4`, exactly matching the `pokesapphire.gba` target documented by `pret/pokeruby`. This makes it the semantic anchor for symbol/source mapping in the next phase.

## Interpretation rule

The coarse classes (`pointer_dense`, `high_entropy`, `compression_candidate_dense`, `mixed`, `sparse`, `FF_blank`) are triage labels, not final semantic labels. `validated_lz77_aligned4` and the bank pointer graph are stronger structural signals than raw entropy or raw compression-header counts. Final labels require source/symbol anchoring or direct disassembly/data-format validation.

## Files

- `manifest.json` — input ROM identity metadata and hashes (no ROM bytes)
- `STRUCTURAL_FINDINGS.md` — per-ROM bank ranges and structural hotspots
- `revision_exact_byte_diffs.csv` — exact byte-level minor-revision differences
- `sapphire_bank_survey.py` — first-pass 64 KiB bank census and aligned comparison
- `sapphire_bank_survey_augment.py` — validated LZ77 parser and bank pointer-graph augmentation

Large row-level CSV outputs are generated reproducibly by the scripts and are retained in the project analysis package; ROM binaries are never committed.
