# GREEN Modern Moves Phase 1

Targets: Pocket Monsters Green Japan Rev 0 and Rev A.

Implemented:
- 64 move-table numeric updates (power / accuracy / PP).
- 7 directly representable effect-code changes.
- Stat-lowering additional-effect chance 33.2% -> 10% for Acid, BubbleBeam, Aurora Beam, Psychic, Constrict, Bubble.
- Priority generalized for Whirlwind -6, Roar -6, Counter -5, Quick Attack +1, Teleport -6, Bide +1.

Deferred only where Gen I cannot express the modern effect without a genuinely new/compound handler or a third chance encoding.

Baseline: canonical main-series values. Champions / Legends Z-A game-specific overrides are kept separate.
