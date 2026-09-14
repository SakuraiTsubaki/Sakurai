# Early sprite verification

This directory stores per-target SHA-256 fingerprints for the first 21 mapped `sprite.c` functions, from `ResetSpriteData` through `CalcCenterToCornerVec`.

Each CSV records the target ID, layout family, function name, runtime address, byte size, and SHA-256 of the exact retail function range. The files are generated from local read-only reference ROMs; no ROM bytes are committed.

Targets covered:

- `JPN-AXPJ-v0.csv`
- `USA-AXPE-v0.csv`
- `EUR-AXPE-v1.csv`
- `USA-EUR-AXPE-v2.csv`
- `DEU-AXPD-v1.csv`
- `FRA-AXPF-v0.csv`
- `FRA-AXPF-v1.csv`
- `ITA-AXPI-v0.csv`
- `ITA-AXPI-v1.csv`

Confirmed whole-block revision equivalence:

- `EUR-AXPE-v1` = `USA-EUR-AXPE-v2`
- `FRA-AXPF-v0` = `FRA-AXPF-v1`
- `ITA-AXPI-v0` = `ITA-AXPI-v1`

Run `make analyze-early-sprite ROM=/path/to/reference.gba` to regenerate fingerprints for one local reference ROM. Exact addresses and sizes are defined in `config/early_sprite.yml`.
