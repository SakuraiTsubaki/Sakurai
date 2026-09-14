# Text / font engine reconstruction — Phase 2, Part 1

This pass begins at the exact `sprite.o -> text.o` boundary established in `SPRITE_PHASE2_PART4.md` and maps the first text/font/window-engine block through `EmptyFunc`.

## Verification scope

- 13 verified Pokémon Ruby ROM targets.
- 2 linked-layout families: Japanese Rev 0 and international/debug.
- 185 target/function fingerprint records reproduced after whole-ROM SHA-1 verification.
- No ROM data is stored in Git; only addresses, sizes, hashes, semantic notes and reproducible tooling are committed.
- The next verified function after this block is `Text_InitWindowWithTemplate` in both layout families.

The machine-readable layouts are in `symbols/text_part1_layouts.csv`, target region fingerprints are in `symbols/text_part1_targets.csv`, and `tools/analyze_text_part1.py` reproduces/validates the records.

## International/debug layout

The international/debug builds follow the function order represented by the reconstructed `pret/pokeruby` `text.c` source:

| Function | Relative offset | Size |
|---|---:|---:|
| `UpdateBGRegs` | `+0x000` | `0x3C` |
| `ClearBGMem` | `+0x03C` | `0x34` |
| `LoadFontDefaultPalette` | `+0x070` | `0x18` |
| `Text_LoadWindowTemplate` | `+0x088` | `0x1C` |
| `InitWindowTileData` | `+0x0A4` | `0x88` |
| `InitVariableWidthFontTileData` | `+0x12C` | `0x54` |
| `LoadFixedWidthFont` | `+0x180` | `0x2C` |
| `LoadFixedWidthFont_Font1Latin` | `+0x1AC` | `0x34` |
| `LoadFixedWidthFont_Font4Latin` | `+0x1E0` | `0x3C` |
| `LoadFixedWidthFont_Braille` | `+0x21C` | `0x34` |
| `MultistepInitWindowTileData` | `+0x250` | `0x58` |
| `MultistepLoadFont` | `+0x2A8` | `0x64` |
| `MultistepLoadFont_LoadGlyph` | `+0x30C` | `0x98` |
| `EmptyFunc` | `+0x3A4` | `0x04` |

All 12 international/debug targets use these exact relative offsets. Their code fingerprints differ where absolute pointers, localized data, or debug-specific addresses differ.

## Japanese Rev 0 layout

Japanese Rev 0 uses an earlier/different text-window interface and linked function order. The first four routines pass a template key through a lookup routine at ROM address `0x08004228`; that lookup iterates key/pointer pairs and returns the associated WindowTemplate pointer. Their descriptive names below are therefore intentionally marked **provisional** until original symbol names are independently established.

| Function / descriptive label | Relative offset | Size | Naming status |
|---|---:|---:|---|
| `JP_Text_LoadWindowTemplateByKey` | `+0x000` | `0x24` | provisional name, behavior verified |
| `JP_ClearBGMemByTemplateKey` | `+0x024` | `0x10` | provisional name, behavior verified |
| `JP_LoadFontDefaultPaletteByTemplateKey` | `+0x034` | `0x10` | provisional name, behavior verified |
| `JP_UpdateBGRegsByTemplateKey` | `+0x044` | `0x10` | provisional name, behavior verified |
| `ClearBGMem` | `+0x054` | `0x30` | behavior verified |
| `LoadFontDefaultPalette` | `+0x084` | `0x18` | behavior verified |
| `UpdateBGRegs` | `+0x09C` | `0x44` | behavior verified |
| `InitWindowTileData` | `+0x0E0` | `0x94` | behavior verified |
| `MultistepInitWindowTileData` | `+0x174` | `0x90` | behavior verified |
| `MultistepLoadFont` | `+0x204` | `0x70` | behavior verified |
| `MultistepLoadFont_LoadGlyph` | `+0x274` | `0xA4` | behavior verified |
| `LoadFixedWidthFont` | `+0x318` | `0x38` | behavior verified |
| `LoadFixedWidthFont_Font1Latin` | `+0x350` | `0x34` | behavior verified |
| `LoadFixedWidthFont_Font4Latin` | `+0x384` | `0x3C` | behavior verified |
| `LoadFixedWidthFont_Braille` | `+0x3C0` | `0x34` | behavior verified |
| `InitVariableWidthFontTileData` | `+0x3F4` | `0x54` | behavior verified |
| `EmptyFunc` | `+0x448` | `0x04` | behavior verified |

The important difference is not a simple address shift: Japan changes both API plumbing and function order, so Japanese text reconstruction must remain a first-class build layout rather than inheriting the international ordering.

## Target regions

| Target | Start | End | Bytes | Region SHA-1 |
|---|---:|---:|---:|---|
| `japan_rev0` | `0x27DC` | `0x2C28` | `0x44C` | `64000792d5a1dc3eef9bdd441f62f8f9702ca01f` |
| `english_rev0` | `0x29AC` | `0x2D54` | `0x3A8` | `4e3e659ce402271de2302169527c0e5e61b8fd9d` |
| `english_rev1` | `0x29AC` | `0x2D54` | `0x3A8` | `2f7d79100843b11c97a4be28df1bbd897ba2fd27` |
| `english_rev2` | `0x29AC` | `0x2D54` | `0x3A8` | `2f7d79100843b11c97a4be28df1bbd897ba2fd27` |
| `germany_rev0` | `0x2AE0` | `0x2E88` | `0x3A8` | `a0184e330f7bc50ef9063d78a27a3372fa5b036a` |
| `germany_rev1` | `0x2AE0` | `0x2E88` | `0x3A8` | `a0184e330f7bc50ef9063d78a27a3372fa5b036a` |
| `germany_debug_rev0` | `0x2AF8` | `0x2EA0` | `0x3A8` | `162f135953bf434b39dcde1dd5ab17236bbba21d` |
| `france_rev0` | `0x2AE0` | `0x2E88` | `0x3A8` | `0774f21d86e839fab37076cc243867d095e8e0d7` |
| `france_rev1` | `0x2AE0` | `0x2E88` | `0x3A8` | `0774f21d86e839fab37076cc243867d095e8e0d7` |
| `italy_rev0` | `0x2AE0` | `0x2E88` | `0x3A8` | `1b81f08223f6ef970147b0af08a86f95151c5b07` |
| `italy_rev1` | `0x2AE0` | `0x2E88` | `0x3A8` | `1b81f08223f6ef970147b0af08a86f95151c5b07` |
| `spain_rev0` | `0x2AE0` | `0x2E88` | `0x3A8` | `d747b47c8bc02a07d6f4b6afead8906ab1c8e962` |
| `spain_rev1` | `0x2AE0` | `0x2E88` | `0x3A8` | `d747b47c8bc02a07d6f4b6afead8906ab1c8e962` |

The previously observed revision pairing continues in this region: English Rev 1/2 and each continental retail Rev 0/1 pair are byte-identical here.

## Source-form reconstruction implications

The public source confirms that these routines consume reconstructed font assets and tables such as Latin/Japanese 1bpp fonts, Braille glyphs, font-width tables, palettes and window templates. These assets must eventually be present in source form in this repository; a complete-ROM `incbin` is not an acceptable final dependency.

## Next pass

Part 2 starts at `Text_InitWindowWithTemplate`. It will map Window initialization, text-state setup, contest printer setup, `Text_PrintWindow8002F44`, the core `PrintNextChar` state machine and the first extended-control-code handlers. Japanese and international layouts remain separate where the ROM proves they differ.
