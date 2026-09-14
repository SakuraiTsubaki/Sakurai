# malloc module

## Scope

`malloc` follows `bg`, but unlike the immediately preceding core modules it is not one byte-layout family across all seven retail targets.

The same 12 semantic functions are present in every target, but the module splits into two verified layout families.

## Family A — Japan / USA / Europe Rev 1

| Target | Start | End exclusive | Size | SHA-1 |
|---|---:|---:|---:|---|
| Japan | `0x00292C` | `0x002C1C` | `0x2F0` | `f73ba9b7a0af92601aa6e3b046e8206dbc5906fa` |
| USA | `0x00292C` | `0x002C1C` | `0x2F0` | `1bd9d2779850f47ff758ed6ed63373cc373bfab3` |
| Europe Rev 1 | `0x002940` | `0x002C30` | `0x2F0` | `1e14d57c47165ee4eb9f668067552bf811126d4d` |

Relative function offsets:

`000, 01C, 030, 0DC, 1BC, 1FC, 254, 270, 284, 298, 2AC, 2C0`

## Family B — Germany / France / Italy / Spain

| Target | Start | End exclusive | Size | SHA-1 |
|---|---:|---:|---:|---|
| Germany | `0x00293C` | `0x002B9C` | `0x260` | `15aee3a08f327ff51afd6c9742988a4f5eea8e49` |
| France | `0x002928` | `0x002B88` | `0x260` | `72d6754ee29bfb48cc905f53c19ad17593a14f31` |
| Italy | `0x00293C` | `0x002B9C` | `0x260` | `bbf2b4575d69e9433a10ff57dfc5f3e8da1bf532` |
| Spain | `0x002928` | `0x002B88` | `0x260` | `b5f9331982a0e6bb77c2f37801d35d2c5be03f81` |

Relative function offsets:

`000, 01C, 030, 0C8, 12C, 16C, 1C4, 1E0, 1F4, 208, 21C, 230`

Family B is exactly `0x90` bytes shorter than Family A.

## Function order

All targets retain this semantic order:

1. `PutMemBlockHeader`
2. `PutFirstMemBlockHeader`
3. `AllocInternal`
4. `FreeInternal`
5. `AllocZeroedInternal`
6. `CheckMemBlockInternal`
7. `InitHeap`
8. `Alloc`
9. `AllocZeroed`
10. `Free`
11. `CheckMemBlock`
12. `CheckHeap`

The exact per-target function addresses remain unchanged and are recorded in `symbols/malloc.csv`.

## Boundary correction

An earlier survey incorrectly ended this module 12 bytes late. Direct Thumb disassembly identified `SetFontsPointer`—the first `text_printer` function—at `0x08002C1C` in Japan/USA, not `0x08002C28`. The corrected boundary has been verified in all seven retail targets.

## Assertion evidence

The USA, Japan, and Europe Rev 1 reference ROMs contain the ASCII path `gflib/malloc.c` used by the allocator's assertion/error-checking paths. The Germany, France, Italy, and Spain ROMs do not contain that string. The Family B code also contracts specifically through the allocator's internal/error-checking region.

This is strong ROM-level evidence that Family B was built with those assertion/debug paths omitted or otherwise compiled away. The precise historical build flag/toolchain cause is not asserted here until independently verified.

## Reconstruction decision

Do **not** force a single byte-layout object for `malloc`.

Use one semantic allocator source where practical, but retain target-family build configuration so that Family A reproduces the longer assertion-bearing layout and Family B reproduces the shorter localized-European layout. The next object begins immediately at the corrected end and belongs to `text_printer`.
