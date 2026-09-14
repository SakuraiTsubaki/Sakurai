# GEN2 Kanto Start — Gold KR Phase 14

## Scope
Phase 14 exposes the Phase 13 multi-version palette engine through an in-game selector without replacing an original RGBY or GSC interaction.

The imported RGBY technology NPC still displays its restored Phase 12 PC/data-storage dialogue first. A second prompt then displays the current profile and asks `변경?`. Selecting Yes advances through `GSC -> RED BLUE -> GREEN -> YELLOW SGB -> YELLOW CGB -> GSC`; No leaves the state unchanged.

## Persistence
Project event flags 1946-1948 store the profile bits in the normal event-flag save area. Phase 14 normalizes the bits every time the selector advances. `reloadmap` immediately reloads the current Pallet map, causing the Phase 13 palette wrapper to apply the new profile.

## Profiles preserved
- GSC CGB / time-of-day palette behavior
- Red/Blue SGB Pallet palette (identical data deduplicated)
- Japanese Green SGB Pallet palette (distinct source data preserved)
- Yellow SGB Pallet palette
- Yellow CGB Pallet palette

## Preservation
- The Phase 12 technology dialogue at `4E:6780` is not modified.
- The GSC fisherman/technology dialogue remains a separate original object.
- Pallet warps, signs, Teacher, RGBY girl, Oak intro, and other Phase 11/12 content are untouched.

## Validation
- Phase 13 -> 14 delta IPS: PASS
- Clean Korean Gold -> Phase 14 cumulative IPS: PASS
- Static selector validator: PASS
- SHA-1: `ddbc98b9c1fafa052e7cfcc38fc120963a5e0974`
- SHA-256: `6cc489183a199f63e858db8610ad63f2e2c62bba217a4887e1c02e6431fff70c`
- Header checksum: `08`
- Global checksum: `E96F`
- Emulator playtest: NOT RUN
