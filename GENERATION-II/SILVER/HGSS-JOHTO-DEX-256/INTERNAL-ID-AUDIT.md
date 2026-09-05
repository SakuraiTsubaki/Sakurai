# SILVER HGSS Johto 256 — Vanilla species-ID audit

## Why this audit comes first
Before assigning any new species, the original one-byte species namespace must be treated as a compatibility contract. A value that is not a normal Pokémon entry may still be an egg marker, null value, list terminator, or other engine sentinel.

## Verified directly in all eight project ROMs
The known Silver base-data table was checked in every project ROM. Each table contains 251 records of 32 bytes, and the leading species/dex byte of record `n` is exactly `n` for all `1..251`.

The New Pokédex Order table was also checked in every ROM. It is 251 bytes and is a complete permutation of `1..251` in every language/revision.

Therefore the normal vanilla species domain is exactly `$01..$FB` (1..251) in all eight targets.

| Target | Base-data offset | New-dex offset | Base IDs | New-dex IDs |
|---|---:|---:|---|---|
| Silver ES | `$051B19` | `$040D62` | exact `1..251` | permutation `1..251` |
| Silver IT | `$051B19` | `$040D71` | exact `1..251` | permutation `1..251` |
| Silver EN | `$051B0B` | `$040D60` | exact `1..251` | permutation `1..251` |
| Silver JP Rev0 | `$051AA9` | `$040C2C` | exact `1..251` | permutation `1..251` |
| Silver JP RevA | `$051AA9` | `$040C2C` | exact `1..251` | permutation `1..251` |
| Silver DE | `$051B00` | `$040D5A` | exact `1..251` | permutation `1..251` |
| Silver KR | `$051BDF` | `$040C61` | exact `1..251` | permutation `1..251` |
| Silver FR | `$051B10` | `$040D68` | exact `1..251` | permutation `1..251` |

None of `$FC/$FD/$FE/$FF` appears as a normal entry in those two canonical species tables.

## Vanilla high-byte semantics from the matching Gold/Silver disassembly
`pret/pokegold` defines Pokémon constants `1..251`, then deliberately skips `$FC`, defines `EGG` as `$FD`, and defines no Pokémon constant for `$FE` or `$FF`.

The name table makes the latent slots visible:

- `$FC` → `?????`
- `$FD` → `EGG`
- `$FE` → `?????`
- `$FF` → `?????`
- species value `$00` underflows the name index and lands on the table's final placeholder; this does **not** make `$00` a safe species ID.

The cry table similarly contains dummy entries for 252–255, confirming that physical lookup padding exists beyond Celebi, but padding is not equivalent to four safely assignable species IDs.

`$FF` is actively used as a species-list terminator. For example, the evolution party loop reads the party-species list and exits when it sees `$FF`.

`$FD` is actively used as the egg species marker in party/day-care logic.

`$FC` and `$FE` are currently undefined as normal species, but **must not be declared free until every species-bearing read/write path is audited**. Their lack of a Pokémon constant is not sufficient proof of safe reuse.

## Consequence for HGSS Johto 256
Five additional real species cannot be represented safely by naively assigning raw one-byte IDs 252, 253, 254, 255, 256:

- 252 (`$FC`) is not a proven-free raw slot.
- 253 (`$FD`) collides with `EGG`.
- 254 (`$FE`) is undefined but not yet proven safe globally.
- 255 (`$FF`) collides with list terminators and other negative/sentinel semantics.
- 256 (`$0100`) cannot be represented in one byte.

Therefore the five HGSS additions may use canonical **16-bit logical IDs** 252–256, but those values must never be written directly into vanilla one-byte species fields.

## Required architecture before engine hookup
The next stage is an ID-reference census followed by a 16-bit logical-species layer. The reference design is the `expand-mon-ID` branch of `fellowship-of-the-roms/pokecrystal16`, whose conversion layer explicitly reserves raw values from `$FD` upward so the egg and negative/sentinel meanings survive.

Audit/port scope includes at minimum:

- party species list and party-mon structs
- box species lists and box-mon structs
- save serialization/checksums
- egg/day-care/breeding state
- base-data lookup
- name lookup
- evolution/level-up data and pointers
- wild encounters
- trainer parties
- scripted gifts/trades/static encounters
- sprites/palettes/icons/cries
- Pokédex order/seen/caught/search
- Hall of Fame
- link/time capsule and Mystery Gift paths
- all `$FF`-terminated species lists
- every range check using `NUM_POKEMON`

## Stage-1 correction
The previously staged Bank `$7E` payload did not overwrite vanilla species IDs and is still usable as isolated 16-bit data. However, any wording that described its logical IDs 252–256 as direct Silver internal/raw IDs was incorrect. Engine routing is blocked until this audit and the conversion layer are complete.
