# Generation V Pokémon Party Screen Audit — BW / B2W2

## Scope

This audit covers the Generation V party interface (Japanese in-game name: ポケモンリスト / Pokémon List) as an implementation reference for Generation V → ポケットモンスター.

ROM binaries are not stored in GitHub. Direct binary claims below were verified against the supplied BW ROM images; external documentation is used only for cross-checking behavior and archive identity.

## Core BW field-party presentation

BW displays up to six party members in a 2-column × 3-row grid on the DS touch screen. The upper-left panel is party slot 0 / the normal lead slot. Party member panels expose the Pokémon icon, nickname/name, gender when applicable, level, HP bar and current/max HP, with context-sensitive state for Eggs/status/etc.

The field-party action layer includes Summary, party-order switching, held-item handling, and usable field moves. Battle invocation uses a different context and legal-action set. B2W2 additionally supports direct held-item movement between party members and registered/Ready-menu access.

## Direct ROM baseline — Black EUR

Supplied Black image:

- game code: `IRBO`
- physical file size: `268,435,456` bytes (`0x10000000`, 256 MiB)
- CRC32: `E2BEE619`
- SHA-1: `a68b3bedf5c1e53556e41e59cdf396c20b331896`
- header logical capacity: 256 MiB
- header used-ROM-size field: `0x0C3B8E00`
- FAT entries: 484
- FAT maximum referenced end: `0x0BFD983C`
- ARM9 overlay entries: 237
- all FAT entries are physically present

## Direct ROM baseline — White EUR

Supplied White image, after full-file recheck:

- game code: `IRAO`
- physical file size: `268,435,456` bytes (`0x10000000`, 256 MiB)
- CRC32: `EDCD5161`
- MD5: `8dfef9a099e1269af5c1fcf9d7736a11`
- SHA-1: `f94d4578956487c09fee20809a591e858017769e`
- header logical capacity: 256 MiB
- header used-ROM-size field: `0x0C3B9400`
- FAT entries: 484
- FAT maximum referenced end: `0x0BFD9C3C`
- ARM9 overlay entries: 237
- all FAT entries are physically present

The earlier 63-MiB truncation conclusion was an analysis error. SHA-1 `9337c23adfa0d200ebbf59bc46e3a1a75061a9b7` is exactly the SHA-1 of the first `0x03F00000` bytes of this complete White image, not the full-file hash.

Public checksum databases identify CRC32 `EDCD5161` as the SweeTnDs-era USA/Europe White image and distinguish it from other canonical dump checksums. Therefore all findings are tied to the exact supplied source checksum rather than generalized to every IRAO image.

## Party subsystem overlay — ARM9 Overlay 91

Direct extraction and BLZ decompression identifies **ARM9 Overlay ID 91** as the Pokémon-list / party-screen subsystem.

### Embedded original source-module names

The decompressed overlay contains these literal source filenames in sequence:

- `pokelist.c`
- `plist_plate.c`
- `plist_message.c`
- `plist_menu.c`
- `plist_battle.c`
- `plist_demo.c`

This is direct binary evidence, not a guessed overlay assignment. It establishes that the overlay contains the general Pokémon list, party-member plate rendering/handling, message layer, menu/action layer, battle-context layer, and demo/special-context layer.

### Black Overlay 91 metadata

- overlay ID: 91
- RAM base: `0x021B6240`
- RAM size: `0x8B40` (35,648 bytes)
- BSS size: `0x20`
- static-init range: `0x021BECF0–0x021BECF4`
- overlay file ID: 91
- ROM range: `0x00166400–0x0016CF70`
- compressed/raw size: `0x6B70` (27,504 bytes)
- decompressed size: 35,648 bytes
- decompressed SHA-1: `0b369df319d81d7eeba7c5687099fb673fd02106`

Embedded module-name offsets in the decompressed image:

- `pokelist.c` at `+0x8ACC`
- `plist_plate.c` at `+0x8AD8`
- `plist_message.c` at `+0x8AE8`
- `plist_menu.c` at `+0x8AF8`
- `plist_battle.c` at `+0x8B08`
- `plist_demo.c` at `+0x8B18`

### White Overlay 91 metadata

- overlay ID: 91
- RAM base: `0x021B6260`
- RAM size: `0x8B40`
- BSS size: `0x20`
- static-init range: `0x021BED10–0x021BED14`
- overlay file ID: 91
- ROM range: `0x00166400–0x0016CF70`
- compressed/raw size: 27,504 bytes
- decompressed size: 35,648 bytes
- decompressed SHA-1: `5dd02b92ad4280e64c253336b8e8a7e0992a68df`

The same six embedded source-module names occur at the same overlay-relative offsets. Black and White decompressed overlay images are not byte-identical: 1,287 byte positions differ. White's overlay RAM base/static-init addresses are shifted by `+0x20` relative to Black. Exact semantic version deltas remain to be reconstructed; addresses must not be assumed interchangeable.

## Six-member hard limit in Overlay 91

Thumb disassembly of Black Overlay 91 shows repeated loops explicitly comparing counters against `6`. Examples occur in the early initialization path at:

- `0x021B6334`: `cmp r6, #0x6`
- `0x021B6382`: `cmp r5, #0x6`
- `0x021B6438`: `cmp r5, #0x6`

Many additional `cmp ..., #0x6` sites occur later in the same overlay. This is direct evidence that six-party-member handling is hard-coded in multiple code paths rather than existing only as a data-table count.

For Generation V → ポケットモンスター this matters if the party model is ever expanded: changing only the saved party-array capacity would be insufficient. Overlay loops, plate arrays, touch hitboxes, action-selection code and battle-context logic all require a hard-bound audit.

## Overlay architecture implication

```text
Overlay 91 / Pokémon List
├── pokelist.c       : application/core list orchestration
├── plist_plate.c    : party-member plate/panel layer
├── plist_message.c  : message/help/status text layer
├── plist_menu.c     : field/menu command handling
├── plist_battle.c   : battle-context party handling
└── plist_demo.c     : demo/special/scripted contexts
```

This confirms that field-party and battle-party behavior are context branches of the same broader Pokémon-list subsystem rather than unrelated screens.

## Confirmed Pokémon icon archive

Black direct FNT/FAT mapping:

- path: `a/0/0/7`
- FAT file ID: 249
- ROM range: `0x04912800–0x049D0E8C`
- archive size: 779,916 bytes
- NARC members: 1,431

External Gen-V filesystem documentation independently identifies `a/0/0/7` as the Pokémon icon archive. Resource identity is CONFIRMED. Exact Overlay-91 loader call-site mapping to this NARC is still pending and should not be replaced with a guessed function/NARC ID.

## Hypothetical Black-donor recovery result

A direct Black-vs-White comparison was run for the region that would have been missing if White really ended at `0x03F00000`.

Among FAT file IDs 246–483:

- 238 logical files are involved;
- 233 are byte-identical between the supplied Black and White images;
- only 5 differ: FIDs 268, 328, 368, 420, and 473.

The raw byte range `0x03F00000–0x06AA6600` is fully identical between the two supplied images. A blind Black-tail append beyond that point is not an exact White reconstruction because version-specific files appear, and FID 473 has a different size; White FIDs 474–483 begin `0x400` bytes later than their Black counterparts.

Therefore any donor repair must be FAT/file-aware. See the ROM-integrity audit for the detailed reconstruction analysis.

## Other relevant Black NARC candidates

| Path | FID | Size | Members | Current classification |
|---|---:|---:|---:|---|
| `a/0/7/0` | 312 | 24,200 B | 6 | menu/UI resource family; exact party use unresolved |
| `a/0/7/7` | 319 | 75,500 B | 8 | summary/ribbon-family cross-reference; not assigned to party |
| `a/0/7/8` | 320 | 170,496 B | 179 | large animated 2D UI bundle; party association still unresolved |

Do not promote `a/0/7/8` to “party NARC” without a direct Overlay-91 resource-loader trace. B2W2 filesystem mappings cannot be blindly back-applied to BW because archive membership/layout differs between the games.

## Party order / action semantics

The six visible positions are semantic party indices, not cosmetic tiles. Party order determines initial send-out order; Triple and Rotation Battles make storage slot, active battle position and legal replacement state separate concepts.

Recommended context/capability split:

- `PARTY_CONTEXT_FIELD`
- `PARTY_CONTEXT_BATTLE`
- `PARTY_CONTEXT_TRADE`
- `PARTY_CONTEXT_FACILITY`
- `PARTY_CONTEXT_SCRIPT_SELECTION`
- `PARTY_SUMMARY`
- `PARTY_SWITCH_ORDER`
- `PARTY_ITEM_GIVE`
- `PARTY_ITEM_TAKE`
- `PARTY_ITEM_MOVE_BETWEEN_MEMBERS` (B2W2)
- `PARTY_FIELD_MOVE_ACTIONS`
- `PARTY_BATTLE_SHIFT`
- `PARTY_BATTLE_POSITION_AWARENESS`
- `PARTY_EGG_PRESENTATION`
- `PARTY_INVALID_OBJECT_PRESENTATION`

Touch is an input adapter, not a semantic dependency; backward ports must retain button-accessible equivalents.

## Verification state

### CONFIRMED

- both supplied BW images are physically 256 MiB in the current direct full-file read;
- all 484 FAT entries are present in both current images;
- Overlay 91 is the Pokémon-list/party subsystem, based on embedded original source filenames;
- Overlay 91 contains repeated hard-coded six-member loops;
- Overlay 91 includes separate plate/message/menu/battle/demo source modules;
- Black `a/0/0/7` is FID 249, 779,916 bytes, 1,431 members; external documentation identifies it as Pokémon icons;
- hypothetical post-63-MiB donor comparison: 233/238 files byte-identical, 5 version-different.

### PARTIAL / UNRESOLVED

- exact function boundaries and original function names inside Overlay 91;
- exact direct Overlay-91 call sites that open each UI NARC;
- exact party plate/background/cursor/touch-hitbox archive/member mapping;
- semantic meaning of all 1,287 Black-vs-White Overlay-91 byte differences;
- exact BW semantics of all five version-different post-63-MiB archives;
- B2W2 binary overlay/NARC correspondence; this must be audited separately rather than inferred from BW.

No guessed overlay numbers, NARC IDs, member numbers or function names are promoted to confirmed facts.
