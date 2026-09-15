# Project Standards

## Canonical role

Sakurai is the **research-control subset** of the project ecosystem. Tsubaki is the **complete non-ROM superset**.

The aggregation universe includes all Disassembly repositories, all Decompilation repositories, and special/standalone project repositories.

## Identity and provenance

- Record the originating repository/project for every aggregate record.
- Use stable repository, project, release/build, and artifact identifiers.
- Preserve exact version/revision/region/language distinctions when material.
- Separate confirmed observations from hypotheses; use `unknown` or `TBD` rather than inventing metadata.

## Structure

- One live structure only.
- No `vN` structure roots, migration layers, retired-tree mirrors, or duplicated historical namespaces.
- Git history is the historical record.
- Individual repositories keep canonical ownership of their game/project work; Sakurai provides the research/control aggregate view.

## Repository safety

Do not commit retail, modified, rebuilt, or otherwise playable ROM images, console keys, or equivalent complete game-image containers.
