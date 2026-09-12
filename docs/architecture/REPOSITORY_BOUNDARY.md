# Sakurai / Tsubaki repository boundary

## Sakurai: reference truth

Sakurai owns source identity, observations, comparisons, specifications, schemas, and verification criteria. Questions about what RGBY/GSC contained, how versions differ, and what restored Kanto must preserve belong here.

Canonical roots:

```text
catalog/  research/  spec/  schemas/  docs/
```

## Tsubaki: executable production

Tsubaki owns local-input tooling, extraction/normalization/conversion code, implementation source, regression tests, generated working data, and build recipes.

Canonical roots:

```text
config/  tools/  src/  tests/  docs/  local/  generated/  build/
```

## Shared contract

The repositories share logical ROM IDs and SHA-256 identities, schema versions, stable Kanto location/event IDs, acceptance criteria, and provenance links. They intentionally do **not** mirror directory trees.

## Restoration authority

- **Generation I:** spatial geography, scale, route/city/dungeon structure, deleted facilities, original exploration layout.
- **Generation II:** engine, era, systems, time/day framework, GSC-era NPC/event state, battle/menu/trainer framework.
- **Unified project:** version-specific events are inventoried and integrated rather than discarded by selecting one edition as the only truth.

ROM bytes and bulk/raw copyrighted extraction outputs are local inputs, not repository artifacts.