# Repository topology for GS Korean → Pocket Monsters

The project consumes canonical release/dump identities from `LIBRARY` and must not create project-local copies of the same source ROM identity.

## Sakurai

- `LIBRARY/.../RELEASES`: official-build facts and release-owned research.
- `LIBRARY/.../DUMPS`: exact observed-file provenance and dump-specific observations.
- `LIBRARY/.../COMPARISONS`: release/revision relationships.
- `PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/MANIFESTS`: source locks and routing.
- `CROSSWALK`: JP/EN source-to-KR terminology/text mappings.
- `DESIGN`: Korean text engine, relocation, pointer, UI, SRAM/name specifications.
- `IMPLEMENTATION`: research-side target maps/specifications.
- `VERIFICATION`: research and integration evidence.

## Tsubaki

- `LIBRARY`: verified reusable original-release assets.
- `PROJECTS/.../SOURCE`: project-owned reconstructable conversion inputs/specifications.
- `CONVERTED`: normalized reusable production resources.
- `IMPLEMENTATION`: target-specific insertion data.
- `PATCHES`: distributable patches, never ROM images.
- `BUILD`: reproducible build inputs and safe generated outputs.

The repository pair shares release IDs, dump IDs, project IDs, and target IDs exactly.
