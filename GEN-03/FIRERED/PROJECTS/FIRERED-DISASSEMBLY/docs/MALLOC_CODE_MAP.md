# `malloc.c` cross-version code map

`malloc.c` begins immediately after `bg.c`, but it has two verified retail build families.

## Assert-enabled family

| Baseline | Start | End exclusive | Size |
|---|---:|---:|---:|
| JP Rev 0 | `0x0800292C` | `0x08002C1C` | 752 |
| US Rev 0 | `0x0800292C` | `0x08002C1C` | 752 |
| US Rev 1 | `0x08002940` | `0x08002C30` | 752 |

These builds retain the `AGB_ASSERT_EX` paths in the allocator. Within this family all observed cross-ROM byte differences are relocation-sensitive address literals or Thumb `BL` displacements.

## Assert-disabled family

| Baseline | Start | End exclusive | Size |
|---|---:|---:|---:|
| JP Rev 1 | `0x08002928` | `0x08002B88` | 608 |
| FR | `0x08002928` | `0x08002B88` | 608 |
| DE | `0x0800293C` | `0x08002B9C` | 608 |
| IT | `0x0800293C` | `0x08002B9C` | 608 |
| ES | `0x08002928` | `0x08002B88` | 608 |

These builds omit the assert/error-reporting paths. The 144-byte reduction is consistent across all five ROMs. Within the family the only cross-ROM differences are Thumb `BL` relocation bytes.

## Build implication

Assertion behavior is a verified per-baseline build feature and must not be inferred from the software revision number alone. JP Rev 1 disables the allocator assertions, while US Rev 1 retains them. The split exactly matches the previously observed optional print/debug initialization family:

- assertions enabled: JP Rev 0, US Rev 0, US Rev 1
- assertions disabled: JP Rev 1, FR, DE, IT, ES

The repository therefore exposes an explicit `FEATURE_ASSERTS_ENABLED` target flag.

Raw measurements are in `analysis/malloc/object_audit.csv`.
