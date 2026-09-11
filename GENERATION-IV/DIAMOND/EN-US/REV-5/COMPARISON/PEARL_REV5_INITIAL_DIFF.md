# Diamond EN-US Rev 5 vs Pearl EN-US Rev 5 — initial raw filesystem diff

## Scope
Byte-level comparison of the uploaded retail ROMs at Nintendo DS FAT/NitroFS file-entry level. This is an initial structural baseline, not the final gameplay-difference catalog.

## Result
- Path-aligned entries compared: 357 unique path/unnamed-entry keys
- Identical entries: 337
- Differing entries: 18 non-FNT/unnamed entries
- Diamond-only named path: `poketool/personal/personal.narc`
- Pearl-only named path: `poketool/personal_pearl/personal.narc`
- All other common named NitroFS paths compared in this pass were byte-identical.

## Interpretation
The visible NitroFS trees are extremely close. A substantial part of Diamond/Pearl version selection is therefore not represented as duplicated differently named resource files; executable/overlay and version-selected data must be tracked separately. The personal-data archive path is explicitly version-specific in the filesystem.

## Next decomposition
1. Map every FAT entry to FNT, ARM9/ARM7 overlay tables, banner, and remaining container roles.
2. Parse all NARCs and compare member counts/member hashes.
3. Map version-exclusive encounter, trainer, script, message, and personal/species behavior to the executable/data selectors that consume them.
4. Separate genuine version differences from revision/localization differences.
