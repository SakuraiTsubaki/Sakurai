# Red whole-ROM reproducibility layer

Deterministic whole-ROM structural analysis for the supplied Pokémon Red-family ROM set. Original ROM binaries, bank dumps, full hex dumps, and replacement byte payloads are not committed.

The canonical generator is `scripts/analyze_roms.py`. It identifies known inputs by SHA-256, deduplicates exact copies, validates header/global checksums, emits per-bank hashes/statistics/layout, conservative 00/FF padding candidates, cross-version bank equivalence, pairwise summaries, and exact difference ranges.

The complete generated snapshot is retained in the project work package; large deterministic derivative tables can be regenerated from the local ROMs with the script.
