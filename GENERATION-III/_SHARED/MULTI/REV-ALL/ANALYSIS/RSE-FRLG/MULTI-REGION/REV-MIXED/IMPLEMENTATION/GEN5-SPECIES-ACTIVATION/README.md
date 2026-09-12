# Generation V species activation in Generation III

Status: **BPEE (Pokémon Emerald USA/Europe) prototype in progress.**

This phase begins after the BW 64×64 battle sprites have already been inserted into the Gen III ROMs. It activates National Dex 387–649 as real Gen III internal species while preserving every vanilla internal slot.

## Fixed internal-ID layout

- National 001–251 -> internal 001–251
- original OLD_UNOWN placeholder block 252–276 remains untouched
- National 252–386 -> original Gen III internal 277–411
- internal 412 = Egg sentinel/special slot remains fixed
- internal 413–439 = vanilla Unown B–? special graphics/form slots remain fixed
- National 387–649 -> new internal 440–702

No existing Gen III species or special slot is shifted or deleted.

## Why NUM_SPECIES is not globally changed

Vanilla Emerald defines `SPECIES_EGG = 412` and uses `NUM_SPECIES` as that historical boundary. Unown special-form arithmetic is based on the slots immediately after that boundary. Replacing every `NUM_SPECIES` comparison with 702 would therefore change semantics outside ordinary species validation and can break Unown handling.

The project instead introduces a separate extended playable/graphics upper bound for the new species and patches only code paths that genuinely mean "unknown species".

## Confirmed first runtime blocker

Emerald's decompression routines construct 412 in Thumb code as:

```asm
movs r0, #0xCE
lsls r0, r0, #1      @ 0xCE << 1 = 412
cmp  speciesReg, r0
```

This appears in the ordinary front/back sprite loaders, causing any internal species above 412 to fall back to the question-mark sprite even when an expanded sprite table exists.

For the already-reserved project range 440–702, the same two-instruction footprint can safely use a guard value of 704:

```asm
movs r0, #0xB0
lsls r0, r0, #2      @ 0xB0 << 2 = 704
```

This is deliberately signature-checked rather than patched by an invented address. The patcher must verify the original Thumb bytes before changing them.

## BPEE core tables to expand first

Verified retail BPEE bases used by the prototype:

- `gSpeciesInfo` / historical `gBaseStats`: ROM `0x3203CC`, 28 bytes per native record
- `gSpeciesNames`: ROM `0x3185C8`, 11 bytes per record
- `gLevelUpLearnsets`: ROM `0x32937C`, 4-byte pointers

The existing BW source data remains authoritative for new species:

- personal: `/a/0/1/6`
- level-up moves: `/a/0/1/8`
- evolutions: `/a/0/1/9`

## Compatibility rules for the first binary prototype

The first runnable core deliberately does not fake unimplemented Gen IV/V engine systems.

- Gen V type IDs are translated through the already-verified Gen V -> Gen III table; they are never raw-copied because Gen III has the `TYPE_MYSTERY` gap.
- True BW Base EXP remains preserved as 16-bit source data; the legacy 8-bit field is only a compatibility field until the 16-bit EXP-award accessor is hooked.
- DS held-item IDs are never written directly into GBA item fields. They stay in source metadata until the item-ID translation table exists.
- Ability IDs not implemented by the native Gen III ability dispatcher are not treated as working abilities merely because their numeric ID exists in BW.
- Level-up entries using moves beyond the currently implemented Gen III move table are retained in the source corpus but are not exposed to the vanilla move dispatcher until move expansion lands.
- Egg/Unown internal slots 412–439 remain reserved. Expanded species data begins at 440 only.

## Activation order

1. Patch the three sprite-loader species guards by verified Thumb signatures.
2. Expand/relocate `gSpeciesInfo` to internal 0–702.
3. Expand/relocate `gSpeciesNames` to internal 0–702.
4. Expand/relocate `gLevelUpLearnsets` to internal 0–702 with compatibility-filtered BW moves for the first bootable core.
5. Add safe coordinate/icon/animation fallbacks, then proper tables.
6. Add Pokédex 387–649 routing.
7. Add evolution-method translation, new moves, abilities, cries, items and forms without deleting original Gen III behavior.
8. Regression-test vanilla 001–386 plus Egg/Unown special paths.

## Validation gate

A build is not called activated merely because data was appended. The minimum validation set is:

- internal 440, 441, 546, 649-equivalent mapping samples, and internal 702 resolve inside every expanded table;
- sprite loader no longer replaces 440–702 with species 0;
- 001–411 records are byte-preserved where intended;
- 412–439 retain their reserved meaning;
- all relocated GBA ROM pointers stay in range and aligned;
- generated ROM keeps the expected BPEE game code;
- runtime/emulator testing is reported separately from static binary validation.

ROM binaries are never committed to GitHub.
