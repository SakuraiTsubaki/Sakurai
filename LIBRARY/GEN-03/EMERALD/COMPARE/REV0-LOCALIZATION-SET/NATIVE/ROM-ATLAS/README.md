# Pokémon Emerald ROM Atlas — v6

This atlas is derived from the six unique supplied Pokémon Emerald header-version-0 GBA images. Raw ROM bytes are not committed.

## Canonical inputs

- `BPEJ-HV0` / `UPLOAD-d7cf8f15`
- `BPEE-HV0` / `UPLOAD-f3ae0881` (two supplied filenames, byte-identical)
- `BPED-HV0` / `UPLOAD-61c2eb2b`
- `BPEF-HV0` / `UPLOAD-ca666651`
- `BPEI-HV0` / `UPLOAD-1692db32`
- `BPES-HV0` / `UPLOAD-fe1558a3`

## Evidence files

- `bank-equivalence.tsv` — full 256-bank same-offset equivalence snapshot.
- `same-offset-bank-equivalence-ranges.tsv` — compact contiguous range summary of those equivalence classes.
- `lz77-bank-counts.tsv` — structurally valid BIOS-LZ77 type-0x10 candidate counts per 64 KiB bank.
- `lz77-census-summary.tsv` — release-level structural compression census summary.

The large evidence snapshots were originally generated before the repository adopted v6 IDs and intentionally retain their original `BPE*-R0` row labels as provenance. Resolve those labels through `../../IDENTITY/pre-v6-id-aliases.tsv`; they refer to the same observed ROM identities now named `BPE*-HV0`. New generated research must emit v6 IDs.

## Routing

Exact dump observations belong under `LIBRARY/GEN-03/EMERALD/SOURCE/GBA/CART/<RELEASE-ID>/DUMPS/<DUMP-ID>/`. Cross-release evidence belongs under this `COMPARE/REV0-LOCALIZATION-SET` tree. Production extraction/materialization belongs in Tsubaki under `PROJECTS/GEN-03/EMERALD-ROM-ASSET-PIPELINE/`.

## Reproducibility

Source identities and hashes are locked in `INFRA/REGISTRIES/ROM-SETS/EMERALD/source-set.tsv`. `INFRA/TOOLING/GBA/rom_census.py` can regenerate exact per-bank hashes and structural LZ77 observations from a locally supplied ROM. Do not commit ROM binaries.
