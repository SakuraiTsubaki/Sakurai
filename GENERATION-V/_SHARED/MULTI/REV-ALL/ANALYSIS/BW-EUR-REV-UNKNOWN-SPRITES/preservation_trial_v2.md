# BW sprite preservation downscale v2

Source: reconstructed battle idle frame 0 from the uploaded Pokémon Black (EUR) ROM, NARC `/a/0/0/4`.

Targets in this trial:
- Generation III-style: 64×64, 4bpp-style palette budget, 5-bit-per-channel color rounding, silhouette/outline stabilization.
- Generation II-style: 56×56, 2bpp-style four-color reinterpretation (white/background + two species tones + black), independent direct conversion from the 96×96 BW source.

Important rules:
- No generative image model is used.
- No chained 96→64→56 resize. Both targets are produced directly from the 96×96 source.
- Nearest-neighbor-only reduction is not accepted as a finished asset.
- Gen III v2 restores tiny rare palette accents where possible while keeping the target palette budget.
- Gen II v2 intentionally reduces color information because the target graphics format has a much smaller palette; species-defining colors are prioritized when they occupy a meaningful part of the source.
- v2 is an automatic structural draft. Final insertion-quality sprites still require per-species one-pixel review, especially eyes, claws, horns, feather tips, tail edges, and ground contact.

Cross-check references:
- pret/pokecrystal build rules: Pokémon front sprites are generated as 2bpp assets from PNG + GBC palette data; large front source strips are 56 px wide.
- pret/pokeemerald graphics workflow: battle Pokémon front assets are 64×64 indexed graphics with a limited palette; project documentation recommends 14 editable colors for new species artwork.
