# RBY title passing Pokémon — frame-level analysis

## Confirmed directly in the uploaded Japanese ROMs

### Red / Green legacy branch
- The core scrolling routine at file `0x48F3–0x491A` is byte-for-byte identical in:
  - Japanese Red Rev 0
  - Japanese Red Rev A
  - Japanese Green Rev 0
  - Japanese Green Rev A
- Pokémon front-sprite tilemap anchor: `(9,10)` = X 72 px.
- Trainer OAM origin: hardware `(Y=$60, X=$30)` = visible `(40,80)`.
- Candidate table: file `0x49C1`.
- Wait: 255 frames.
- Outgoing motion: 20 raster-synchronized frames, `SCX = 0,8,16,...,152`.
- Incoming motion: 12 raster-synchronized frames, `SCX = 160,168,...,248`.
- New front sprite upload: fixed 49-tile 2bpp buffer, copied 8 tiles/VBlank → **7 explicit VBlank frames**.
- Tilemap transfer before selecting/loading the next Pokémon: **3 frames**.
- Minimum fixed/synchronized cycle: **297 frames ≈ 4.973 s**, plus unsynchronized CPU decompression/RNG time.

### Blue revised branch
- Japanese Blue contains the easing tables at file `0x37244`.
- Those tables and the raster scroll core through `0x372AB` are byte-identical to the supplied English Red and Blue ROMs.
- Pokémon tilemap anchor: `(5,10)` = X 40 px.
- Trainer OAM origin: hardware `(Y=$60, X=$5A)` = visible `(82,80)`.
- Candidate table: file `0x4592`.
- Wait: 200 frames.
- Outgoing motion: 18 frames with increasing speed.
- One extra input-check frame follows the outgoing motion.
- If the outgoing Pokémon is Bulbasaur, Charmander, or Squirtle, a **10-frame Poké Ball arc** runs.
- Incoming motion: 17 frames with decreasing speed.
- Tilemap transfer: 3 frames.
- Front-sprite VRAM upload: 7 frames.
- Minimum non-starter cycle: **246 frames ≈ 4.119 s** + CPU work.
- Minimum starter cycle: **256 frames ≈ 4.286 s** + CPU work.

## Exact Blue easing

Outgoing SCX:
`0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 50, 58, 66, 75, 84`

Incoming SCX:
`136, 146, 156, 165, 174, 183, 192, 200, 208, 216, 224, 230, 236, 242, 247, 252, 255`

The new Pokémon therefore enters quickly and decelerates as it reaches its resting position.

## Poké Ball arc in Japanese Blue

The 10 hardware OAM Y values are:
`$71, $6F, $6E, $6D, $6C, $6D, $6E, $6F, $71, $74`

After the Game Boy OAM Y bias of 16 px, the visible Y positions are:
`97, 95, 94, 93, 92, 93, 94, 95, 97, 100`

The ball rises from Y 97 to Y 92 and then drops to Y 100.

## Do all 16 Pokémon have different movement?

No. The movement code is species-independent.

Every front sprite is decompressed and centered inside a fixed **7×7 tile** buffer. The actual source artwork can be 5×5, 6×6, or 7×7 tiles. That changes the visible footprint by a few pixels/one animation frame, but the SCX trajectory is the same for all 16 candidates.

See `rby_title_passing_pokemon_candidate_frame_matrix.csv` for every species, source size, and first/last visible frame.

## Random selection

The engine takes the low nibble of the RNG (`0..15`) and indexes the 16-entry version-specific table. If the result equals the Pokémon already displayed, it retries.

Assuming the RNG low nibble is uniform, each of the other 15 candidates has probability **1/15** on the next transition. Immediate repeats cannot occur.
