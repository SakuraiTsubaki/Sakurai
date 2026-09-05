# Generation IV Sprite Census — Pass 1

Date: 2026-09-05

This report records sprite-asset structure verified directly from the project ROMs. ROM files themselves are not stored in this repository.

## ROMs inspected

- Pokémon HeartGold (Korean)
- Pokémon SoulSilver (Korean)
- Pokémon Platinum (Korean)
- Pokémon Diamond (USA)
- Pokémon Pearl (USA)

## HGSS sprite archives verified locally

| Category | ROM path | Archive size | Internal files | Notes |
|---|---|---:|---:|---|
| Pokémon battle sprites | `a/0/0/4` | 11,778,676 B | 2,964 | 494 slots × 6 files |
| Alternate-form battle sprites | `a/1/1/4` | 1,047,468 B | 261 | NCGR/NCLR form assets |
| Trainer back sprites | `a/0/0/6` | 523,924 B | 85 | 17 groups × 5 files |
| Pokémon icons | `a/0/2/0` | 589,656 B | 551 | 544 NCGR plus palette/cell/animation resources |
| Trainer front sprites | `a/0/5/8` | 1,663,908 B | 645 | 129 groups × 5 files |
| Overworld sprites | `a/0/8/1` | 4,637,368 B | 863 | 832 BTX0 entries plus BMD0/metadata entries |

## HG vs. SS equality

The following extracted archives are byte-for-byte identical between the analyzed HeartGold and SoulSilver ROMs:

| Archive | SHA-256 |
|---|---|
| `a/0/0/4` | `e8ae001c0a342e947494b6a0f49a95cdb13f6016b83821a4865edc36ff064ac2` |
| `a/0/0/6` | `52f8fecd7da9cf81ab0218a049c0d9a1f3c670ee246390a2b3854fa6aa79d7fc` |
| `a/0/2/0` | `ffc35362fa9e0880fa8023a89c34a94adbc78f06aa28ae966ff4028ad3d6b7e0` |
| `a/0/5/8` | `468cbb561e7299725c9cc96d3c5e1304c925c678d92c58dfa6a8db1498247f64` |
| `a/0/8/1` | `77db7598d62b7ecc28e92cb78c2bd9562aca2c496b083eb8e19cd6f653de5ac9` |
| `a/1/1/4` | `032604ea022dd39504ea3548d78e3c2f74204649588aad48ef219b0c17bcfeb1` |

For the sprite families above, HG and SS do not need separate extraction baselines.

## Pokémon battle sprite layout

`a/0/0/4` contains 2,964 internal files = 494 species slots × 6 files.

For slot `N`, members `N*6 + 0..5` are:

1. female back NCGR
2. male back NCGR
3. female front NCGR
4. male front NCGR
5. normal NCLR palette
6. shiny NCLR palette

Genderless/male-only species can have an empty female NCGR slot. Each non-empty battle NCGR is 160×80 worth of 4-bpp data and contains two 80×80 frames side-by-side.

## Sprite encryption verified

Pokémon battle NCGR data in HGSS uses the Platinum-style forward stream cipher over 16-bit words. Decryption starts from the first encrypted word and advances a 16-bit LCRNG with:

- multiplier: `0x41C64E6D`
- increment: `0x6073`

After decryption, the NCGR data renders normally with its matching NCLR palette.

## Diamond / Pearl / Platinum comparison

Diamond and Pearl use `poketool/pokegra/pokegra.narc` for the main Pokémon battle sprite archive. Both analyzed ROMs contain the same 11,778,676-byte / 2,964-member structure, and the Diamond/Pearl archives are byte-identical:

- D/P SHA-256: `3320b89c6c84341784f58f9632dbe93b44ee34e0fe16d3a6b8673aed70a9adc2`

Platinum keeps the same 2,964-member / 494×6 structure in both:

- `poketool/pokegra/pokegra.narc` — SHA-256 `71e0090fbcbdf63d74c58ad78b5d256d8da09d3d028cc18faf6f5dcd99e8c424`
- `poketool/pokegra/pl_pokegra.narc` — SHA-256 `d99ed134b21b03ae7eef8a1c8aff3072fa50ead053179bb747c008e1cfb7ed9f`

The archive structure is therefore directly comparable across DP/Pt/HGSS even though the actual sprite payloads differ.

## Practical source priority

For the Generation-IV sprite replacement baseline:

1. HGSS assets are the primary source.
2. Platinum assets are the first fallback when HGSS lacks a needed variant/asset.
3. Diamond/Pearl assets are the secondary fallback and are identical to each other for the main battle sprite archive analyzed here.
4. HG and SS can share one extracted sprite baseline for the verified categories because the archives are byte-identical.

## External format references used for cross-checking

- magical/pokemon-nds-sprites, `docs/pokegra.rst`: documents the 6-file Pokémon sprite grouping and HGSS main/alternate archive paths.
- magical/pokemon-nds-sprites, `ncgr.c`: documents the DP/PT NCGR stream-cipher routines.
- Project Pokémon HGSS File System documentation: cross-checks HGSS archive roles such as battle sprites, trainer sprites, icons, and overworld sprites.

## Next pass

Build an index-level manifest and extraction set for:

- all 493 Pokémon front/back normal/shiny/gender slots
- alternate forms and eggs
- trainer front/back sprites
- Pokémon icons
- overworld/following-Pokémon sprites
- animation/cell resources

No ROM data should be committed; only manifests, hashes, tooling, and derived analysis records belong in the repository.
