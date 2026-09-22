# Korean message-code and width-descriptor confirmation

## SoulSilver message code → glyph ID

The Korean SoulSilver message archive is NitroFS `a/0/2/7` (822 NARC members). Its member 233 contains 496 short name entries and aligns with the species-name bank: message 1 is 이상해씨, 2 이상해풀, 3 이상해꽃, 4 파이리, etc.

The retail message decryption algorithm from the HGSS message format yields u16 codes. Rendering maps each non-control u16 value as a one-based glyph ID, so font slot = code - 1. Examples from the supplied IPGK-HV0 image:

- `0A0C 085D 0CAA 0942 FFFF` → slots 2571, 2140, 3241, 2369 → 이상해씨
- `0A0C 085D 0CAA 0C80 FFFF` → 이상해풀
- `0A0C 085D 0CAA 04E5 FFFF` → 이상해꽃
- `0C38 0A0C 06FE FFFF` → 파이리
- `0C99 0B63 0B4C FFFF` → 피카츄

This confirms the 2350-syllable KS X 1001/Wansung slot sequence `1024..3373` against actual retail text, not only visual order. The locally generated `soulsilver_msg233_species_names.csv` records the complete decoded bank.

Compatibility-jamo mapping also has direct message evidence: several banks store standalone jamo strings using the corresponding high glyph IDs. Only observed jamo slots are promoted to `confirmed_message_use`; unobserved members of the A4A1..A4D3 sequence remain marked inferred.

Slots 3427 and 3428 are real non-fallback glyphs but the entire `a/0/2/7` message archive contains no use of glyph IDs 3428/3429, so their identity remains unresolved rather than guessed.

## Korean width descriptor

The `widthDataStart` region is a segmented descriptor, not a flat `numGlyphs` width array. The 509-glyph Korean-localized member has one section; 3440-glyph members have three.

For 3440-glyph members the section boundaries are 509, 1024 and 3440. The first section uses selector `FFFF` and points to the following 509-byte VWF table. The second uses `FFFE` for the reserved 509..1023 region. The third selector is a literal Korean advance width: 11, 12, 13, 12, 11 for HGSS Font IDs 0,1,2,4,5 respectively.

`korean_width_descriptor.csv` records the raw descriptor fields. The `FFFE` runtime semantics still require executable-path confirmation; no semantic name is assigned yet.
