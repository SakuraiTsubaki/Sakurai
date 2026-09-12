# Emerald v3 -> v4 migration

The v3 `GAMES/GEN-03/EMERALD` tree is superseded by the repository-wide v4 identity model.

- v3 release IDs such as `GBA-JP-JA-BPEJ-REV-0` become native GBA release IDs such as `BPEJ-R0`.
- Exact supplied ROM images are represented below `DUMPS/PROJECT-<sha1-prefix>`; duplicate filenames with identical bytes share one dump identity.
- Release facts and exact dump observations live under `LIBRARY/GEN-03/GBA/EMERALD`.
- Multi-release bank/disassembly research lives under `COMPARISONS/REV0-LOCALIZATION-SET`.
- Generic GBA census tooling moves to `INFRA/TOOLS/GBA`.
- No ROM binaries are committed.
