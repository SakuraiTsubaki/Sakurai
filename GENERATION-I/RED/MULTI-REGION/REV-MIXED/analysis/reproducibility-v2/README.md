# Pokémon Red full-ROM reproducibility v2

This is the GitHub-safe reproducibility layer for the complete uploaded Red ROM set.

## Coverage
- 8 recognized input files, deduplicated to 7 unique ROM images.
- DE Rev 0, EN USA/Europe Rev 0, ES Rev 0, FR Rev 0, IT Rev 0, JP Rev 0, JP Rev A.
- Every unique ROM has 100% byte coverage through generated 16 KiB bank source skeletons.
- Actual local `build.py -> verify.py` tests: 7/7 PASS.
- No `.gb`/`.gbc` binaries or replacement-byte dumps are stored here.

## Exact semantic source pins
- EN Red: `pret/pokered` commit `a1a22aaf84d1675bcdbaeb194592379d586d838e`, SHA-1 `ea9bcae617fdf159b045185467ae58b2e4a48b9a`.
- JP Red Rev 0 / Rev A: `Narishma-gb/pokegreen` commit `953f41b34108621b2bf13c3b1e53abfc9c3e5aec`, SHA-1 `0623ad12f48c259447980d68bd85ddbf8204b2cd` / `ef74c79cded14204ac79e77f4964d9cb25003120`.

## Generated corpus
The generator emits `.asm`, `.inc`, `.sym`, `.map`, CSV/JSON manifests, far-pointer candidates, raw branch/call xref candidates, memory-reference candidates, MBC bank-switch candidates, free/padding candidates, source-layout coverage, and exact roundtrip proofs for all seven ROMs.

DE/FR/IT/ES are structurally anchored to the exact EN disassembly by same-bank similarity. Candidate scans are explicitly marked as candidates until semantic proof confirms them.

Local complete archive SHA-256: `dddd6823babffc70af8502abe7614f40cc8bfdb5b98c049f1a508a5f6069124d`.
