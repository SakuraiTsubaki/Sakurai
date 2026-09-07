# GEN2 Kanto Start — Gold KR Phase 11

## Scope
Phase 11 activates the imported RGBY Pallet Town map data and replaces the Phase 04 bootstrap warp with a Gen II-native reconstruction of the RGB + Yellow opening sequence.

## Implemented
- Pallet uses Phase 09 RGBY remapped 10x9 blocks before starter acquisition.
- After the common starter flag (event 1936) is set, Pallet returns to the original Gold 10x9 block map.
- Original Gold Pallet Fly callback is retained.
- Phase 04 `(8,1)/(9,1)` bootstrap coordinates are removed from the active event table.
- Final pre-starter north triggers are RGBY path cells `(10,1)` and `(11,1)`.
- Professor Oak is added as a Pallet outdoor object and reconstructs the RGB/Yellow stop event.
- Yellow's special Lv.5 Pikachu incident is reproduced with Gen II `CatchTutorial`, the closest native analogue to Yellow's scripted old-man-style capture sequence.
- CatchTutorial is hooked only when the tutorial species is Pikachu (`wTempWildMonSpecies = D1D4`); Route 29's Rattata tutorial still uses the original `어떤 선배` name.
- Oak then physically leads the player through Pallet with `follow` + Gen II movement commands. Both left/right intro paths end at Oak Lab door `(12,11)`; the player is one tile behind at `(12,12)` and steps onto the warp.
- GSC Teacher and Fisher are retained. RGBY girl and technology Fisher are added as separate objects.
- Gold's 3 warps and 4 BG events are byte-preserved.
- Pallet outdoor sprite set retains every sprite actually used by Pallet/Route 1 and replaces only two unused swimmer slots with Oak and Lass.

## Reserved project event flags
- 1936: common starter obtained (existing project flag)
- 1941: Oak escort complete
- 1942: Yellow Pikachu scripted capture reached
- 1943: Oak hidden
- 1944: GSC Teacher hidden during RGBY-era intro state
- 1945: right north exit used

The original Gold event table leaves the tail of the event-flag space unused up through NUM_EVENTS=2048, so these project flags do not overwrite an original event.

## ROM placement
- Pallet scripts/callbacks: `4E:6200`
- Intro scripts: `4E:6500`
- Movement data: `4E:6600`
- Pallet event table: `4E:6A00`
- RGBY remapped Pallet blocks: `73:7300`
- CatchTutorial Pikachu/Oak name hook: `08:7994 -> 08:7E50`
- Oak tutorial name data: `08:7E60`

## Validation
- Clean cumulative IPS replay: PASS
- Phase10 delta IPS replay: PASS
- Output SHA-1: `9b5fabe4a4de0a9a3f841c71103b7b9ca888cc6e`
- Output SHA-256: `45802bb0b8ad98785abbe557570a2e25fa0f3723fffcc0ec153d799a60c47455`
- Header checksum: `08` PASS
- Global checksum: `07CD` PASS
- Original Gold Pallet warps: 3/3 byte-preserved
- Original Gold Pallet BG events: 4/4 byte-preserved
- Existing GSC Fisher object: byte-preserved
- Existing Teacher object: identical except its project visibility flag
- RGBY escort path collision validation: 2/2 routes, no WALL/WATER cells
- CatchTutorial original use survey: original Gold uses it only for Route 29 Rattata; Pikachu condition therefore leaves the stock tutorial untouched.

## Fidelity correction discovered after the Phase 11 alpha build
Yellow's opening `BATTLE_TYPE_PIKACHU` battle uses `ProfOakPicBack`, not `OldManPicBack`. The two battle types share old-man-style scripted battle behavior, but the Yellow opening explicitly selects Professor Oak's own backpic. Phase 11 still uses Gen II `DudeBackpic`; importing the Yellow `ProfOakPicBack` is therefore an explicit remaining fidelity task.

## Still required before the Pallet cluster is declared final
1. RGBY girl's complete original dialogue localization (Phase 11 temporarily reuses the localized GSC raising-Pokemon line).
2. RGBY technology NPC's complete original PC-storage dialogue localization (Phase 11 temporarily reuses the GSC technology Fisher script).
3. Yellow `ProfOakPicBack` battle graphic fidelity instead of Gen II `DudeBackpic`.
4. RGBY Classic SGB palette profile alongside the GSC CGB profile.
5. Actual emulator playthrough validation when an emulator runtime is available.

No original Pallet event or NPC is deleted to make room for these additions.
