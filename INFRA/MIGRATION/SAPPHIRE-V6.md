# Sapphire v6 migration

Canonical source root: `LIBRARY/GEN-03/SAPPHIRE/SOURCE/GBA/CART/`.

Canonical same-game comparison root: `LIBRARY/GEN-03/SAPPHIRE/COMPARE/`.

Canonical ROM-set registry: `INFRA/REGISTRIES/ROM-SETS/SAPPHIRE/source-set.tsv`.

Identity migration: legacy `<GAME-CODE>-R<HEADER-VERSION>` → `<GAME-CODE>-HV<HEADER-VERSION>` and `PROJECT-<SHA1-8>` → `UPLOAD-<SHA1-8>`. Hashes and source bytes are unchanged. The old v4 material remains in `LEGACY/PRE-V6-2026-09-12/` only as migration quarantine/history until cross-project references have been retired.

No original ROM binaries are committed.
