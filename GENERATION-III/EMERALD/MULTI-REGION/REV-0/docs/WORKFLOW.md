# Workflow and repository policy

1. Keep source `.gba` files read-only and outside GitHub.
2. Verify ROM identity before extracting or modifying anything.
3. Generate analysis from scripts; never hand-edit generated CSV/JSON outputs.
4. Preserve source offsets, sizes, checksums, and tool version with each extracted record.
5. Put cross-language analysis under `GENERATION-III/EMERALD/MULTI-REGION/REV-0/<WORK TYPE>`.
6. Put language-specific outputs under the corresponding language/region path.
7. Put research, surveys, manifests, address maps and validation in `Sakurai`; implementation assets, source, patches and reusable build assets belong in `Tsubaki`.
8. Do not commit original ROMs or any artifact whose purpose is to substitute for the original copyrighted ROM.
