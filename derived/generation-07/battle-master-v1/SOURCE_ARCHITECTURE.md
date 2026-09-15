# Generation VII BATTLE_MASTER_V1 source architecture

Status: **Phase 1 evidence map.** Unknown details remain `TBD` until verified against stronger game-primary or preservation evidence.

## 1. Source-family split

Generation VII is not one graphics pipeline.

### Nintendo 3DS family

- Pokémon Sun
- Pokémon Moon
- Pokémon Ultra Sun
- Pokémon Ultra Moon

Core Pokémon battle visuals are 3D model/texture/material/animation assets. Do not describe external 2D renders as native Gen VII battle sprites.

### Nintendo Switch family

- Pokémon: Let's Go, Pikachu!
- Pokémon: Let's Go, Eevee!

Core Pokémon battle visuals are also 3D, but use the Switch-era Game Freak container/model/texture stack. Do not reuse 3DS archive/member assumptions.

---

## 2. Sun / Moon

### Confirmed Pokémon model archive

`romfs/a/0/9/3`

Contemporary Sun/Moon GARC mapping identifies:

- `a/0/9/3` = Pokémon Models
- `a/0/9/4` = DUMMY

This distinction is important because USUM moves the Pokémon archive to `a/0/9/4`.

Primary public research reference:

- Project Pokémon, “Sun and Moon Important GARC File Locations”
  - https://projectpokemon.org/home/forums/topic/39695-solved-sun-and-moon-important-garc-file-locations/

### Related graphics evidence

The same public GARC mapping identifies `a/0/6/2` as Pokémon sprites. This is tracked as a separate 2D/UI/reference asset family and is **not automatically treated as the canonical battle master source**.

### Static Pokédex render evidence

Project Pokémon preserves Sun/Moon and USUM Pokédex images and describes the Pokédex as using a 2D version of the 3D models while scrolling:

- https://projectpokemon.org/home/files/file/2628-pokemon-sm-and-usum-pokedex-images/

These are valuable front-view validation/reference material, but they do not replace battle model, battle pose, camera/orientation and back-view reconstruction evidence.

---

## 3. Ultra Sun / Ultra Moon

### Confirmed Pokémon model archive

`romfs/a/0/9/4`

Contemporary USUM model-ripping research identifies `a/0/9/4` as the Pokémon archive.

Reference:

- The VG Resource archive, Pokémon Model Ripping Project, USUM GARC mapping
  - https://archive.vg-resource.com/archive/index.php/thread-25872-134.html

The same mapping records other battle-related areas such as battle backgrounds and Z-move/effect archives, but these are not assumed to define Pokémon pose/camera until traced to the relevant load/render behavior.

---

## 4. 3DS model-package evidence

Current open-source 3DS import research supports direct handling of Pokémon X/Y, ORAS, Sun/Moon and USUM Game Freak assets.

Observed/handled source structures include:

- Game Freak `PC` / `PS` containers;
- LZ10 / LZ11 compression;
- `GFModel` and Nintendo `BCH` models;
- `GFMaterial` material state;
- `GFTexture` / BCH textures;
- `GFMotion` skeletal animation;
- model skeletons, meshes, skin weights, multiple UV sets, vertex colours and material settings.

Texture formats handled by current research include:

- RGBA8
- RGB8
- RGBA5551
- RGB565
- RGBA4
- LA8
- L8
- A8
- LA4
- L4
- A4
- ETC1
- ETC1A4

Reference:

- sxrmss/n3ds_importer
  - https://github.com/sxrmss/n3ds_importer

### Working member-group model

Public preservation/model-ripping documentation commonly describes a Pokémon/form package in a roughly nine-member sequence containing model, normal/shiny/greyscale texture sets and several animation groups.

This is **not yet accepted as a universal fixed member contract**. Exact member numbers, empty entries, aliases and special-form exceptions must be inventoried from game-primary data or a trustworthy exact extraction before final slot mapping.

### Material/shader warning

A DAE/SMD export can lose source-side render information. The canonical rendering stage must preserve or reconstruct the source material state, vertex colour use, UV transforms, alpha behavior and relevant shader-dependent effects as far as verifiable.

A model exported without these features is a derivative source and must not silently outrank a more complete game-file import.

---

## 5. Let's Go Pikachu / Eevee

### Confirmed container/model/texture family

Public Switch Toolbox documentation for Pokémon Let's Go describes:

- Pokémon models in `.gfbmdl`;
- most models stored inside `.gfpak` archives;
- Pokémon/level/trainer/NPC textures inside `.gfpak`;
- texture containers/files exposed as `.bntx` in documented workflows;
- texture export to PNG/DDS for inspection;
- model export to DAE for external inspection/editing;
- material/shader relationships that should be kept rather than discarded.

References:

- Texture workflow:
  - https://github.com/KillzXGaming/Switch-Toolbox/wiki/Pokemon-Let%27s-Go-%26-Sword-Shield-%3A-Texture-Edits
- Model workflow:
  - https://github.com/KillzXGaming/Switch-Toolbox/wiki/Pokemon-Let%27s-Go-%26-Sword-Shield-%3A-Model-Importing

### Current unknowns

The exact LGPE per-Pokémon RomFS directory/archive naming contract and exact battle animation/camera/anchor mapping are not yet fixed in this master. They remain `TBD` rather than being inferred from later Sword/Shield layouts.

---

## 6. Canonical-source hierarchy

For a final Gen III front/back reconstruction, use the strongest available evidence in this order:

1. exact game model + normal/shiny texture/material set + battle animation/pose + game battle orientation/camera/anchor data;
2. exact game-internal static/Pokédex render as visual validation evidence;
3. provenance-preserving extracted model/texture/animation package tied to exact game/archive/member;
4. pinned preservation/community render set for cross-checking;
5. ordinary web preview or screenshot only when nothing better exists, marked provisional.

No lower tier silently replaces a higher tier merely because it is easier to process.

---

## 7. Current binary PNG evidence

### Batch 0001 — committed to Tsubaki

Tsubaki commit containing the first PNG binary batch:

`5d4ced54d6dafe8e00d0a29d8f17d8ea93b1ca3b`

Path:

`derived/generation-07/battle-master-v1/source-png/usum-pokeapi-external-crosscheck/batch-0001/`

Contents:

- 0722 Rowlet through 0731 Pikipek;
- normal + shiny;
- 20 PNG files total;
- 128x128 each;
- PNG signature checked;
- SHA-256 recorded per file;
- upstream PokeAPI/sprites commit pinned to `2ecb4eeacd5a1718621fc30f12772e3f60d830b9`.

Status: **external visual cross-check only**. These are not game-primary sources and are not accepted final 64x64 battle sprites.

The PokeAPI repository documents its Generation VII USUM set as 128x128 front PNGs with female, shiny and shiny-female variants where applicable. It does not provide a corresponding USUM back-sprite set, which reinforces that it cannot be the authoritative Gen III front/back master by itself.

Repository:

- https://github.com/PokeAPI/sprites

### Higher-quality static-reference track

A 256x256 Sun/Moon Pokédex-render acquisition from Bulbagarden Archives was attempted first. The hosted GitHub Actions runner received HTTP 403 from the MediaWiki endpoint, so no binary was recorded as acquired. That track remains pending; the failure is evidence, not completion.

---

## 8. Required canonical render specification

Before the first species can become an accepted 64x64 master, record at minimum:

- exact species/form/gender logical role;
- normal/shiny source mapping;
- game and revision;
- source archive/container and member/file;
- model/skeleton identity;
- material/texture identities;
- battle animation identity;
- deterministic pose or frame-selection rule;
- front-view orientation;
- back-view orientation;
- battle anchor/ground contact;
- source camera assumptions or recovered camera data;
- render projection type;
- light/material treatment;
- alpha/transparent-material handling;
- source render dimensions;
- source render SHA-256;
- visual-validation references.

Only after that stage may the true-color/3D source proceed to Gen III palette design, 64x64 pixel reconstruction, 4bpp packing and compression.

---

## 9. Acceptance boundary

A 128x128/256x256 external render is source evidence, not completion.

A 64x64 PNG is still not completion.

`BATTLE_MASTER_V1` acceptance requires the complete fixed-contract package: final PNG, palette, 4bpp, compressed binary, provenance, hashes, logical-slot mapping, dedup mapping, scripts/settings, source/final comparison and validation records.
