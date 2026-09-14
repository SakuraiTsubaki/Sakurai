# text_printer module

## Scope

`text_printer` begins immediately after the corrected `malloc` boundary and ends at the start of the `window` module.

The six international builds share one semantic/function layout. The Japanese build is a distinct layout family with shorter printer-state structures and a shorter `RunTextPrinters` path.

## Module ranges

| Target | Start | End exclusive | Size | SHA-1 | Family |
|---|---:|---:|---:|---|---|
| Japan | `0x002C1C` | `0x003AEC` | `0xED0` | `f5bae5cd841f18fe292f37a3e2916a939e1ffb97` | JP |
| USA | `0x002C1C` | `0x003B20` | `0xF04` | `b9a5efe8c33fef6f19219af6384a9d8476786639` | INTL |
| Europe Rev 1 | `0x002C30` | `0x003B34` | `0xF04` | `246e3ad45fe969e65145f8dcc4c76d1a4d219392` | INTL |
| Germany | `0x002B9C` | `0x003AA0` | `0xF04` | `1d57f46eb55461622ceac7eca85901301157ce37` | INTL |
| France | `0x002B88` | `0x003A8C` | `0xF04` | `471c92a51926ddc9d49496eb6e86500cc7d3d9dc` | INTL |
| Italy | `0x002B9C` | `0x003AA0` | `0xF04` | `940a92a5d86bea8b00c2254ae27d9df934b5b573` | INTL |
| Spain | `0x002B88` | `0x003A8C` | `0xF04` | `9e2f43ac917541e4872cf9820bba2bd95ae016aa` | INTL |

## Verified function order

The international layout contains these functions in order:

1. `SetFontsPointer`
2. `DeactivateAllTextPrinters`
3. `AddTextPrinterParameterized`
4. `AddTextPrinter`
5. `RunTextPrinters`
6. `IsTextPrinterActive`
7. `RenderFont`
8. `GenerateFontHalfRowLookupTable`
9. `SaveTextColors`
10. `RestoreTextColors`
11. `DecompressGlyphTile`
12. `GetLastTextColor`
13. `CopyGlyphToWindow`
14. `CopyGlyphToWindow_Parameterized`
15. `ClearTextSpan`

The Japanese layout preserves the same order through `CopyGlyphToWindow_Parameterized`, but does not contain a separate `ClearTextSpan` function at the end of this object.

Exact addresses for all verified functions are recorded in `symbols/text_printer.csv`.

## Boundary evidence

`SetFontsPointer` was identified directly from its Thumb sequence and its write to the `gFonts` pointer. This corrected the preceding `malloc` boundary by 12 bytes.

For the international builds the final bytes are two adjacent empty Thumb functions: `ClearTextSpan` followed by `window.c`'s `nullsub_8`. `InitWindows` immediately follows the second empty function.

In the Japanese build only the `window.c` empty stub is present at the boundary. `InitWindows` starts at `0x08003AF0`, so `text_printer` ends at `0x003AEC`.

## Reconstruction decision

Treat `text_printer` as two target families rather than forcing the Japanese ROM onto the international binary layout. Shared semantic source should be used where possible, with target-specific structure sizes/compile-time behavior retained wherever required for exact output.

The next module is `window`.
