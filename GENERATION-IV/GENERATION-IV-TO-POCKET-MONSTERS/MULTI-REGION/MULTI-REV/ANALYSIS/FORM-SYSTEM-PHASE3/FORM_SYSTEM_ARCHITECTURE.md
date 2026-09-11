# Generation II / III → Generation IV Form System — Phase 3

## Result of checking the actual uploaded ROM families

### Gen II
Uploaded Gold/Silver KR ROM headers declare 32 KiB cartridge RAM.
Crystal EN Rev A also declares 32 KiB; Crystal JP declares 64 KiB.

The Gold/Silver BoxMon layout has two skipped bytes after Pokérus before level.
That means Gold/Silver can gain a persistent form field without changing the
BoxMon/PartyMon structure length. Crystal cannot use the same bytes because
Crystal uses them as caught-data.

Proposed Gold/Silver byte 0:
- bit 0: extended species ID high bit (needed for #256+)
- bits 1..5: stored form 0..31
- bits 6..7: reserved
The second skipped byte stays reserved.

Crystal uses a packed 6-bit sidecar instead:
- 1 bit extended species high
- 5 bits stored form

A worst-case 286 persistent slots needs 215 bytes. Crystal's documented save
layout contains 0x18A (394) bytes of padding in both main/backup save areas, so
the extension fits without overwriting caught-data. The save/copy/checksum
routines still need explicit extension hooks.

### Gen III
Every uploaded Gen III ROM contains the FLASH1M_V save-library signature.

Gen III already stores species as u16, so no species-width sidecar is needed.
However the encrypted BoxPokemon payload has no safe general 5-bit form field.
The four 'unused ribbon' bits are not enough for Arceus's 18 forms and should
not be repurposed.

Use a packed form sidecar:
- party: 6 * 5 bits = 4 bytes
- boxes: 14 * 30 * 5 bits = 263 bytes
- total: 267 bytes

Emerald PokemonStorage occupies 0x83D0 bytes. Its nine 3968-byte save sectors
provide 35712 bytes, leaving 1968 bytes of capacity, so the 263-byte box form
sidecar fits comfortably there. Party forms must live in a save block that is
written by link saves; do not put party forms only in PokemonStorage.

R/S/FR/LG have to be checked individually for the exact tail address before
binary insertion even though their overall save format is closely related.

## Form model

Base species ID stays the National Dex species.

Examples:
- Rotom = species 479, form 0..5
- Giratina = species 487, effective form 0..1
- Shaymin = species 492, form 0..1
- Arceus = species 493, effective form 0..17

Not every form is persisted:
- DERIVED: Unown (native DV/personality rule)
- VOLATILE: Castform, Cherrim
- PERSISTENT: Deoxys, Burmy, Wormadam, Shellos, Gastrodon, Rotom
- CONDITIONAL: Giratina, Shaymin, Arceus according to Gen IV rules

## Required engine hooks

A form value must travel with a Pokémon through:
- party swap/compact
- deposit/withdraw
- box-to-box move/copy
- daycare
- evolution
- egg creation/hatching
- gift/static creation
- wild creation
- trade/link serialization
- Hall of Fame / battle facilities where a persistent copy is made

GetEffectiveForm() then selects the actual battle/species-data record using:
stored form + held item + weather + field/time/status conditions as applicable.

## Status

This package establishes the storage model and source-level accessors.
It intentionally does not claim a playable binary patch yet.
The next binary stage is:
1. bind sidecar storage to verified per-ROM save addresses,
2. hook mon move/copy/save/load paths,
3. implement one persistent-form proof case (Rotom) and one dynamic proof case
   (Castform/Cherrim),
4. regression-test save/load and box/party moves on every uploaded ROM.
