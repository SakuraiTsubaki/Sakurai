# Black / White battle-sprite source structure

This path owns ROM-derived structure/evidence only. Production conversion belongs in Tsubaki.

## Source archive

The historical ROM-primary survey identifies NitroFS `a/0/0/4` as the battle Pokémon graphics archive used by the static/animation investigation.

For the surveyed 20-member Pokémon/form block convention, the production-facing static slots are:

| Relative member | Role |
|---:|---|
| +0 | male front static graphics |
| +1 | female front static graphics |
| +9 | male back static graphics |
| +10 | female back static graphics |
| +18 | normal palette |
| +19 | shiny palette |

Other members participate in the multipart animation structure and must not be discarded merely because the older target engine uses a static 64x64 sprite representation.

## Preservation rule

The project maintains two tracks:

1. static insertion master for older-engine compatibility;
2. multipart animation preservation/engine-expansion track.

Do not collapse the animation data into the static track and then treat the source animation as disposable.

## Identity

Evidence is tied to the locked IRBO-R0 / IRAO-R0 supplied dump observations. Because the SweeTnDs images require clean-dump revalidation for TWL-specific conclusions, every derived graphics inventory must preserve dump provenance.