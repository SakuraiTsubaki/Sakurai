# Repository Structure V2

Sakurai is reorganized around project/product roots instead of generation-number roots.

## Canonical roots

```text
projects/      # buildable/public projects
shared/        # schemas and reusable tooling
docs/          # repository-wide documentation
.github/       # CI and repository automation
```

For the current Kanto reverse-port project, the canonical root is:

`projects/gscrgby/`

Legacy roots such as `GEN-01/`, `GEN-02/`, and `CROSS-GEN/` are migration sources only. New GSCRGBY work must not be added there.

## GSCRGBY ownership

- `engine/gen1/`: Generation I runtime/format adapters.
- `sources/gen1/`: RGBY source descriptors and version differences.
- `sources/gen2/`: GSC source descriptors, especially Kanto.
- `integration/`: maps, tilesets, blocks, objects, warps, events, scripts, text and localization after cross-generation conversion.
- `patches/`: redistributable patch products.
- `manifests/`: ROM fingerprints, routing and build identity.
- `tools/`: reproducible converters/extractors.
- `tests/`: map/warp/collision/event/regression validation.
- `docs/`: public architecture and migration notes.

The private evidence/reverse-engineering counterpart lives in `SakuraiTsubaki/Tsubaki` under `workspaces/gscrgby/`.
