# Text / font engine reconstruction — Phase 2, Part 2

Part 2 continues from the `Text_InitWindowWithTemplate` boundary established by Part 1 and maps the window/text-printer initialization layer through the function immediately before `PrintNextChar`.

## Verification scope

- 13 verified Pokémon Ruby ROM targets.
- 93 target/function records reproduced after whole-ROM SHA-1 verification.
- International/debug builds share one stable relative layout.
- Japanese Rev 0 again has a distinct API/function order and contains additional routines at this location.
- The next verified boundary in all targets is `PrintNextChar`.

## International/debug layout

| Function | Relative offset | Size |
|---|---:|---:|
| `Text_InitWindowWithTemplate` | `+0x000` | `0x6C` |
| `Text_InitWindow` | `+0x06C` | `0x8C` |
| `Text_InitWindow8002E4C` | `+0x0F8` | `0x44` |
| `Text_SetWindowText` | `+0x13C` | `0x20` |
| `Contest_StartTextPrinter` | `+0x15C` | `0x94` |
| `Text_PrintWindow8002F44` | `+0x1F0` | `0x5C` |
| `sub_8002FA0` | `+0x24C` | `0x40` |

The public reconstructed source confirms the important control flow: `Text_PrintWindow8002F44` repeatedly handles newline/placeholder state and calls `PrintNextChar`; `sub_8002FA0` temporarily substitutes a placeholder string, invokes `Text_PrintWindow8002F44`, then restores the saved text/language state.

## Japanese Rev 0 layout

| Function / label | Relative offset | Size | Status |
|---|---:|---:|---|
| `Text_InitWindowWithTemplate` | `+0x000` | `0x40` | behavior verified |
| `Text_InitWindow` | `+0x040` | `0x58` | behavior verified |
| `JP_TextPrinterHelper_02CC0` | `+0x098` | `0x3C` | provisional name, behavior verified |
| `Text_InitWindow8002E4C` | `+0x0D4` | `0x20` | probable source-equivalent wrapper |
| `Contest_StartTextPrinter` | `+0x0F4` | `0x98` | behavior verified |
| `sub_8002FA0` | `+0x18C` | `0x34` | behavior verified |
| `Text_PrintWindow8002F44` | `+0x1C0` | `0x50` | behavior verified |
| `Text_SetWindowText` | `+0x210` | `0x1C` | behavior verified |
| `Text_PrintWindowSimple` | `+0x22C` | `0x38` | behavior verified |

`JP_TextPrinterHelper_02CC0` creates/initializes a temporary window through the Japanese WindowTemplate lookup path and immediately drives the synchronous printer. Its behavior is established from the ROM, but a trustworthy original symbol name has not yet been established, so the descriptive name remains provisional.

The Japanese build also places `Text_PrintWindowSimple` before `PrintNextChar`, unlike the international source order represented by the current public reconstruction. This is another reason to keep Japan as its own linked layout rather than forcing it through international offsets.

## Target regions

| Target | Start | End | Bytes | Region SHA-1 |
|---|---:|---:|---:|---|
| `japan_rev0` | `0x2C28` | `0x2E8C` | `0x264` | `4b49d7724124d8a40f947f0a3f9873bd0717baec` |
| `english_rev0` | `0x2D54` | `0x2FE0` | `0x28C` | `fe45f2796364ca6f814f0ccae6b7903f651a4eb4` |
| `english_rev1` | `0x2D54` | `0x2FE0` | `0x28C` | `d13643ce31522a5ee969f1b742eeeddc25956b0b` |
| `english_rev2` | `0x2D54` | `0x2FE0` | `0x28C` | `d13643ce31522a5ee969f1b742eeeddc25956b0b` |
| `germany_rev0` | `0x2E88` | `0x3114` | `0x28C` | `358243a01b2c9b2d99a0193bc24b8fec8791eee9` |
| `germany_rev1` | `0x2E88` | `0x3114` | `0x28C` | `358243a01b2c9b2d99a0193bc24b8fec8791eee9` |
| `germany_debug_rev0` | `0x2EA0` | `0x312C` | `0x28C` | `9ba4eed300f6c4a5f45d2de7f18b7aeba172d1d0` |
| `france_rev0` | `0x2E88` | `0x3114` | `0x28C` | `b2eca139ad0f153781943ab5eeab24e085ab870e` |
| `france_rev1` | `0x2E88` | `0x3114` | `0x28C` | `b2eca139ad0f153781943ab5eeab24e085ab870e` |
| `italy_rev0` | `0x2E88` | `0x3114` | `0x28C` | `d0732eac6d78ebf8a469aa57605aaf2efb2ba171` |
| `italy_rev1` | `0x2E88` | `0x3114` | `0x28C` | `d0732eac6d78ebf8a469aa57605aaf2efb2ba171` |
| `spain_rev0` | `0x2E88` | `0x3114` | `0x28C` | `e7cd47f1f8d50655ea6d68a4ca4b9b89539184ee` |
| `spain_rev1` | `0x2E88` | `0x3114` | `0x28C` | `e7cd47f1f8d50655ea6d68a4ca4b9b89539184ee` |

## Next pass

Part 3 begins at `PrintNextChar`. It will map the core text state machine plus the initial extended-control-code dispatcher/handlers. This area is especially important because it defines how encoded text, placeholders, colors, font switches, pauses, input waits, music commands and escaped glyphs are interpreted.
