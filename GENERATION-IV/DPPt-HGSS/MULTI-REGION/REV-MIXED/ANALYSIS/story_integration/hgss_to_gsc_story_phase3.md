# HGSS → GSC Story Integration — Phase 3

## Scope

Third event-integration pass covering Route 32, the optional Ruins of Alph branch, Union Cave, Route 33, Azalea Town, Kurt, Slowpoke Well, Bugsy, the Azalea rival battle, Ilex Forest, the second HGSS Kimono Girl encounter, and the overlapping Crystal/HGSS Celebi special-event material.

The fixed project rule remains: preserve G/S/C story facts and freedom first, then add HGSS characterization, choreography, state tracking, and new story actors. Version-exclusive special events remain separately identifiable rather than being rewritten as one fictional “official” event.

## Direct verification of uploaded HG/SS ROMs

The uploaded Korean HeartGold and SoulSilver ROMs were parsed through their NDS filesystem and the field-script NARC `a/0/1/2`. All checked Phase 3 script entries are byte-identical between the two uploaded ROMs:

| Script | Decomp label | Size | SHA-1 of script entry | HG = SS |
|---:|---|---:|---|---|
| 56 | `D25R0101 — Union Cave 1F` | 8 | `e8cf4832db8e1131f810e3ee00cbece3df9fff08` | Yes |
| 57 | `D25R0102 — Union Cave B1F` | 8 | `e8cf4832db8e1131f810e3ee00cbece3df9fff08` | Yes |
| 58 | `D25R0103 — Union Cave B2F` | 152 | `884e200bed523dcee943786b72aee0d31ac47881` | Yes |
| 59 | `D26R0101 — Slowpoke Well Entrance` | 508 | `c6241b406ced18902f7bcfb6ea963c2c409a92af` | Yes |
| 60 | `D26R0102 — Slowpoke Well B1F` | 508 | `94564bce695e0d584ade9a687491ae42513a95b2` | Yes |
| 92 | `D36R0101 — Ilex Forest` | 8728 | `af367ecc970ec2c333581926c5ad0e7286155005` | Yes |
| 232 | `R32 — Route 32` | 1848 | `de2e2fd85a8cec627bc397a2846beaea5892119b` | Yes |
| 236 | `R33 — Route 33` | 52 | `74d962abbe9e8fd1f45f8498272bfb5f3ab78cd9` | Yes |
| 866 | `T23 — Azalea Town` | 1160 | `34ff20affe453d4cf472ffe50ad2f8a6c49814eb` | Yes |
| 868 | `T23GYM0101 — Azalea Gym Entrance` | 112 | `cad04b67b57ff3b4c92b95861c5ab23abed81a4a` | Yes |
| 869 | `T23GYM0102 — Azalea Gym` | 472 | `00f37d5594ae887719a0066be5bee42ecad4400b` | Yes |
| 873 | `T23R0201 — Azalea Charcoal Kiln` | 220 | `39d28c5e57e1b96b5764a3580d4f531285634220` | Yes |
| 874 | `T23R0501 — Kurt's House` | 1024 | `c0ea5de673da7afc3f093b202b0e805302f71c1d` | Yes |

Result: for this Route 32 → Ilex Forest story block, no HG-vs-SS field-script divergence was found in the checked entries. Version differences may still exist in encounters, text resources, maps, graphics, or later special-event conditions and must be audited separately.

## Event integration matrix

| ID | Event | Gold / Silver | Crystal | HeartGold / SoulSilver | Integration decision |
|---|---|---|---|---|---|
| PH3-001 | Route 32 southbound gate / Miracle Seed | The Route 32 man checks Zephyr Badge and the Togepi Egg handoff before letting the early southbound progression settle; he gives Miracle Seed after the requirements are met. | Same core Route 32 progression and Miracle Seed role. | Keeps the Zephyr Badge / Togepi Egg checks with expanded movement, follower handling, and explicit state. Item 239 is Miracle Seed. | Keep the GSC gate conditions authoritative. Backport HGSS movement/state bookkeeping, but do not create a stricter new story gate. |
| PH3-002 | Route 32 million-dollar SlowpokeTail salesman | A salesman offers a SlowpokeTail for 1,000,000, foreshadowing the Slowpoke exploitation plot before Azalea. | Same narrative foreshadowing. | The same SlowpokeTail sales pitch remains in Route 32 message data. | Preserve this scene unchanged as deliberate foreshadowing for the Azalea/Slowpoke Well story. |
| PH3-003 | Ruins of Alph branch before Union Cave | Ruins of Alph is reachable as an optional side branch and is not required to reach Azalea. | Retains the optional branch while expanding Crystal-specific Ruins content elsewhere. | Retains the branch as optional side content rather than a main-story gate. | Do not force the Ruins into the main story. Preserve optional access and later integrate version-specific Ruins content in its own event pass. |
| PH3-004 | Union Cave traversal | Union Cave is the required route toward Route 33/Azalea, with side floors remaining exploratory content. | Same main-story traversal role. | Same core traversal role; the checked 1F/B1F/B2F scripts do not introduce a new main-story branch. | Preserve GSC progression. Treat HGSS cave changes as map/encounter/presentation work, not a story rewrite. |
| PH3-005 | Azalea arrival: missing Slowpoke and Rocket guard | Slowpoke are absent from town and a Team Rocket member guards access to Slowpoke Well. NPC dialogue establishes that tails are being sold. | Same core crisis and town-state change. | Retains missing Slowpoke / Rocket occupation states with explicit hide/show flags and additional actors. | Keep the GSC crisis state as canonical. Import HGSS object-state bookkeeping so town NPCs and Slowpoke restore cleanly after the well is cleared. |
| PH3-006 | HGSS Rocket harasses an Azalea civilian | No equivalent staged harassment scene; Rocket presence is conveyed mainly by guards and dialogue. | No equivalent HGSS-style staged scene. | Azalea script stages a Rocket member physically harassing/chasing a civilian and records dedicated before/after flags. | Add the staged harassment as an HGSS narrative layer without replacing any GSC Rocket guard or civilian dialogue. |
| PH3-007 | Kurt explains Team Rocket and rushes to the well | Kurt explains Team Rocket's history and SlowpokeTail operation, then rushes out to confront them. | Same core story beat. | Preserves the scene and explicitly mentions Red having broken up Team Rocket three years earlier in post-rescue dialogue; adds movement/state handling. | Preserve the GSC Kurt sequence and dialogue facts. Backport HGSS choreography and the explicit Red continuity line where it does not duplicate existing text. |
| PH3-008 | Kurt is injured in Slowpoke Well | Kurt falls into the well, hurts his back, and asks the player to defeat Team Rocket in his place. | Same core scene. | Preserves Kurt's injury and post-battle recovery with more explicit follower/movement handling. | Keep the GSC story fact exactly; use HGSS choreography and safer completion flags only. |
| PH3-009 | Slowpoke Well Rocket command structure | The well contains four ordinary Rocket grunt encounters; the final grunt delivers the 'underground activities' warning before the group leaves. | Same basic grunt-led confrontation. | The final authority is named Executive Proton, who warns the player after battle that Team Rocket continued operating underground. | Do not erase the GSC grunt roster. Keep the original grunt battles/dialogue and add Proton as the final commander after them, making the HGSS hierarchy additive rather than substitutive. |
| PH3-010 | Rocket retreat / Slowpoke restoration / Ilex activation | Clearing the well removes Rockets, restores Azalea Slowpoke, activates the Azalea rival scene and Ilex Farfetch'd quest, then returns the player to Kurt's house. | Same core state transition. | One completion script clears/sets town, rival, Ilex, Farfetch'd, and Rocket flags and warps to Kurt's house. | Use one atomic completion routine modeled on HGSS so all GSC and HGSS states switch together and cannot partially desynchronize. |
| PH3-011 | Kurt's first Ball reward and phone contact | After the rescue Kurt rewards the player with a Lure Ball, then opens his Apricorn Ball service. | Same core first reward/service. | Kurt's scripted first reward is item 492, Fast Ball, and his granddaughter can register Kurt's Pokégear number. | Preserve the GSC Lure Ball. Add the HGSS Fast Ball as a second documented reward after Ball/item expansion, and add optional Kurt phone registration. Never replace the original reward. |
| PH3-012 | Bugsy and Azalea Gym | Bugsy is the second Johto Gym Leader; gym trainers and the badge story remain independent of the rival encounter timing. | Same core story role. | Same badge role but the gym is rebuilt around Spinarak-shaped moving platforms/switches and expanded state handling. | Preserve GSC story progression. Treat the HGSS gym mechanism as a separate map/puzzle backport, not as a reason to delete the original gym implementation. |
| PH3-013 | Bugsy TM reward | Bugsy gives TM49 Fury Cutter after the Hive Badge. | Same TM49 reward. | Bugsy gives TM89 U-turn. | Keep TM49 Fury Cutter as the GSC reward. Add TM89 U-turn only after Gen IV TM expansion, explicitly marked as an HGSS integration reward. |
| PH3-014 | Azalea rival battle timing | Clearing Slowpoke Well activates the rival battle at the west/Ilex exit. It is not inherently tied to defeating Bugsy first. | Same essential timing freedom. | Slowpoke Well completion sets the Azalea rival-scene variable to 1; the west-exit coordinate trigger runs the rival battle and then advances it to 2. | Preserve this freedom. Do not incorrectly force Bugsy before the rival battle just because it is the common play order. |
| PH3-015 | Ilex Forest Farfetch'd rescue | One missing Farfetch'd is chased through a ten-position movement puzzle; returning it enables the charcoal master to give Cut. | Retains the single-Farfetch'd chase structure. | Rebuilds the quest around two missing Farfetch'd, branch-noise facing, blind spots, and separate FOUND_FIRST/FOUND_SECOND flags. | Use the original GSC Farfetch'd as the first rescue and preserve its classic chase path. Add the second HGSS Farfetch'd as a new second rescue using the behind/branch mechanic; completion requires both only in the HGSS-expanded quest state. |
| PH3-016 | HM01 Cut reward | The charcoal master gives HM01 Cut after the Farfetch'd quest. | Same story reward. | Still gives HM01 after both Farfetch'd are found. | No reward conflict. Keep HM01 and connect it to the merged Farfetch'd completion state. |
| PH3-017 | Second HGSS Kimono Girl encounter in Ilex Forest | No comparable main-story Kimono Girl encounter in Ilex Forest. | No HGSS-style five-sister story chain here. | A Kimono Girl is lost in Ilex Forest, asks the player for directions, and the player's lead/following Pokémon demonstrates the way out. She is a different sister from the Violet encounter. | Add as `EVENT_HGSS_KIMONO_ILEX_SEEN`, dependent on the Phase 2 Kimono chain being enabled but not on choosing a specific dialogue answer. Preserve the follower-Pokémon assist when that system is available; provide equivalent movement staging otherwise. |
| PH3-018 | Crystal GS Ball / Celebi shrine event | No Crystal GS Ball shrine event. | Kurt returns the GS Ball through an Azalea scene; when the forest is restless, bringing the GS Ball to the Ilex shrine can start the Celebi encounter. | Does not use the Crystal GS Ball sequence for its Celebi special event. | Preserve the Crystal GS Ball story as its own event chain and flags. Do not overwrite it with HGSS's Event Celebi time-travel story. |
| PH3-019 | HGSS Event Celebi / Giovanni time-travel chain | No equivalent time-travel event. | Has the separate GS Ball → Celebi shrine encounter, but not the HGSS Giovanni flashback/time-travel chain. | A special Celebi-related Ilex shrine script transitions to Route 22 and later Giovanni-related scenes, using dedicated hidden-object and scene flags. | Keep this as a separate HGSS special-event chain. Crystal GS Ball Celebi and HGSS Event Celebi may coexist, with independent eligibility/completion flags and separately documented project access methods. |

## State-machine rules fixed in Phase 3

### Azalea / Slowpoke Well

Use a consolidated set of story facts instead of tying logic to object visibility alone:

- `EVENT_AZALEA_ROCKET_CRISIS_ACTIVE`
- `EVENT_AZALEA_CIVILIAN_HARASSMENT_SEEN`
- `EVENT_KURT_LEFT_FOR_WELL`
- `EVENT_SLOWPOKE_WELL_CLEARED`
- `EVENT_HGSS_PROTON_DEFEATED`
- `EVENT_AZALEA_SLOWPOKES_RESTORED`

`EVENT_SLOWPOKE_WELL_CLEARED` atomically restores town Slowpoke, clears Rocket occupation actors, activates the Azalea rival exit scene, and enables the Ilex Farfetch'd quest.

### Rocket roster preservation

The GSC grunt roster is not deleted to make room for Proton.

Integration order:
1. retain the original GSC grunt encounters and their dialogue;
2. place Proton after the original confrontation chain as the HGSS commander;
3. Proton's defeat is the final completion condition for the expanded version of the well;
4. if the HGSS commander layer is disabled, the original GSC final grunt still completes the well exactly as before.

This keeps a clean compatibility path for an original-story mode while allowing the HGSS hierarchy to exist in the integrated build.

### Kurt rewards

Keep the original reward and the remake reward separately traceable:

- GSC reward: `LURE_BALL`
- HGSS reward: `FAST_BALL`
- HGSS extension: optional Kurt Pokégear number

The Lure Ball is never replaced. Fast Ball exposure is additive after the required Ball/item data expansion.

### Azalea rival timing

The rival event is tied to clearing Team Rocket from Slowpoke Well, not to Hive Badge ownership.

- Slowpoke Well clear → rival exit scene becomes active.
- Player may fight the rival before or after Bugsy.
- Defeating Bugsy must not silently consume or move the rival scene.

### Ilex Farfetch'd merge

Preserve both implementations instead of replacing one with the other:

- Farfetch'd A: retain the GSC single-Pokémon chase behavior as the first rescue.
- Farfetch'd B: add the HGSS second Farfetch'd and branch-noise / blind-spot capture behavior.
- `EVENT_ILEX_FARFETCHD_A_FOUND`
- `EVENT_ILEX_FARFETCHD_B_FOUND`
- `EVENT_ILEX_FARFETCHD_QUEST_COMPLETE`

In the full HGSS-expanded story, both A and B are required before the charcoal master hands over HM01. A compatibility/original branch can still resolve after A alone.

### Kimono Girl chain

The Ilex encounter is the second HGSS Kimono Girl story beat and is a different sister from the Violet encounter.

- `EVENT_HGSS_KIMONO_VIOLET_SEEN`
- `EVENT_HGSS_KIMONO_ILEX_SEEN`

The Ilex scene should remain viewable even if the player answers that they do not know the way; the following/lead Pokémon provides the narrative solution.

### Ilex shrine special-event separation

Do not merge Crystal and HGSS Celebi stories into one flag.

Crystal:
- `EVENT_CRYSTAL_GS_BALL_RETURNED`
- `EVENT_CRYSTAL_FOREST_RESTLESS`
- `EVENT_CRYSTAL_CELEBI_ENCOUNTER_DONE`

HGSS:
- `EVENT_HGSS_EVENT_CELEBI_ELIGIBLE`
- `EVENT_HGSS_CELEBI_TIME_TRAVEL_STARTED`
- `EVENT_HGSS_GIOVANNI_EVENT_DONE`

A project-added in-game method for accessing either formerly distribution-dependent event must be documented as a project rule, not retroactively described as original GSC/HGSS behavior.

## Reward conflicts recorded

- Kurt: GSC `Lure Ball` vs HGSS `Fast Ball`
- Bugsy: GSC `TM49 Fury Cutter` vs HGSS `TM89 U-turn`

Neither conflict is resolved by overwriting the GSC reward. Both Gen IV rewards are additive after the necessary item/TM expansion.

## Key implementation conclusion

This phase shows why a literal HGSS overwrite is the wrong architecture. The best integrated sequence is:

`Route 32 original progression`
→ `GSC SlowpokeTail foreshadowing`
→ `Azalea crisis + HGSS civilian harassment`
→ `Kurt rushes to Slowpoke Well`
→ `original GSC grunt encounters`
→ `HGSS Proton final command battle`
→ `atomic town restoration`
→ `Kurt original Lure Ball + optional HGSS Fast Ball/phone extension`
→ `Bugsy and rival in the player's original flexible order`
→ `Ilex first GSC Farfetch'd + second HGSS Farfetch'd`
→ `HM01 Cut`
→ `second HGSS Kimono Girl`
→ `Crystal GS Ball and HGSS Celebi/Giovanni special-event branches kept separate`.

This preserves the complete GSC narrative while adding HGSS's strongest story expansions rather than replacing the older implementation.
