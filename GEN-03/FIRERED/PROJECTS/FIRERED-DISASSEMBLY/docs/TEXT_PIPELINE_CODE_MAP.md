# Text / window pipeline code map

The audited FireRed text/display pipeline after `malloc.c` is now split into exact source-object ranges rather than one coarse "text" region.

## Object sequence

`text_printer.c` → `window.c` → `blit.c` → `window_8bpp.c` → `text.c` → `sprite.c`

### `text_printer.c`

Two real implementation families exist:
- Japanese: 3792 bytes
- International: 3844 bytes

Within each family, all regional/revision differences are relocation-only. See `docs/TEXT_PRINTER_CODE_MAP.md` and `analysis/text_printer/object_audit.csv`.

### `window.c`

All eight builds use one 3904-byte implementation. Every observed difference is a link-address literal or Thumb `BL` displacement.

### `blit.c`

All eight builds use the same 1492 bytes **byte-for-byte**, despite the object being linked at different addresses.

### `window_8bpp.c`

All eight builds use one 840-byte implementation. Cross-version differences are relocation-only.

### `text.c`

A second genuine localization split appears here:
- Japanese: 4932 bytes
- International: 6036 bytes

Within the Japanese pair and within the six international builds, every observed difference is relocation-only. Japanese versus international is therefore a real compile-time text-engine implementation/data difference rather than a simple link-layout shift.

## Exact boundaries

| Object | JP Rev0 | US Rev0 |
|---|---|---|
| `text_printer.c` | `08002C1C..08003AEB` | `08002C1C..08003B1F` |
| `window.c` | `08003AEC..08004A2B` | `08003B20..08004A5F` |
| `blit.c` | `08004A2C..08004FFF` | `08004A60..08005033` |
| `window_8bpp.c` | `08005000..08005347` | `08005034..0800537B` |
| `text.c` | `08005348..0800668B` | `0800537C..08006B0F` |
| next: `sprite.c` | `0800668C` | `08006B10` |

The other six baselines are recorded in `analysis/code_object_spans.csv` and the per-object audit CSV files.
