# Pokémon White Version — ROM Baseline

## Canonical hierarchy

`GENERATION-V → WHITE → EN-USA-EUR → REV-0 → analysis`

## Uploaded read-only source

- Filename: `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds`
- Scene identity: `Pokemon.White.Version.EUR.NDS-SweeTnDs`
- Game code: `IRAO`
- ROM version byte: `0`
- Actual file size: `268,435,456` bytes (256 MiB)

## Locally measured hashes

These values were computed directly from the uploaded bytes on 2026-09-08.

- CRC32: `EDCD5161`
- MD5: `8DFEF9A099E1269AF5C1FCF9D7736A11`
- SHA-1: `F94D4578956487C09FEE20809A591E858017769E`
- SHA-256: `93E4F473CE9A0543BCCF2E689ECD07AB4FCC39DD00FB4F194343CBD5E70E17ED`

## Structure census

- FAT entries: `484`
- ARM9 overlays: `237`
- named FNT/NitroFS files: `247`
- ARM7 overlays: `0`
- detected top-level NARC containers: `237`
- full payload inventory rows (top-level + NARC members): `54,538`

## Rebuild verification

Two independent no-change rebuild paths were executed:

1. source-ROM template + extracted editable regions
2. source-independent 1 MiB physical base chunks + extracted editable regions

Both rebuilt images matched the uploaded source byte-for-byte. CRC32, MD5, SHA-1 and SHA-256 all matched exactly.

## Black / White consolidation result

At equivalent payload paths, `54,287 / 54,538` payloads are byte-identical between Black and White. Only `251` payload paths differ. This allows a common-base + version-delta workflow.

## Repository policy

- The uploaded ROM and source-derived binary payloads are read-only/private working material and are never committed to GitHub.
- `Sakurai` stores hashes, inventories, reports, reproducibility scripts and verification results.
- Reusable implementation assets/patches belong in `SakuraiTsubaki/Tsubaki` under the same hierarchy.
