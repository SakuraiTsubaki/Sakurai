# Generation VII battle sprite master v1

## Status

**Phase 1 active: source architecture and source-PNG acquisition. Final Generation III 64x64 master is not yet approved.**

The fixed conversion/preservation contract is in [`FIXED_CONTRACT.md`](FIXED_CONTRACT.md).

This project covers both Generation VII source families:

- Nintendo 3DS: Pokémon Sun, Moon, Ultra Sun, Ultra Moon
- Nintendo Switch: Pokémon: Let's Go, Pikachu! and Pokémon: Let's Go, Eevee!

They are not assumed to share one native graphics structure.

## Inherited baseline

The Generation IV `BATTLE_MASTER_V1` established whole-canvas 80x80 -> 64x64 indexed-source preservation. Generation V generalized the same approach for its dedicated static NCGRs and kept animated multipart data as a separate track.

Generation VII changes the source problem: the core battle Pokémon are 3D model/texture/material/animation assets rather than native Generation III-style 2D indexed battle sprites. Therefore the project must preserve the Generation IV/V principles while changing the source stage rather than pretending a native 2D battle sprite exists.

## Confirmed 3DS Pokémon model archive locations

| Game family | Pokémon model archive | Verification state | Notes |
| --- | --- | --- | --- |
| Sun / Moon | `romfs/a/0/9/3` | verified by multiple contemporary preservation/research references | Do not substitute the USUM path. |
| Ultra Sun / Ultra Moon | `romfs/a/0/9/4` | verified by multiple USUM model/research references | Expanded-model projects also target this file. |

Important: later tutorials sometimes describe `a/0/9/4` while discussing “Sun/Moon” generically. Contemporary Sun/Moon file-location research identifies `a/0/9/3` as Pokémon Models and `a/0/9/4` as dummy in SM, while USUM research identifies `a/0/9/4` as Pokémon. The games are therefore tracked separately.

Research references:

- Project Pokémon Sun/Moon GARC map: https://projectpokemon.org/home/forums/topic/39695-solved-sun-and-moon-important-garc-file-locations/
- VG Resource Sun/Moon model-ripping discussion: https://archive.vg-resource.com/archive/index.php/thread-25872-100.html
- VG Resource USUM GARC map: https://archive.vg-resource.com/archive/index.php/thread-25872-134.html
- Pokémon USUM Expansion release notes referring to `a/0/9/4`: https://github.com/TheSomewhatUnknownGuy/PokemonUSUMExpansion/releases

## 3DS model package structure

Public preservation documentation consistently describes Pokémon/form data as a group of roughly nine members. The commonly documented order is:

1. model;
2. normal texture set;
3. shiny texture set;
4. greyscale texture set;
5. battle animations;
6. Pokémon Refresh animations;
7. idle/walk/run animations;
8. lip animations;
9. empty/auxiliary member.

This is a working archive-layout contract, **not permission to assume every form has nine semantically identical non-empty members**. Exact member identity, emptiness, aliases and special cases must be verified during archive inventory.

References:

- SPICA model-export workflow and model index notes: https://github.com/gdkchan/SPICA/pull/55/files
- USUM model-data documentation: https://www.gamebrew.org/wiki/Ultra_Sun_and_Ultra_Moon_Pokemon_Model_Data_and_Tools_3DS

## Native 3DS asset formats

Modern open-source importers that build on SPICA/Ohana research confirm that the Pokémon 3DS assets can contain:

- `GFModel` model/skeleton/mesh data;
- `GFMaterial` material state;
- `GFTexture` textures;
- `GFMotion` skeletal animations;
- Nintendo `BCH` variants in related assets/containers;
- PICA200 texture encodings including RGBA8, RGB8, RGBA5551, RGB565, RGBA4, LA8, L8, A8, LA4, L4, A4, ETC1 and ETC1A4.

Reference implementation/documentation:

- https://github.com/sxrmss/n3ds_importer
- https://projectpokemon.org/home/forums/topic/42362-spica-model-tool/

These formats are source formats. Exported DAE/SMD/TGA/PNG files are derivatives and must retain their provenance back to the corresponding game archive/member.

## No native 2D battle-sprite fiction

Sun/Moon and Ultra Sun/Ultra Moon do not supply a Generation III-style 2D indexed front/back battle sprite as the core battle Pokémon visual. The final 64x64 front/back sprites are therefore reconstructions from canonical 3D visual sources.

Do not label a web PNG or a rendered still as “the original Gen VII battle sprite.”

## Game-internal Pokédex render track

Sun/Moon and USUM also use 2D Pokédex images derived from the 3D models. Public preservation sets expose these as 256x256 PNGs, including normal/shiny and many form/gender distinctions.

These images are useful because they are game-derived static visual evidence, but they do not replace the primary battle model/animation/camera source and they do not provide the required back-view master by themselves.

References:

- Project Pokémon preserved Pokédex-image set: https://projectpokemon.org/home/files/file/2628-pokemon-sm-and-usum-pokedex-images/
- Bulbagarden SM Pokédex-image category: https://archives.bulbagarden.net/wiki/Category:Sun_and_Moon_Pok%C3%A9dex_images
- Bulbagarden SM shiny Pokédex-image category: https://archives.bulbagarden.net/wiki/Category:Sun_and_Moon_Shiny_Pok%C3%A9dex_images

### Source hierarchy for the 3DS family

For final `BATTLE_MASTER_V1` work, use this priority order:

1. exact game model + textures/materials + battle animation/pose + game battle orientation/camera/anchor data;
2. exact game-internal Pokédex/static render as front-view validation evidence;
3. provenance-preserving extracted model/texture/animation sets whose source game/archive/member is documented;
4. preserved community mirrors/render sets as cross-checks;
5. ordinary web previews/screenshots only when no better source is available, clearly marked provisional.

## 3D -> Generation III reconstruction requirements

For every logical Pokémon role, the reconstruction stage must eventually establish:

- species/form identity;
- gender visual role or alias state;
- normal/shiny source;
- canonical battle model;
- canonical battle idle pose/frame or deterministic pose rule;
- front battle orientation;
- back battle orientation;
- source model scale and battle anchor;
- material/shader-sensitive features such as rim, emissive, transparency, normal-map-dependent or metallic-looking details;
- source render dimensions and transparent background handling;
- Generation III 64x64 placement;
- Generation III palette selection with visual-identity validation;
- final 4bpp/compressed output and hashes.

The 3D path does **not** mechanically reuse indexed `preservation-v2` color voting because the source is not an indexed sprite. The preservation-v2 principles still govern no-generative-tools, no arbitrary crop/scale normalization, provenance, deduplication, silhouette preservation and visual validation.

## Source PNG batch 0001

The first small review batch is deliberately source-only before final palette/4bpp conversion.

Species:

- 0722 Rowlet
- 0723 Dartrix
- 0724 Decidueye
- 0725 Litten
- 0726 Torracat
- 0727 Incineroar
- 0728 Popplio
- 0729 Brionne
- 0730 Primarina
- 0731 Pikipek

For each species the batch acquires the preserved Sun/Moon 256x256 Pokédex image in normal and shiny state. These 20 PNGs are **source/reference assets, not accepted final 64x64 battle sprites**.

The Tsubaki asset location is:

`derived/generation-07/battle-master-v1/source-png/sm-pokedex-external/batch-0001/`

The binary acquisition job resolves each Bulbagarden file through the MediaWiki API, records source metadata, validates the PNG signature/dimensions, computes SHA-256 and commits the binary PNG plus a manifest. This avoids falsely claiming a binary asset was uploaded through a text-only connector.

## Next acceptance gate

Before any 64x64 result is called final, the following must be resolved for at least the first test species:

1. canonical battle model/member mapping;
2. normal/shiny texture member mapping;
3. battle-animation member and idle pose/frame;
4. deterministic front/back battle render orientation and anchor;
5. true-color -> Generation III palette policy that preserves identifying rare colors instead of frequency-only reduction;
6. side-by-side validation against the model/Pokédex render and in-game battle appearance;
7. PNG + palette + 4bpp + compressed binary + complete manifest/hash package.

Until those gates pass, source PNGs and test renders remain explicitly provisional/source evidence.
