# 0722 Rowlet — canonical battle-source gate

Status: **source identity partially verified; final Gen III front/back reconstruction blocked pending exact battle-source mapping.**

## Identity

- National Dex: 0722
- English: Rowlet
- Japanese: モクロー
- Generation VII source family: Nintendo 3DS Alola titles
- Required target roles: front/back, normal/shiny; gender alias/difference state must be verified rather than assumed

## Game archive family

### Sun / Moon

- Pokémon model GARC: `romfs/a/0/9/3`
- exact Rowlet group/member: `TBD`

### Ultra Sun / Ultra Moon

- Pokémon model GARC: `romfs/a/0/9/4`
- exact Rowlet group/member: `TBD`

Do not infer the exact GARC member from an external exporter filename.

## Preserved model-package evidence

A public Sun/Moon preservation extraction at The Models Resource identifies a Rowlet package with:

- `Rowlet.FBX`
- `Rowlet.SMD`
- `Rowlet_OpenCollada.DAE`
- multiple body/eye SMD parts
- normal and shiny texture directories
- texture names in the `pm0841_00_*` family, including body, eye, normal-map/ID-related files.

Reference:

- https://models.spriters-resource.com/3ds/pokemonsunmoon/asset/301376/

This proves that a preserved Rowlet model/texture extraction exists and provides a useful derivative identifier family (`pm0841_00`). It does **not** by itself prove that `0841` is the exact SM/USUM GARC member number. The project therefore records:

- derivative/export identifier: `pm0841_00`
- canonical archive member: `TBD`

instead of conflating them.

## Normal / shiny

The preserved Rowlet extraction contains distinct normal and shiny texture sets. Exact game-primary source members for those texture sets remain `TBD` until the GARC package is inventoried or an exact provenance-preserving extraction map is found.

Current external USUM visual cross-check assets are committed in Tsubaki batch 0001:

- normal: `derived/generation-07/battle-master-v1/source-png/usum-pokeapi-external-crosscheck/batch-0001/normal/0722-rowlet.png`
- shiny: `derived/generation-07/battle-master-v1/source-png/usum-pokeapi-external-crosscheck/batch-0001/shiny/0722-rowlet.png`

They are 128x128 visual evidence only, not the canonical battle source.

## Battle pose / motion

Sun/Moon-era developer commentary explicitly emphasizes Pokémon motion as a design focus and cites Rowlet's head-turning behavior. This reinforces that the animation state is part of the source identity and should not be replaced by an arbitrary static model pose.

Reference:

- https://nintendoeverything.com/pokemon-sunmoon-devs-on-more-expressive-characters-inspiration-behind-z-moves-theme-and-more/

Exact battle animation group/member: `TBD`

Exact canonical idle animation: `TBD`

Exact deterministic frame/phase rule: `TBD`

## Battle camera / orientation

Contemporary Sun/Moon gameplay coverage documents dynamic battle camera behavior and persistent trainer visibility. Therefore an arbitrary screenshot angle or generic model-viewer front view is not accepted as the final canonical front/back orientation.

References:

- https://www.shacknews.com/article/95297/e3-2016-pokemon-sun-and-moon-additional-details-revealed
- https://twinfinite.net/news/pokemon-sun-moon-alola-ui/

Required unresolved fields:

- front battle orientation: `TBD`
- back battle orientation: `TBD`
- battle anchor / ground contact: `TBD`
- camera target: `TBD`
- projection / FOV: `TBD`
- battle-scale behavior: `TBD`

## Material / texture fidelity

The preserved extraction exposes separate body/eye textures and normal/ID-related texture files. A flat diffuse-only render is therefore insufficient unless validated to reproduce the in-game appearance.

Required unresolved fields:

- material definitions: `TBD`
- alpha behavior: `TBD`
- vertex colors: `TBD`
- UV transforms: `TBD`
- normal-map role: `TBD`
- ID/mask texture role: `TBD`
- lighting/rim/shader behavior used in battle: `TBD`

## Canonical-source priority for Rowlet

1. exact SM/USUM game model + textures/materials + battle animation + battle orientation/camera/anchor;
2. game-internal static/Pokédex render for front-view validation;
3. provenance-preserving extracted package tied to exact GARC members;
4. preserved model package such as the `pm0841_00` extraction for structural/visual cross-checking;
5. pinned PokeAPI 128x128 render for visual regression cross-checking.

## Gen III conversion gate

No Rowlet sprite may be labelled final `BATTLE_MASTER_V1` until all of the following are resolved:

- [ ] exact SM and/or USUM model group/member provenance
- [ ] normal texture member mapping
- [ ] shiny texture member mapping
- [ ] battle animation mapping
- [ ] deterministic canonical idle pose/frame rule
- [ ] canonical front orientation
- [ ] canonical back orientation
- [ ] battle anchor/scale rule
- [ ] material/alpha/shader treatment
- [ ] source render generated and hashed
- [ ] source-vs-game/reference visual validation
- [ ] 64x64 reconstruction
- [ ] Gen III <=16-color palette accepted by visual review
- [ ] 4bpp packing
- [ ] Gen III compression
- [ ] all required hashes/manifests/dedup/logical-slot relationships

Until then, any Rowlet 64x64 image is a prototype only and must not be stored as an accepted final asset.
