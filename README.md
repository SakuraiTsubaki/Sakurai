# Sakurai

Pokémon ROM research, release/dump identity, reverse engineering, comparison, crosswalk, design, and verification repository.

## Canonical path model: v5

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/...
PROJECTS/<PROJECT-ID>/...
INFRA/...
```

`RELEASE` is the official build identity. `DUMP` is one exact observed image under that release. `HV` means the ROM/header version byte and is not silently equated with preservation-set revision labels.

The paired `Tsubaki` repository uses the same generation/game/platform/package/release/dump/project/target identities but owns production assets, conversion indexes, patches, build inputs, and generated implementation resources.

Legacy `GENERATION-*`, standalone `GEN-*`, `GAMES/`, v4 release paths, `_SHARED`, `MULTI`, `REV-ALL`, and similar pseudo-owner paths are migration inputs only.

Original ROM/executable binaries are never committed.