# HGSS Korean FontID 4/5 call-site census

Status: complete for the supplied Korean SoulSilver retail ROM `IPGK01 Rev.00`.

ROM SHA-256: `8e1c82d2f718fa404f0b13df1666c70cdfaa75cb67e0adcbdcfb6c002f4d8b55`

## Binary method

The Korean retail ROM itself is the primary evidence.

- ARM9 ROM image: `0xBAD18` bytes, Nintendo backward-LZ compressed.
- ARM9 expands to `0x1128F8` bytes at runtime base `0x02000000`.
- `FontID_Alloc` is at runtime address `0x02002CEC`.
- ARM9 overlay table contains 129 entries.
- Every compressed overlay was expanded using the Nitro backward decompression format and checked against its declared runtime `ramSize`.
- Every Thumb `BL` targeting `0x02002CEC` was decoded.
- The immediate FontID in `r0` was recovered at every call site; unresolved call sites: **0**.
- Full machine-readable addresses are in `fontid-callsite-census.csv`.

## Complete Korean retail call counts

Across ARM9 + all 129 ARM9 overlays:

| FontID | member | calls to FontID_Alloc | interpretation |
| ---: | ---: | ---: | --- |
| 0 | 0 | 1 | core/system font, allocated during ARM9 startup |
| 1 | 1 | 1 | core/message font, allocated during ARM9 startup |
| 2 | 2 | 13 | subscreen/special-screen font |
| 3 | 3 | 1 | base 509-glyph class, allocated during ARM9 startup |
| 4 | 4 | 65 | broad application/UI font |
| 5 | 10 | 2 | compact special-purpose font used by Pokéwalker UI |
| **total** |  | **83** |  |

The overlay portion alone contains 74 calls: FontID 2 = 11, FontID 4 = 61, FontID 5 = 2.

## FontID 4

FontID 4 / member 4 is not an isolated font. It is broadly allocated across application overlays. The Korean retail binary contains 65 allocations in total, including battle/application/menu-class overlays and the Pokéwalker overlay.

This supports keeping member 4 as an original HGSS application/UI source rather than discarding it or treating it as a duplicate of the normal message font.

## FontID 5 / member 10

The earlier source-index-only search falsely suggested that FontID 5 might be unused. The Korean retail binary disproves that.

Exactly two allocations occur in `OVY_112`:

- `0x021E9B14` → FontID 5
- `0x021E9B66` → FontID 5

`OVY_112` is the Pokéwalker connection application. The main-menu source registers `OVY_112` for `ov112_App_MainMenu_SelectOption_ConnectToPokewalker`.

Direct inspection of the corresponding public `asm/overlay_112.s` also shows the same two semantic FontID 5 uses:

1. a routine that obtains the player profile name with `PlayerProfile_GetPlayerName_NewString`, allocates FontID 5, and prints the player name with font ID 5;
2. a routine that opens message bank `0xED`, allocates FontID 5, and prints Pokéwalker UI strings with font ID 5.

Therefore HGSS member 10 is a **used, original compact Pokéwalker UI font**, not unused data.

## Why the earlier search missed it

A GitHub repository-wide Code Search for `FontID_Alloc` returned 101 indexed files with `incomplete_results=false`, but `asm/overlay_112.s` was not in that result set despite containing four allocations, including the two FontID 5 calls.

For this project, Code Search result completeness must therefore not be treated as proof of call-site completeness. The retail binary scan is the authoritative census; direct source-file inspection is used for semantic labeling.

## Emerald integration consequence

The phase-1 mapping can now be tightened:

- `FONT_NORMAL` ← Gen IV MESSAGE / FontID 1 source.
- `FONT_SMALL` ← Gen IV SYSTEM / FontID 0 source.
- `FONT_SHORT` ← Gen IV SUBSCREEN / FontID 2 source.
- `FONT_NARROW` ← HGSS FontID 5 / member 10 is acceptable as the compact source, **but this is a project mapping**. Its original HGSS use is specifically Pokéwalker UI/player-name rendering, not a global narrow-font role.
- FontID 4 / member 4 should remain available as an additional HGSS application/UI source.

This preserves the distinction between original usage and the Emerald integration choice.
