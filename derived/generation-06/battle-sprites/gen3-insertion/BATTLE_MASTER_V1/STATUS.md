# Generation VI → Generation III BATTLE_MASTER_V1 status

## Current phase

**Phase 1 — source census, logical visual-state inventory, and secondary PNG evidence collection.**

The final 64×64 Generation III battle sprites are **not yet approved or generated as final assets**. Current work establishes the source/provenance and reconstruction framework required before final rasterization.

## Completed

### Master contract

- [x] Generation III insertion requirements fixed.
- [x] Generation VI classified as 3D/true-color source, not native 2D battle-sprite source.
- [x] No AI/generative redraw, antialiasing, bilinear/bicubic interpolation, or automatic frequency-only 16-color reduction allowed.
- [x] Mandatory PNG/palette/4bpp/compressed/manifest/hash/validation outputs defined.
- [x] Sakurai/Tsubaki repository roles defined.

Primary document: `README.md`

### Archive baseline

- [x] XY Pokémon model archive recorded: `a/0/0/7`.
- [x] ORAS Pokémon model archive recorded: `a/0/0/8`.
- [x] XY/ORAS retained as separate game identities.
- [x] ORAS reported eight-member model/texture/animation block pattern recorded without promoting it to game-verified status.

Files:

- `SOURCE_BASELINE.md`
- `source_archives.csv`
- `source-ledgers/oras_member_pattern_public.csv`

### XY Generation VI new-species public member ledger

- [x] Public No.650–721 model-range segment transcribed.
- [x] Member span `6868–7851` represented as 123 contiguous eight-member blocks.
- [x] Total represented archive members: 984.
- [x] Four missing public labels around Pumpkaboo/Gourgeist preserved explicitly as unresolved rather than guessed.
- [x] Deterministic structural validator added.
- [x] Structural validation recorded as PASS without claiming retail-ROM verification.

Files:

- `source-ledgers/xy_model_ranges_public_gen6.csv`
- `tools/validate_xy_model_range_ledger.py`
- `validation/xy_model_ranges_public_gen6.md`

### No.650–721 Generation VI logical visual states

- [x] 72 species enumerated.
- [x] 125 logical Generation VI visual states defined.
- [x] 124 states marked as requiring Generation III battle targets.
- [x] Xerneas Neutral Mode retained as source/provenance-only state; Active Mode is the battle target.
- [x] Mega Diancie and Hoopa Unbound separated as ORAS-only Generation VI states.
- [x] Eternal Flower Floette retained as Generation VI data-defined but then-unobtainable state.
- [x] Later-generation forms/naming prevented from contaminating the Generation VI inventory.
- [x] Generated CSV committed automatically through GitHub Actions.

Files:

- `tools/build_gen6_650_721_logical_states.py`
- `logical_visual_states_gen6_650_721.csv`
- `validation/logical_visual_states_gen6_650_721.md`
- `LATER_GENERATION_EXCLUSIONS.md`

### Provenance / output schema

- [x] Manifest schema created for source identity, archive/member data, model/textures, animation, camera/pose, palette reconstruction, final 64×64 target, hashes, manual corrections, deduplication, and verification level.

File:

- `manifest.schema.json`

### Canonical-render evidence hierarchy

- [x] Direct game-native model reconstruction established as Tier A.
- [x] Verified in-game captures established as Tier B.
- [x] Pokémon Showdown XY animated front/back captures classified as derivative Tier C evidence rather than native sprites.
- [x] PokeAPI version PNGs classified as secondary/provisional visual evidence.
- [x] Front and back targets required to be reconstructed/validated independently; no front mirroring shortcut.

Files:

- `CANONICAL_RENDER_EVIDENCE.md`
- `SECONDARY_PNG_POLICY.md`

### Existing upstream PNG audit

- [x] Existing Chespin PNG in X/Y/ORAS/AS decompilation repositories audited.
- [x] Existing public PokeAPI provenance retained.
- [x] Existing PNGs explicitly prevented from being mislabeled as native Generation VI battle sprites.

File:

- `source-ledgers/upstream_existing_png_audit.csv`

### First small PNG evidence batch

- [x] XY No.650–659 collected as a small reviewable batch.
- [x] Default and shiny public PNGs collected where available.
- [x] Female / shiny-female paths checked and missing states recorded explicitly instead of ignored.
- [x] PNG byte size, width, height, SHA-256, URL, destination, collection time, and evidence class recorded.
- [x] Actual PNG binary files committed through GitHub Actions rather than falsely claiming a text-only connector uploaded them.

Files:

- `tools/fetch_secondary_pokeapi_pngs.py`
- `.github/workflows/fetch-gen6-secondary-png-batch-0650-0659.yml`
- `secondary-evidence/pokeapi/x-y/batch-0650-0659/manifest.csv`
- `secondary-evidence/pokeapi/x-y/batch-0650-0659/png/`

### Future direct-extraction readiness

- [x] Deterministic archive-member inventory tool added.
- [x] Tool records member index, path, byte size, SHA-256, compression hint, signature hint, file prefix and unresolved semantic role.
- [x] Tool enforces XY=`a/0/0/7`, ORAS=`a/0/0/8` archive/game pairing.

File:

- `tools/inventory_gen6_model_archive.py`

## Explicit unresolved items

### ORAS exact member-number mapping

**Unresolved.**

The contemporary `mradocy/pokemonModelList` repository linked by the original research thread has been reported deleted. No exact ORAS species/form member table is fabricated from arithmetic or later-generation indices.

See `ORAS_MEMBER_MAPPING_RECOVERY.md`.

### Member-level XY role mapping

The public eight-member ranges are recorded, but the exact signature/semantic role of every offset still requires stronger evidence.

### Canonical battle pose

Exact XY/ORAS battle-idle motion IDs and timestamps are not yet finalized.

### Canonical cameras

Exact opponent-side and player-side battle camera/projection parameters are not yet finalized.

### Relative species scale / anchor

A common render convention that reproduces XY/ORAS relative battle scale and placement still requires game-backed verification.

### Final Generation III palette reconstruction

Not started globally. It must be based on source-supported semantic color roles per visual state, not a generic most-frequent-color quantizer.

### Final 64×64 / 4bpp / compressed assets

Not yet approved. Tsubaki production output begins only after the canonical-source/render requirements are satisfied for the relevant batch.

## Next execution order

1. Continue secondary PNG evidence in small numbered batches without confusing it with the master source.
2. Recover/verify XY member roles and ORAS member-number mappings from surviving public reverse-engineering evidence.
3. Inventory front/back battle-presentation evidence and form-specific camera/pose behavior.
4. Establish a reproducible canonical render convention.
5. Run the first small canonical reconstruction batch rather than converting all species at once.
6. For each accepted state, generate and retain source render → automatic 64×64 → validated 64×64 → palette → 4bpp → compressed data → complete hash/manifest chain.
7. Store final insertable production assets in Tsubaki only after acceptance checks pass.

## Completion rule

No asset is `BATTLE_MASTER_V1 complete` unless source provenance, canonical rendering evidence, final PNG, Generation III palette, 4bpp, compressed graphics, hash chain, logical/canonical mapping, deduplication, visual comparison, validation, and rebuild metadata all exist and pass.
