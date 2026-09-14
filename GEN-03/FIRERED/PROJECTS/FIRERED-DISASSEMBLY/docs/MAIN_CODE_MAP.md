# Early `main.c` code map

This document tracks the first `main.c` functions recovered after `AgbMain` across all eight FireRed baselines.

## Address-family result

`AgbMain` starts at the same address in every baseline (`0x080003A4`) but has four emitted sizes because of independently verified regional startup features. Once `AgbMain` ends, the subsequent audited `main.c` functions retain the same ordering and relative placement through `DoSoftReset`.

Using US Rev 0 as the reference, the observed address shifts are:

| Family | Baselines | Shift |
|---|---|---:|
| Base | JP Rev 0, US Rev 0 | `0x0` |
| Short startup | JP Rev 1, FR, ES | `-0x4` |
| Flash-guard startup | DE, IT | `+0x10` |
| Print + flash-guard startup | US Rev 1 | `+0x14` |

This means the audited sequence after `AgbMain` does **not** require eight duplicated source files. The functions can be represented as shared source while the linker naturally resolves each target's addresses.

## Recovered sequence

The current map covers these functions in source order:

1. `UpdateLinkAndCallCallbacks`
2. `InitMainCallbacks`
3. `CallCallbacks`
4. `SetMainCallback2`
5. `StartTimer1`
6. `SeedRngAndSetTrainerId`
7. `GetGeneratedTrainerIdLower`
8. `EnableVCountIntrAtLine150`
9. `InitKeys`
10. `ReadKeys`
11. `InitIntrHandlers`
12. `SetVBlankCallback`
13. `SetHBlankCallback`
14. `SetVCountCallback`
15. `SetSerialCallback`
16. `VBlankIntr`
17. `InitFlashTimer`
18. `HBlankIntr`
19. `VCountIntr`
20. `SerialIntr`
21. `RestoreSerialTimer3IntrHandlers`
22. `IntrDummy`
23. `WaitForVBlank`
24. `SetVBlankCounter1Ptr`
25. `DisableVBlankCounter1`
26. `DoSoftReset`

Exact addresses for all eight builds are stored in `analysis/main/function_starts.csv`. The family shifts are stored in `analysis/main/address_families.json`.

## Reconstruction policy

- Shared logic stays shared.
- Region/revision-specific behavior is represented by explicit target features only when ROM evidence requires it.
- Literal addresses and `BL` destinations are not hard-coded as copied ROM bytes; they remain symbols/relocations in the eventual build.
- A function is promoted from analysis into final `src/` only after its surrounding symbols, compiler settings, and linker placement can be verified reproducibly.

The next audit continues forward from `DoSoftReset` and records the first point where any additional code-size divergence appears.
