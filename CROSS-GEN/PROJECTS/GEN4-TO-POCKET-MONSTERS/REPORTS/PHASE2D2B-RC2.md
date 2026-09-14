# Generation IV -> Gen III Phase 2D2B RC2

## Status
RC2 fixes both form-context gaps found during review of the first Phase 2D2B candidate. The five cumulative Japanese-target IPS32 patches were regenerated and reapplied to clean source ROMs byte-for-byte successfully.

## RC2 fixes
- The graphics resolver now accepts both scratch representations: `valid personality-signature + form` before graphics loading and `species + form` after graphics loading for palette handoff. This preserves the same form when a picture is loaded again without another `GetBoxMonData` call.
- `SetBoxMonData(..., MON_DATA_GEN4_FORM=0x7F)` now refreshes the signature/form scratch immediately after writing the persistent 5-bit form state. A display immediately after a form change no longer needs a separate getter call to obtain the new context.

## Form lookup verification
- Nonzero source/form records: DP 30, Platinum 37, HGSS 38 (105 total).
- Front/back form graphics paths checked: 210.
- Normal/shiny form palette paths checked: 210.
- All runtime f0 graphics resolve to LZ10 output length 2048.
- Emerald full front form graphics resolve to LZ10 output length 4096.
- All form palettes resolve to C3 LZ10 output length 32.
- Scratch-state simulation cases: 237,832; errors: 0.

## Target patches
### RUBY_JP_REV0
- RC2 work SHA-256: `40a43aa5849fb586595f4fcc7e188f2b7259128e7da3c238a41c8547c6c1d965`
- IPS32 SHA-256: `f4fd0e387cd3db291a1cf3dd3254a82f7bb3cbb6fc7c21219ddadc66b87cdbc8`
- IPS32 bytes: 4,603,872
- Resolver code: `0xc63000`
- RC2 extension: `0xc63500`
- Clean-source reapply exact: `true`

### SAPPHIRE_JP_REV0
- RC2 work SHA-256: `671a07debc97f4ebd83d301f10bf1b3299994e5051fc320f1def3d13931c488a`
- IPS32 SHA-256: `391cbb8e2a785afc499ad9fa2d45227c5efb406533722bb94e4009089e8b0c13`
- IPS32 bytes: 4,603,872
- Resolver code: `0xc63000`
- RC2 extension: `0xc63500`
- Clean-source reapply exact: `true`

### EMERALD_JP_REV0
- RC2 work SHA-256: `d99f0f9f23f14b0a28b29c451f2ca30958694def8cf59a7c6ef0541a3923b855`
- IPS32 SHA-256: `0826c6d293f820b27e4f808dcc60d51e9a44c02b965926a693f488839b9cdfa9`
- IPS32 bytes: 5,284,943
- Resolver code: `0x1509000`
- RC2 extension: `0x1509500`
- Clean-source reapply exact: `true`

### FIRERED_JP_REV1
- RC2 work SHA-256: `ae4067b0fc89032382f670deff4282e3d20df51c8ecb788e3e0b70fb97374bc9`
- IPS32 SHA-256: `756f82bc30c9b662886ebf467805c3984925bb07b7f2d0fcf913da327c8c1062`
- IPS32 bytes: 4,604,795
- Resolver code: `0x1463000`
- RC2 extension: `0x1463500`
- Clean-source reapply exact: `true`

### LEAFGREEN_JP_REV0
- RC2 work SHA-256: `ba7c84a2d21d0513916cb20edac766830fa926c130a833fbee708c3cb8953c4d`
- IPS32 SHA-256: `92447abdf03db63c2bec098f08b0524c265ca3eed933efd3fb8343b8d6d347b4`
- IPS32 bytes: 4,604,795
- Resolver code: `0x1463000`
- RC2 extension: `0x1463500`
- Clean-source reapply exact: `true`

## Boundary
No emulator is installed in the current execution environment, so this release is **not** claimed as boot-tested. Static ROM, lookup, LZ10, context-state, and clean-source patch-reapply verification are complete.

Gen IV gameplay rules that *change* the stored form (weather, Rotom appliances, Griseous Orb, Gracidea, Plates/Multitype, Burmy cloak environment, etc.) remain the next independent rule-engine phase.