# Secondary PNG evidence policy

## Purpose

Generation VI X/Y and ORAS do not provide Generation III-style native 2D front/back Pokémon battle sprites. Public PNG collections can still be useful for visual cross-checking, provenance comparisons, color references, and quick human review, but they must not be confused with the canonical model-based source or the final Generation III reconstruction.

## Existing upstream state

The four Generation VI decompilation repositories currently contain one public-source Pokémon PNG each for National Dex 650 Chespin:

- X: `assets/pokemon/sprites/650.png` — 48×64 — PokeAPI X/Y source
- Y: `assets/pokemon/sprites/650.png` — 48×64 — same recorded PokeAPI X/Y blob as X
- Omega Ruby: `assets/pokemon/sprites/650.png` — 46×61 — PokeAPI ORAS source
- Alpha Sapphire: `assets/pokemon/sprites/650.png` — 46×61 — same recorded PokeAPI ORAS blob as Omega Ruby

The upstream manifests already label these as public-source preservation evidence rather than direct retail-ROM verification. This classification is retained.

See `source-ledgers/upstream_existing_png_audit.csv`.

## Classification

PokeAPI Generation VI version PNGs are classified in this project as:

`secondary-provisional-visual-evidence`

They may be retained and expanded as a review set, but they are not by themselves eligible to become:

- native Generation VI battle sprites;
- direct ROM extractions;
- verified Generation VI model renders;
- final `BATTLE_MASTER_V1` canonical renders;
- final Generation III 64×64 insertable sprites.

## Why they are still useful

They can help with:

- quick species recognition checks;
- normal/shiny visual comparison;
- gender-difference comparison where the public source supplies a female variant;
- XY versus ORAS public-render comparison;
- detecting gross color or silhouette mistakes in a later model-derived reconstruction;
- preserving already-used public-source evidence without discarding earlier work.

## What they cannot prove

A public front PNG cannot establish:

- the exact game-native model member;
- exact model/texture hashes;
- the opponent battle camera;
- the player-side rear battle camera;
- the canonical idle motion/frame;
- the complete material/visibility state;
- relative in-battle scale and anchor;
- a native back view;
- Gen III palette membership;
- final 4bpp identity.

## PokeAPI path families

Current public repository structure documents Generation VI front-view PNG families under:

- `sprites/pokemon/versions/generation-vi/x-y/`
- `sprites/pokemon/versions/generation-vi/omegaruby-alphasapphire/`

with applicable subpaths including:

- default front: `<id>.png`
- female front: `female/<id>.png` when present
- shiny front: `shiny/<id>.png`
- shiny female front: `shiny/female/<id>.png` when present

Availability is species-dependent; a missing female file is not an error when the public source itself has no distinct female image.

## Batch rule

Secondary PNG evidence must be collected in small reviewable batches.

Each batch records at minimum:

- source repository and exact path;
- fetched URL or repository coordinate;
- species ID;
- variant;
- byte size;
- PNG width/height;
- SHA-256;
- collection timestamp when generated outside Git;
- evidence class;
- destination path;
- missing/not-applicable status.

Do not silently replace an existing PNG. If bytes differ, keep the existing file and investigate provenance before changing it.

## Relationship to the final battle master

The final pipeline remains:

`verified Generation VI model + textures + battle pose/camera evidence`

→ `canonical front/back renders`

→ `semantic ≤16-color Generation III palette reconstruction`

→ `deterministic 64×64 pixel conversion`

→ `validated PNG + palette + 4bpp + compressed asset`

Public PNG evidence is a side-channel cross-check, not the source-of-truth shortcut.
