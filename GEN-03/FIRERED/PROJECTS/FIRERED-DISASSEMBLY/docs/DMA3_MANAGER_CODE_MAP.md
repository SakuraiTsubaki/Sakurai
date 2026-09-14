# `dma3_manager.c` cross-version code map

`dma3_manager.c` follows `gpu_regs.c` in every audited FireRed baseline.

Using US Rev 0 as the reference, the object spans `0x08000BFC..0x08001027` (1,068 bytes). The next text object, `bg.c`, begins at `0x08001028`.

All eight baselines preserve the same object size and function ordering; only the inherited address-family shift differs.

Recovered function order:

1. `ClearDma3Requests`
2. `ProcessDma3Requests`
3. `RequestDma3Copy`
4. `RequestDma3Fill`
5. `WaitDma3Request`

Exact addresses are recorded in `analysis/dma3_manager/function_starts.csv`.

No additional regional or revision-dependent code-size divergence was observed in this object. It is therefore a shared-source candidate for all eight builds.
