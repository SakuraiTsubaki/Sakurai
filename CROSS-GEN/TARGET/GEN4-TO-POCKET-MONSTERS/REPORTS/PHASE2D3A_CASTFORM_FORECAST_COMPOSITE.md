# Generation IV -> Gen III Phase 2D3A — Castform Forecast Composite

## Status
Static integration complete for all five Japanese Gen III targets. No emulator is available, so boot/battle execution is not claimed.

## Source result
- DP/Pt/HGSS Castform f0 graphics for all four Forecast forms are byte-identical after the established preservation-v2 conversion.
- The only observed Castform graphics difference in these C3 members is DP Normal back **f1**; Gen III Forecast composite consumes f0 only, so the live Gen III Forecast representation is common across the three source families.
- All eight Castform palettes (4 normal + 4 shiny) are byte-identical across DP/Pt/HGSS.

## Gen III compatibility
- Front composite: 4 x 2048 bytes = 8192 bytes, order Normal/Sunny/Rainy/Snowy.
- Back composite: 4 x 2048 bytes = 8192 bytes, same order.
- Normal palette composite: 4 x 32 = 128 bytes.
- Shiny palette composite: 4 x 32 = 128 bytes.
- Emerald animated-front Castform entry intentionally points to the same 8192-byte front composite, matching the vanilla Emerald Castform arrangement.
- Original Forecast and `gBattleMonForms` rule logic is preserved; this phase changes compatible assets/data routing, not weather logic.

## Converted front coordinates
- Normal: size=0x34, y_offset=20
- Sunny: size=0x45, y_offset=14
- Rainy: size=0x45, y_offset=14
- Snowy: size=0x46, y_offset=13

## Targets
### RUBY_JP_REV0
- Work SHA-256: `58f7036403528dbff128071fdd892285d9d44fd7063cb57fbee842198a19589a`
- IPS32 SHA-256: `c1da6697ffb1591ab0332df0578dfdbbd29c6c1d28efabffc5aba96f4278cac9`
- Patch bytes: 4,610,024
- Castform bank offset: `0xc63900`
- Clean-source reapply exact: `true`
- Verification errors: 0

### SAPPHIRE_JP_REV0
- Work SHA-256: `07fc10e7bee50227a1ccaddf68bf7add30a1afdcc9f8caee30c59585b01d2d59`
- IPS32 SHA-256: `932cc258bee2ebb15a64325e3fe1ac1727deafaa4723f4ae1e3943e69ae660d7`
- Patch bytes: 4,610,024
- Castform bank offset: `0xc63900`
- Clean-source reapply exact: `true`
- Verification errors: 0

### EMERALD_JP_REV0
- Work SHA-256: `2ebaaa929fa2ca77af32164bc45a3b31aeebfa4a1e8343d341e07ca64af4b6b1`
- IPS32 SHA-256: `01d40bff3674873f9ca572c5cabd1aede9e59a70abad9198d01928ef724364b1`
- Patch bytes: 5,291,095
- Castform bank offset: `0x1509900`
- Clean-source reapply exact: `true`
- Verification errors: 0

### FIRERED_JP_REV1
- Work SHA-256: `90dee6d112c9b37767abd5ac28008dbcb1a84cd818caf54d29b0d17a18527597`
- IPS32 SHA-256: `4e454093b7fdbeab809a8e897cb6451edf5f0e0733869fabe756c54860c9817a`
- Patch bytes: 4,610,947
- Castform bank offset: `0x1463900`
- Clean-source reapply exact: `true`
- Verification errors: 0

### LEAFGREEN_JP_REV0
- Work SHA-256: `412b753620a834358dd20473e35462ef94bdd945aefcb9eff9fbcaa4496cc852`
- IPS32 SHA-256: `f3587aae126e63e28a2447330d7673f92f032c6e45fd1519011e9a0ad046db1a`
- Patch bytes: 4,610,947
- Castform bank offset: `0x1463900`
- Clean-source reapply exact: `true`
- Verification errors: 0

## Boundary
Runtime behavior is statically grounded by original Gen III Forecast structure, table routing, LZ10 round-trip checks, coordinate replacement, and clean-source IPS32 reapplication. Actual boot, battle weather-change animation, save/load, and contest execution remain untested without an emulator.
