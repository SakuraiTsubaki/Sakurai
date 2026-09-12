# Phase 4 provenance and confidence

## Primary evidence

The uploaded Pokémon Black and Pokémon White ROMs are the primary evidence. All counts, hashes, index relations, archive equality/differences, entity totals, map-name decoding, and graph edges in this phase were regenerated from those ROMs.

## External technical cross-checks

- PlatinumMaster/BeaterLibrary `Formats/Zone/ZoneHeader.cs` at commit `a2a5267898361ae1e654edfe0cd82b1355ea1c0a`: documents the 0x30-byte ZoneHeader parser and packed bitfields.
- The same BeaterLibrary commit: `ZoneEntities.cs`, `Proxy.cs`, `NPC.cs`, `Warp.cs`, `Trigger.cs`, `InitializationScript.cs`, and `TriggerRelated.cs`: documents the field-zone entity record layouts used as the parser cross-check.
- Universal Pokémon Randomizer ZX `gen5_offsets.ini` (commit `cb4e986e69dbb13c90c47873d26382982f212487`) identifies BW1 `MapTableFile=a/0/1/2`, `Scripts=a/0/5/7`, `MapFiles=a/1/2/5`, `WildPokemon=a/1/2/6`, and `MapNamesTextOffset=89` for IRBO, with White IRAO inheriting the common structure.
- Project Pokémon PPRE `pokemon/msgdata/msg.py` commit `3909054ecf26cbe779a8d9aeafef79c3a87f98c0` was used to cross-check the Generation V text-container decryption algorithm.

## Confidence policy

Fields whose meaning is directly expressed by multiple mature parsers and agrees with ROM index ranges are named normally. Fields still labeled `unknown`, `candidate`, or packed upper bits remain intentionally unresolved. B2W2-only interpretations are not promoted to BW1 facts.
