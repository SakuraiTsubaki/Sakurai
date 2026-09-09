# Banks $00–$0F deep dive

This is the first semantic tranche of the full bank survey. Difference counts are direct byte comparisons against the uploaded English Gold ROM; Japanese revision deltas are Rev 0 ↔ Rev A.

| Bank | Semantic role | JP Rev delta | KR vs EN | ES vs EN | DE vs EN | FR vs EN | IT vs EN | Finding |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| `$00` | vectors/header/home | 5 | 14,820 | 12,071 | 11,991 | 11,944 | 11,943 | Region-specific home code/addresses; KR RST implementation differs materially |
| `$01` | link wait, OAM, map objects, menus, map init, learn/math/items/NPC/events | 0 | 13,099 | 12,977 | 13,055 | 6,625 | 13,072 | JP revisions identical; heavy localization/linkage differences |
| `$02` | palettes, player object, sine, predefs, color | 0 | 10,607 | 312 | 319 | 317 | 319 | Western builds are extremely close; KR/JP engine layout diverges |
| `$03` | time/flags/specials/items/overworld/battle UI/PC/breeding/item effects | 0 | 14,024 | 12,127 | 6,935 | 6,988 | 13,845 | Large regional layout differences despite same logical engine family |
| `$04` | movement/pack/time/TMHM/naming/menus/events/bug contest/Pokérus | 5 | 14,080 | 13,468 | 13,226 | 12,254 | 13,171 | One of ten JP revision-change banks |
| `$05` | RTC/overworld/save/map setup/marts/mom/daycare/Unown/photo/mystery gift/breeding | 1 | 8,663 | 11,307 | 11,300 | 11,355 | 11,387 | One-byte JP revision fix; substantial regional relocation |
| `$06` | tileset data 1 | 0 | 12,727 | 12,666 | 12,641 | 12,666 | 12,664 | Same logical graphics bank but binary packing differs heavily |
| `$07` | roofs / tileset data 2 / extra songs 1 | 0 | **4** | **2** | **2** | **2** | **2** | Near-global common bank; only tiny pointer/address adjustments. Strong shared-data anchor |
| `$08` | clock reset / tileset data 3 / catch tutorial / egg moves | 0 | 10,881 | 1,115 | 1,016 | 1,015 | 1,114 | Western versions remain close; translated/tutorial-dependent content causes deltas |
| `$09` | text buffers/menus/item description UI/pokepic/trainer card/decorations/battle helpers | 1 | 14,383 | 11,492 | 11,096 | 6,555 | 12,537 | One-byte JP revision change; localization-sensitive UI bank |
| `$0A` | link / mystery gift / wild Pokémon | 1 | 15,872 | 15,289 | 15,342 | 15,220 | 15,056 | Highly region-dependent link/wild implementation/placement |
| `$0B` | item/move description UI, trainer HUD, AI, TMHM, Pokérus | 0 | 861 | 497 | **122** | 2,027 | 2,020 | Strong common engine bank; German especially close to EN |
| `$0C` | tileset data 4 | 0 | **0** | **0** | **0** | **0** | **0** | **Byte-identical across all eight ROMs.** Best universal anchor bank found in `$00–$0F` |
| `$0D` | battle effect commands | 0 | 9,566 | 7,171 | 7,298 | 7,194 | 7,058 | Same semantic subsystem; pointer/layout shifts are substantial |
| `$0E` | trainer AI/items/scoring/attributes/party | 0 | 7,937 | 7,066 | 7,550 | 7,523 | 7,309 | Trainer/localized data mixed with common code |
| `$0F` | battle core + effect command pointers | 2 | 13,381 | 3,157 | 9,505 | 13,300 | 3,141 | JP revision has 2-byte change; Spanish/Italian closest to EN among localizations |

## Confirmed common anchors

- **Bank `$0C` is byte-for-byte identical in all eight uploaded ROMs.** This makes it a high-confidence cross-region alignment anchor.
- Bank `$07` differs from English by only 2 bytes in ES/DE/FR/IT and 4 bytes in KR. Its payload is effectively shared with small pointer/address adjustments.
- Japanese Rev 0 and Rev A are identical for `$01,$02,$03,$06,$07,$08,$0B,$0C,$0D,$0E`; changes in this tranche occur only in `$00,$04,$05,$09,$0A,$0F`.

## Disassembly consequence

Do not copy addresses between regions even where logical roles match. Use `$0C` and the near-identical `$07` as alignment anchors, then reconstruct local symbol maps outward. Banks `$00,$04,$05,$09,$0A,$0F` must preserve revision-specific Japanese labels/bytes instead of collapsing Rev 0 and Rev A into a single source.
