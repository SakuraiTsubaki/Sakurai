# Repository layout v2 — Sakurai

## Rule

Paths are organized by *project role*, not by console generation. `GEN-01/GEN-02/CROSS-GEN` made cross-generation work scatter across three roots, so GSCRGBY now lives under one project root.

```text
projects/
  gscrgby/
    engine/
      gen1/
        asm/
        data/
        formats/
    sources/
      gen1/
        red/
        green/
        blue/
        yellow/
      gen2/
        gold/
        silver/
        crystal/
    integration/
      maps/
      tilesets/
      blocks/
      objects/
      warps/
      events/
      scripts/
      text/
      localization/
    patches/
    manifests/
    tools/
    tests/
    docs/
shared/
  schemas/
  tools/
docs/
.github/
```

## Public/private boundary

Sakurai stores reproducible, redistributable project material. ROM paths are represented by fingerprints and logical IDs. Full ROM images, raw full-ROM dumps, and build products containing unmodified ROM bytes are excluded.

## Migration

1. Freeze new GSCRGBY additions under legacy `GEN-01`, `GEN-02`, and `CROSS-GEN`.
2. New GSCRGBY work goes only to `projects/gscrgby`.
3. Move reusable generation-specific code into `projects/gscrgby/engine` or `sources`.
4. Move cross-generation result data into `integration`.
5. After path-equivalence tests pass, remove duplicate legacy copies in a dedicated cleanup PR.

No destructive legacy deletion is part of the bootstrap commit.
