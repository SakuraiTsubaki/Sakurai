# WITHDRAWN — HGSS Johto 256 Runtime v2

This runtime direction is **withdrawn** and must not be used as the project baseline.

Reason: it assumed a 16-bit species-ID migration before exhaustively accounting for Pokémon Green's existing 8-bit internal-ID space.

The corrected investigation is now under:

`GENERATION-I/GREEN/analysis/internal-species-id-census/`

Key finding: Green's internal species byte has 151 real Kanto species, 36 ordinary MissingNo holes, 3 pseudo-species IDs used only for fossil/ghost graphics, and the undefined range `$BF-$FF`. Reclaiming the holes/pseudo IDs plus the upper undefined range leaves the HGSS 256 target only one value short **if `$00` remains reserved**. Therefore the correct next question is whether `$00` and `$FF` sentinel semantics can be removed/reworked so all 256 byte values can become valid species IDs. That 8-bit saturated design may avoid the much larger party/box/save 16-bit migration.

No further ROM/runtime work should build on this withdrawn 16-bit prototype until the census decision is complete.
