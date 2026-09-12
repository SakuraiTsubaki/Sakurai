# Repository Pair Routing v4.1

This specification tightens Repository Structure v4 without changing its canonical roots.

## Identity spine

The stable identity chain is:

`GENERATION -> PLATFORM -> GAME -> RELEASE -> DUMP`

A transformation uses a separate chain:

`PROJECT -> TARGET -> ARTIFACT`

These chains may reference one another but must never be collapsed. Locale, filename, extension, CGB/SGB capability, mapper, preservation-set revision label, and hash are metadata unless they are part of the platform-native release identity defined by `STRUCTURE.md`.

## Sakurai is authoritative for source truth

Sakurai owns official release identity, exact dump observations, hashes, ROM/header facts, reverse engineering, census, disassembly, symbols, text/data research, cross-release comparisons, and verification evidence.

Source-derived factual tables belong in `LIBRARY`. Cross-release work belongs in `COMPARISONS`. Project-specific research/design belongs in `PROJECTS`.

## Tsubaki is authoritative for production truth

Tsubaki owns transformed or project-produced assets, conversion inputs that are appropriate to track, implementation source, build inputs, patches, generated target resources, and production verification.

Tsubaki references Sakurai release identities through project source-lock/release-lock manifests. Mirroring the complete Sakurai research tree into Tsubaki is forbidden.

## No fake releases

A localization, modernization, restoration, port, or fan-produced build is a `PROJECT` target, not an official `RELEASE`. A bad/trimmed/duplicate/renamed dump is a `DUMP`, not another release.

## Canonical pseudo-owner ban

New paths below `LIBRARY` or `PROJECTS` must not use `MULTI`, `REV-ALL`, `ALL-RELEASES`, or `MULTI-REGION` as ownership nodes. Use a named `COMPARISON-ID`, `_SHARED` only where explicitly reserved, or a real project/target ID.

## ROM binary policy

Original ROM/executable binaries are never committed. Hashes, manifests, structural metadata, verification results, patches, tools, and lawful project-produced/converted resources may be tracked according to repository responsibility.