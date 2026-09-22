# Generation IV Korean font census — Pt / HGSS → Emerald integration

Status: working census from supplied retail ROMs; raw `.nds` images are not repository artifacts.

## Confirmed ROM evidence

- Korean Platinum CPUK-HV0 (`SHA-256 51050f65…11d7b`): `graphic/font.narc` and `graphic/pl_font.narc`, 10 members each.
- Korean SoulSilver IPGK-HV0 (`SHA-256 8e1c82d2…8b55`): `a/0/1/6`, 13 members.
- The principal Korean members have a 16-byte simple-font header: `tableOffset=0x35C10`, `numGlyphs=3440`, `16x16`, `2bpp`, total member size `220717`.
- The tail is only `541` bytes. It decomposes structurally as a 32-byte block plus exactly `509` bytes, not 3440 bytes. Therefore the Korean extension does **not** simply append a width byte for every Korean glyph. The exact localized width code path remains to be pinned from Korean executable code.

## Slot layout now established

Pixel identity and visible glyph order establish the following layout:

- slots `0..508`: legacy/base 509-glyph set;
- slots `509..1023`: 515 repeated fallback/reserved slots;
- slots `1024..3373`: 2350 KS X 1001/Wansung Hangul syllables, in EUC-KR `B0A1..C8FE` row-major order (mapping recorded as inferred pending message-code correlation);
- slots `3376..3426`: 51 modern compatibility jamo corresponding to EUC-KR `A4A1..A4D3` (same caveat);
- `3374,3375,3429..3439`: fallback/unmapped;
- `3427..3428`: real non-fallback glyphs, exact character identity still requires message correlation.

This means the Gen IV Korean table contains 2403 clearly usable Korean glyph slots (2350 syllables + 51 modern jamo + 2 still-unidentified non-fallback glyphs), not all modern Unicode Hangul syllables.

## Cross-game pixel identity

For corresponding Korean members 0/1/2, **all 2416 slots in 1024..3439 are byte-identical between Platinum and SoulSilver**. Pt `graphic/font.narc` vs Pt `graphic/pl_font.narc` likewise keeps those Korean slots byte-identical for members 0/1/2. The game/archive differences are primarily in the base 509 region and reserved/fallback region.

HGSS members 4 and 10 are genuinely different Korean designs; they are not copies of members 0/1/2.

## HGSS Korean glyph geometry

- FontID 0 → member 0: Korean ink is exactly 11×11 across the 2350 Wansung syllables.
- FontID 1 → member 1: exactly 12×12.
- FontID 2 → member 2: about 12–13×11–12.
- FontID 4 → member 4: about 11–12×11–12.
- FontID 5 → member 10: exactly 11×10.
- FontID 3 → member 3 is the 509-glyph class and is not a 3440 Korean member.

Platinum names the first four logical fonts `SYSTEM=0`, `MESSAGE=1`, `SUBSCREEN=2`, `UNOWN=3`. HGSS maps Font IDs `0,1,2,3,4,5` to members `0,1,2,3,4,10`.

## Emerald mapping decision (phase 1)

The mapping is by original usage and actual Korean pixel geometry, not by copying one DS font everywhere:

- `FONT_NORMAL` ← Gen IV MESSAGE / HGSS FontID 1.
- `FONT_SMALL` ← Gen IV SYSTEM / HGSS FontID 0.
- `FONT_SHORT` ← Gen IV SUBSCREEN / HGSS FontID 2.
- `FONT_NARROW` ← HGSS FontID 5 / member 10 as the compact source, subject to completion of its original call-site census.
- `FONT_SMALL_NARROW` ← deterministic 8px project derivative of member 10; there is no direct Gen IV 8px Korean original.

HGSS FontID 4 is retained as an additional application/UI source rather than discarded; it is heavily used by HGSS application screens and may become a separate project UI font if Emerald screen-specific routing warrants it.

Important engine point: Emerald's `TextGlyph` buffer is already 16 pixels wide (`gfxBufferTop[16]` + `gfxBufferBottom[16]` rows), and the Japanese width tables already use widths around 10–12 even where the Latin `FontInfo.maxLetterWidth` is smaller. Therefore Korean glyphs do **not** need to be crushed to 5–6 pixels. The correct route is a Korean decompressor/lookup path that preserves roughly 10–13 pixel glyph widths.

## Encoding direction

Emerald's stock byte encoding has no room for 2350+ syllables. `CHAR_EXTRA_SYMBOL (0xF9)` only expands to a 256-entry secondary range and is insufficient. A multi-byte Korean token must be added while preserving existing single-byte characters/control codes. The preferred implementation direction is a dedicated extended token with a 12-bit-or-larger glyph index, with every string-length/copy/width/render helper updated consistently. Exact control-code allocation is not frozen until the full text helper audit is complete.

## Next executable work

1. Correlate Korean message codes against the 1024+ glyph slots to promote the EUC-KR mapping from inferred to confirmed and identify slots 3427/3428.
2. Pin the localized Korean width logic in Pt/HGSS ARM9/overlays.
3. Complete HGSS FontID 4/5 call-site census.
4. Feed the extracted Gen IV pixels into the existing Hangul generator pipeline, replacing the vector-font raster source for covered syllables; generate only missing modern syllables as explicitly marked project derivatives.
5. Implement the Emerald multi-byte Korean token and 16px-capable glyph lookup without replacing existing Latin/Japanese assets.
