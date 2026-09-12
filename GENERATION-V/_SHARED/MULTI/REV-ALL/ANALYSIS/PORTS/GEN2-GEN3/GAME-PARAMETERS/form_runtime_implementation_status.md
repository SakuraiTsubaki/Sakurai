# Gen II / Gen III Form Runtime Implementation Status

Status: source-level implementation pass 1 complete; ROM-binary hooks remain target-specific.

## Verified source/ROM facts

- Uploaded Gen II ROMs expose no generic persistent form field.
- Uploaded Gen III ROMs expose no generic persistent form field.
- Gen III BoxPokemon has 4 header bits explicitly unused by the stock engine.
- Gen III PokemonSubstruct3 has 4 unused ribbon bits.
- BW personal data directly extracted from the uploaded Black ROM has a maximum form count of 28 (Unown), therefore the project form selector is 5 bits.
- Gen II party_struct has a stock one-byte `Unused` field.
- Gen II `sBoxSpecies[]` is a separate list from the species byte stored inside each boxed-mon record, but multiple stock routines read the list directly or rely on its iteration semantics.

## Implemented source assets

Stored in Tsubaki under:

`GENERATION-V/BW/EUR/REV-MIXED/IMPLEMENTATION/GEN2-GEN3-FORM-RUNTIME/`

### Gen III

- `MON_DATA_FORM` patch for pokefirered.
- `MON_DATA_FORM` patch for pokeemerald.
- `Project_GetBoxMonForm`, `Project_SetBoxMonForm`, `Project_GetMonForm`, `Project_SetMonForm`, `Project_ResolveMonForm`.
- Storage contract: low 4 form bits in `BoxPokemon.unused`; high form bit in `unusedRibbons` bit 0.
- `FORM_AUTO = 31`; stock Unown personality-derived form is supported as an automatic resolver.

### Gen II

- Packed extension-byte-0 helper source.
- bits 0..1 = species bits 8..9.
- bits 2..6 = form bits 0..4.
- bit 7 reserved.
- party extension access uses `PartyMon.Unused`.
- box extension access is prepared for repurposed `sBoxSpecies[slot]`, but is intentionally not activated until every stock consumer is migrated.
- verified initial direct-consumer audit includes `tempmon.asm`, `lucky_number.asm`, and `bills_pc.asm`.

## Tests

Host-side exhaustive round-trip tests pass for:

- Gen II packed species/form extension: 1024 species values × 32 form values.
- Gen III split 5-bit form representation: all 32 values.

## Next implementation block

1. Add form initialization to Gen III CreateMon/CreateBoxMon paths.
2. Add runtime `gBattleMonForms[]` and initialize it on battler creation.
3. Route Gen5 personal lookups through `(canonical species, resolved form)`.
4. Replace Gen III legacy OLD_UNOWN species-indexed ordering with canonical National Dex ordering in rebuilt tables.
5. For Gen II, complete every `sBoxSpecies` consumer conversion before enabling that array as extension storage.
6. Add a 16-bit project current-species runtime variable before any Gen II 252+ species is allowed into battle/PC logic.

No full ROM binary is stored in GitHub.
