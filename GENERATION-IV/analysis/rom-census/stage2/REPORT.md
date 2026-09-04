# Generation IV ROM Census — Stage 2

## Scope

This stage expands the Stage 1 Nintendo DS ROM structural census into record/member-level analysis for the five project ROMs:

- Pokémon Diamond (USA)
- Pokémon Pearl (USA)
- Pokémon Platinum (Korea)
- Pokémon HeartGold (Korea)
- Pokémon SoulSilver (Korea)

ROM bytes are never committed to this repository. Only analysis, metadata, hashes, decoded parameter ledgers, comparison results, and reproducible tooling are tracked.

## Method

The ROMs were parsed directly from their NDS headers/FAT/FNT/NitroFS. NARC archives were parsed down to individual members. Known structures were validated against the current `pret/pokeplatinum` and `pret/pokeheartgold` decompilations where available. Every table described below was also checked against its observed member length/count so that an external structure definition was not accepted blindly.

Message data was structurally decrypted with the Generation IV MAT algorithm used by the game code: per-message offset/length entries are decrypted from the bank key and index, then each UTF-16-like code unit is decrypted with the index-derived rolling key. This stage inventories decrypted code units and message boundaries; character-table-to-human-text transcription is a later layer.

## Level-up learnsets

The learnset entry is a 16-bit value: move ID in bits 0–8, level in bits 9–15, with `0xFFFF` as the terminator.

| ROM | Slots | Level/move entries | Max entries/slot | Validation issues |
|---|---:|---:|---:|---:|
| Diamond | 501 | 6,597 | 20 | 0 |
| Pearl | 501 | 6,597 | 20 | 0 |
| Platinum | 508 | 6,753 | 20 | 0 |
| HeartGold | 508 | 6,764 | 20 | 0 |
| SoulSilver | 508 | 6,764 | 20 | 0 |

Exact member comparisons:

- Diamond vs Pearl: 0 / 501 changed.
- Diamond/Pearl vs Platinum: 81 / 501 shared slots changed; Platinum adds 7 slots.
- Platinum vs HGSS: 14 / 508 changed: 155, 156, 157, 249, 250, 382, 383, 384, 449, 450, 483, 484, 487, 501.
- HeartGold vs SoulSilver: 0 / 508 changed.

## Trainer headers and parties

Trainer-header tables are 20-byte fixed records in all examined games, but party-member encodings are not identical across the whole generation.

- Diamond/Pearl party records use a D/P-specific layout and omit the later capsule/seal tail used by Platinum. Valid record widths by trainer data type are 6, 14, 8, and 16 bytes.
- Platinum uses a 16-bit IV scale and adds the seal/capsule field. The four party member structures correspond to base, custom moves, item, and custom moves + item.
- HGSS uses an 8-bit difficulty field plus an 8-bit gender/ability override, with its own capsule-bearing party structures.

All trainer party archives were decoded with the game-specific layout and passed length/party-size validation.

| ROM | Trainers | Party Pokémon | Type 0 | Type 1 | Type 2 | Type 3 | Nonzero-form mons | Explicit custom-move slots | Held-item mons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Diamond | 850 | 1,585 | 621 | 208 | 0 | 21 | 0 | 1,970 | 21 |
| Pearl | 850 | 1,585 | 621 | 208 | 0 | 21 | 0 | 1,970 | 21 |
| Platinum | 928 | 1,878 | 672 | 198 | 4 | 54 | 10 | 2,609 | 59 |
| HeartGold | 738 | 1,776 | 487 | 177 | 7 | 67 | 0 | 2,755 | 69 |
| SoulSilver | 738 | 1,776 | 487 | 177 | 7 | 67 | 0 | 2,755 | 69 |

Exact member comparisons:

- Diamond vs Pearl trainer headers: all 850 identical.
- Diamond vs Pearl trainer party members: all 850 identical.
- HeartGold vs SoulSilver trainer headers: all 738 identical.
- HeartGold vs SoulSilver trainer party members: all 738 identical.

## Wild encounters

### Diamond / Pearl / Platinum

The DPPt encounter member is 424 bytes. Each examined encounter archive contains 183 location records.

- Diamond contains its Diamond archive plus the Pearl archive.
- Pearl contains its Pearl archive plus the Diamond archive.
- Platinum contains the Diamond and Pearl legacy encounter archives and a Platinum encounter archive.
- Diamond active archive: 224 unique species IDs.
- Pearl active archive: 225 unique species IDs.
- Platinum active archive: 230 unique species IDs.

### HeartGold / SoulSilver

HGSS encounter members are 196-byte `EncounterData` records. Each Gold/Silver archive contains 142 location records, 135 of which are nonzero encounter locations.

- Gold archive: 165 unique species IDs.
- Silver archive: 165 unique species IDs.
- Both HeartGold and SoulSilver contain both Gold and Silver encounter archives.
- The Gold archive is byte-identical between HeartGold and SoulSilver.
- The Silver archive is byte-identical between HeartGold and SoulSilver.

This means the ordinary Gold/Silver encounter archive difference is selected by runtime/version logic rather than by shipping a different copy of these two archives in each ROM.

## Messages

All listed message banks passed MAT table validation and were decrypted to message boundaries and code units with zero invalid banks.

| ROM/archive | Banks | Messages | Decrypted 16-bit code units |
|---|---:|---:|---:|
| Diamond active | 624 | 30,211 | 1,222,674 |
| Pearl active | 624 | 30,211 | 1,222,674 |
| Platinum legacy DP | 612 | 27,232 | 611,593 |
| Platinum active | 714 | 43,276 | 1,149,410 |
| HeartGold active | 822 | 47,515 | 1,305,229 |
| HeartGold legacy PBR | 612 | 27,232 | 611,593 |
| SoulSilver active | 822 | 47,515 | 1,305,229 |
| SoulSilver legacy PBR | 612 | 27,232 | 611,593 |

Exact comparisons reveal several important lineage facts:

- Diamond and Pearl: all 624 active message-bank members are byte-identical.
- Platinum legacy DP message archive and HGSS `pbr` legacy message archive: all 612 banks are byte-identical.
- Platinum active vs HGSS active: all 714 shared bank indices differ, and HGSS adds 108 active banks.
- HeartGold vs SoulSilver: all 822 active message banks are byte-identical.

The full per-message metadata census contains 47,515 active messages per HGSS ROM and records bank/message indices, decrypted lengths and hashes. Human Korean text rendering requires the next character-map/font-code layer and is intentionally not guessed here.

## Field archives

| ROM | Scripts | Events | Map matrices | Land data |
|---|---:|---:|---:|---:|
| Diamond | 1,051 | 512 | 245 | 578 |
| Pearl | 1,051 | 512 | 245 | 578 |
| Platinum | 1,124 | 534 | 289 | 666 |
| HeartGold | 965 | 491 | 288 | 676 |
| SoulSilver | 965 | 491 | 288 | 676 |

Additional member-level observations:

- Diamond/Pearl scripts: 1,051 members, 437 unique SHA-1 payloads, one zero-length member.
- Platinum scripts: 1,124 members, 511 unique SHA-1 payloads.
- HGSS scripts: 965 members, 558 unique SHA-1 payloads.
- D/P land archives have 578 unique members; Platinum has 666; HGSS has 676.
- HGSS core paths include `a/0/1/2` scripts, `a/0/2/7` messages, `a/0/3/2` events, `a/0/3/3` learnsets, `a/0/3/4` evolutions, `a/0/3/7` Gold encounters, `a/0/4/1` map matrices, `a/0/5/5` trainer headers, `a/0/5/6` trainer parties, `a/0/6/5` land data, and `a/1/3/6` Silver encounters.

## Battle-sprite archive census

The main battle Pokémon graphics archive in every examined title contains exactly 2,964 NARC members, forming 494 six-member slots. Each slot follows the observed pattern of four RGCN graphic members followed by two RLCN palette members.

Binary six-member slot-group comparison:

- Diamond vs Pearl: 494 / 494 identical.
- Diamond vs Platinum: 494 / 494 binary groups differ.
- Platinum vs HeartGold: 230 identical, 264 differ.
- HeartGold vs SoulSilver: 494 / 494 identical.

The Diamond→Platinum result is a binary-group result, not a claim that every visible artwork is visually different; container metadata/encoding can also change a group hash.

## NARC member format census

Stage 1 had already indexed 234,759 NARC members. Stage 2 classifies their leading file signatures. Common classes include RGCN, RLCN, LZ10/LZ11, BMD0, BTX0, RCSN, RECN and RNAN, while the largest class consists of raw/format-specific members without one of these magic headers.

HGSS has notably larger counts of RGCN/RLCN and LZ-compressed members than D/P, consistent with its expanded graphics/UI/content footprint.

## Font observations

The HGSS main font archive `a/0/1/6` has 13 members and is 1,201,508 bytes. HGSS also retains legacy compatibility resources, including PBR/DPPt-lineage data. Stage 1 already established that one retained HGSS PBR font archive is an exact match for the Korean Platinum font resource, while the HGSS main font is separately expanded.

## Canonical Stage 2 artifacts

The local full Stage 2 package contains:

- every level-up learnset entry and per-slot hash ledger;
- every trainer header and trainer-party Pokémon record;
- every decoded wild encounter record;
- every message bank and per-message decrypted metadata record;
- every core script/event/map-matrix/land archive member hash;
- battle-sprite slot/member hashes;
- font archive member census;
- NARC member magic/signature census;
- cross-version comparison JSON;
- SHA-256 artifact manifest;
- reproducible builder script.

The repository keeps this report, machine-readable summaries/comparisons, the artifact manifest, and the reproducible builder. Very large purely-derived row indexes can be regenerated byte-for-byte from the project ROMs and builder and are represented by their SHA-256 hashes in the manifest rather than committing ROM-derived bulk data unnecessarily.

## Source-validation references

- `pret/pokeheartgold`: `include/wild_encounter.h`, `include/pokemon.h`, `include/trainer_data.h`, `src/msgdata.c`.
- `pret/pokeplatinum`: `include/struct_defs/trainer_data.h`.

These external definitions were used as validation aids; the census values/counts/hashes above come from the uploaded project ROMs themselves.
