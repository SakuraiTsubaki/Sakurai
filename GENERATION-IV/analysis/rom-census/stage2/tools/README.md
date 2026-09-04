# Stage 2 census tools

Run `build_stage2_extensions.py` from this directory to reproduce the full Stage 2 analysis. It imports and executes `build_stage2.py` first, then adds the battle-sprite slot census, cross-generation key findings, final manifest, and final ZIP package.

Requirements: Python 3, pandas, the Stage 1 `gen4_census` per-ROM file ledgers, and the five local project ROMs at the paths configured in `build_stage2.py`.

No ROM is written to the GitHub output. The generated analysis package contains CSV/JSON/Markdown metadata only.

Verified local hashes after the completed Stage 2 rebuild:

- full local builder (`gen4_stage2_build.py` including the extension block): `d2eb5b84872034e89b43a045ba71135061b79ea784d918d155c302918aff18c5`
- extension script: `246f709189eb93f88491931d0fe6f32a72fcc1424de5a3377aeb63ec3875bebe`
- `Generation_IV_ROM_Census_Stage2.zip`: `ead6042575e1092b063cfa05aa52f70218402fb01303ef9145d4df4066d4eb36`
