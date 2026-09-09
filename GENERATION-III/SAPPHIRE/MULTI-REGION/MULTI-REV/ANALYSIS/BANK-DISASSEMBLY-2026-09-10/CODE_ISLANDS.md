# Post-main-code Thumb islands

The `gScriptCmdTable`-equivalent marks the end of the contiguous main Thumb code region, **not** the end of all executable ROM code. Direct `BL`/branch reachability discovers later library/stub islands without linearly decoding intervening data.

| ROM | Main code/data boundary | Later statically reachable code banks |
|---|---:|---|
| AXPJ_rev0 | 0x08145190 | `1A` (3,152 B), `1B` (9,488 B) |
| AXPD_rev1 | 0x0814B208 | `1E` (12,640 B) |
| AXPE_rev0 | 0x0814AE30 | `1D` (4,210 B), `1E` (8,430 B) |
| AXPE_rev1 | 0x0814AE50 | `1D` (4,186 B), `1E` (8,454 B) |
| AXPE_rev2 | 0x0814AE50 | `1D` (4,186 B), `1E` (8,454 B) |
| AXPF_rev0 | 0x0814B2EC | `1E` (12,640 B) |
| AXPF_rev1 | 0x0814B2EC | `1E` (12,640 B) |
| AXPI_rev0 | 0x0814B250 | `1D` (1,744 B), `1E` (10,896 B) |
| AXPI_rev1 | 0x0814B250 | `1D` (1,744 B), `1E` (10,896 B) |

Validation rule: later blocks must be reached from accepted code through real Thumb control-flow edges; arbitrary multiply-referenced data pointers are not sufficient seeds. Final scan has **0 block-limit failures**, which removed false long decodes in structured data.
