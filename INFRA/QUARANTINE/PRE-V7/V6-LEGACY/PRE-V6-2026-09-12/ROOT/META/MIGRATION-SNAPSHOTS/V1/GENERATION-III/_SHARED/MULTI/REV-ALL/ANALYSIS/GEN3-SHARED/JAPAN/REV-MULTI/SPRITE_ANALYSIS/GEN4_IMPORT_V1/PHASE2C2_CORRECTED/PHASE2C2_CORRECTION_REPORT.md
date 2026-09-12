# Gen IV → Gen III Phase 2C2 Corrected

## Critical correction
Earlier Phase 2A/B/C cumulative patches used an invalid `national_dex + 25` assumption for Gen III internal species IDs #252–386.
Gen III stores Hoenn species in an engine-specific internal order. The corrected build reads each target ROM's own `gSpeciesToNationalPokedexNum` table (species IDs 1..411) and inverts the true mapping for National Dex 001..386.

Spot checks:
- National #252 Treecko -> internal ID 277
- National #278 Wingull -> internal ID 309
- National #327 Spinda -> internal ID 308
- National #351 Castform -> internal ID 385
- National #358 Chimecho -> internal ID 411
- National #386 Deoxys -> internal ID 410
- National #387 Turtwig -> new ID 440
- National #493 Arceus -> new ID 546

## Verification
- All five Japanese Gen III targets carry an identical 411-entry internal-species→National mapping table.
- Phase 2A2 graphics/table verification: 0 errors on all targets.
- Phase 2B2 cumulative patch reapply: exact on all targets.
- Phase 2C2 cumulative patch reapply: exact on all targets.
- Selected problematic internal-ID sprites match the authoritative HGSS converted graphic SHA-256.
- Legacy 440-entry graphics/coordinate/palette tables remain byte-preserved in place.
- IDs 252..276 OLD_UNOWN special slots remain preserved.
- New Gen IV species use IDs 440..546; 547..548 remain safe fallback graphics slots.

Previous Phase 2A/B/C cumulative patches MUST be treated as superseded.
