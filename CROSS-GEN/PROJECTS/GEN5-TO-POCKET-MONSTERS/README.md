# Generation V → ポケットモンスター

This directory is the single project-facing entry point for this project.

## Project work

- `GEN-05/` — complete current Generation V research/release work tree, mirrored losslessly from repository-root `GEN-05/` by reusing the same Git tree object.
- `CROSSWALK/` — Generation V → target correspondence tables.
- `DESIGN/` — engine/data-model/integration design.
- `MANIFESTS/` — project locks, provenance, routing and status.
- `REPORTS/` — project reports and audits.
- `TOOLS/` — project research and validation tools.
- `VERIFICATION/` — regression and port verification evidence.

The repository-root `GEN-05/` remains preserved for generation-wide ownership and reuse by other projects. This project root must nevertheless remain a complete, discoverable view: whenever Generation V work belonging to this project changes, the project-facing `GEN-05/` tree is refreshed in the same update.

Complete playable ROM images are excluded from GitHub. All other project artifacts are eligible for version control.
