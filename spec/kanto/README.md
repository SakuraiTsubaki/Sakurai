# Kanto restoration specification

This directory defines the canonical desired state of the Generation II Kanto restoration.

## Authority split

- **Generation I geography is authoritative:** city/route scale, map topology, building placement, gates, caves, dungeons, water, fences, cliffs, entrances, and the exploration distance/density that existed in RGBY.
- **Generation II era and systems are authoritative:** engine behavior, battle/menu systems, time/day framework, trainer/NPC event model, Pokégear-era mechanics, and the fact that the story takes place after Generation I.
- **Version content is additive:** meaningful RGBY/GSC version-specific events are inventoried and integrated rather than silently discarded by choosing one edition as the only truth.

## Domain layout

```text
geography/      # dimensions, topology, outdoor layout requirements
connections/    # route/city/gate/cave graph and boundary contracts
facilities/     # buildings and functional sites
 dungeons/      # multi-floor exploration structures
 events/        # event inventory and Gen II-era continuation
 trainers/      # trainer placement and balance requirements
 encounters/    # encounter-area requirements
 localization/  # naming/text policy; implementation remains in Tsubaki
```

## Acceptance principle

A player familiar with Generation I should recognize the same Kanto spatial structure and travel distance, while NPCs, facilities, events, and systems communicate that time has advanced into the Generation II era.

Implementation details live in Tsubaki; source observations supporting each requirement live under `research/`.