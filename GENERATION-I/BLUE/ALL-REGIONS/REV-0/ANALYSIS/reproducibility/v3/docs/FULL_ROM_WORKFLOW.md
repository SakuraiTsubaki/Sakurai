# Full-ROM workflow

The corpus is deliberately layered so later semantic discoveries never invalidate the physical reconstruction baseline.

## Layer 0 — identity
Match each local ROM by cryptographic hash. Reject unexpected inputs.

## Layer 1 — physical reconstruction
Treat every ROM as ordered 16 KiB banks. Each bank is covered by stable 0x100-byte `INCBIN` work chunks. This is the lossless fallback representation.

## Layer 2 — structural survey
Regenerate bank hashes, entropy, fill runs, pointer-shaped values, pointer-table candidates, text-like candidates, tile-unit statistics, and cross-version exact-byte alignment.

## Layer 3 — semantic promotion
Promote a raw chunk to a real extractor/source module only when its format is understood: GBZ80 code; character maps/text pointers; Pokémon/move/item/trainer tables; Pokédex; maps/events; pictures/font/tiles; tilesets; audio; SGB data.

## Layer 4 — lossless reassembly
Every semantic module must provide an inverse encoder/reinserter. Accept it only when the generated ROM matches the original SHA-256 exactly.

## Layer 5 — editable derivative work
Only after Layer 4 succeeds does that area become safe for modification. Raw source ROM bytes never need to enter version control.
