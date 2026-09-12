# GBA release identity — v4.1 clarification

Canonical GBA retail release IDs use `<GAME-CODE>-R<HEADER-VERSION>`.

When two materially distinct official/development builds share the same GBA game code and header version, the non-retail build MUST append a stable build-kind qualifier: `<GAME-CODE>-R<HEADER-VERSION>-<BUILD-KIND>`. Example: Pokémon Ruby German retail `AXVD-R0` and German debug `AXVD-R0-DEBUG`.

Allowed build-kind qualifiers are factual, uppercase machine slugs such as `DEBUG`, `PROTO`, `DEMO`, or `KIOSK`; never invent a qualifier to encode ordinary locale data already represented by the native game code. Every release manifest MUST carry `build_kind` even when the retail path omits `-RETAIL`.

Exact observed files remain separate dump identities under `DUMPS/<PROVENANCE>-<SHA1-PREFIX>/` or the established project provenance slug. ROM binaries are never committed.
