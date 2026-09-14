# bg module

## Scope

The background/VRAM tilemap manager follows `dma3_manager` and has the same relative function topology in all seven supported LeafGreen ROMs.

USA/Japan reference range: `0x001028–0x00292B`, size `0x1904` / 6404 bytes.

## Target ranges

| Target | Start | End inclusive | Size |
|---|---:|---:|---:|
| Japan | `0x001028` | `0x00292B` | `0x1904` |
| USA | `0x001028` | `0x00292B` | `0x1904` |
| Europe Rev 1 | `0x00103C` | `0x00293F` | `0x1904` |
| Germany | `0x001038` | `0x00293B` | `0x1904` |
| France | `0x001024` | `0x002927` | `0x1904` |
| Italy | `0x001038` | `0x00293B` | `0x1904` |
| Spain | `0x001024` | `0x002927` | `0x1904` |

## Structural result

All targets preserve the same 50-function ordering and the same relative function offsets. A ROM-wide Thumb `BL` target census produces the same 47 referenced entry offsets for Japan, USA, Europe Rev 1, Germany, France, and Italy; Spain contains one additional false-positive-looking `BL` pattern inside the module data/code stream, but the verified function layout remains unchanged.

Three entry points are present but not reached by the ordinary external `BL` census in the reference image and were recovered from function boundaries/source order:

- `Unused_ResetBgControlStruct` at relative `+0x0064`
- `InitBgFromTemplate` at relative `+0x0710`
- `Unused_LoadBgPalette` at relative `+0x08B0`

The module begins with `ResetBgs` and ends with `IsTileMapOutsideWram`; `malloc` begins immediately afterward.

## Raw-byte hashes

Raw module hashes differ because relocation-sensitive calls/literals point at target-specific addresses even though the function topology is invariant.

| Target | SHA-1 of module slice |
|---|---|
| Japan | `ce1c4738712844bf006027cf67aa4bff59371994` |
| USA | `3e2b21fa70d2be1ed917d5ac1e843a16755342ed` |
| Europe Rev 1 | `c835d551e0296848114f4907484b1a4f2c4699a7` |
| Germany | `7a2b1049975e4c6d41b003e74b08db6783090fd4` |
| France | `9dc2a474d6ada2bd7d51ea72158ce8f33cc027ce` |
| Italy | `e154f52450bd4f9983af3266c680e808d29bc786` |
| Spain | `452c5e2e8ea01df7580318df7a6e4e3c262e501a` |

## Function map

The complete 50-function cross-version address matrix is stored in `symbols/bg.csv`. Relative offsets are the canonical identity for reconstruction.

Key checkpoints:

| Relative | USA symbol |
|---:|---|
| `+0x0000` | `ResetBgs` |
| `+0x0270` | `LoadBgVram` |
| `+0x07A8` | `LoadBgTiles` |
| `+0x0860` | `LoadBgTilemap` |
| `+0x0938` | `IsDma3ManagerBusyWithBgCopy` |
| `+0x0B68` | `ChangeBgX` |
| `+0x0CE0` | `ChangeBgY` |
| `+0x1244` | `CopyRectToBgTilemapBufferRect` |
| `+0x1714` | `GetBgMetricTextMode` |
| `+0x1870` | `GetBgType` |
| `+0x18D8` | `IsTileMapOutsideWram` |

## Reconstruction decision

Use one semantic `bg` source module with target-specific linking/relocation. Do not fork the source merely because the raw bytes have different hashes; the verified function sizes/order/relative entries are shared across all seven retail targets.
