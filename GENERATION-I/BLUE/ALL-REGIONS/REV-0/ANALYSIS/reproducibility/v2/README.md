# Pokémon Blue/Ao full-ROM corpus v2

This layer extends the physical-bank baseline into a deterministic whole-ROM work scaffold for the six supplied Blue/Ao ROMs (JP, EN, DE, FR, IT, ES).

It preserves byte exactness first: every ROM byte is assigned to exactly one 0x100-byte scaffold chunk, every physical bank is represented, and semantic labels are promoted only after lossless extractor/reassembler proof.

Generated locally by `build_full_corpus.py`:
- 256-byte chunk ledger for all ROM bytes
- per-region RGBDS bank scaffolds with stable chunk labels
- exact cross-version alignment runs
- pointer-target hotspot hypotheses
- byte-value histograms
- exact coverage proof

ROM binaries and extracted bank binaries are never committed.
