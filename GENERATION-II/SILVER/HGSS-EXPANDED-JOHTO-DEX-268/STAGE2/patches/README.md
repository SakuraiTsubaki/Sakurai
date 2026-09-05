# Stage 2 IPS patch manifest

These IPS patches are generated deterministically by `../make_ips_patches.py` from the exact clean Silver ROM revisions listed in `../build_report.json`.

Every patch was reapplied to its matching clean source and verified byte-for-byte against the corresponding Stage-2 `DATA-STAGED` output ROM.

| Target | IPS SHA-256 |
|---|---|
| Pocket Monsters Eun (Korea) | `a8f7fdd3fd22685c96aea6b98b6fda1f024a0428e95ffca01ba67b2e56e13b9a` |
| Pocket Monsters Gin (Japan) | `478ca731c68cc718da8afee1e2909cbe0fd0448fc1a2dcadf91bf57e6a1945a2` |
| Pocket Monsters Gin (Japan) (Rev A) | `b6b15900b1752991bd6ce3bda820d5627dfa7d162cb0409f226a0acab2c92569` |
| Pokemon - Edicion Plata (Spain) | `608a0f1548ac2b0f573df88010f0dd2a423443e03719754e2dc1127cd80ae135` |
| Pokemon - Silberne Edition (Germany) | `2a1df43c3b7295c03e0b68590e2d27b2d4dfdc53a4074eabdd2d40591b7f5b0e` |
| Pokemon - Silver Version (USA, Europe) | `29c8b72bb9364acd23e2724d21656b9193fbf9ffc0089d4b8a6ab7648f48db8b` |
| Pokemon - Version Argent (France) | `4a171c37ca8d3e74c941ec70979ac9996469bf76d7b0054b460cf4730b9b7ded` |
| Pokemon - Versione Argento (Italy) | `5c7137cdd67cc0e95833eb5914ee9656a03afb80918ac6d62b78537ddd4e8020` |

ROM binaries are intentionally not committed. The distributable local Stage-2 package contains the generated IPS files; the scripts and hash manifest here are sufficient to reproduce and verify them.
