# Korean Generation IV font width routing — ARM9 confirmation

Status: confirmed against supplied Korean retail Platinum and SoulSilver ROMs.

## Retail binaries

- Platinum Korean `CPUK`: ARM9 runtime base `0x02000000`; localized range-width function at `0x02023AD4`.
- SoulSilver Korean `IPGK`: ARM9 is Nintendo backward-LZ compressed in the ROM image. The compressed ARM9 is `0xBAD18` bytes and expands to `0x1128F8` bytes. Runtime base is `0x02000000`; localized range-width function at `0x02026514`.
- The complete 90-byte range-width function bodies at Pt `0x02023AD4` and SS `0x02026514` are byte-identical.

## Width metadata block

For the 3440-glyph Korean font members, `header.widthDataStart = 0x35C10`. The remaining 541 bytes are not a flat 3440-byte width table.

Layout:

- `+0x00 u32 payload_size = 0x219` (537 bytes after this field)
- `+0x04 u32 range_count = 3`
- `+0x08`: three 8-byte range descriptors
- `+0x20`: 509-byte legacy variable-width table

Each 8-byte descriptor is interpreted as:

```text
u16 endExclusive;
s16 widthModeOrValue;
u32 tableOffset;
```

The range-width function tracks the previous range end as `start`, selects the first descriptor where `glyphIndex < endExclusive`, then handles `widthModeOrValue` as follows:

- `-1 / 0xFFFF`: variable width. Return `base[tableOffset + glyphIndex - start]`.
- `-2 / 0xFFFE`: use the fallback glyph width by recursively querying zero-based glyph `0x01AB` (427; one-based glyph ID 428).
- any other value: return its low byte directly as a fixed width.

Pseudo-code reconstructed from both retail ARM9 binaries:

```c
u32 GetGlyphWidth_Korean(FontData *font, u16 glyphIndex)
{
    WidthBlock *w = font->widthBlock;
    u16 start = 0;

    for (u32 i = 0; i < w->rangeCount; i++) {
        Range *r = &w->ranges[i];
        if (glyphIndex < r->endExclusive) {
            if (r->mode == -1)
                return *((u8 *)w + r->tableOffset + glyphIndex - start);
            if (r->mode == -2)
                return GetGlyphWidth_Korean(font, 0x01AB);
            return (u8)r->mode;
        }
        start = r->endExclusive;
    }

    return GetGlyphWidth_Korean(font, 0x01AB);
}
```

## Korean font descriptors

Localized Pt `graphic/pl_font.narc` and HGSS `a/0/1/6` use:

```text
range 0: end= 509, mode=0xFFFF, tableOffset=0x1C
range 1: end=1024, mode=0xFFFE, tableOffset=0
range 2: end=3440, mode=<fixed Korean width>, tableOffset=0
```

The `0x1C` table offset is relative to the width payload beginning immediately after the leading `payload_size` field: `4-byte range_count + 3*8-byte descriptors = 0x1C`.

Fixed Korean widths:

| logical source | member | Korean range width |
| --- | ---: | ---: |
| SYSTEM / HGSS FontID 0 | 0 | 11 px |
| MESSAGE / HGSS FontID 1 | 1 | 12 px |
| SUBSCREEN / HGSS FontID 2 | 2 | 13 px |
| HGSS FontID 4 | 4 | 12 px |
| HGSS FontID 5 | 10 | 11 px |

This explains why the Korean font can contain 3440 glyphs while carrying only 509 individual width bytes: only the legacy `0..508` range is per-glyph variable-width. The Korean `1024..3439` range is fixed-width per font design.

## Generic Platinum archive difference

Pt `graphic/font.narc` has the same 3-range structure, but its middle `509..1023` descriptor uses fixed width `0` instead of `0xFFFE`. Pt localized `graphic/pl_font.narc` and HGSS localized `a/0/1/6` use `0xFFFE`, which routes that reserved range to the normal fallback glyph width.

## Initialization behavior

The Korean Pt/HGSS FontData initialization path does not allocate `numGlyphs` width bytes. It:

1. reads the 4-byte `payload_size` from `widthDataStart`;
2. allocates exactly that many bytes;
3. reads the width payload from `widthDataStart + 4`;
4. assigns the range-aware width function above.

This differs from the current public decompilation source's simplified flat-width-table implementation and must be preserved when reconstructing Korean behavior.

## Emerald consequence

For the Emerald backport, Gen IV Korean source glyphs should retain their original font-specific fixed advance widths rather than using a generated width per syllable:

- dialogue/body source: 12 px;
- system source: 11 px;
- subscreen source: 13 px;
- compact HGSS sources: 12 px / 11 px as above.

The reserved/fallback behavior should also remain explicit rather than silently treating all unassigned Korean token values as width zero.
