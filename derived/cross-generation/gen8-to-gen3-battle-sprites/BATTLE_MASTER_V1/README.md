# Generation VIII → Generation III Battle Sprite Master V1

## Status

**Phase 1 in progress: canonical visual-source and native asset-structure research.**

This directory is the cross-repository research/control master for converting Generation VIII Pokémon battle visuals into reproducible Generation III-compatible 64×64 battle-sprite packages.

The fixed project contract is [`GEN3_PORTING_CONTRACT_KO.md`](GEN3_PORTING_CONTRACT_KO.md). The contract overrides older assumptions that a locally available ROM is required before work can continue.

No generated-image or AI image tool is permitted in this pipeline.

## Contributing upstream repositories

Generation VIII source identities remain separate and must never be flattened into one anonymous asset pool:

- `SakuraiTsubaki/PocketMonsters-Sword-Decompilation`
- `SakuraiTsubaki/PocketMonsters-Shield-Decompilation`
- `SakuraiTsubaki/PocketMonsters-BrilliantDiamond-Decompilation`
- `SakuraiTsubaki/PocketMonsters-ShiningPearl-Decompilation`
- `SakuraiTsubaki/PokemonLegends-Arceus-Decompilation`

The final target is Generation III-compatible battle graphics; game-specific Generation III insertion work remains a later target-integration stage rather than being conflated with this source master.

## Core finding

Generation VIII does **not** provide one common native 2D battle-sprite format analogous to Generation IV/V.

Sword/Shield, Brilliant Diamond/Shining Pearl, and Pokémon LEGENDS: Arceus are 3D-rendered battle games. Their party/box icons and other 2D UI images are valid assets to inventory, but they are **not automatically canonical battle-sprite sources**.

Therefore this master must separate:

1. canonical model/mesh source;
2. normal/shiny material and texture source;
3. form/gender/model-variant source;
4. battle rig and animation source;
5. battle camera / placement / scale source;
6. supplemental official battle captures used for visual validation;
7. the reconstructed 2D render used as the immediate source for Generation III conversion;
8. the final 64×64 indexed/4bpp-compatible output package.

## Source evidence hierarchy

The current hierarchy is:

### Tier A — direct game-derived structure

Highest priority when accessible:

- original model, mesh, skeleton, material and texture resources;
- original battle animation data;
- resource tables / archive mappings;
- original battle transform, scale and camera data;
- game-version/update identity and archive/member hashes.

### Tier B — code-backed reverse-engineering / extraction projects

Use when they document or decode the actual game formats and filesystem structure. Current key references include pkNX, Switch-Toolbox, OpenDPR and maintained Pokémon Switch model-import tooling.

### Tier C — verified preservation extracts

Prepared model/texture/animation extracts and established preservation sites may be used when direct files are unavailable. Their extraction history, transformations and hashes must be recorded where possible.

### Tier D — official rendered reference

Official websites, trailers, screenshots and other official captures may define or cross-check battle appearance, camera, pose, effects and design details. They are rendered references, not automatically equivalent to raw model/texture data.

### Tier E — preview/mirror/community images

Usable only when better evidence is unavailable or for cross-checking. Resizing, compression, filtering and recoloring must be assumed possible until disproven.

## Pokémon Sword / Shield

### Confirmed native direction

Public reverse-engineering tooling confirms that Sword/Shield Pokémon models are 3D resources rather than native Generation III-style battle sprites.

Evidence currently established:

- pkNX maps Sword/Shield models to `bin/archive/pokemon`.
- Switch-Toolbox documentation records Pokémon models as `.gfbmdl`, commonly stored in `.gfpak` archives.
- Switch-Toolbox documents Pokémon textures in `.gfpak` resources and BNTX texture containers.
- Current Pokémon Switch Blender tooling identifies `GFBANM` as the animation format used by Pokémon Let's Go and Sword/Shield.

### Current canonical-source rule

For Sword/Shield, the target source order is:

1. game Pokémon `.gfpak` resource;
2. contained model/mesh/skeleton/material/texture data;
3. original battle animation / idle animation;
4. game battle transform, scale and camera evidence;
5. official in-game battle captures for visual cross-check;
6. verified extracted model/texture packages only when direct structure is unavailable.

The 68×56 Sword/Shield box/party icon is **not** the canonical battle source. It remains a separate UI-asset track.

### States requiring independent inventory

At minimum:

- base species/forms;
- regional forms;
- gender-dependent visual differences;
- normal / shiny appearance;
- Gigantamax forms as distinct visual models/forms;
- Dynamax as a battle state/effect rather than automatically a separate species sprite;
- DLC-added/re-enabled Pokémon and forms;
- model/material aliases and truly identical assets;
- version/update differences where present.

## Brilliant Diamond / Shining Pearl

### Confirmed native direction

BDSP uses Unity and provides a well-documented AssetBundle-based Pokémon resource layout.

OpenDPR identifies the game as built on Unity 2019.4.27f1 and uses AssetRipper-based reconstruction of game resources.

Community reverse-engineering documentation records Pokémon resources under:

`romfs/Data/StreamingAssets/AssetAssistant/Pokemon Database/pokemons/`

The currently documented structure separates at least:

- `common`: model mesh, main animations, extra textures and normal/shiny texture variants;
- `battle`: battle rig/scripts and battle-exclusive animations;
- `field`: overworld rig/scripts and field-exclusive animations.

Documented naming distinguishes forms and appearance variants. Community filesystem documentation records normal/shiny texture resources and gender/form identifiers rather than treating them as one flattened Pokémon image.

### Current canonical-source rule

For BDSP, use the **battle model pipeline**, not the chibi overworld model, for Generation III battle sprites:

1. common model/mesh resource;
2. battle rig and battle animation resource;
3. normal/shiny texture/material variant;
4. form/gender resource mapping;
5. in-game battle placement/camera validation;
6. only then generate the deterministic 2D reconstruction source.

Field/chibi resources remain an independent asset category and must not replace the battle model simply because they are easier to render.

### Version rule

Brilliant Diamond and Shining Pearl remain separate game identities in the manifest even if a given model or bundle proves byte-identical.

## Pokémon LEGENDS: Arceus

### Confirmed native direction

pkNX maps Pokémon resources to `bin/archive/pokemon` and records Pokémon resource-list/table data including:

- `bin/appli/res_pokemon/list/pokemon_info_list.bin`
- `bin/pokemon/table/poke_resource_table.trpmcatalog`

Current maintained Pokémon Switch model tooling identifies the newer model family used by Legends: Arceus with resources including `TRMDL` and associated model components; the same tooling distinguishes a `_rare.trmtr` material path for shiny/rare material loading.

The maintained animation exporter identifies `TRANM` as the animation format used by Pokémon Legends: Arceus (as opposed to Sword/Shield's GFBANM family).

### Current canonical-source rule

1. PLA Pokémon archive/resource-table identity;
2. TRMDL model and linked mesh/skeleton/material/texture resources;
3. normal / rare material relationship;
4. battle animation (`TRANM`) source;
5. battle/world scale and placement parameters;
6. official/in-game capture for pose and rendering validation;
7. deterministic 2D reconstruction source;
8. Generation III conversion.

### States requiring independent inventory

At minimum:

- Hisuian forms;
- new evolutions/forms introduced in PLA;
- gender differences;
- normal/shiny materials;
- Alpha state and its scale/effect treatment as a battle/world state rather than silently creating a new species form;
- Noble/Lord/Lady or special presentation states where relevant;
- form-change and special-resource aliases;
- Strong Style / Agile Style animation differences in the separate animation-preservation track.

## Front / back reconstruction rule for 3D Generation VIII games

Generation VIII has no native pair of 2D `front.png` / `back.png` battle sprites to preserve. Therefore a Generation III pair must be reconstructed from the canonical 3D battle source without mislabeling that reconstruction as an original 2D source.

The working rule is:

- **front** = opponent-side battle presentation derived from the game's battle model, battle pose/idle and opponent-view camera semantics;
- **back** = player-side battle presentation derived from the same canonical battle source and the player-view/back-facing battle semantics;
- do not create `back` by blindly mirroring or rotating an already flattened front PNG;
- preserve original model scale/placement evidence; do not opaque-bbox normalize every species to the same apparent size;
- preserve one documented semantic animation phase for the static master and retain the full animation source separately.

The exact per-title pose/frame/camera contract remains **not yet fixed** until battle-animation and camera evidence is reconciled.

## Generation III output contract

Each accepted logical battle role ultimately requires the complete package defined by the fixed contract, including:

- 64×64 human-viewable final PNG;
- source/reconstructed-source image;
- target indexed pixel map;
- Generation III-compatible palette data;
- 4bpp graphics data;
- compressed insertion asset;
- full source and output SHA-256 chain;
- logical-role → canonical-asset map;
- cross-game SHA-256 dedup map;
- source provenance and version identity;
- automated output and any manual correction kept separately;
- visual comparison and validation records;
- deterministic rebuild scripts/settings.

A PNG by itself is never considered complete.

## Current unresolved items — blocking final render, not blocking research

The following still require exhaustive research before the first **final** Generation VIII battle sprite can be approved:

- exact Sword/Shield Pokémon archive/member naming and model-to-form map;
- exact Sword/Shield battle idle-animation and camera/scale parameters;
- exact BDSP battle bundle → form/gender/model/animation mapping across all supported species/forms;
- exact PLA archive/member naming and resource-table interpretation for every available Pokémon/form;
- per-title normal/shiny material semantics and any exceptions;
- deterministic static battle-pose selection contract;
- front/back camera/anchor contract;
- Generation III target palette construction for true-color/3D sources without automatic frequency-only quantization;
- all form, gender, special-state and duplicate relationships;
- patch/update and version differences.

These are research tasks, not reasons to stop work when ROM files are unavailable.

## External technical references currently used

- pkNX — Nintendo Switch Pokémon ROM/data research and game-file mappings: https://github.com/kwsch/pkNX
- pkNX `GameFileMapping.cs`: https://github.com/kwsch/pkNX/blob/master/pkNX.Game/File/GameFileMapping.cs
- Switch-Toolbox: https://github.com/KillzXGaming/Switch-Toolbox
- Sword/Shield model-format notes: https://github.com/KillzXGaming/Switch-Toolbox/wiki/Pokemon-Let%27s-Go-%26-Sword-Shield-%3A-Model-Importing
- Sword/Shield texture-format notes: https://github.com/KillzXGaming/Switch-Toolbox/wiki/Pokemon-Let%27s-Go-%26-Sword-Shield-%3A-Texture-Edits
- OpenDPR: https://github.com/TeamLumi/opendpr
- BDSP filesystem/visual research: https://bdsp-modding.wiki/index.php/Visuals
- BDSP Pokémon bundle-path cross-check: https://github.com/BlupBlurp/BDSP-Texture-Recolor-Tool
- maintained Pokémon Switch model/animation importer: https://github.com/ChicoEevee/Pokemon-Switch-Model-Importer-Blender
- older PLA model-import preservation reference: https://github.com/SomeKitten/LegendsArceusBlenderScript
- official Sword/Shield Battle Stadium reference: https://swordshield.pokemon.com/en-us/gameplay/pokemon-battle-stadium/
- official BDSP battling reference: https://diamondpearl.pokemon.com/en-us/trainersguide/fundamentals/battling/

## Next phase

Build a complete structured source inventory before any final 64×64 asset is approved:

1. Sword/Shield resource/form inventory;
2. BDSP resource/form inventory;
3. PLA resource/form inventory;
4. cross-title species/form identity table;
5. normal/shiny/gender/form/state coverage matrix;
6. battle animation + camera/anchor research;
7. deterministic render-source specification;
8. only then begin reviewable PNG → palette → 4bpp → compressed asset batches.

Work must proceed in small reviewable batches and all evidence/state must remain traceable to its exact upstream game/repository identity.
