# GS Korean-style Generation I Korean title family

This directory documents the shared title-logo design pass for Japanese Generation I -> Korean localization.

## Fixed design rule
- Korean Gold/Silver is the technical and visual Korean implementation reference.
- Preserve the GS Korean common `포켓몬스터` title logo exactly, including the final `터`.
- Replace only the version-name zone.
- Use actual GS Korean Hangul glyph silhouettes for readability.
- Apply candidate B treatment: exterior-only black outline plus top/left highlight by recoloring existing glyph pixels.
- Do not use generated artwork.

## Current visual family
- Red: `레드`
- Green: `그린`
- Blue: `블루`
- Pikachu: `피카츄`

`피카츄` is three syllables, so it uses a narrower layout while remaining inside the version-name zone and never overwriting the common logo.

## Status
These are title-design assets. Per-ROM integration must still be validated separately for Red, Green, Blue, and each relevant Pikachu revision because their title routines and ROM layouts are not assumed to be identical.

No ROM binaries are stored in GitHub.
