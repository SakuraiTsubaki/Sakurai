# Pokémon Emerald ROM Atlas

This atlas is derived from the six unique supplied Pokémon Emerald Rev 0 GBA images. Raw ROM bytes are not committed.

## Inputs

- BPEJ-R0 / PROJECT-d7cf8f15
- BPEE-R0 / PROJECT-f3ae0881 (two supplied filenames, byte-identical)
- BPED-R0 / PROJECT-61c2eb2b
- BPEF-R0 / PROJECT-ca666651
- BPEI-R0 / PROJECT-1692db32
- BPES-R0 / PROJECT-fe1558a3

## Files

- `bank64k-all.tsv` — all 256 64 KiB banks for all six releases. Columns include SHA-256, CRC32, Shannon entropy, zero/FF ratios, and aligned GBA-ROM-pointer counts.
- `bank-equivalence.tsv` — same-offset bank equivalence classes across the six releases.
- `lz77-bank-counts.tsv` — counts of structurally valid BIOS-LZ77 type-0x10 candidates per 64 KiB bank. Candidate status is structural only; semantic ownership (sprite/tilemap/etc.) requires later pointer/table analysis.

## Routing rule

Exact supplied-file observations belong under `RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/`. Cross-release tables derived from two or more dumps belong under `COMPARISONS/REV0-LOCALIZATION-SET/`. Production extraction/materialization belongs in Tsubaki under `PROJECTS/EMERALD-ROM-ASSET-PIPELINE/`.

## Reproducibility

The source hashes are locked in `INFRA/REGISTRY/ROM-SETS/EMERALD/source-set.tsv`. Re-run the repository GBA census and LZ77 scanner against a locally supplied ROM; do not commit ROM binaries.
