# RGBY + GSC event integration policy

## Integration order

1. Integrate every Red, Green, Blue, and Yellow event into the Generation I base.
2. Then integrate every Gold, Silver, and Crystal Kanto event into the same project.

`RGBY` always includes Green; do not reduce the scope to RBY.

## No deletion

No source event is deleted merely because another version has a similar or conflicting event. Version-exclusive, region-exclusive, revision-specific, external-distribution, and in-game events remain separately represented whenever they can be made available in one game.

## No mutually exclusive version branch as the default

Version differences are not collapsed into a single branch that permanently excludes the other versions. Separate events/content paths should exist so the player can experience all preserved content in the integrated game.

## External events become in-game

Existing external/distribution events that are part of the supported source corpus are converted into in-game obtainable events where technically feasible, while preserving their identity and result.

## Time and weekday rule

The player may choose time/weekday during the opening setup as designed, but event availability must not depend on waiting for a specific weekday or time. Events that were time- or weekday-gated in Generation II are made continuously available through Generation I-compatible event logic. The time choice is not removed; the availability gate is removed.

## Conversion rule

Generation II script bytecode does not need to be reproduced instruction-for-instruction. Reimplement the same player-facing condition, action, flag transition, reward, NPC state, and progression result with Generation I event mechanisms. Simplification is allowed only when the core condition/result and progression meaning are preserved.
