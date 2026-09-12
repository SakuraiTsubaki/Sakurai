# Generation IV → ポケットモンスター — ROM structure census

This report records ROM-derived structural observations for the currently locked source/target set. Original ROM binaries are not committed.

## Generation IV NDS sources

| Game | Release | Locale | ROM size | FAT entries | FNT directories | Named NitroFS files | Named NARC files |
|---|---|---|---:|---:|---:|---:|---:|
| Diamond | `ADAE-R5` | US-EN | 64 MiB | 356 | 69 | 269 | 149 |
| Pearl | `APAE-R5` | US-EN | 64 MiB | 356 | 70 | 269 | 149 |
| Platinum | `CPUK-R0` | KR-KO | 128 MiB | 461 | 105 | 339 | 215 |
| HeartGold | `IPKK-R0` | KR-KO | 128 MiB | 511 | 46 | 382 | 308 |
| SoulSilver | `IPGK-R0` | KR-KO | 128 MiB | 511 | 46 | 382 | 308 |

### Sprite/resource structure observations

- Diamond: `poketool/pokegra/pokegra.narc` — 11,778,676 bytes, 2,964 members.
- Pearl: `poketool/pokegra/pokegra.narc` — 11,778,676 bytes, 2,964 members.
- Platinum: `poketool/pokegra/pl_pokegra.narc` — 11,778,676 bytes, 2,964 members; `poketool/pokegra/pokegra.narc` is also present.
- HeartGold/SoulSilver: `a/0/0/4` — 11,778,676 bytes, 2,964 members. This is a strong sprite-archive candidate because its NARC structure/count matches DPPt `pokegra`; content differs, so the semantic label remains provisional.
- HGSS `a/2/2/8` exactly matches the DPPt Pokémon icon NARC by SHA-1.
- HGSS `a/1/1/1` exactly matches DPPt `poketool/pokeanm/pokeanm.narc` by SHA-1.
- HGSS `a/0/6/9` exactly matches DPPt `poketool/pokefoot/pokefoot.narc` by SHA-1.
- HGSS `a/1/9/4`, `a/1/9/5`, `a/1/3/5`, `a/1/3/7`, and `a/1/3/2` exactly match the corresponding DPPt height/shadow/y-offset resources by SHA-1.

Production-facing mappings live in Tsubaki under `PROJECTS/GEN4-TO-POCKET-MONSTERS/SOURCE/SPRITES/SPRITE-SOURCE-MAP.json`.

## Generation III Japanese target baselines

All five target ROM headers pass the GBA header-complement checksum test.

| Game | Release | Size | Largest mechanically detected long 00/FF run |
|---|---|---:|---:|
| Ruby | `AXVJ-R0` | 8 MiB | 163,464 bytes (`FF`) |
| Sapphire | `AXPJ-R0` | 8 MiB | 163,488 bytes (`FF`) |
| Emerald | `BPEJ-R0` | 16 MiB | 2,008,864 bytes (`FF`) |
| FireRed | `BPRJ-R1` | 16 MiB | 5,492,044 bytes (`FF`) |
| LeafGreen | `BPGJ-R0` | 16 MiB | 5,473,412 bytes (`FF`) |

### Allocation safety rule

The long 00/FF census is **not** a free-space certificate. A candidate range cannot be allocated until pointer references, compressed-data boundaries, table extents, executable reachability, and runtime/regression behavior are checked. ROM expansion or deliberate relocation remains preferred when ownership cannot be proven safely.

## Ownership under Structure v4

- Release-intrinsic observations belong under `LIBRARY/GEN-XX/<PLATFORM>/<GAME>/RELEASES/<RELEASE-ID>/...`.
- Exact supplied-file observations belong below that release's `DUMPS/<DUMP-ID>/...`.
- The source/target relationship is project-relative and is locked in `PROJECTS/GEN4-TO-POCKET-MONSTERS/MANIFESTS/release-lock.json`.
- Cross-generation mapping, design, implementation planning, and integration verification belong under `PROJECTS/GEN4-TO-POCKET-MONSTERS/`.
- Original ROM images and wholesale ROM/NitroFS binary dumps are excluded from GitHub.
