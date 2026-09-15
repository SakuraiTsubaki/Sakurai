# Generation VIII → Generation III Battle Master — Logical Slot Schema

## Purpose

This schema keeps **logical battle roles** separate from physical/canonical assets.

A logical role must never disappear merely because its final rendered pixels deduplicate to another role. Physical output files may be globally deduplicated by SHA-256; logical identities remain complete in the manifest.

The schema also separates a Pokémon's actual form/model identity from temporary battle/world presentation states such as Dynamax or Alpha scaling.

## Primary logical key

Every candidate static battle role is identified by the tuple:

```text
source_generation
source_game
source_version
source_region
source_language
source_revision_or_update
species
form
model_variant
gender
shiny_state
battle_side
visual_state
pose_contract
static_frame_selector
```

### Required meanings

- `source_generation`: fixed to `8` for this master.
- `source_game`: one of `SWORD`, `SHIELD`, `BRILLIANT_DIAMOND`, `SHINING_PEARL`, `LEGENDS_ARCEUS`.
- `source_version`: retail/base/update version when known.
- `source_region`, `source_language`: retained even when the graphics prove shared.
- `source_revision_or_update`: exact patch/build identity where known; otherwise explicit `UNKNOWN`.
- `species`: canonical species identity / National Pokédex number.
- `form`: game data form identity. Do not infer from appearance alone.
- `model_variant`: resource-level variant index/name when the game's resource organization distinguishes models beyond the semantic form label.
- `gender`: logical gender/model state. Use `SHARED` only after equivalence/aliasing is verified.
- `shiny_state`: `NORMAL` or `SHINY`; resource representation may be texture/material-only rather than mesh-distinct.
- `battle_side`: `FRONT` (opponent-side presentation) or `BACK` (player-side presentation) for the Generation III target.
- `visual_state`: temporary or presentation-specific state that is not automatically a species form, e.g. `NORMAL`, `DYNAMAX`, `ALPHA`, or another verified state.
- `pose_contract`: identifier for the deterministic battle pose / animation semantic selected for static reconstruction.
- `static_frame_selector`: deterministic time/frame/sample within that pose contract.

## Source-resource identity

Every logical role must point to a source-resource record containing, where applicable:

```text
resource_table
resource_entry
archive_path
archive_member
model_path
mesh_path
skeleton_path
material_path
texture_paths
animation_path
config_path
effect_paths
battle_rig_path
battle_script_path
camera_source
scale_source
anchor_source
source_sha256
```

Unknown fields remain explicit `UNKNOWN`; they are never synthesized.

## Three identity layers

### Layer 1 — semantic Pokémon identity

Species, form, gender, shiny state and game/version identity.

### Layer 2 — presentation state

Battle side, pose, animation phase, Dynamax/Alpha/other battle state, camera, scale and anchor.

### Layer 3 — canonical physical output

Final rendered-pixel SHA-256 and the canonical PNG/palette/4bpp/compressed asset selected after deduplication.

These layers must not be conflated.

## Form vs state rules

### Sword / Shield

- Gigantamax forms are distinct visual/model identities and receive distinct form/model logical records where supported by game data.
- Dynamax is recorded as a presentation/battle state unless game data proves a distinct model asset relationship that needs separate resource identity.
- DLC presence/re-enablement is a version/update availability property, not silently a new form.

### Brilliant Diamond / Shining Pearl

- Resource variant indices after the Pokédex number are preserved exactly as resource identifiers.
- Semantic interpretation as form or gender is recorded only when verified by game data/documentation.
- Normal/shiny texture variants remain separate logical shiny states even if geometry is shared.
- `battle` and `field` resources are separate source roles; the battle master uses battle semantics and does not substitute the field/chibi presentation.

### Pokémon LEGENDS: Arceus

- `Species`, `Form` and `Gender` from the Pokémon resource table are first-class semantic keys.
- `ArceusType` is recorded independently when present rather than being discarded.
- Alpha size/status is a presentation/world/battle state unless a separate semantic model resource identity is proven.
- normal/rare (shiny) material relationships are retained independently from geometry.

## Front / back rule for native 3D sources

Generation VIII does not supply native Generation III-style 2D front/back sprite pairs.

Therefore:

- `FRONT` is a deterministic 2D reconstruction of the canonical battle source under opponent-side battle semantics.
- `BACK` is a deterministic 2D reconstruction of the canonical battle source under player-side battle semantics.
- `BACK` must not be produced by merely mirroring an already flattened `FRONT` image.
- both sides point back to the same verified model/material/animation identity unless the game actually uses different resources.

## Static vs animation track

The static insertion master and full animation preservation remain separate:

```text
STATIC_MASTER
ANIMATION_MASTER
```

The static master records one deterministic, documented semantic pose/frame per logical role.

The animation master retains original animation resources, names, timelines/tracks and transforms where available. The chosen static pose must reference this preserved animation evidence rather than deleting it.

## Reconstruction-source record

Before 64×64 conversion, each logical role gets an immediate 2D reconstruction record:

```text
render_width
render_height
projection
camera_transform
model_transform
world_scale
anchor
animation_name
animation_time
lighting_contract
background_alpha
render_engine_and_version
render_script_sha256
reconstructed_source_png_sha256
```

This reconstructed image is an **intermediate derived source**. It must never be labeled as an original in-game 2D battle sprite.

## Generation III output record

Every accepted role must resolve to:

```text
final_png
final_png_sha256
rendered_pixel_sha256
target_palette
target_palette_sha256
target_4bpp
target_4bpp_sha256
compressed_graphics
compressed_graphics_sha256
canonical_asset_id
manual_correction_id_or_NONE
validation_status
```

## Deduplication

Deduplication is performed on the exact final rendered pixel result (and tracked separately for palette/binary identity where useful).

If two or more logical roles are identical:

```text
logical roles N -> canonical physical asset 1
```

All N logical roles stay in the manifest.

No semantic role, source game identity, form, gender slot, shiny state, version identity or presentation state is deleted merely because the physical image is shared.

## Completion gate

A logical role is `FINAL` only when source provenance, reconstructed source, 64×64 PNG, palette, 4bpp, compressed binary, hash chain, canonical/dedup relationship and validation all exist.

Allowed pre-final states include:

- `INVENTORIED`
- `SOURCE_MAPPED`
- `SOURCE_VERIFIED`
- `POSE_PENDING`
- `RENDERED_PROVISIONAL`
- `PALETTE_PENDING`
- `VALIDATION_PENDING`
- `FINAL`

Missing ROM/game files may keep evidence at a lower tier but do not stop the inventory/research pipeline.
