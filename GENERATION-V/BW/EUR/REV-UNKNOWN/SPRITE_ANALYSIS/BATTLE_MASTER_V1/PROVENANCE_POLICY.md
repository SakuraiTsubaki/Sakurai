# Provenance policy

Every logical sprite role must remain traceable through the full chain:

`game/version/region/revision -> archive/member/source asset -> decoded source -> conversion -> target indexed pixels -> target palette -> 4bpp -> compressed binary -> canonical asset`.

Deduplication may collapse identical final asset bytes but never collapses or deletes the upstream logical identities that reference them.

Unknown or unresolved source facts remain explicitly marked as such. No guessed species/form/member relationship is promoted to canonical provenance.
