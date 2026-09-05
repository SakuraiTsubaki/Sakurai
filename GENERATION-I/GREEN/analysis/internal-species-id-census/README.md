# Pokémon Green — internal species ID census for HGSS Johto 256

Date: 2026-09-05 (Asia/Seoul)

## Conclusion first

The project should **not** migrate species IDs to 16-bit yet.

Pokémon Green already uses an 8-bit internal species index. An exhaustive count shows that the HGSS Johto 256 roster can fit exactly in the full byte domain `$00-$FF` while preserving all 151 original Kanto internal IDs.

The price is that **every one of the 256 byte values becomes a valid species ID**, so the few places that currently use `$00` or `$FF` as species-list sentinels/format markers must be converted to count/length/state-driven formats.

This is still substantially less invasive than doubling the species field in party, box, save, battle, trainer and wild structures.

## Existing Green ID space

Current declared internal range is `$00-$BE`.

- `$00`: `NO_MON`
- `$01-$BE`: 190 nonzero index values
  - 151 real Kanto species
  - 36 ordinary MissingNo holes
  - 3 pseudo-species graphics IDs: `$B6/$B7/$B8`
- `$BF-$FF`: outside the current Pokémon index tables

The 36 ordinary holes are:

`1F 20 32 34 38 3D 3E 3F 43 44 45 4F 50 51 56 57 5E 5F 73 79 7A 7F 86 87 89 8C 92 9C 9F A0 A1 A2 AC AE AF B5`

The three pseudo-species slots are:

- `$B6` `FOSSIL_KABUTOPS`
- `$B7` `FOSSIL_AERODACTYL`
- `$B8` `MON_GHOST`

They are not real party species. Their purpose is to feed special fossil/Ghost sprite dimensions and pointers through `GetMonHeader`. They can be moved to explicit special-graphics paths and their three IDs reclaimed.

## Exact capacity arithmetic

The HGSS Johto regional Pokédex has 256 real species. Green already has all 151 Kanto species, so 105 additional species IDs are required.

Reclaimable byte values:

- 36 ordinary MissingNo holes
- 3 pseudo-species IDs
- 65 values `$BF-$FF`
- 1 value `$00`

Total: **105**.

Therefore:

`151 preserved Kanto IDs + 105 reclaimed/new IDs = 256 species exactly`

There is no spare species ID and no null species byte in the final saturated layout.

## Why internal ID $00 is technically attractive for species #256

Several central Green tables already index with the pattern `dec a` before table lookup.

If the table is expanded to 256 entries:

- internal ID `$01` -> table entry 1
- ...
- internal ID `$FF` -> table entry 255
- internal ID `$00` -> `dec` wraps to `$FF` -> table entry 256

This behavior already exists in `GetMonName` and `IndexToPokedex`.

The reverse `PokedexToIndex` increments an 8-bit counter while scanning `PokedexOrder`. If the unique encoded Pokédex value for regional #256 is `$00` and it is stored only in the 256th entry, the counter naturally wraps from `$FF` to `$00` at that entry. Thus internal ID `$00` and regional Pokédex #256 encoded as `$00` are mutually compatible with the existing byte arithmetic.

The seen/owned flag path also decrements the one-byte Pokédex number before bit indexing. Regional #256 encoded as `$00` therefore becomes bit index `$FF` = bit 255, exactly the 256th bit of a 32-byte bitset.

## Sentinel/format conflicts that must be removed

### `$FF`

Player/enemy party and box species lists have explicit count fields **and** a trailing `$FF` terminator. Multiple routines stop on `$FF` instead of the count. To make `$FF` a real species ID, these loops must be changed to use `wPartyCount`, `wEnemyPartyCount`, or `wBoxCount`.

Examples include:

- healing loop
- party menu draw loop
- Hall of Fame party iteration
- trade-center party list
- party/box add/remove code

Hall of Fame saved teams also terminate with `$FF`; because the HOF record is fixed-width, this can be replaced by an explicit count or by a non-species field sentinel such as level 0.

### `$00`

Trainer party data uses `$00` as end-of-team in both common-level and per-Pokémon-level formats. `$FF` is additionally used as the 'special trainer/per-Pokémon levels' format marker. Both meanings collide with a fully saturated species byte.

The clean replacement is a counted trainer-party format, for example a header carrying `count + format`, followed by exactly that many species records. This removes both `$00` and `$FF` from trainer species control flow.

`NO_MON` also needs to stop being represented by species byte `$00`; absence should be represented by the surrounding count/state variable instead.

## Other required high-ID fixes

### GetName HM/TM collision

`GetName` currently performs `cp HM01` before checking which name list is being requested. `HM01` is `$C4`, and the source itself asserts that Pokémon IDs must stay below that value because otherwise a Pokémon name can be misrouted to `GetMachineName`.

For a 256-ID roster this must be fixed by applying the HM/TM branch **only when the requested list type is ITEM_NAME**. Direct `GetMonName` already uses byte-table arithmetic suitable for a 256-entry name table.

### Zero-as-invalid checks

Some graphics/palette routines explicitly treat internal ID or converted Pokédex value `$00` as invalid/no Pokémon. Those checks must be audited and removed or made context-specific. This is a finite call-site patch; it is not a reason to widen every stored species ID.

### Bounds checks

Checks such as `cp NUM_POKEMON_INDEXES + 1` cannot express 257 in a byte once there are 256 species. They must be removed, inverted to table-safe logic, or replaced by context validity/count checks.

## Tables to expand from 190 to 256 internal entries

The Green source ties these directly to `NUM_POKEMON_INDEXES`:

- `MonsterNames`
- `EvosMovesPointerTable`
- `CryData`
- `PokedexOrder`
- `PokedexEntryPointers`

Other internal-ID-indexed graphics/palette paths must be audited as part of the call-site census.

Base stats themselves are Pokédex-number indexed in vanilla Green, so the HGSS parameter conversion can either expand that dex-indexed layer to 256 entries or introduce a direct 256-entry personal table while preserving the 8-bit internal species field.

## Architecture decision

**Preferred baseline: saturated 8-bit species IDs (`$00-$FF`), not 16-bit species IDs.**

Preserve every original Kanto ID. Reclaim all 39 non-real IDs inside `$01-$BE`, extend into `$BF-$FF`, and use `$00` as the 256th species ID after sentinel removal.

This keeps the species member of party/box/battle/save records one byte wide and avoids a cascading binary-format migration across nearly every Pokémon structure.

## Next implementation pass

1. Assign the 105 non-Kanto HGSS species to the 105 available byte IDs deterministically, with internal `$00` reserved for HGSS regional #256.
2. Produce a complete 256-row `internal_id <-> HGSS Johto slot <-> National Dex` ledger.
3. Convert party/box/HOF species iteration from `$FF` termination to counts/state.
4. Convert trainer parties from `$00/$FF` sentinel format to counted format.
5. Fix `GetName` for Pokémon IDs `$C4-$FF`.
6. Expand the five core internal-ID tables to 256 entries.
7. Expand the Pokédex seen/owned bitsets to 32 bytes and audit all `$00`-as-invalid checks.
8. Only after these tests pass, inject exact HGSS personal/evolution/learnset parameters.

The previously committed 16-bit runtime prototype is explicitly marked withdrawn and is not the active baseline.
