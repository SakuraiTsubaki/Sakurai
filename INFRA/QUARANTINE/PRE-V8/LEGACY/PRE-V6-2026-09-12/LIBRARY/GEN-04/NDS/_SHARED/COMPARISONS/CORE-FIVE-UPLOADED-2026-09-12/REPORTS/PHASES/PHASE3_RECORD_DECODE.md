# Generation IV Phase 3 — Individual Record Decode

## Scope

This phase converts the semantic NARC map from Phase 2 into record-level, field-level ledgers for the five uploaded Generation IV ROM baselines: Diamond EN-US Rev 5, Pearl EN-US Rev 5, Platinum KO-KR Rev 0, HeartGold KO-KR Rev 0, and SoulSilver KO-KR Rev 0.

The original ROMs are read-only. The current runtime copy of HeartGold is truncated at 114,098,176 bytes; Phase 3 only uses archives fully present before that boundary. The full-ROM Phase 1 baseline remains authoritative for HeartGold whole-ROM identity and tail resources.

## Validation

- 2,526 / 2,526 level-up learnset members contain the 0xFFFF terminator.
- Every evolution record is 44 bytes and all trailing u16 values are zero.
- 4,104 / 4,104 trainer party members validate after separating DP, Platinum, and HGSS record layouts and NARC alignment.
- 1,080 / 1,080 HGSS Headbutt members validate after applying six coordinate pairs per logical tree group and the 4-byte empty-map case.
- HGSS egg-move archives are both 4,092 bytes / 2,046 u16 values with 199 species/sentinel markers.

## Pokémon personal

Each personal record is 44 bytes: six base stats, two types, catch rate, base EXP, six EV yields, two held-item slots, gender ratio, hatch cycles, base friendship, growth rate, two Egg Groups, two abilities, Safari flee rate, body color/flip flag, and four u32 TM/HM masks.

Record counts: Diamond 501, Pearl 501, Platinum 508, HeartGold 508, SoulSilver 508.

The seven Pt/HGSS records after the D/P range are Giratina Origin (501), Shaymin Sky (502), and Rotom Heat/Wash/Frost/Fan/Mow (503–507). The shared 496–500 tail contains Deoxys Attack/Defense/Speed and Wormadam Sandy/Trash; 494–495 are Egg and Bad Egg.

## Growth tables

Every ROM has eight 404-byte growth tables containing 101 u32 cumulative EXP values. Rates 0–5 are the six normal curves. Rates 6 and 7 are explicitly named unused in the decompilation, byte-identical to Medium Fast, and unused by every personal record in the five baselines.

## Evolution

Each evolution member is seven `{u16 method,u16 param,u16 target}` records plus a trailing zero u16. There are exactly 246 active paths in every game. All shared evolution data is byte-identical from D/P through Pt and HGSS.

HGSS retains the Magnetic Field, Moss Rock, and Ice Rock records, but `MapHeader_GetMapEvolutionMethod()` always returns `EVO_NONE` and is marked as a D/P/Pl leftover. Thus the retained normal-location triggers are unreachable in HGSS for Magneton→Magnezone, Eevee→Leafeon/Glaceon, and Nosepass→Probopass.

## Level-up learnsets

Packed u16 format: level=`raw>>9`, move=`raw&0x1FF`, terminator=0xFFFF.

Entry counts: Diamond 6,597; Pearl 6,597; Platinum 6,753; HeartGold 6,764; SoulSilver 6,764.

D/P learnsets are identical. D/P→Pt changes 81 common records. Pt→HGSS changes 14 records: 155,156,157,249,250,382,383,384,449,450,483,484,487,501.

## Move data

Each ROM contains 471 × 16-byte records. Normal move IDs are 0–467; 468–470 are outside the normal runtime move range.

Normal-range cross-title changes found:

- Hypnosis (#95): accuracy 70 in D/P, 60 in Pt/HGSS.
- Hail (#258): unresolved offset-0x0B flag byte changes 2 in D/P/Pt → 0 in HGSS. No semantic flag name is assigned until bit-level tracing is complete.

D/P move tables are identical. HG/SS move tables are identical.

## Item data

Record counts: D 442, P 442, Pt 446, HG 514, SS 514. Each 34-byte record is decoded into price, held effect/parameter, Pluck/Fling/Natural Gift data, pocket/toss/register flags, field/battle functions, and party-use status/stat/EV/friendship parameters.

D/P item data is identical. D/P→Pt changes 242 / 442 shared records. Pt→HGSS changes 29 / 446 shared records. HG/SS item data is identical.

## Trainers

Trainer headers / decoded party Pokémon:

- Diamond: 850 / 1,585
- Pearl: 850 / 1,585
- Platinum: 928 / 1,878
- HeartGold: 738 / 1,776
- SoulSilver: 738 / 1,776

Headers are 20 bytes. Party layouts:

- D/P: 6 / 14 / 8 / 16 bytes for base / custom moves / item / item+moves.
- Platinum: 8 / 16 / 10 / 18 bytes; adds capsule/seal and packs form into species.
- HGSS: same lengths as Pt, but begins with `u8 difficulty + u8 gender/ability override` rather than Pt's u16 IV scale.

Party NARC records are 4-byte aligned. Trainer ID 0 is a zero sentinel in every game. D/P trainer headers and parties are byte-identical; HG/SS trainer headers and parties are byte-identical.

## DPPt wild encounters

Each bank is 424 bytes and is split into grass, swarm, day/night replacements, Poké Radar, form/rate fields, Unown table ID, Dual-slot Ruby/Sapphire/Emerald/FireRed/LeafGreen, Surf, an explicit unused water block, and Old/Good/Super Rod tables.

Each D/P ROM stores both the Diamond and Pearl encounter archives (183 banks each). Their comparison yields 127 changed decoded rows across 24 banks, all species-ID changes. The D and P archives themselves are identical between the two ROM files.

The explicit `unused` WaterEncounters block is zero-filled in all 915 decoded D/P/Pt bank instances.

## HGSS wild encounters

Each bank is 196 bytes: walking/surf/Rock Smash/rod rates, 12 morning/day/night grass slots, Hoenn/Sinnoh Sound replacements, Surf, Rock Smash, three rod tables, and swarm/special replacements.

Both HG and SS ROMs store `g_enc_data` and `s_enc_data`, 142 banks each; the active archive is selected by the HEARTGOLD build condition. Comparing the two archives gives 9,372 comparable rows, 642 changed rows across 53 banks, 624 species changes, 52 min-level changes, 52 max-level changes, and no rate changes. The g/s archive binaries themselves are identical between the HG and SS ROM files.

Current decompilation labels bank IDs 45,47,49,50,64,90,138 as unused; all are fully zero in the uploaded Korean encounter archives. The source also exposes an `UNUSED_142` symbol, while the uploaded Korean NARCs contain exactly 142 members indexed 0–141; that symbol remains a source/development residue pending region comparison.

## HGSS Headbutt

540 banks per version. Empty maps use a 4-byte count header. Non-empty members contain common/rare/secret 6-slot encounter tables plus six XY coordinate pairs for every logical regular/secret tree group.

Across HG/SS: 1,080 encounter-slot rows per version, 5,232 coordinate pairs per version, zero coordinate differences, and 79 species-slot differences across 33 banks. Levels and tree geometry are identical.

## HGSS egg moves

One 4,092-byte / 2,046-u16 member per version. Species marker=`20000+species`; following <=20000 values are move IDs; 65535 is the terminal sentinel.

Each version decodes to 1,847 egg-move assignments across 198 species. HG and SS are identical.

## Cross-version core findings

### Diamond vs Pearl

Only 6 / 501 personal records differ; all differences are held-item slot placement. Moves, items, evolutions, level-up learnsets, trainer headers, and trainer-party blobs are otherwise identical.

- Electabuzz 125: D 322/0, P 0/322
- Magmar 126: D 0/323, P 323/0
- Elekid 239: D 322/0, P 0/322
- Magby 240: D 0/323, P 323/0
- Electivire 466: D 322/0, P 0/322
- Magmortar 467: D 0/323, P 323/0

322=Electirizer, 323=Magmarizer.

### D/P → Platinum

Among the first 501 personal records, only six change: item fields at 125/239/466 and Safari flee-rate at 114/352/357. Pt adds seven data-form records. Hypnosis changes 70→60 accuracy. 81 common level-up learnsets change. Item and trainer datasets are heavily revised. Evolution data remains unchanged.

### Platinum → HGSS

272 / 508 personal records change, mostly TM/HM compatibility and Safari flee data. Fourteen comparable level-up records change. Hail's unresolved flag byte changes 2→0. Twenty-nine of 446 common item records change. Evolution records remain identical but map-based evolution triggers are disabled by the HGSS map helper.

### HeartGold vs SoulSilver

Personal, growth, move, item, evolution, level-up, trainer headers, trainer parties, egg moves, and Headbutt coordinate geometry are identical. Version distinctions are carried by version-selected encounter archives, Pokédex-related data, and Headbutt species slots.

## Confirmed unused / reserved / retained-inaccessible

- Growth tables 6/7: confirmed unused aliases of Medium Fast; no species references them.
- DPPt `WildEncounters.unused`: explicitly unused and zero in every decoded bank; preserve as reserved structure unless the engine is extended.
- Trainer ID 0: sentinel/reserved; do not repurpose.
- HGSS encounter banks 45,47,49,50,64,90,138: explicitly unused and zero-filled in uploaded Korean ROMs.
- HGSS `ENCDATA_UNUSED_142`: source symbol without a corresponding member in the uploaded Korean 142-member archives; region/revision validation required.
- Move data 468–470 and move scripts 468–500: normal-ID-unreachable residual/dummy space confirmed in Phase 2.
- HGSS evolution methods 24/25/26: valid retained records with normal trigger disabled by the map helper.

## Next phase

Phase 4 should bind these numeric ledgers to authoritative identifiers and text, map encounter/trainer/script records to concrete maps and events, trace candidate unused/reserved structures against runtime references, and begin explicit language/region/revision comparison beyond the five current baselines.
