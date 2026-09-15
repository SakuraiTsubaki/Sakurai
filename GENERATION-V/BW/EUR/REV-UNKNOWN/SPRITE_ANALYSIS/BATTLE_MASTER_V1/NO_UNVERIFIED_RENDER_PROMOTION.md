# No unverified render promotion

Intermediate source renders are not canonical merely because their container headers decode successfully.

Tile/layout order, palette association, transparency, orientation, and source-slot identity must be independently validated before a reconstructed PNG may feed preservation-v2 or be published as a source asset.
