# European Crystal map-script expansion: Banks 75, 76 and 79

## Finding

The uploaded EN Rev 0, EN Rev A and JP Rev 0 ROMs have all-zero banks 75, 76, 79 and 7A. The uploaded ES, DE, FR and IT ROMs instead contain substantial data in 75, 76 and 79; 7A remains all-zero in all seven ROMs.

Exact semantic disassemblies for Spanish and French independently identify these three banks as additional map-script banks:

| Bank | European semantic section |
|---:|---|
| `75` | `Map Scripts 26` |
| `76` | `Map Scripts 27` |
| `79` | `Map Scripts 28` |
| `7A` | unused / all-zero in all seven surveyed ROMs |

This means the European localizations expanded the map-script/text layout from the English layout's 25 map-script sections to 28. These banks must not be treated as generic free space in European ROM work.

## Spanish source anchors

`erosunica/pokecrystal-es` maps:
- Bank 75 → `Map Scripts 26`; the section begins with `Route36NationalParkGate.asm`, `ViridianGym.asm`, ...
- Bank 76 → `Map Scripts 27`; the section begins with `ManiasHouse.asm`, `CianwoodGym.asm`, ...
- Bank 79 → `Map Scripts 28`; the section begins with `LakeOfRageHiddenPowerHouse.asm`, `LakeOfRageMagikarpHouse.asm`, ...

## French source anchor

`qwilvove/pokecrystal-fr/layout.link` independently maps the same bank numbers to `Map Scripts 26`, `Map Scripts 27`, and `Map Scripts 28`.

## Implication for German and Italian reconstruction

No exact rebuildable DE/IT disassembly repository was confirmed in the current GitHub survey. Their bank occupancy, however, matches the European expansion pattern. The reconstruction workflow should therefore lift the ES/FR section boundaries and map identities, then recover DE/IT symbol addresses with byte-sequence alignment, pointer tables, script opcodes and text terminators. Every recovered section must be validated against the original DE/IT ROM by byte-perfect rebuild.
