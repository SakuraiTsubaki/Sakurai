# Generation I — Active Status

Updated: 2026-09-16 (KST)

## Japanese originals

| Game | Revisions | Banks | Active disassembly boundary | Next byte | Repository |
| --- | --- | ---: | --- | --- | --- |
| Aka | Rev 0, Rev 1 | 32 each | Bank `$00` source through `$01C3` | `$01C4` | `PocketMonsters-Aka-Disassembly` |
| Midori | Rev 0, Rev 1 | 32 each | Bank `$00` source through `$0BF0` | `$0BF1` | `PocketMonsters-Midori-Disassembly` |
| Ao | Japanese original | 32 | Bank `$00` source through `$035E` | `$035F` | `PocketMonsters-Ao-Disassembly` |
| Pikachu | Rev 0, 1, 2, 3 | 64 each | Bank `$00` source through `$01AE` | `$01AF` | `PocketMonsters-Pikachu-Disassembly` |

These boundaries are target-specific. They are not treated as common RGBY addresses.

## Program state

Active now:

- Japanese RGBY bank-by-bank disassembly
- regional/localization/revision inventory
- complete map/event/NPC/trainer/progression survey
- Pokémon/move/type/item/system survey
- text/font/UI/graphics/audio survey
- unused/debug/bug/special-behavior survey
- evidence/symbol/address-map verification infrastructure
- Tsubaki asset extraction and proven-equivalence deduplication
- later Kanto/system comparison backlog, downstream of verified Generation I originals

## Immediate disassembly order

For each game/revision:

1. finish Bank `$00` in address order;
2. keep every unresolved byte under `INCBIN`;
3. split only verified code/data boundaries into labeled source;
4. rebuild/byte-check each reconstructed range against the correct target;
5. proceed sequentially through all remaining banks;
6. map each discovered table/routine into the appropriate species/moves/items/maps/events/text/graphics/audio/system workstream.

## Target identity rule

- Aka/Midori/Ao/Pikachu are independent originals.
- Pikachu Rev 0/1/2/3 are independent targets.
- International Red/Blue/Yellow and localized releases are separate regional target families.
- Physical board variants do not automatically imply a different ROM revision; ROM identity is determined from the image/revision evidence.

## Preservation rule

ROM binaries never enter GitHub. Source, scripts, manifests, symbols, analysis, extracted/recreated assets, patches and verification metadata are retained.