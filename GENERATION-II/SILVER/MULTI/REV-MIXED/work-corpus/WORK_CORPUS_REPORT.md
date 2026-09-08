# Pokémon Silver whole-ROM reproducibility work corpus

This corpus extends the byte-exact baseline into whole-ROM addressable work material for all eight targets. It deliberately does **not** contain ROM bytes.

## What is now reproducible

- exact ROM identity and header/checksum verification
- complete 16 KiB bank census
- complete 0x100-byte fingerprint coverage for every source byte
- fill/free-space candidates (never automatically treated as safe)
- local and far-pointer table candidates
- text candidates, including Korean 2-byte-codepoint-aware scanning
- LR35902 opcode-walk diagnostics for every 0x100 block
- duplicate block fingerprints
- English-reference semantic bank roles with confidence/evidence for localization transfer
- cross-version bank correspondence and per-bank diff counts
- JP Rev0 ↔ RevA exact diff-run address map (hashes only)
- six international-release identical-chunk consensus

## Reference provenance

English bank-role reference: `https://github.com/pret/pokegold/blob/656583c939d30f920a316177311a502dd222b57c/layout.link` at commit `656583c939d30f920a316177311a502dd222b57c`.
English character map reference: `https://github.com/pret/pokegold/blob/656583c939d30f920a316177311a502dd222b57c/constants/charmap.asm` at the same pinned commit.
Korean character-map behavior is referenced from `SakuraiTsubaki/pokegold-kr/constants/charmap.asm`; its first byte `0x01..0x0B` selects a Hangul table and the following byte selects the table entry.

## Important boundary

This is a complete **byte coverage + structural candidate corpus**, not a claim that every byte already has a final human semantic symbol. Candidate records remain candidates until matched to source symbols/routines/tables. The corpus is designed so that those later verified symbols can be added without losing provenance or byte coverage.
