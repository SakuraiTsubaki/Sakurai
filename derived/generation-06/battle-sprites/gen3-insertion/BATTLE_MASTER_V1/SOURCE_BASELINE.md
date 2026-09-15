# Generation VI battle source baseline

## Purpose

This file records the currently verified public-source baseline for the Generation VI → Generation III battle-sprite reconstruction project. It deliberately separates confirmed archive facts from provisional reconstruction decisions.

## Evidence levels

- **confirmed-public** — supported by multiple technical references or a mature reverse-engineering implementation.
- **reported-public** — documented by a preservation/research source but still requires direct per-member verification.
- **provisional** — project reconstruction rule awaiting direct game-level verification.
- **unresolved** — not yet established.

## XY archive baseline

| Field | Current value | Status |
|---|---|---|
| Pokémon model archive | `a/0/0/7` | confirmed-public |
| Box/party icon archive | `a/0/9/3` | confirmed-public |
| Box/party icon canvas | 40×30 | confirmed-public |
| Item icon archive | `a/0/9/4` | confirmed-public |
| Item icon canvas | 30×30 | confirmed-public |
| Native 2D front/back Pokémon battle sprite sheet | none identified; Generation VI battle presentation is model-based | confirmed-public |

The published XY model-member map shows an eight-member stride for ordinary model/form blocks in the documented range and explicitly separates many gender/model/form states. Example ranges include Bulbasaur `4–11`, Ivysaur `12–19`, Venusaur male `20–27`, Venusaur female `28–35`, and Mega Venusaur `36–43`. This is useful mapping evidence, but every member role still requires signature/hash verification before final-master status.

## ORAS archive baseline

| Field | Current value | Status |
|---|---|---|
| Pokémon model archive | `a/0/0/8` | confirmed-public |
| Trainer overworld models | `a/0/2/1` | confirmed-public |
| Trainer battle models | `a/1/3/3` | confirmed-public |
| Trainer mugshots | `a/1/6/0` | confirmed-public |
| Native 2D front/back Pokémon battle sprite sheet | none identified; Generation VI battle presentation is model-based | confirmed-public |

Public ORAS extraction research reports recurring Pokémon/form groups with approximately eight members:

1. model/geometry container (`.pc` in older extraction-tool naming),
2. small animation-related member (`.pf`),
3. normal texture (`.pt`),
4. shiny texture (`.pt`),
5. additional texture-related member,
6. animation-related member (`.pb`),
7. animation-related member (`.pk`),
8. small container/member (`.pc`).

Separate blocks are reported for some forms and gender differences. Treat the eight-member pattern as `reported-public`, not as an invariant, until member signatures and loading behavior are reconciled.

## Resource format baseline

Modern open-source Nintendo 3DS asset tooling supports the relevant Game Freak/Nintendo resource families used by XY/ORAS:

- PC / PS containers,
- GFModel / BCH model structures,
- GFMaterial / BCH materials,
- GFTexture / BCH textures,
- GFMotion / BCH animation structures,
- LZ10 / LZ11 compression where applicable.

Supported texture encodings documented by current tooling include RGBA8, RGB8, RGBA5551, RGB565, RGBA4, LA8, L8, A8, LA4, L4, A4, ETC1, and ETC1A4. The exact encoding of each retained Pokémon texture must be recorded per source member rather than inferred globally.

## Important negative finding

The following must **not** be treated as the native battle master source:

- 40×30 Pokémon box/party icons,
- third-party 120×120 PNG render sets,
- arbitrary model-viewer screenshots,
- marketing art used without game-render validation,
- a model exported in its bind/default viewer pose.

These may be useful as secondary comparison evidence only.

## Generation III target baseline

The target engine family uses 64×64 Pokémon battle sprites with 4bpp object graphics and separate front/back sprite tables plus normal/shiny palette handling. The project therefore targets:

- 64×64 final front image,
- 64×64 final back image,
- indexed 4bpp-compatible output,
- maximum 16 palette entries including transparency as required by the target encoding,
- normal and shiny palette outputs,
- insertable 4bpp graphics,
- target-engine compressed graphics/palette data,
- deterministic manifest and hash chain.

## Reconstruction questions still unresolved

The following are intentionally not yet marked final:

1. exact XY per-member model/texture/animation signatures for the complete archive;
2. exact ORAS per-member model/texture/animation signatures for the complete archive;
3. exact battle-idle animation identifier(s) used by each Pokémon/form;
4. exact canonical frame/timestamp for a static Generation III reconstruction;
5. exact opponent-side battle camera parameters;
6. exact player-side rear battle camera parameters;
7. exact species-relative battle scaling/anchor behavior;
8. which XY source assets are byte-identical to ORAS assets;
9. whether specific forms share geometry but switch only textures/material visibility;
10. full special/tail member inventory after the ordinary species/form blocks.

Until these are resolved, a generated sprite may be useful for preview/research but cannot be labeled final `BATTLE_MASTER_V1`.

## Current conversion classification

Generation VI is classified as:

```text
3D / true-color source
→ evidence-backed canonical battle render
→ semantic palette reconstruction
→ deterministic pixel-art down-conversion
→ 64×64 indexed Generation III target
→ 4bpp / compressed insertion assets
```

This is intentionally different from Generation IV/V `indexed source canvas → preservation-v2 → 64×64`.

## Public technical references

- Project Pokémon, X/Y File System: https://projectpokemon.org/home/docs/gen-6/xy-file-system-r89/
- Project Pokémon, ORAS File System: https://projectpokemon.org/home/docs/gen-6/oras-file-system-r32/
- Project Pokémon, Consolidated Tutorial for X/Y ROM Data Extraction: https://projectpokemon.org/home/forums/topic/36499-consolidated-tutorial-for-xy-rom-data-extraction/
- Project Pokémon, Listing the Pokémon models extracted from ORAS: https://projectpokemon.org/home/forums/topic/34387-listing-the-pokemon-models-extracted-from-oras/
- Public XY model-range list / RomFS notes: https://seatgem.com/2021/12/pokemon-x-and-y-romfs-a-folder-content-notes.html
- Ohana3DS Rebirth: https://github.com/gdkchan/Ohana3DS-Rebirth
- Nintendo 3DS GFModel/GFTexture/GFMotion importer: https://github.com/sxrmss/n3ds_importer
- pret/pokeemerald target reference: https://github.com/pret/pokeemerald

## Next inventory milestone

Build a complete XY and ORAS source-member ledger with one row per archive member and a second logical table mapping every species/form/gender state to those members. Do not begin global final-sprite approval until that ledger can distinguish model, normal texture, shiny texture, animation/material/visibility data, auxiliary members, aliases, and unresolved members without silent gaps.
