# Validation requirements

An accepted BW → Generation III battle-sprite batch must pass all of these checks.

## Source

- source provenance exists
- source archive/member exists in manifest
- stored and decoded source hashes exist
- native canvas and palette relationship are recorded
- empty/alias/female/form state is explicit

## Conversion

- full native canvas mapped to full 64×64 canvas
- source palette indices retained for indexed source
- no RGB interpolation, antialiasing, or generated colors
- rare-index preservation enabled under the fixed algorithm/configuration
- 50% silhouette protection enabled

## Visual review

- silhouette recognizable and source-faithful
- head/face/eyes preserved
- limbs/wings/tail preserved
- markings and species-defining accent colors preserved
- no unintended crop or species-specific artificial enlargement

## Generation III output

- final PNG exists
- palette exists and passes target constraints
- raw 4bpp exists and decodes to the final indexed pixels
- compressed graphics exists and round-trips to the raw 4bpp bytes
- all SHA-256 values match the manifest

## Canonical/dedup

- rendered-pixel SHA-256 resolves to one canonical asset
- every logical slot resolves to a canonical asset
- zero logical references are lost during deduplication

## Reproducibility

- script/configuration used by the batch is recorded
- source + configuration reproduces the same target indices
- reconstructed final binary hashes match the published Tsubaki files

A batch failing any mandatory check remains provisional/incomplete and is not promoted to the canonical master.
