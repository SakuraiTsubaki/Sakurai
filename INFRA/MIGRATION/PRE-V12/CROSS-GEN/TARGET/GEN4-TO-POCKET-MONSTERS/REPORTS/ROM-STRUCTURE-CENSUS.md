# Generation IV → ポケットモンスター — ROM structure census

## NDS sources
| Game | Release | FAT | FNT dirs | Named NitroFS | Named NARC |
|---|---|---:|---:|---:|---:|
| Diamond | `ADAE-HV5` | 356 | 69 | 269 | 149 |
| Pearl | `APAE-HV5` | 356 | 70 | 269 | 149 |
| Platinum | `CPUK-HV0` | 461 | 105 | 339 | 215 |
| HeartGold | `IPKK-HV0` | 511 | 46 | 382 | 308 |
| SoulSilver | `IPGK-HV0` | 511 | 46 | 382 | 308 |

D/P `poketool/pokegra/pokegra.narc` and Platinum `poketool/pokegra/pl_pokegra.narc` are 11,778,676 bytes with 2,964 members. HGSS `a/0/0/4` has the same size/member count and is retained as a strong sprite-archive candidate until semantics are independently verified. HGSS icon/animation/footprint/height/shadow/y-offset paths recorded in Tsubaki are exact SHA-1 matches to the corresponding DPPt containers/resources where marked confirmed.

## GBA targets
All five header complement checks pass. Largest mechanically detected long 00/FF runs: Ruby 163,464 bytes; Sapphire 163,488; Emerald 2,008,864; FireRed 5,492,044; LeafGreen 5,473,412.

These are **allocation candidates only**, not certified free space. Pointer, compressed-data, table-boundary, executable reachability, and runtime regression checks are mandatory before use.
