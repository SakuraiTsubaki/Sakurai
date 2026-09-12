# Pokémon Yellow source routing — Repository Structure v6

Canonical source truth is `LIBRARY/GEN-01/YELLOW/`.

The four Japanese Pocket Monsters Pikachu revisions have CGB flag `0x00` and are routed under `SOURCE/GB/CART/`. The five international Yellow releases have CGB flag `0x80` and are routed under `SOURCE/GBC/CART/`.

Exact observed images use `USER-UPLOAD-<SHA1-8>` dump IDs beneath the owning release. The 14 supplied filenames collapse to 9 byte-unique dumps; identical `.gb`/`.gbc` filename variants are aliases, not separate releases.

Same-game multi-release research belongs in `COMPARE/SOURCE-SET-2026-09-12/`. Release-independent Yellow parsers/tools belong in `SHARED/`. Transformation-specific work belongs in `PROJECTS/GEN-01/YELLOW-MODERNIZATION/`.

No official Korean Yellow source release is fabricated. Original ROM binaries remain read-only locally and are never committed.
