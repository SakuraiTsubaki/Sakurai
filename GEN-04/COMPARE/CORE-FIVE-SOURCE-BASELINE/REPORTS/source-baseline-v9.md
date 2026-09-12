# Generation IV core-five source baseline — v9

Observed directly from the five supplied NDS images. ROM binaries are not committed.

| Game | Release | Dump | Locale | Size | SHA-1 | FAT | FNT dirs | Named NitroFS | Named NARC |
|---|---|---|---|---:|---|---:|---:|---:|---:|
| Diamond | `ADAE-HV5` | `LGC-a46233d8` | US-EN | 67,108,864 | `a46233d8b79a69ea87aa295a0efad5237d02841e` | 356 | 69 | 269 | 149 |
| Pearl | `APAE-HV5` | `LGC-99083bf1` | US-EN | 67,108,864 | `99083bf15ec7c6b81b4ba241ee10abd9e80999ac` | 356 | 70 | 269 | 149 |
| Platinum | `CPUK-HV0` | `UPLOAD-f811d9c7` | KR-KO | 134,217,728 | `f811d9c7ab5262f593012da794c2fa81dbcdbcc1` | 461 | 105 | 339 | 215 |
| HeartGold | `IPKK-HV0` | `UPLOAD-5834fb3a` | KR-KO | 134,217,728 | `5834fb3a2d751c48501d47d6a56898d7af6ccf9e` | 511 | 46 | 382 | 308 |
| SoulSilver | `IPGK-HV0` | `UPLOAD-0330e644` | KR-KO | 134,217,728 | `0330e6449306606114a92bdbb3f9d3d51d392b96` | 511 | 46 | 382 | 308 |

## Immediate structural observations

- Diamond and Pearl have the same FAT entry count and named-file count but differ by one FNT directory.
- Platinum expands the visible filesystem substantially over D/P.
- HeartGold and SoulSilver share the same high-level FAT/FNT/NARC counts; byte-level equality is not implied by those counts.
- HeartGold ARM9 size is 765,204 bytes; SoulSilver is 765,208 bytes, so even where top-level filesystem counts match they must remain separate release observations.

Per-dump header observations and filesystem summaries live under each release `DUMPS/<DUMP>/HEADER` and `DUMPS/<DUMP>/INDEXES` tree.
