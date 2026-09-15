# Canonical deduplication rule

Use SHA-256 of the final rendered pixel result as the global visual deduplication key.

When different logical roles render identically, store one canonical asset. Preserve every source game/version/region/revision/species/form/gender/frame/palette logical reference and point it to that canonical asset.

Deduplication removes duplicate bytes, not provenance or logical relationships.
