# Sakurai

Pokémon project analysis, reverse-engineering, census, verification, localization research, and source-ROM provenance repository.

## Canonical hierarchy — Source-ROM Path V2

Every game is split by ownership before work type:

- `SOURCE` — official source builds only
- `TARGET` — derived/localized/modernized outputs
- `COMPARE` — cross-release or cross-revision research
- `SHARED` — release-independent game-wide material

Canonical examples:

`GEN-01/RED/SOURCE/JP-JA/REV-0/MANIFESTS/...`

`GEN-01/RED/TARGET/KR-KO/JP-JA-REV-0/LOCALIZATION/...`

`GEN-02/CRYSTAL/TARGET/KR-KO/US-EU-EN-REV-A/TEXT/...`

A target language is never allowed to masquerade as an official source release. The supplied source set contains Korean Gold and Silver ROMs, but no Korean Crystal source ROM.

See `STRUCTURE.md` for the full V2 grammar and `META/SOURCE-ROM-CATALOG.md` for the verified 23-ROM Generation I/II source inventory.

ROM binaries are never stored here.
