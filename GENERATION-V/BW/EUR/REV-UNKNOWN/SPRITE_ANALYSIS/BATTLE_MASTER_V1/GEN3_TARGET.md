# Generation III target contract

The baseline insertion target for each accepted static Pokémon battle sprite is a 64×64 indexed/4bpp-compatible asset suitable for the Generation III engine.

The package must include the viewable PNG plus the actual target palette, raw 4bpp graphics bytes, and target compressed graphics bytes. The PNG is not a substitute for the binary asset chain.

For an indexed source such as BW, palette/index provenance is preserved through down-conversion rather than regenerated from an RGB render.
