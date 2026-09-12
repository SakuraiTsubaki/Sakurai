# Pokémon White IRAO-HV0 — W3 trainer and wild-encounter structures

Status: **record boundaries and size/flag relationships verified directly from the supplied White ROM.** Field semantics are cross-checked with BW-specific tools where noted.

## 1. Trainer metadata — `a/0/9/2` (`trdata`)

Direct archive profile:

- members: **616** (`0..615`)
- member 0: **16 zero bytes** (dummy/truncated zero record)
- members 1..615: **20 bytes each**

For normal trainer records the 20-byte layout is:

| Offset | Size | Field |
|---:|---:|---|
| `0x00` | 1 | format flags |
| `0x01` | 1 | trainer class |
| `0x02` | 1 | battle type |
| `0x03` | 1 | party count |
| `0x04` | 2 | battle item 1 |
| `0x06` | 2 | battle item 2 |
| `0x08` | 2 | battle item 3 |
| `0x0A` | 2 | battle item 4 |
| `0x0C` | 4 | AI flags |
| `0x10` | 1 | secondary battle-type / auxiliary field |
| `0x11..0x13` | 3 | padding / auxiliary |

The BW-specific archive identity is independently cross-checked by Project Pokémon BW Trainer Editor research and TrainerTyrant: `trdata=a/0/9/2`, `trpoke=a/0/9/3`.

### Format-flag distribution

Among trainer IDs 1..615:

- flag `0`: **546** trainers
- flag `1`: **42** trainers
- flag `2`: **20** trainers
- flag `3`: **7** trainers

## 2. Trainer party data — `a/0/9/3` (`trpoke`)

The archive also has **616 members**, so trainer metadata and party data are index-aligned.

Directly pairing `trdata.party_count` with each party blob proves the per-Pokémon record widths:

| `trdata` format flag | Trainers | Per-Pokémon bytes | Structural interpretation |
|---:|---:|---:|---|
| 0 | 546 | 8 | base trainer-Pokémon record |
| 1 | 42 | 16 | base + 8 bytes (four explicit `u16` moves) |
| 2 | 20 | 10 | base + 2 bytes (held item) |
| 3 | 7 | 18 | base + held item + four explicit moves |

Every trainer 1..615 satisfies `len(trpoke_member) == party_count × per_pokemon_width` for the width selected by its format flag. There are **zero mismatches**.

This gives a stronger structural result than treating the party NARC as variable unknown blobs: the low two bits of the trainer format select the optional held-item and custom-moves payloads. TrainerTyrant independently describes the same relationship: the Trainer Data `Format` determines whether Pokémon records contain explicit Item and Moves fields.

Member 0 is a special dummy case: `trdata[0]` is 16 zero bytes and `trpoke[0]` is 6 zero bytes. It must not be used to infer the normal record width.

## 3. Wild encounter archive — `a/1/2/6`

Direct archive profile:

- members: **112**
- 100 members are **232 bytes**
- 12 members are **928 bytes**
- `928 = 4 × 232` exactly

The 12 four-block members are IDs:

`2, 44, 45, 46, 47, 48, 49, 73, 84, 88, 93, 94`

This is the concrete ROM-level representation of locations that carry four seasonal encounter blocks. Until map-header/ZoneData linkage is completed, the blocks are stored as `season_block_0..3`; the exact Spring/Summer/Autumn/Winter ordinal will be tied to runtime/map evidence rather than guessed from file order.

### One 232-byte Gen V encounter block

The BW encounter structure cross-checks against PPRE and sums exactly to 232 bytes:

- `0x00`: walk rate
- `0x01`: double-grass rate
- `0x02`: special-walk rate
- `0x03`: surf rate
- `0x04`: special-surf rate
- `0x05`: Super Rod rate
- `0x06`: special-Super-Rod rate
- `0x07`: eighth/auxiliary rate
- `0x08..0x97`: walking tables = 3 groups × 12 slots × 4 bytes
  - normal grass: 12 slots
  - double grass: 12 slots
  - special/shaking grass: 12 slots
- `0x98..0xBF`: surfing = normal 5 slots + special/rippling 5 slots
- `0xC0..0xE7`: Super Rod = normal 5 slots + special/rippling 5 slots

Walking slot (`4 bytes`):

- packed `u16`: species ID + form bit
- `u8` minimum level
- `u8` maximum level

Water/fishing slot (`4 bytes`):

- packed `u16`: species ID + wider form field
- `u8` minimum level
- `u8` maximum level

The directly observed 232-byte size is therefore fully accounted for; no unexplained tail remains.

## 4. White-first preservation rules from W3

1. Do not flatten seasonal 928-byte encounter members into one table; all four 232-byte blocks are source data and must remain individually addressable.
2. Do not derive trainer-party record widths from the party blob alone; `trdata` format bits select the optional item/move extensions.
3. Preserve trainer ID 0 as a special dummy/truncated record rather than padding it to 20/8 bytes and silently changing the source representation.
4. BW trainer paths must remain separate from B2W2 paths; B2W2 shifts the trainer NARCs.
5. The next map pass must join encounter member IDs to ZoneData/map headers before assigning human-readable location names or season ordinals.

## Cross-check references

- Project Pokémon BW Trainer Editor research: BW `trdata=a/0/9/2`, `trpoke=a/0/9/3`.
- ThirdLemon/TrainerTyrant: Gen V trainer Format controls explicit held-item and custom-move fields.
- Project Pokémon PPRE `pokemon/field/encounters.py`: Gen V encounter-rate fields and 12/12/12 walking + surf/Super-Rod normal/special slot layout.

All member counts, sizes, flag distributions and zero-mismatch checks above were recomputed directly from the supplied White ROM.
