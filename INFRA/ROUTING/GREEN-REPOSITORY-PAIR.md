# GREEN artifact routing

This file defines repository responsibility for the verified Japanese Pokémon Green V1.0/V1.1 ROM pair. Original ROM binaries are never committed.

## Sakurai
Store release/dump identity, hashes, bank maps, reverse engineering, text/data maps, disassembly notes, revision analysis, symbols, and verification evidence.

## Tsubaki
Store production-facing source locks, verified extracted assets, converted assets, deduplication outputs, modernization build inputs, patches, and generated target artifacts.

## Identity spine
- `LIBRARY/GEN-01/GB/GREEN/RELEASES/JP-JA-HV0` = Japanese Green V1.0 / header version 0.
- `LIBRARY/GEN-01/GB/GREEN/RELEASES/JP-JA-HV1` = Japanese Green V1.1 / header version 1 (Rev A).
- Exact uploaded files live as dump observations beneath their releases in Sakurai.
- `PROJECTS/GREEN-MODERNIZATION` consumes both releases and keeps target outputs separate.

## No pseudo-owners
Do not create `REV-ALL`, `MULTI`, `GENERAL`, `MISC`, or locale-only pseudo-releases. Cross-release work belongs to `COMPARISONS`; derived modernization belongs to `PROJECTS`.
