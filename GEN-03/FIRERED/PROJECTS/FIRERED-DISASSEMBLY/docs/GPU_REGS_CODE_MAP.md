# `gpu_regs.c` cross-version code map

The `gpu_regs.c` text immediately follows `main.c` in every audited FireRed baseline.

## Object extent

Using US Rev 0 as the reference:

- start: `0x08000968`
- next object (`dma3_manager.c`): `0x08000BFC`
- text span: `0x294` bytes (660 bytes)

All eight baselines preserve the same `0x294`-byte span. No new regional or revision-dependent code-size divergence was observed in this object. The only address differences are the address-family shifts already introduced by the different `AgbMain` sizes.

## Recovered function order

1. `InitGpuRegManager`
2. `CopyBufferedValueToGpuReg`
3. `CopyBufferedValuesToGpuRegs`
4. `SetGpuReg`
5. `GetGpuReg`
6. `SetGpuRegBits`
7. `ClearGpuRegBits`
8. `SyncRegIE`
9. `EnableInterrupts`
10. `DisableInterrupts`
11. `UpdateRegDispstatIntrBits`

Exact addresses for all eight baselines are in `analysis/gpu_regs/function_starts.csv`.

## Build implication

`gpu_regs.c` can be treated as shared source across JP Rev 0, JP Rev 1, US Rev 0, US Rev 1, French, German, Italian, and Spanish builds. Pointers and branch destinations must remain symbolic so normal linking accounts for the inherited target-specific address shift.

The next text object is `dma3_manager.c`.
