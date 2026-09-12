# Generation V → Generation II parameter implementation

Status: **parameter bridge started; native save/party species-ID widening is still a prerequisite for full 252–649 gameplay.**

Sprites are excluded from this phase.

## What is implemented here

- A converter that takes the canonical 650 × 60-byte BW personal base table and emits Gen II-friendly columnar binaries.
- Every generated column is kept under one 16 KiB ROMX bank.
- Banked RGBDS `INCBIN` sections for stats, types, catch rate, EV yield, three held-item slots, gender, hatch counter, per-species friendship, growth rate, egg groups, three abilities, escape rate, form-routing data, body color, 16-bit Base EXP, height, weight, Gen V TM/HM compatibility and tutor compatibility.
- A 16-bit-project-species accessor core using `GetFarByte` / `GetFarWord`.
- Explicit Gen V → Gen II type-ID translation.
- Runtime accessors already provided for base stats, types, catch rate, gender, hatch counter, friendship, growth group, escape rate, body color, 16-bit Base EXP, height, weight, three ability slots and three held-item source slots.

## Why the table is columnar

The complete BW base personal layer is 650 × 60 = 39,000 bytes, which spans multiple GBC ROM banks. Splitting by field produces independently bankable tables; the largest current column is the 16-byte TM/HM bitset at 10,400 bytes, so no individual column has to cross a 16 KiB ROMX boundary.

This is preferable to deleting Generation V fields or truncating records to the native Gen II base-data structure.

## Species-ID contract

The accessor accepts a **16-bit project species ID in DE**. This is deliberate.

Native Gen II still stores species and move IDs in 8-bit-era structures. Full integration therefore still requires the separate widened-ID/save compatibility layer. The parameter bridge is being built first so that the widened species namespace has a complete data source when it comes online.

Do not write species 252–649 into native one-byte party/box species fields yet.

## Preserved native systems

Original Gen II `BaseData` is not replaced. The project keeps explicit profiles:

- `GEN2_ORIGINAL`
- `GEN5_BW_ORIGINAL`
- `GEN5_B2W2_ORIGINAL`
- `PROJECT_APPLIED`

Existing Pokémon can therefore retain original Gen II behavior when required while Generation V data remains independently addressable.

## Important semantic boundaries

- `Gen5GetAbilityRaw` returns a Gen V ability ID; Gen II still needs a new ability engine and effect hooks.
- `Gen5GetHeldItemRaw` returns a Gen V item ID; it must pass through a target item-ID mapping before storage or use.
- Modern EV yield is present in the table, but Gen II still uses stat experience natively; the EV/stat-exp migration is a separate subsystem.
- 16-bit Base EXP is available, but the Gen V EXP-award formula/profile has not yet replaced the original calculation.
- Form-routing source fields are retained; a form-state representation still has to be added.

## Next implementation block

1. Widen project species and move identities without deleting native IDs.
2. Add compact persistent sidecar state for high species/move bits, form and ability selection where unused native state is insufficient.
3. Route creation/battle/stat/EXP/breeding/evolution/TM code through profile-aware accessors.
4. Add the ability engine, modern EV behavior, physical/special/status move classification and Gen V item/evolution handlers.
5. Verify Korean Gold/Silver and Japanese/English Crystal separately; no address or bank is assumed identical between revisions.
