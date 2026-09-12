# Generation V -> Pocket Monsters: ROM baseline census

Status: canonical project baseline derived from the currently supplied ROM set. ROM binaries remain external/read-only.

Registry of record: `INFRA/REGISTRY/ROM-SETS/GEN5-TO-POCKET-MONSTERS-2026-09-12.yaml`.

## Generation V sources

| Game | Canonical release | Supplied dump | Size | SHA-1 | Header identity | Structural baseline |
|---|---|---|---:|---|---|---|
| Black | `IRBO-R0` | `SWEETNDS-a68b3bed` | 256 MiB | `a68b3bedf5c1e53556e41e59cdf396c20b331896` | `POKEMON B`, `IRBO`, ROM version 0 | ARM9 456,856 B; ARM7 167,812 B; 237 ARM9 overlays; 247 named NitroFS files; 484 FAT entries |
| White | `IRAO-R0` | `SWEETNDS-f94d4578` | 256 MiB | `f94d4578956487c09fee20809a591e858017769e` | `POKEMON W`, `IRAO`, ROM version 0 | ARM9 456,868 B; ARM7 167,812 B; 237 ARM9 overlays; 247 named NitroFS files; 484 FAT entries |

The two supplied SweeTnDs images are dump observations, not clean-preservation authorities. NTR/NitroFS observations may be used with provenance; TWL/DSi-specific conclusions remain revalidation-required.

Black 2 and White 2 are required by project scope but are intentionally not represented by fabricated release folders until verified source builds are bound.

## Generation II targets

| Game | Release | Size | SHA-1 | Header/build facts |
|---|---|---:|---|---|
| Gold KR | `KR-KO-HV0` | 2 MiB | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | `POKEMON_GLDAAUK`; header version 0; 128 x 16 KiB banks; 32 KiB save RAM |
| Silver KR | `KR-KO-HV0` | 2 MiB | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` | `POKEMON_SLVAAXK`; header version 0; 128 x 16 KiB banks; 32 KiB save RAM |
| Crystal JP | `JP-JA-HV0` | 2 MiB | `95127b901bbce2407daf43cce9f45d4c27ef635d` | `PM_CRYSTAL`; header version 0; 128 x 16 KiB banks; 64 KiB save RAM |
| Crystal EN | `US-EU-EN-HV1` | 2 MiB | `f2f52230b536214ef7c9924f483392993e226cfb` | `PM_CRYSTAL`; header version 1 / Rev A; 128 x 16 KiB banks; 32 KiB save RAM |

## Generation III targets

| Game | Release | Size | SHA-1 |
|---|---|---:|---|
| Ruby JP | `AXVJ-R0` | 8 MiB | `5c5e546720300b99ae45d2aa35c646c8b8ff5c56` |
| Ruby EN | `AXVE-R2` | 16 MiB | `5b64eacf892920518db4ec664e62a086dd5f5bc8` |
| Sapphire JP | `AXPJ-R0` | 8 MiB | `3233342c2f3087e6ffe6c1791cd5867db07df842` |
| Sapphire EN | `AXPE-R2` | 16 MiB | `89b45fb172e6b55d51fc0e61989775187f6fe63c` |
| Emerald JP | `BPEJ-R0` | 16 MiB | `d7cf8f156ba9c455d164e1ea780a6bf1945465c2` |
| Emerald EN | `BPEE-R0` | 16 MiB | `f3ae088181bf583e55daf962a92bb46f4f1d07b7` |
| FireRed JP | `BPRJ-R1` | 16 MiB | `7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857` |
| FireRed EN | `BPRE-R1` | 16 MiB | `c4d0119d9bcb36687f41a8f7ca72ab7af60558e4` |
| LeafGreen JP | `BPGJ-R0` | 16 MiB | `5946f1b59e8d71cc61249661464d864185c92a5f` |
| LeafGreen EN/EU | `BPGE-R1` | 16 MiB | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

All GBA build identities use the native four-character game code plus the header revision. Known save-library observations remain release-specific analysis, not path components.

## Repository routing

### Sakurai

Store ROM identity and provenance, header/section/bank maps, filesystem and archive catalogs, pointer/symbol maps, normalized data tables, release comparisons, reverse-engineering notes, extraction/rebuild verification, crosswalks, and behavioral tests.

### Tsubaki

Store only production-facing material: verified input locks, asset catalogs/fingerprints, conversion recipes, insertion-ready generated data, converters, build manifests, patches, and transformed project assets. Raw ROMs and unmodified ROM-extracted asset dumps are not repository payloads.

## Canonical ownership rule

An observation about one original build belongs to `LIBRARY`. A fact about one exact supplied file belongs below that release's `DUMPS`. A relationship among releases belongs to `COMPARISONS`. Generation V -> target conversion logic belongs to `PROJECTS/GEN5-TO-POCKET-MONSTERS`.
