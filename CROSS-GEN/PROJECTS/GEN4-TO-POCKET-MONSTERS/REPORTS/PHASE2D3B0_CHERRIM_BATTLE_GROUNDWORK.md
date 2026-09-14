# Phase 2D3B0 — Cherrim battle-form groundwork

## Status
Source-specific Cherrim battle-runtime assets are generated and embedded in all five cumulative Japanese Gen III targets. **The live weather/form hook is intentionally not enabled in B0.** This prevents a visual-only Sunshine Form from being mislabeled complete before Flower Gift and weather-suppression behavior are integrated.

## Original-rule classification
- Cherrim has Overcast Form (0) and Sunshine Form (1).
- Sunshine is treated as a battle/weather state, not a persistent individual form.
- Platinum and HGSS battle code change `BattleMon.formNum` based on effective sunny weather and revert when sun is absent or suppressed by Cloud Nine/Air Lock.
- Therefore the project must not persist Sunshine through `MON_DATA_GEN4_FORM = 0x7F` as though it were a stable box form.
- Flower Gift's battle-stat behavior is a separate but coupled ability effect and remains required before 2D3B can be called runtime-complete.

## Source asset differences
- C3 graphics members 92–95 are Cherrim Overcast/Sunshine back/front.
- DP differs from Pt/HGSS for multiple f0/f1 payloads.
- Pt and HGSS graphics are identical for these compared Cherrim members.
- Platinum's four Cherrim normal/shiny palettes differ from DP/HGSS.
- DP and HGSS palettes match for these four palette records.
- No cross-version asset collapse is performed.

## Runtime bank
- File: `CHERRIM_BATTLE_RUNTIME_V1.bank`
- Bytes: 10,176
- SHA-256: `22df0bbd4ffd87206483d76b364cfe81f5bf1ae513e1b328ba102bc352241f70`
- Logical records: 30
- Unique compressed payloads: 19
- Contains source-specific front f0, back f0, Emerald-capable front f0+f1, and normal/shiny palettes for both forms.

## Cumulative targets
- Ruby JP Rev0: bank `0xC65100`, patch SHA-256 `9eba605ef8d2a765ef8734343d20dcde534366f349db1e75b51dd66a51a6ec84`, clean-source reapply exact.
- Sapphire JP Rev0: bank `0xC65100`, patch SHA-256 `3f127db7008452a607dda911122daf8c165676b96c58e539c4acb7ec1f4191a1`, clean-source reapply exact.
- Emerald JP Rev0: bank `0x150B100`, patch SHA-256 `9e18e0c35c6f7bb57b325ad8497c97bda98823d69c70a6d8437e13364e327ac3`, clean-source reapply exact.
- FireRed JP Rev1: bank `0x1465100`, patch SHA-256 `1cb6fb447d65dea5cdfee32bdc8e756e14427d4dea5ecdccb615bfcf68d94352`, clean-source reapply exact.
- LeafGreen JP Rev0: bank `0x1465100`, patch SHA-256 `dccbf34afeba083bc9cc84b87015f60e827c98e50b8fe2a8269d205f258d0a03`, clean-source reapply exact.

## Boundary
B0 is an asset/rule groundwork milestone, not the live Cherrim transformation milestone. `runtime_rule_hook_active=false`. Sunshine transformation, Flower Gift Attack/Sp. Def behavior, weather suppression, battle graphics swap, and actual boot/battle execution are not claimed complete. No emulator is installed in the current environment.
