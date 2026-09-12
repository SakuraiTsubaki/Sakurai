# Sakurai / Tsubaki repository boundary

## Sakurai: reference truth

Sakurai owns source identity, observations, comparisons, specifications, schemas, and verification criteria. A question beginning with **what did RGBY/GSC contain?**, **how did the versions differ?**, or **what must the restored Kanto preserve?** belongs here.

Canonical roots:

```text
catalog/  research/  spec/  schemas/  docs/
```

## Tsubaki: executable production

Tsubaki owns local-input tooling, extraction/normalization/conversion code, implementation source, regression tests, generated working data, and build recipes. A question beginning with **how do we extract/convert/implement/test/build it?** belongs there.

Canonical roots:

```text
config/  tools/  src/  tests/  docs/  local/  generated/  build/
```

## Shared contract

The repositories share:

1. logical ROM IDs and SHA-256 identities;
2. schema versions;
3. stable Kanto location/event identifiers;
4. acceptance criteria;
5. provenance links from implementation back to source observations.

They intentionally do **not** mirror directory trees.

## Restoration rule

The project resolves cross-generation authority by domain:

- **Generation I:** spatial geography, scale, route/city/dungeon structure, deleted facilities, and the original exploration layout.
- **Generation II:** engine, era, systems, time/day mechanics, GSC-era NPC/event state, battle/menu/trainer framework, and implementation behavior.
- **Unified project:** preserves all relevant version-specific events as independently representable content instead of deleting one version in favor of another.

## Source-material rule

ROM bytes and bulk/raw copyrighted extraction outputs are local inputs, not repository artifacts. Repositories version metadata, facts, schemas, code, scripts, compact derived observations, patches where appropriate, and reproducibility information.