# `AgbMain` cross-version audit

`AgbMain` is the first Thumb function entered by `src/crt0.s`. All eight baselines enter it at GBA address `0x080003A4` (`0x080003A5` as a Thumb function pointer), but the emitted function is not identical across releases.

## Function extents

| Baseline | End exclusive | Size | Thumb `BL` count |
|---|---:|---:|---:|
| JP Rev 0 | `0x080004B0` | `0x10C` | 29 |
| JP Rev 1 | `0x080004AC` | `0x108` | 28 |
| US Rev 0 | `0x080004B0` | `0x10C` | 29 |
| US Rev 1 | `0x080004C4` | `0x120` | 30 |
| FR | `0x080004AC` | `0x108` | 28 |
| DE | `0x080004C0` | `0x11C` | 29 |
| IT | `0x080004C0` | `0x11C` | 29 |
| ES | `0x080004AC` | `0x108` | 28 |

## Two independent build features

The ROMs expose at least two independent compile-time differences in the startup routine.

| Baseline | Additional print-init call | Flash-memory guard |
|---|---|---|
| JP Rev 0 | yes | no |
| JP Rev 1 | no | no |
| US Rev 0 | yes | no |
| US Rev 1 | yes | yes |
| FR | no | no |
| DE | no | yes |
| IT | no | yes |
| ES | no | no |

The flash-memory guard is the Thumb sequence that loads the flash-present state, compares it with `1`, and, when absent, calls the local main-callback setter with `NULL`. The public FireRed decompilation represents this behavior as a revision-conditional check, but the eight-ROM audit shows that **software-version number alone is not sufficient for this multi-region project**: German and Italian revision-0 ROMs contain the guard while Japanese revision 1 does not.

Likewise, the extra initialization call immediately following the save-failure-screen initialization is present in JP Rev 0, US Rev 0, and US Rev 1, but absent from the other five baselines. Its position corresponds to the optional print initialization in the reference source.

## Build implication

Do not use one global rule such as `REVISION >= 1` to represent all regional behavior. This repository instead records explicit per-baseline feature flags in `config/build_features.json`.

This approach is required for byte-exact reproduction while still sharing the common logical source.

## Next source task

`AgbMain` should be reconstructed as shared C/Thumb source with feature predicates driven by the verified per-baseline configuration. Branch targets and literal addresses must remain symbolic so the linker can place the rest of each regional build naturally.
