# Gen III Species Parameter Accessor — Pass 6

Status: source-level accessor implemented and validated against the uploaded Pokémon Black EUR ROM. Target ROM binary hooks are not yet applied.

## Corrected BW personal NARC boundary

Direct inspection of `a/0/1/6` confirms 669 NARC members total, but they are not 669 uniform personal records:

- member 0: 56 bytes
- members 1..667: 60-byte personal records
- member 668: 1300-byte auxiliary payload, not a personal record

For target builds, member 0 is padded to 60 bytes and members 0..667 are packed into a 40,080-byte build blob. Member 668 is excluded. The highest form-personal member referenced by species 1..649 is 667.

## Accessor layer

Added `ProjectSpeciesParams` with target-facing values for:

- six base stats
- two types
- catch rate
- 16-bit base EXP
- six EV-yield values
- gender ratio
- egg cycles
- base friendship
- growth rate
- two egg groups
- ability slots 1/2/hidden
- form count
- body color
- height / weight

Profiles remain separate:

- `GEN3_ORIGINAL`
- `GEN5_BW`
- `PROJECT_APPLIED`

Current project-applied profile uses BW values while original Gen III values remain queryable.

## Verified direct-reference replacement targets

High-priority `gSpeciesInfo` consumers confirmed in pret/pokefirered:

- `CreateBoxMon`: growth rate, initial friendship
- `CalculateMonStats`: all six base stats
- gender calculation: gender ratio
- EV gain: EV yield
- battle switch/reset: battle types
- EXP award: base EXP
- ability resolution: replace 2-slot bool semantics with 0/1/2 ability slot

## Validation

Uploaded Black ROM checks passed for Bulbasaur, Mewtwo, Reshiram, Zekrom and the previously identified EV-yield changes for Yanma, Misdreavus and Blissey.

No full ROM binary is committed. Extracted 40,080-byte personal blob is build-local only; GitHub stores the extractor and validation metadata, not the ROM-derived binary.

## Next

1. Wire the accessor into an actual FireRed target build.
2. Replace battle type and EXP-yield direct reads first.
3. Replace stat/gender/EV/ability direct reads.
4. Apply the same adapter to LeafGreen / Ruby / Sapphire / Emerald with revision-specific hooks.
5. Then continue with held-item 3, TM/HM compatibility and evolution/learnset routing.
