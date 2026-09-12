# Generation IV -> Gen III Sprite Integration — Phase 2C3 / 2D2A

## Status

Phase 2C3 corrects the form-archive source model. Phase 2D2A activates runtime selection among the DP, Platinum, and HGSS base battle-sprite sources while preserving the Phase 2D1 gender/front-back resolver.

## Phase 2C3 source correction

Three logical sources are preserved:

1. `DP_PT_COMMON` — 213 members, reverse/back-to-front NCGR encoding.
2. `PLATINUM_EXTENDED` — 253 members, forward/front-to-back encoding.
3. `HGSS_MAIN` — 261 members from the actual HGSS main-game `a/1/1/4` archive, forward/front-to-back encoding.

HGSS `pbr/otherpoke.narc` is retained in documentation as a DP-compatible 213-member archive, but is **not** used as the authoritative HGSS main-game form source.

HGSS members 256–260 are Substitute back/front + palette and Shadow graphics + palette. Pichu normal/spiky graphics occupy 154–157, with their palettes at 252–255.

The C3 bank contains 727 logical members (455 graphics, 272 palettes). Converted-payload deduplication yields 160 unique graphics and 94 unique palettes. Bank size is 182,896 bytes. All logical entries passed LZ10 decompression/hash roundtrip verification.

## Phase 2D2A runtime source selector

The Phase 2D1 resolver originally selected HGSS by hardcoding source-block offset `2 * 494 = 988`. Phase 2D2A replaces only that source-block calculation with a local helper in previously blank resolver space.

Source config values:

- `0` — Diamond/Pearl source
- `1` — Platinum source
- `2` — HeartGold/SoulSilver source (default)

The existing Gen IV gender-ratio resolver, front/back selection, Unown handling, Spinda postprocessing, and Emerald f0+f1 front-frame path are left intact.

Per ROM, 5,916 source/gender/side combinations were statically checked: `3 sources × 493 species × 2 gender selections × 2 sides`. All entries resolve to valid resident LZ10 graphics. The cumulative IPS32 patches reapply exactly to clean source ROMs.

## Persistent forms boundary

Persistent per-Pokémon form state is **not yet enabled** in Phase 2D2A. The safe design is to preserve form state in the existing BoxPokemon structure and pass form context to both graphics and palette loaders. Because many Gen III display routines pass only species/personality into the final picture loader, a graphics-only hook would not guarantee the same form in battle, summary, storage, trade, evolution, and other views. Phase 2D2B therefore remains pending until storage + graphics + palettes share one verified form context path.

## Supersession

Phase 2C2's form bank is superseded for HGSS form-source authority because it used the 213-member `pbr/otherpoke.narc` compatibility archive. Phase 2C3 adds and promotes the actual HGSS main-game 261-member `a/1/1/4` archive while keeping the compatibility archive documented.

No full ROM image is distributed by this phase.