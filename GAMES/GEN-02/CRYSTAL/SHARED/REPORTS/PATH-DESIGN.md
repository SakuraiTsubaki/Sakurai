# Pokémon Crystal — v3 path design

This design is derived from the seven verified Crystal source ROM builds currently supplied to the project.

## Canonical release IDs

- `GBC-JP-JA-BXTJ-REV-0`
- `GBC-US-EU-EN-BYTE-REV-0`
- `GBC-US-EU-EN-BYTE-REV-A`
- `GBC-EU-DE-BYTD-REV-0`
- `GBC-EU-FR-BYTF-REV-0`
- `GBC-EU-IT-BYTI-REV-0`
- `GBC-EU-ES-BYTS-REV-0`

Each ID represents exactly one official ROM build. Region, language, header code, revision, hashes, and cartridge metadata are recorded in `MANIFESTS/release.json` rather than split into additional ownership levels.

## Canonical Crystal tree

```text
GAMES/GEN-02/CRYSTAL/
  RELEASES/
    GBC-JP-JA-BXTJ-REV-0/
    GBC-US-EU-EN-BYTE-REV-0/
    GBC-US-EU-EN-BYTE-REV-A/
    GBC-EU-DE-BYTD-REV-0/
    GBC-EU-FR-BYTF-REV-0/
    GBC-EU-IT-BYTI-REV-0/
    GBC-EU-ES-BYTS-REV-0/
  COMPARISONS/
    RELEASE-MATRIX/
  PROJECTS/
    LOCALIZATION-KO/
      COMMON/
      TARGETS/
        GBC-KR-KO/
  SHARED/
```

## Legacy routing

- `GENERATION-II/CRYSTAL/KR-KO/REV-0/...` → `GAMES/GEN-02/CRYSTAL/PROJECTS/LOCALIZATION-KO/TARGETS/GBC-KR-KO/...`
- `GENERATION-II/CRYSTAL/MULTI/REV-ALL/ANALYSIS/REV-COMPARISON/...` → `GAMES/GEN-02/CRYSTAL/COMPARISONS/RELEASE-MATRIX/ANALYSIS/ROM-RELEASE-COMPARISON/...`
- `GENERATION-II/CRYSTAL/MULTI/REV-ALL/TOOLS/REV-COMPARISON/...` → `GAMES/GEN-02/CRYSTAL/COMPARISONS/RELEASE-MATRIX/TOOLS/ROM-RELEASE-COMPARISON/...`
- Tsubaki Japanese Rev 0 patch assets → `RELEASES/GBC-JP-JA-BXTJ-REV-0/PATCHES/...`
- Tsubaki English header-version-1 patch assets → `RELEASES/GBC-US-EU-EN-BYTE-REV-A/PATCHES/...`

`REV-A` is the canonical human revision label for the English build whose Game Boy header version byte is `1`; the old `REV-1` path is removed.

## Provenance correction

No official Korean Crystal ROM is present in the supplied source set. Existing Korean Crystal material is explicitly derived from Japanese Crystal Rev 0, with Korean Gold/Silver assets used as official localization references. It is therefore project-owned, not a source release.

Original ROM binaries remain local, read-only, and outside GitHub. Git stores only manifests, analysis, source, assets, patches, and other distributable project artifacts.
