# Pokémon Black/White EUR — Game Parameter Map

Current ROMs were read-only. This note consolidates the parameter-bearing archives and adds a direct Black-vs-White member comparison from the uploaded ROM pair.

## ROM pair

- Black: `POKEMON B`, game code `IRBO`, 256 MiB.
- White: `POKEMON W`, game code `IRAO`, 256 MiB.
- Both expose 484 NitroFS file IDs; 247 named filesystem files and 237 NARC archives.

## Core parameter archives

|Role|Path|Members|Record / payload shape|Black vs White|
|---|---|---:|---|---|
|personal|`a/0/1/6`|669|members 1..649 base species 60 B; 650..667 alt forms 60 B; 668 local-Dex map 1300 B|identical|
|growth|`a/0/1/7`|8|8 × 404 B growth curves|identical|
|level_up_moves|`a/0/1/8`|668|668 variable members, 4–92 B|identical|
|evolutions|`a/0/1/9`|668|668 × 42 B; 7 × 6 B slots|identical|
|baby_base|`a/0/2/0`|650|650 × 2 B|identical|
|move_data|`a/0/2/1`|560|560 × 36 B|identical|
|item_data|`a/0/2/4`|627|627 × 36 B|identical|
|trainer_meta|`a/0/9/2`|616|616 members, 16–20 B|identical|
|trainer_party|`a/0/9/3`|616|616 variable members, 6–108 B|identical|
|egg_moves|`a/1/2/3`|650|650 members; u16 count + move IDs|identical|
|encounters|`a/1/2/6`|112|112 members; 100 × 232 B + 12 × 928 B seasonal|29 differing members|
|zone_data|`a/0/1/2`|1|1 × 20496 B = 427 × 48 B|identical|
|field_scripts|`a/0/5/7`|899|899 variable members|identical|
|overworlds|`a/1/2/5`|428|428 variable members|identical|
|main_text|`a/0/0/2`|288|288 members|identical|
|story_text|`a/0/0/3`|472|472 members|identical|

## Species / form parameter block (`a/0/1/6`)

- Species IDs 1..649 have one 60-byte `PersonalInfo5BW` record each.
- 18 alternate-form stat records occupy members 650..667.
- Member 668 is `650 × u16` and maps species IDs 0..649 to the original Unova Dex number; non-members use sentinel `999`.
- Original Unova numbering is 0..155: Victini 494→0, Snivy 495→1, Genesect 649→155.
- Key 60-byte fields: base stats, types, catch rate, EV yield, held items, gender, hatch cycles, friendship, growth group, egg groups, three ability slots, form routing, base EXP, height, weight, 101 TM/HM bits and tutor bits.

## Black/White parameter delta

- Every compared core archive is byte-identical between Black and White **except wild encounters `a/1/2/6`**.
- `a/1/2/6` has 29 differing member IDs: `0,5,6,49,52,53,58,69,71,75,77,79,80,81,82,83,84,95,98,99,100,101,102,104,105,106,107,108,109`.
- Existing whole-ROM census additionally shows species-indexed seasonal/location availability `a/1/7/8` differs in 26 members.
- Therefore species stats, learnsets, evolutions, moves, items and trainer teams are not version-specific in this ROM pair; version identity is applied mainly through encounter/availability resources plus non-parameter presentation/code differences.

## Expansion dependencies

An expanded Unova/Generation-V dex cannot be implemented by appending PersonalInfo alone. At minimum the species-indexed chain must be extended coherently:

1. PersonalInfo + form routing (`a/0/1/6`) and the local-Dex map member.
2. Level-up learnsets (`a/0/1/8`), evolutions (`a/0/1/9`), baby/base map (`a/0/2/0`) and egg moves (`a/1/2/3`).
3. Species-indexed availability (`a/1/7/8`) and any encounter/trainer/script references that use new species IDs.
4. Pokémon names/text, sprites/animations (`a/0/0/4`), menu icons (`a/0/0/7`) and Pokédex presentation resources.
5. Executable consumers of the current boundaries. Literal-xref census already proves active comparisons against 649/650/651 in ARM9 and overlays, so code limits must be patched rather than assuming NARC growth alone is sufficient.
6. Save/Pokédex bitfields and UI/search loops still need consumer-level proof before declaring a safe maximum species count.

## Current conclusion

The data model itself is highly modular and NARC-based, which is favorable for expansion. The hard part is not the 60-byte species record; it is making every species-count consumer, species-indexed table, save structure and presentation subsystem agree on the new maximum.
