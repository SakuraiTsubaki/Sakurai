# Pokémon White IRAO-HV0 — W4 ZoneData / script / overworld / encounter linkage

Status: **directly revalidated against the supplied White ROM.** This phase establishes the field-zone graph without assigning human-readable map names yet.

## 1. ZoneData spine — `a/0/1/2`

The archive contains one member of **20,496 bytes**. It splits exactly into:

- **427 ZoneHeaders**
- **48 bytes (`0x30`) per ZoneHeader**

Scanning all 427 records gives four strong invariants:

| Offset | Direct relation |
|---:|---|
| `0x06` | `mapScriptsIndex = 2 × zoneIndex` |
| `0x08` | `initializationScriptsIndex = 2 × zoneIndex + 1` |
| `0x14` | encounter member ID, or `0xFFFF` for no encounter table |
| `0x16` | `zoneId = zoneIndex` (`0..426`) |

All four relations hold for every one of the 427 records; there are no exceptions.

## 2. Script archive — `a/0/5/7`

- total members: **899**
- ZoneData consumes members `0..853` as **427 exact pairs**:
  - even member: map/main script container
  - odd member: initialization script container
- members `854..898`: **45 additional members** outside the fixed per-zone pair range

Those 45 members are preserved as global/special script candidates. They are not labeled unused merely because they sit beyond the zone-pair range.

## 3. Overworld/entity archive — `a/1/2/5`

- total members: **428**
- ZoneData `zoneId` is an identity mapping `0..426`, giving a one-to-one zone index for the first 427 entity members under the established BW field model
- member `427` is the sole extra member and is exactly **4 zero bytes** (`00 00 00 00`)

Member 427 is therefore preserved as a special zero/sentinel candidate and is not silently discarded.

## 4. Encounter linkage — `a/1/2/6`

The ZoneHeader encounter field at `0x14` resolves perfectly against the 112-member encounter archive:

- **112** ZoneHeaders contain encounter IDs `0..111`
- every encounter ID occurs **exactly once**
- **315** ZoneHeaders contain `0xFFFF`
- there are no out-of-range encounter references

Combined with W3:

- 100 encounter members = one 232-byte encounter block
- 12 encounter members = four 232-byte seasonal blocks (928 bytes)

Thus White's 112 encounter containers are fully referenced from ZoneData with no orphan encounter member.

## 5. Graph invariants

For zone `z` in `0..426`:

- ZoneHeader record = `a/0/1/2[0][z * 0x30 : (z+1) * 0x30]`
- main map script member = `a/0/5/7[2*z]`
- initialization script member = `a/0/5/7[2*z + 1]`
- overworld/entity member = zone-linked member `0..426` under `zoneId`
- encounter member = `a/1/2/6[id]` when header `0x14 != 0xFFFF`

This is now the canonical White-first join key for subsequent NPC, warp, trigger, item, trainer, text and story-event analysis.

## 6. Next decode boundary

The next White pass should decode the content of the 427 entity members and 899 script members, then join:

- NPC objects and their script IDs
- interactable objects
- warps and target zones
- triggers / trigger conditions
- trainer-battle references
- item-give / item-ball references
- static Pokémon and gift events
- flag and variable accesses
- text-bank/message references

The 45 non-paired script members and entity member 427 stay explicitly tracked until call/reference tracing determines their runtime reachability.

## Provenance

All counts and index relations in this report were recomputed directly from `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds` (`SWEETNDS-f94d4578`). Prior BW map research was used only to identify the semantic role of the ZoneData fields; the relations themselves were re-tested across every White record.
