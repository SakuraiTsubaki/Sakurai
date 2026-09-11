# Pocket Monsters Green modern parameters — Phase 1 implementation

Rev 0 and Rev A are separate implementation targets. This phase applies only later-generation base-stat changes that map unambiguously to the original Generation I five-stat base-data layout.

## Applied now

13 direct stat-byte changes per revision: Attack, Defense, or Speed. Both revisions receive the same gameplay changes independently.

## Deferred until engine expansion

- Generation I Special -> separate Sp. Atk / Sp. Def
- Steel and Fairy type support and type-chart integration
- Any modern parameter changes that depend on those structures

The original ROMs remain untouched. Local work ROMs are generated only for verification. Repository-distributed implementation artifacts are IPS patches plus scripts/manifests. Both outputs recalculate the Game Boy global checksum while preserving a valid header checksum.
