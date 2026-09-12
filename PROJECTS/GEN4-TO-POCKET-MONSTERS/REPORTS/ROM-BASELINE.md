# Generation IV → ポケットモンスター — ROM baseline

- Sources locked: 5
- Targets locked: 5
- Original ROM binaries committed: **no**
- Identity model: repository v4 (`RELEASE` != `DUMP`)

## Sources

- `DIAMOND` → `ADAE-R5` / `LGC-a46233d8` / `a46233d8b79a69ea87aa295a0efad5237d02841e`
- `PEARL` → `APAE-R5` / `LGC-99083bf1` / `99083bf15ec7c6b81b4ba241ee10abd9e80999ac`
- `PLATINUM` → `CPUK-R0` / `UPLOAD-f811d9c7` / `f811d9c7ab5262f593012da794c2fa81dbcdbcc1`
- `HEARTGOLD` → `IPKK-R0` / `UPLOAD-5834fb3a` / `5834fb3a2d751c48501d47d6a56898d7af6ccf9e`
- `SOULSILVER` → `IPGK-R0` / `UPLOAD-0330e644` / `0330e6449306606114a92bdbb3f9d3d51d392b96`

## Targets

- `RUBY` → `AXVJ-R0` / `UPLOAD-5c5e5467` / `5c5e546720300b99ae45d2aa35c646c8b8ff5c56`
- `SAPPHIRE` → `AXPJ-R0` / `UPLOAD-3233342c` / `3233342c2f3087e6ffe6c1791cd5867db07df842`
- `EMERALD` → `BPEJ-R0` / `UPLOAD-d7cf8f15` / `d7cf8f156ba9c455d164e1ea780a6bf1945465c2`
- `FIRERED` → `BPRJ-R1` / `UPLOAD-7c7107b8` / `7c7107b87c3ccf6e3dbceb9cf80ceeffb25a1857`
- `LEAFGREEN` → `BPGJ-R0` / `UPLOAD-5946f1b5` / `5946f1b59e8d71cc61249661464d864185c92a5f`

## Extraction scope

- NDS: header, FAT/FNT-derived NitroFS file inventory, NARC catalog, per-file SHA-1.
- GBA: header/checksum identity and mechanical long `00`/`FF` run census.
- GBA padding runs are allocation candidates only, never automatically treated as safe free space.
- Tsubaki receives production-facing asset source indexes and target build baselines; wholesale ROM/NitroFS dumps are intentionally excluded.
