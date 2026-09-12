# HGSS → GSC Story Integration — Phase 1

## Scope

First-pass event comparison for the opening chapter from New Bark Town through the first rival battle in Cherrygrove City. The goal is not to replace GSC with HGSS, but to preserve G/S/C event identity while backporting HGSS additions as compatible branches and extensions.

## Source verification

### Uploaded ROMs

| Game | Header / code | SHA-1 | Notes |
|---|---|---|---|
| HeartGold (Korea) | `POKEMON HG` / `IPKK` | `5834fb3a2d751c48501d47d6a56898d7af6ccf9e` | 128 MiB NDS |
| SoulSilver (Korea) | `POKEMON SS` / `IPGK` | `0330e6449306606114a92bdbb3f9d3d51d392b96` | 128 MiB NDS |
| Gold (Korea) | `POKEMON_GLDAAUK` | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | 2 MiB GBC |
| Silver (Korea) | `POKEMON_SLVAAXK` | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` | 2 MiB GBC |
| Crystal (Japan) | `PM_CRYSTAL` | `95127b901bbce2407daf43cce9f45d4c27ef635d` | 2 MiB GBC |
| Crystal (English Rev A) | `PM_CRYSTAL`, rev 1 | `f2f52230b536214ef7c9924f483392993e226cfb` | Matches pret Crystal v1.1 SHA-1 |

### Reverse-engineering references

- `pret/pokegold`: Gold/Silver disassembly.
- `pret/pokecrystal`: Crystal disassembly.
- `pret/pokeheartgold`: HGSS decompilation/disassembly.
- HGSS `a/0/1/2` is mapped by `pokeheartgold/filesystem.mk` to `fielddata/script/scr_seq.narc`.

### Direct HGSS script archive check

The uploaded Korean HG and SS copies contain 965 entries in `a/0/1/2` (`scr_seq.narc`). The opening-area scripts below are byte-identical between HG and SS:

| Script | Decomp label | HG/SS size | SHA-1 of entry | HG = SS |
|---:|---|---:|---|---|
| 842 | `T20` — New Bark Town | 5964 | `e9f12fa8897de031c5fcb64b6295f4a3b8749998` | Yes |
| 843 | `T20R0101` — Elm's Lab | 4440 | `f6b402c841d48ce9d2219ecdd118c97f6b8b1c3a` | Yes |
| 850 | `T21` — Cherrygrove City | 2864 | `3fed886cdd1fbad13dbcc3580d991b23ce1c6468` | Yes |

This means the opening story flow can initially use one shared HGSS logic specification; version-specific branches can be introduced only where later evidence shows HG/SS differences.

## Opening story event matrix

| ID | Event | Gold / Silver | Crystal | HeartGold / SoulSilver | Integration decision |
|---|---|---|---|---|---|
| OP-001 | New Bark west-exit safety gate | NPC stops player if they try to leave without a Pokémon. | Same structure. | Opening progression is handled with expanded scene variables and scripted NPC sequences. | Preserve the GSC no-Pokémon exit gate exactly. HGSS scene variables are not needed as a replacement; add only new branch flags. |
| OP-002 | Rival outside Elm's Lab | Rival watches Elm's Lab and physically shoves the player away when approached. | Same core event. | Rival remains part of the opening, while the opposite-gender protagonist/friend and Marill are also present as new New Bark story actors. | Keep the original rival spying/shove event. Add the HGSS friend + Marill introduction as a separate event so neither replaces the other. |
| OP-003 | First meeting with Elm | Elm immediately establishes the errand and leads into starter selection. | Expanded: Elm asks for help, the player accepts, Elm receives the message/email, explains the mission, then directs the player to choose a Pokémon. | Expanded scripted introduction with movement, communication sound cue, multiple messages, then starter selection. | Use Crystal/HGSS as the mandatory cinematic structure. Preserve G/S wording/content as supplementary Elm dialogue rather than deleting it. |
| OP-004 | Starter selection | Three Poké Balls in the lab; choice sets starter flags. | Same three-ball selection, with Crystal's longer lead-in. | Dedicated starter-selection application; starter becomes the lead/following Pokémon. | Preserve the three-starter choice and original starter flags. Port the HGSS immediate post-selection flow on top of it. |
| OP-005 | Immediate starter nickname | No immediate nickname prompt. | No immediate nickname prompt. | Player is offered a nickname immediately after choosing the starter. | Add the HGSS nickname prompt. It is independent of the follower system and can be implemented even before follower sprites are complete. |
| OP-006 | Starter following player | Not present. | Not present. | Starter is transitioned into the following-Pokémon system during the lab sequence. | Add only after the follower system itself is backported. Story flags must not require follower rendering to progress. |
| OP-007 | Elm aide support item | Aide gives 1 Potion after starter selection. | Same basic event. | Aide gives 5 Potions; script explicitly checks bag space for quantity 5. | Treat quantity as a documented balance difference. Default integration candidate: HGSS quantity 5, but keep a compatibility constant so original GSC quantity 1 can be restored without rewriting the event. |
| OP-008 | Cherrygrove guide tour | Optional guided city tour; accepting it ends with the Map Card added to Pokégear. | Same core event. | Expanded forced-style introduction: guide escorts player around town, gives Running Shoes, later returns and registers the Map Card. | Preserve the GSC choice to accept/decline the tour. If accepted, use HGSS rewards/order: Running Shoes at tour end, Map Card when the guide returns. If declined, leave both available via re-interaction so no content is lost. |
| OP-009 | First rival battle | Rival intercepts player returning from Mr. Pokémon, uses the starter strong against the player's choice, then leaves. | Same core battle. | Same story role; Cherrygrove script selects one of three `PASSERBY_BOY` trainer entries based on starter choice and sets `FLAG_MET_PASSERBY_BOY`. | Keep GSC battle position/scene identity. Backport HGSS pre-name trainer identity/flag structure only where useful for later dialogue branching. |
| OP-010 | Rival naming after theft report | Police officer at Elm's Lab asks the player to identify/name the thief. | Same core event. | Elm's Lab script calls the dedicated `NameRival` command after the police sequence; the opposite-gender friend participates in the expanded scene. | Preserve GSC police naming as the core. Add the HGSS friend as witness/context before the naming screen; do not move rival naming to a different chapter. |

## State-machine design for GSC target

New event state should be additive rather than replacing original GSC flags.

Suggested new flags/variables for the opening chapter:

- `EVENT_HGSS_FRIEND_INTRO_SEEN`
- `EVENT_HGSS_MARILL_INTRO_SEEN`
- `EVENT_HGSS_STARTER_NICKNAME_OFFERED`
- `EVENT_HGSS_CHERRYGROVE_RUNNING_SHOES_GIVEN`
- `EVENT_HGSS_CHERRYGROVE_MAP_CARD_RETURN_DONE`
- `EVENT_HGSS_FRIEND_WITNESS_THEFT`
- `VAR_STORY_COMPAT_OPENING_MODE` reserved for testing original-GSC vs integrated flow; not exposed as a player-facing mode unless needed.

Existing GSC flags such as starter acquisition, Mystery Egg progression, rival encounter, Pokégear/Map Card state and Elm laboratory scenes should remain authoritative wherever they already represent the same story fact.

## Implementation rule established by Phase 1

For overlapping scenes, use this priority:

1. Preserve the original GSC progression fact and completion flag.
2. Insert HGSS-only actors, dialogue, movements and rewards around that fact.
3. Reuse Crystal's expanded scene when Crystal already forms the bridge between G/S and HGSS.
4. Add new flags only for genuinely new HGSS content; do not duplicate an existing GSC state flag.
5. Never make a cosmetic HGSS feature such as a following sprite a hard dependency for story progression.

## Next comparison block

Continue from Route 30 / Mr. Pokémon's house through Violet City and Falkner, including:

- Mr. Pokémon + Professor Oak sequence
- Mystery Egg handoff
- catching tutorial differences
- Route 30 trainer gate and phone registration
- Violet City arrival
- Sprout Tower ordering
- Falkner / badge / Elm call
- Togepi Egg delivery changes
- first HGSS friend reappearances
