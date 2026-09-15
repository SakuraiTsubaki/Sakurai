# Generation VI canonical render evidence hierarchy

## Purpose

Generation VI does not provide dedicated Generation III-style front/back 2D Pokémon battle sprites. The `BATTLE_MASTER_V1` pipeline therefore has to reconstruct static front/back targets from the official 3D visual system without inventing a false native 2D source.

This file defines which visual evidence can establish the model, pose, camera, silhouette, scale, and front/back appearance of the reconstructed target.

## Evidence hierarchy

### Tier A — direct game-native model reconstruction

Highest priority when available:

- verified XY/ORAS Pokémon model member;
- verified normal/shiny texture member;
- verified material/visibility/skeletal animation members;
- verified battle idle motion/state;
- verified battle-side camera/transform data or a reproducible game-equivalent render setup;
- verified game-specific scale/anchor behavior.

A Tier-A render is the preferred canonical source render.

### Tier B — verified in-game battle capture

Use as direct visual validation and, when Tier-A camera/animation parameters remain unresolved, as strong reconstruction evidence:

- unscaled or losslessly preserved capture from XY/ORAS battle presentation;
- known title/version/side (opponent or player);
- known normal/shiny/form/gender state;
- capture provenance recorded.

A screenshot/GIF frame is still a rendered output, not the underlying model data. It must not be mislabeled as a native sprite.

### Tier C — preservation-community captures derived from the official 3D game presentation

Useful for cross-checking front/back pose, silhouette, color, and form coverage when their production method is documented.

One important surviving corpus is the Pokémon Showdown `xyani` family:

- `xyani/` — front animated visual
- `xyani-back/` — back animated visual
- `xyani-shiny/` — front shiny animated visual
- `xyani-back-shiny/` — back shiny animated visual

Historical Showdown model/sprite discussion documents a capture workflow based on a Nintendo 3DS capture card or emulator, followed by frame-by-frame background removal and GIF assembly. Therefore these assets are valuable official-game-render-derived evidence, but they remain derivative captures rather than archive-native model resources.

Current indices:

- https://play.pokemonshowdown.com/sprites/xyani/
- https://play.pokemonshowdown.com/sprites/xyani-back/
- https://play.pokemonshowdown.com/sprites/xyani-shiny/
- https://play.pokemonshowdown.com/sprites/xyani-back-shiny/

Historical process discussion:

- https://www.smogon.com/forums/threads/ps-model-mod-fixing-thread.3500358/

### Tier D — other public static/animated mirrors

Examples include PokeAPI version PNGs and other preservation mirrors. These are useful for recognition and color/silhouette cross-checking, but provenance may not establish exact game camera/pose or archive identity.

Existing PokeAPI PNG handling is governed by `SECONDARY_PNG_POLICY.md`.

### Tier E — official marketing/render artwork

Official artwork can confirm design structure and semantic colors, particularly details that become difficult to read at battle distance. It does not establish game-native battle pose, camera, or rendering scale by itself.

## Front/back rule

Generation III requires separate front and back targets.

For Generation VI:

- front target = opponent-side canonical battle presentation;
- back target = player-side rear canonical battle presentation.

A front asset is never mirrored or rotated mechanically to create the back target. Back-view evidence must be reconstructed/validated independently from the official 3D model and/or a documented in-game rear-view capture.

## Animation-frame rule

Do not pick the first GIF frame or model-viewer frame merely because it is convenient.

For every canonical source render record, preserve:

- motion/animation identity if known;
- timestamp/frame chosen;
- material/visibility state;
- camera/view side;
- model transform/scale/anchor;
- why that frame is representative of the normal in-battle idle presentation;
- supporting capture/model evidence.

If the exact game-native idle state is not established, mark the chosen frame `provisional`.

## Scale and canvas rule

Derivative GIF/PNG dimensions are not the canonical Generation III scale.

Do not:

- resize every Pokémon independently to fill 64×64;
- use each GIF's tight image bounds as an implicit species-size standard;
- assume a preservation site's canvas size is a native XY/ORAS canvas.

Instead establish a common canonical render canvas/anchor and validate relative battle scale against game evidence before the final 64×64 conversion.

## Shiny rule

Whenever the game-native shiny texture is available, it outranks recolored or independently recreated shiny imagery.

Showdown/PokeAPI shiny assets may validate appearance, but they do not replace the source texture member in final provenance.

## Acceptance levels

A final 64×64 target should record one of:

- `canonical-source=tier-a`
- `canonical-source=tier-a+b`
- `canonical-source=tier-a+b+c`

Tier C/D/E evidence can support validation, but a result based only on derivative web imagery remains provisional unless no better source can be recovered and the limitation is explicitly recorded under the project-wide fallback rule.
