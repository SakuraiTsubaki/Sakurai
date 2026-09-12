# GS Korean → Pocket Monsters Crystal: title B analysis

## Selected direction

- Title: `포켓몬스터 크리스탈`
- Common `포켓몬스터`: preserve the official Korean Gold/Silver common title artwork exactly through x=128.
- Version block: `크 리 / 스 탈` in a 2×2 arrangement.
- Styling: approved B treatment — exterior-only 1 px black outline, gray body, top/left white highlight by recoloring existing glyph pixels only.
- Do not redraw Hangul stroke topology.
- Do not modify the final `터` of `포켓몬스터`.

## Verified GS Korean glyph codes

| Glyph | Korean table | Index |
|---|---:|---:|
| 크 | 9 | 0x79 |
| 리 | 4 | 0x3E |
| 스 | 6 | 0x4A |
| 탈 | 9 | 0x8B |

Cross-check source: `Narishma-gb/pokegold-kr/constants/charmap/korean_table_4.asm`, `korean_table_6.asm`, and `korean_table_9.asm`.

## Output geometry

- Visual block: 31×32 px.
- Tile-aligned implementation asset: 32×32 px = 4×4 Game Boy 2bpp tiles = 256 bytes.
- Layout: `크 리` / `스 탈`.
- Main-title invariant: pixels x=0..128 in the common logo zone remain pixel-identical to official Korean Gold/Silver.

## Source ROM fingerprints

- Korean Gold SHA-256: `9c273e86e6120c6a038160ccb0153b8b20425b84fc08a496281c1d1bcac492f6`
- Korean Silver SHA-256: `ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22`
- Japanese Crystal SHA-256: `136ada06cb68656b7de475fa4b278d37dbeff8f5257e7dfdf7f4a4aec19a90f3`

## Status

Visual/title asset complete. Actual Japanese Crystal title-screen tile/VRAM/animation insertion and runtime validation are pending. ROM binaries are not stored in GitHub.
