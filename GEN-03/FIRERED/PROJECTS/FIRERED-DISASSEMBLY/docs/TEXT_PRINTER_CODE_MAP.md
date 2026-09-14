# `text_printer.c` cross-version code map

The text-printer object begins immediately after `malloc.c`. This is the first audited code object where Japanese and international FireRed require genuinely different compiled implementations.

| Baseline | Start | End exclusive | Size | Family |
|---|---:|---:|---:|---|
| JP Rev 0 | `0x08002C1C` | `0x08003AEC` | 3792 | Japanese |
| JP Rev 1 | `0x08002B88` | `0x08003A58` | 3792 | Japanese |
| US Rev 0 | `0x08002C1C` | `0x08003B20` | 3844 | International |
| US Rev 1 | `0x08002C30` | `0x08003B34` | 3844 | International |
| FR | `0x08002B88` | `0x08003A8C` | 3844 | International |
| DE | `0x08002B9C` | `0x08003AA0` | 3844 | International |
| IT | `0x08002B9C` | `0x08003AA0` | 3844 | International |
| ES | `0x08002B88` | `0x08003A8C` | 3844 | International |

Within the Japanese family, JP Rev 0 and JP Rev 1 differ only by relocation-sensitive address literals and Thumb `BL` displacements. The same is true among all six international builds when compared with US Rev 0.

A direct Japanese-vs-international comparison, however, leaves thousands of bytes outside those relocation categories. This is real localization-dependent implementation/data divergence, not merely a shifted link layout. The build must therefore preserve a Japanese text-printer path and an international text-printer path while continuing to share the common higher-level API.

Raw object measurements are recorded in `analysis/text_printer/object_audit.csv`.
