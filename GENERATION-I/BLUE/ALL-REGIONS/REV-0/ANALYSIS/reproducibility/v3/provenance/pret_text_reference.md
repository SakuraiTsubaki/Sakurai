# pret/pokered text-system reference

Reference repository: `pret/pokered` (canonical English Red/Blue disassembly).

Files consulted:

- `constants/charmap.asm` — character/control-code reference.
- `macros/scripts/text.asm` — text command/macro reference; blob `a848f587f6abd6985cc08569733c7564e0472c03`.
- `layout.link` — semantic bank layout reference used by the v2 crosswalk.

Key encoding facts used only for candidate scanning:

- string terminator `@` = `$50`
- English uppercase `A..Z` = `$80..$99`
- English lowercase `a..z` = `$A0..$B9`
- digits `0..9` = `$F6..$FF`
- text command range begins at `$00`; `TX_FAR` = `$17`; `TX_END` = `$50`

The candidate scanner does not dump decoded dialogue. Exact text extraction will be implemented as a separate reversible extractor and must pass whole-ROM SHA-256 reconstruction before promotion.
