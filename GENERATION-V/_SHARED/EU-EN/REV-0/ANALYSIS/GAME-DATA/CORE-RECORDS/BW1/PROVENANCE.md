# Generation V BW Phase 3 — Field Provenance

## Evidence policy

The uploaded Black/White ROMs are the authority for record counts, byte lengths, hashes, version equality/differences, and all emitted raw values. Historical technical documentation is used to name fields only when it matches the observed record layout. Black 2/White 2 material is never used to substitute a BW path; it is used only as a structure cross-check where the runtime format is known to persist. Unresolved bytes remain explicitly unknown/candidate.

## Technical references used

- Project Pokémon RawDB — Pokémon Black move format: https://projectpokemon.org/rawdb/black/formats/movedata.php
- Project Pokémon RawDB — Pokémon Black trainer format: https://projectpokemon.org/rawdb/black/formats/trdata.php
- Project Pokémon RawDB — Pokémon Black evolution format: https://projectpokemon.org/rawdb/black/formats/evo.php
- Project Pokémon — B/W Trainer Editor (`trdata=a/0/9/2`, `trpoke=a/0/9/3`): https://projectpokemon.org/home/forums/topic/12078-bw-trainer-editor/
- Project Pokémon — B/W Move Data (36-byte parser and move flags): https://projectpokemon.org/home/forums/topic/14212-bw-move-data/
- Project Pokémon — B/W Item Data (36-byte item record research): https://projectpokemon.org/home/forums/topic/13695-bw-item-data/
- Project Pokémon — B/W Wild Pokémon Editing (slot structure and seasonal ordering): https://projectpokemon.org/home/forums/topic/12594-pok%C3%A9mon-bw-wild-pokemon-editing/
- Project Pokémon — encounter header reverse engineering (same thread/profile repost): https://projectpokemon.org/home/profile/18827-kaphotics/content/page/291/?all_activity=1
- Project Pokémon — B2W2 General ROM Info, page 2 (trainer Pokémon 8/16/10/18-byte templates and personal struct cross-check): https://projectpokemon.org/home/forums/topic/22629-b2w2-general-rom-info/page/2/
- Project Pokémon — BW TM/HM compatibility: https://projectpokemon.org/home/forums/topic/15903-what-do-i-use-to-edit-tmhm-compatability/
- Project Pokémon — BW Pokémon Data (TM/HM bits and tutor compatibility): https://projectpokemon.org/home/forums/topic/14101-bw-pokemon-data/

## Important caveats

- `personal.narc` member indices 650–667 are alternate-form parameter records. This does **not** mean every such number is safely usable as a normal party species ID; Gen V also has special Egg/Bad Egg index semantics in this range.
- `personal.narc` member 668 is not a Pokémon record. It is a 650-entry u16 BW Unova Pokédex mapping table.
- Item bytes whose original research remains tentative are emitted with `candidate` or `unknown` names.
- Move bytes 30–31 and 34–35 are preserved as unknown.
- Trainer `ability_gender_byte` is split into high/low nibbles, while exact runtime semantics are kept separate from the raw value.
- Encounter map/location identity is intentionally not guessed in Phase 3; it will be joined through ZoneData and field-event data in the next phase.
