# Generation V — Pokémon Black / White ROM baseline (SweeTnDs dump set)

Status: initial ROM-identification and filesystem baseline.

## Scope

Read-only source images supplied for the project:

- `Pokemon.Black.Version.EUR.NDS-SweeTnDs.nds`
- `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds`

The ROM images themselves are not to be committed to GitHub. Only metadata, hashes, manifests, analysis, source code, and later patches are tracked.

## Identity

| Field | Black | White |
|---|---:|---:|
| ROM size | 268,435,456 bytes (256 MiB) | 268,435,456 bytes (256 MiB) |
| Internal title | `POKEMON B` | `POKEMON W` |
| Game code | `IRBO` | `IRAO` |
| Maker code | `01` | `01` |
| Unit code | `0x02` (NDS + DSi) | `0x02` (NDS + DSi) |
| Device capacity | `0x0B` (256 MiB image) | `0x0B` (256 MiB image) |
| DSi game-revision field | `0x4003` | `0x4003` |
| ROM version byte | `0` | `0` |
| CRC32 | `E2BEE619` | `EDCD5161` |
| MD5 | `f45fd94bb761721e30bd3a0a4fde124a` | `8dfef9a099e1269af5c1fcf9d7736a11` |
| SHA-1 | `a68b3bedf5c1e53556e41e59cdf396c20b331896` | `f94d4578956487c09fee20809a591e858017769e` |
| SHA-256 | `2e40416b8e8183d936084c7be0adeaab4fa3f786a68f90d7291ab77d340f0c1d` | `93e4f473ce9a0543bccf2e689ecd07ab4fcc39dd00fb4f194343cbd5e70e17ed` |

`IRBO` / `IRAO` are the English `O`-code Black/White builds used for USA/Europe releases. The supplied filenames say EUR, but the internal game code itself is the stronger identifier.

## Dump-quality warning

The exact CRC32 pair `E2BEE619` / `EDCD5161` is catalogued by preservation/cheat databases as `[b]` (bad/incomplete dump) for the USA/Europe DSi-enhanced releases. A community preservation note specifically associates the SweeTnDs-era image with incomplete/missing DSi-related dump data.

Therefore:

1. Keep these two images as read-only supplied-source references.
2. Do not call them a verified clean/full preservation dump.
3. NTR/NitroFS content can still be analyzed and compared.
4. DSi/TWL-specific conclusions must be revalidated against a known-good full cartridge dump before being treated as canonical.

The images do contain non-zero ARM9i/ARM7i/TWL-area bytes according to their headers, so the exact defect must not be guessed from the `[b]` tag alone. We record the external classification and defer a byte-exact clean-dump comparison until a verified full dump is available.

## NDS/TWL structure baseline

| Field | Black | White |
|---|---:|---:|
| ARM9 size | 456,856 | 456,868 |
| ARM7 size | 167,812 | 167,812 |
| ARM9 overlays | 237 | 237 |
| FNT directories | 31 | 31 |
| Named NitroFS files | 247 | 247 |
| FAT entries | 484 | 484 |
| ARM9i size (header) | 77,604 | 77,596 |
| ARM7i size (header) | 291,064 | 291,064 |
| Banner size | 9,152 | 9,152 |

The FAT count decomposes exactly as `237 ARM9 overlay files + 247 named NitroFS files = 484 FAT entries`.

## Black / White direct structural comparison

- FNT directory structure: identical.
- Named NitroFS path set: identical (247/247).
- ARM7 binary: byte-identical.
- ARM9 binary: differs.
- ARM9 overlay table: differs.
- Icon/banner: differs.
- FAT payloads that differ: **185 / 484**.
  - ARM9 overlay payloads differing: **180 / 237**.
  - Named NitroFS payloads differing: **5 / 247**.

The five differing named NitroFS files are:

| FAT ID | Path | Black size | White size | Initial identification |
|---:|---|---:|---:|---|
| 268 | `a/0/2/6` | 22,228 | 22,528 | title-screen archive (externally documented) |
| 328 | `a/0/8/6` | 3,356 | 3,356 | unresolved in this baseline; do not guess |
| 368 | `a/1/2/6` | 35,284 | 35,284 | wild encounter data (externally documented for BW) |
| 420 | `a/1/7/8` | 168,792 | 168,792 | unresolved in this baseline; species-sized NARC (649 entries) |
| 473 | `a/2/3/1` | 1,208,900 | 1,210,248 | unresolved in this baseline; do not guess |

This is only a top-level archive comparison. Each differing NARC still needs entry-level parsing to isolate the exact version-exclusive records.

## External cross-checks used for this baseline

- DSiBrew, `DSi Cartridge Header` — header offsets and TWL extended-header fields.
- Project Pokémon PPRE source — Gen V game-code/language mapping and known NARC paths.
- Project Pokémon research threads / RawDB — BW NARC structure, `a/1/2/6` encounter data, and title-screen research.
- GameHacking.org — exact CRC32s and `[b]` classification for IRBO/IRAO.

## Next required work

1. Parse all 237 ARM9 overlay records and map code/data responsibilities.
2. Parse the five differing NitroFS archives recursively and identify every differing subfile/record.
3. Build a complete NARC catalogue for all 247 named files: magic, archive member count, decompression state, known function, confidence, source.
4. Establish reproducible extraction/rebuild checks: extract -> rebuild -> compare hashes for unchanged data.
5. Replace `REV-UNKNOWN` only after revision/dump identity is reconciled with a verified full dump; keep supplied-dump status separately recorded.
6. Continue into the requested full BW survey: data tables, maps, scripts, text, trainers, encounters, graphics, sound, communications, unused data, bugs, and regional/language differences.
