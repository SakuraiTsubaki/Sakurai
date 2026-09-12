# Generation V — Pokémon Black / White ROM baseline (SweeTnDs dump set)

Status: initial ROM-identification and filesystem baseline.

## Scope

Read-only source images supplied for the project:

- `Pokemon.Black.Version.EUR.NDS-SweeTnDs.nds`
- `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds`

The ROM images themselves are not committed to GitHub. Only metadata, hashes, manifests, analysis, source code, and patches are tracked.

## Identity

| Field | Black | White |
|---|---:|---:|
| ROM size | 268,435,456 bytes | 268,435,456 bytes |
| Internal title | `POKEMON B` | `POKEMON W` |
| Game code | `IRBO` | `IRAO` |
| Maker code | `01` | `01` |
| Unit code | `0x02` | `0x02` |
| Device capacity | `0x0B` | `0x0B` |
| DSi game-revision field | `0x4003` | `0x4003` |
| ROM version byte | `0` | `0` |
| CRC32 | `E2BEE619` | `EDCD5161` |
| MD5 | `f45fd94bb761721e30bd3a0a4fde124a` | `8dfef9a099e1269af5c1fcf9d7736a11` |
| SHA-1 | `a68b3bedf5c1e53556e41e59cdf396c20b331896` | `f94d4578956487c09fee20809a591e858017769e` |
| SHA-256 | `2e40416b8e8183d936084c7be0adeaab4fa3f786a68f90d7291ab77d340f0c1d` | `93e4f473ce9a0543bccf2e689ecd07ab4fcc39dd00fb4f194343cbd5e70e17ed` |

`IRBO` / `IRAO` are the stronger canonical identities than the distribution wording in the filenames.

## Dump-quality warning

These exact supplied SweeTnDs images remain dump observations, not canonical clean-dump claims. NTR/NitroFS analysis is retained; DSi/TWL-specific conclusions require revalidation against a verified full dump.

## NDS/TWL structure baseline

| Field | Black | White |
|---|---:|---:|
| ARM9 size | 456,856 | 456,868 |
| ARM7 size | 167,812 | 167,812 |
| ARM9 overlays | 237 | 237 |
| FNT directories | 31 | 31 |
| Named NitroFS files | 247 | 247 |
| FAT entries | 484 | 484 |
| ARM9i size | 77,604 | 77,596 |
| ARM7i size | 291,064 | 291,064 |
| Banner size | 9,152 | 9,152 |

The FAT count decomposes as `237 ARM9 overlay files + 247 named NitroFS files = 484 FAT entries`.

## Black / White direct structural comparison

- FNT directory structure: identical.
- Named NitroFS path set: identical (247/247).
- ARM7 binary: byte-identical.
- ARM9 binary: differs.
- ARM9 overlay table: differs.
- Icon/banner: differs.
- FAT payloads differing: **185 / 484**.
  - ARM9 overlay payloads differing: **180 / 237**.
  - Named NitroFS payloads differing: **5 / 247**.

Differing named NitroFS files:

| FAT ID | Path | Black size | White size | Initial identification |
|---:|---|---:|---:|---|
| 268 | `a/0/2/6` | 22,228 | 22,528 | title-screen archive |
| 328 | `a/0/8/6` | 3,356 | 3,356 | unresolved |
| 368 | `a/1/2/6` | 35,284 | 35,284 | wild encounter data |
| 420 | `a/1/7/8` | 168,792 | 168,792 | unresolved species-sized NARC (649 entries) |
| 473 | `a/2/3/1` | 1,208,900 | 1,210,248 | unresolved |

This is a top-level archive comparison; semantic labels remain confidence-tracked.

## Provenance

Restored into the V4 canonical comparison root from the pre-V4 ROM survey in Git history. Release identity and exact dump identity remain separated by the V4 manifests.
