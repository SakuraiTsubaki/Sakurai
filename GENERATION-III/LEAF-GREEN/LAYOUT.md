# Pokémon LeafGreen Layout Census

This stage scans each ROM locally for coarse layout signals. It does not copy ROM bytes into the repository.

## Entry point and terminal padding validation

| File | Code | Entry target | Pointer-like aligned words | Tail FF start | Tail length | Pointer-like targets in tail |
|---|---|---:|---:|---:|---:|---:|
| Pocket Monsters - Leaf Green (Japan).gba | `BPGJ` | `0x00000204` | 64,502 | `0x0FDFFFF` | 131,073 | 155 |
| Pokemon - Blattgruene Edition (Germany).gba | `BPGD` | `0x00000204` | 63,402 | `0x0EB2338` | 1,367,240 | 513 |
| Pokemon - Edicion Verde Hoja (Spain).gba | `BPGS` | `0x00000204` | 63,565 | `0x0EB2388` | 1,367,160 | 518 |
| Pokemon - Leaf Green Version (Europe) (Rev 1).gba | `BPGE` | `0x00000204` | 63,732 | `0x0EB0E14` | 1,372,652 | 543 |
| Pokemon - Leaf Green Version (USA).gba | `BPGE` | `0x00000204` | 63,724 | `0x0EB0E14` | 1,372,652 | 543 |
| Pokemon - Version Vert Feuille (France).gba | `BPGF` | `0x00000204` | 63,548 | `0x0EB2318` | 1,367,272 | 535 |
| Pokemon - Versione Verde Foglia (Italy).gba | `BPGI` | `0x00000204` | 63,514 | `0x0EB244C` | 1,366,964 | 508 |

### Interpretation

- All seven headers branch to the same startup entry target: ROM offset `0x204`.
- The pointer-like scan is only a heuristic: aligned 32-bit words whose normalized value falls in `0x08000000..0x08FFFFFF`. Compressed, graphic, or arbitrary data can produce false positives, so these counts are **not** treated as verified references.
- The Japanese image has a much shorter terminal `0xFF` run than the international images, so free-space planning must be version-specific.
- International builds also contain a ~5.9 MiB pure-`0xFF` gap ending at `0x0CFFFFFF`; the Japanese build has a ~5.22 MiB pure-`0xFF` gap ending at `0x0BFFFFFF`. These are high-priority candidates for reference-aware free-space validation.

## Fully `0xFF` 1 MiB windows

- **International builds (DE/ES/EN Rev 0/EN Rev 1/FR/IT):** regions `0x800000–0xCFFFFF` and `0xF00000–0xFFFFFF` are completely `0xFF`.
- **Japanese build:** regions `0x700000–0xBFFFFF` and `0xE00000–0xEFFFFF` are completely `0xFF`; unlike the international builds, region `0xF00000–0xFDFFFE` contains data before the final `0xFF` tail.

This proves the coarse physical layout differs substantially between JP and international builds even though the startup entry point is shared. These windows are still labeled **unused/padding candidates**, not guaranteed insertion space, until reference-aware analysis and runtime regression tests are done.

## 1 MiB region census

`region_usage_1m.csv` records per-region `0xFF`/`0x00` density, pointer-like source density, pointer-like target density, and a SHA-256 fingerprint. This is the first coarse map for locating shared engine areas, localization-heavy areas, and likely padding.

## Large constant runs

`large_constant_runs.csv` lists the largest >=4 KiB `0x00`/`0xFF` runs and counts pointer-like aligned words whose values land inside each run. A run is not classified as safe free space until cross-reference and behavior checks are complete.
