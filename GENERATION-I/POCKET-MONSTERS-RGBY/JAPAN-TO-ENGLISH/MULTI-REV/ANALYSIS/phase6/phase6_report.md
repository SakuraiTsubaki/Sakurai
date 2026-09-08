# RGBY English text controls — phase 6

## Result

- Added target-runtime `PAGE` (`$49`), English `PKMN` (`$4A`), and English-period `DEXEND` (`$5F`) handling to all nine verified Japanese ROM revisions.
- Added the English single-spaced `NEXT` behavior behind layout-flag bit 2. With the flag clear, the original two-tile-row spacing remains unchanged.
- Kept the Japanese decoder/source namespace separate: `$4A` remains Japanese `<GA>` while extracting source text, but becomes target English `<PKMN>` only in rebuilt English ROMs.
- Reused the verified English font and phase-4 `TX_FAR` implementation cumulatively.
- Used no new ROM bank and did not grow Bank 0. The new 92-byte dispatcher/handler block occupies only verified unused header padding after the existing `TX_FAR` block.

## Diagnostic design

Each diagnostic patch temporarily redirects `OakSpeechText1` through `TX_FAR` to a revision-specific, uniquely matched unused blob. Its test script enables single spacing and exercises this sequence:

`A` → `<NEXT>` → `B <PKMN>` → `<PAGE>` → `OK<DEXEND>`

The diagnostic patch is test-only. Core patches contain no Oak redirect or test payload, and original uploaded ROMs are never modified.

## Verification

- Exact original opcode validation at every hook
- Exact 1024-byte English-font hash validation
- Header-gap bounds and handler-size checks
- Per-revision checksum regeneration
- IPS round-trip and diff-confinement tests
- PyBoy runtime verification passed all nine revisions; details are recorded in `runtime_control_results.json`
