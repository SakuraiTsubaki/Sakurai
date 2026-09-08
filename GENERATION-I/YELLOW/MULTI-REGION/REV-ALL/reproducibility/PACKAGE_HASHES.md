# Reproducibility package hashes

Final verified package set built 2026-09-08.

- `yellow_repro_workspace_public.zip`
  - SHA-256: `b572ae990579a9d570e2059b53d2defceedbf200c4b4705d592dfad188158dcf`
  - Contains documentation, manifests, hashes, reports, compressed analysis inventories, reference locks, tools and tests. No source ROMs or raw bank slices.

- `yellow_repro_workspace_full_private.zip`
  - SHA-256: `80b00a48a5224846736491019fd6585b5293ac6de956f4ef4faf2a927c4aca06`
  - Contains the entire public workspace plus local-only 16 KiB bank slices and generated relationship IPS patches. Treat as private working material.

Verification at packaging time:

- workspace manifest: PASS
- lossless bank split/rebuild: 9/9 PASS
- deterministic relationship patch rebuild: 8/8 PASS
