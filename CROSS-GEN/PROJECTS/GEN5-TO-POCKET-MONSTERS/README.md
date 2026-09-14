# Generation V → ポケットモンスター

This directory is the single project-facing entry point for the Generation V project in Sakurai.

## Everything in one place

- `BLACK/` — active Pokémon Black research/release corpus.
- `WHITE/` — active Pokémon White research/release corpus, including the restored W1–W5 deconstruction work.
- `COMPARES/` — Black/White comparison, delta, dedup and structural comparison material.
- `SHARED/` — shared Generation V tooling and common material.
- `CROSSWALK/` — Generation V → target correspondence tables.
- `DESIGN/` — engine/data-model/integration design.
- `MANIFESTS/` — project locks, provenance, routing and status.
- `REPORTS/` — project reports and audits.
- `TOOLS/` — project research and validation tools.
- `VERIFICATION/` — regression and port verification evidence.
- `SESSION-INDEX.md` — project-session-to-artifact lookup index.

Sakurai no longer requires a separate repository-root `GEN-05/` tree for this project view: the active Generation V research corpus is consolidated directly under this project root so project work is discoverable without chasing migration or legacy paths.

`INFRA/MIGRATION/` is historical evidence only. Current project artifacts must not exist only in migration quarantine.

Complete playable ROM images are excluded from GitHub. All other project artifacts are eligible for version control.