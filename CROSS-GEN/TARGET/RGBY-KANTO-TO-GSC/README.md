# RGBY Kanto → GSC

Canonical target ID: `RGBY-KANTO-TO-GSC`

Repository role: **Sakurai / research + specification + verification authority**.

## Scope

This target describes the cross-generation transfer/integration of Kanto material from Generation I RGBY source families into a Generation II GSC-compatible target. Source release identities remain owned by their respective `GEN-01/<GAME>/SOURCE/...` paths; this directory owns only the cross-generation target specification.

## Canonical sections

```text
CROSS-GEN/TARGET/RGBY-KANTO-TO-GSC/
├── README.md
├── MANIFESTS/      # source/target IDs and hashes; no ROM bytes
├── SPEC/           # behavior, content and compatibility requirements
├── MAPPING/        # Gen I ↔ Gen II semantic mappings
├── RESEARCH/       # evidence and analysis
├── REFERENCE/      # secondary/external reference metadata
└── VERIFICATION/   # acceptance criteria and evidence
```

Create a section only when tracked content exists; empty directories are not required.

## Repository handoff

Sakurai defines **what** is being transferred and **how correctness is judged**. The matching Tsubaki path implements **how it is extracted, converted, built and patched**:

```text
SakuraiTsubaki/Tsubaki:
CROSS-GEN/TARGET/RGBY-KANTO-TO-GSC/
```

## ROM boundary

No original or complete patched ROM image is committed. A local ROM is identified by manifest/hash and remains outside Git. Any substantial proprietary extraction that cannot be redistributed also remains local; Git stores the tooling, mappings, manifests, patches and verification evidence needed to reproduce the work from a legally obtained local source.

## Initial work lanes

The project should be decomposed by semantic domain rather than by ad-hoc dump folders:

```text
MAPPING/
├── MAPS/
├── EVENTS/
├── OBJECTS/
├── TEXT/
├── ITEMS/
├── SPECIES/
├── MOVES/
├── TRAINERS/
├── ENCOUNTERS/
├── AUDIO/
└── GRAPHICS/
```

Cross-domain rules belong in `SPEC/`; implementation-specific files do not belong in Sakurai.
