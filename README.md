# Sakurai

Pokémon ROM research, release/dump identity, reverse engineering, comparison, crosswalk, design, and verification repository.

## Canonical path model: v6

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/...
PROJECTS/GEN-XX/<PROJECT-ID>/...
PROJECTS/CROSS-GEN/<PROJECT-ID>/...
INFRA/...
LEGACY/PRE-V6-2026-09-12/...
```

`RELEASE` is the official build identity. `DUMP` is one exact observed image under that release. Human market/language labels do not replace stronger platform-native build identity.

The paired `Tsubaki` repository uses the same generation/game/platform/package/release/dump/project/target identities while owning production assets, conversions, patches, build inputs, and generated implementation resources.

`LEGACY` is read-only migration quarantine. New work must use `LIBRARY`, generation-scoped `PROJECTS`, or `INFRA`.

Original ROM/executable binaries are never committed.
