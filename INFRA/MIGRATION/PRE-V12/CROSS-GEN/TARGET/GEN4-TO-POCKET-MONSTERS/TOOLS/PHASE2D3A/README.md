# Phase 2D3A tooling

Canonical local build script: `build_phase2d3a_castform.py`.

The script reconstructs the cumulative Phase 2D2B-RC2 targets from clean Japanese Gen III ROMs, reads the C3 all-otherpoke bank, verifies DP/Pt/HGSS Castform source equivalence for the Gen III Forecast-consumed f0 frames and palettes, constructs the Gen III four-form composite, repoints expanded Castform sprite/palette tables, replaces the dedicated Castform front-coordinate array, emits cumulative IPS32 patches, and verifies clean-source patch reapplication.

The exact script is retained in the user-facing Phase 2D3A package. ROM binaries are never repository artifacts.
