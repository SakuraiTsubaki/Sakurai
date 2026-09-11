# Generation IV → Gen III Phase 2C — All Otherpoke Forms Resident

## Result

- Shared DP/Pt/HGSS `otherpoke` archive: 213/213 members converted and retained.
- Platinum `pl_otherpoke` archive: 253/253 members converted and retained.
- Logical members: 466 total = 294 NCGR graphics + 172 NCLR palettes.
- Every NCGR preserves both f0 and f1; each frame is preservation-v2 converted from 80x80 to 64x64 and stored as GBA OBJ 4bpp.
- Each NCLR is stored as 16-color little-endian BGR555.
- Converted payloads are independently GBA BIOS LZ10-compressed and byte-identical payloads share storage without deleting logical member entries.
- Forms bank size: 169,984 bytes.
- Forms bank SHA-256: `07ec596769bf3dc62d8437f8ab3792e04753f31657812e8f4b523be1d1e5801d`.
- Internal forms-bank decompression/hash verification errors: 0.

## Source/archive verification

The shared `otherpoke` archive is byte-identical in uploaded Diamond, Pearl, Platinum, HeartGold and SoulSilver ROMs: SHA-256 `cab7af2e4fef1878af6a7002eecc24c7a1c879166aaf5dfd61ebdc0bd4b92681`.

Platinum `pl_otherpoke.narc`: SHA-256 `bcce60993746ec909b6d4eee51f8b04dc7176e637bc7f41572cb133a005a2ca5`.

Common archive NCGR uses reverse/back-to-front decoding; Platinum `pl_otherpoke` uses forward/front-to-back decoding. Both directions were verified from the uploaded ROM data and by decoded transparency/plausibility.

## Gen III insertion

- RUBY_JP_REV0: forms bank @ `0xb8cf00`, cumulative IPS32 `3,895,264` bytes, patch reapply exact = `True`.
- SAPPHIRE_JP_REV0: forms bank @ `0xb8cf00`, cumulative IPS32 `3,895,264` bytes, patch reapply exact = `True`.
- EMERALD_JP_REV0: forms bank @ `0x1433b00`, cumulative IPS32 `4,579,407` bytes, patch reapply exact = `True`.
- FIRERED_JP_REV1: forms bank @ `0x138cf00`, cumulative IPS32 `3,896,187` bytes, patch reapply exact = `True`.
- LEAFGREEN_JP_REV0: forms bank @ `0x138cf00`, cumulative IPS32 `3,896,187` bytes, patch reapply exact = `True`.

All five cumulative patches were independently reapplied to the clean source ROMs and reproduced the generated Phase 2C work ROM bytes exactly. Previous Phase 2B content was preserved byte-for-byte before the new bank insertion point.

## Boundary

This phase makes every original form/archive member physically resident in all five Japanese Gen III work ROMs. The semantic/runtime resolver that chooses DP/Pt/HGSS, gender and alternate-form member during gameplay is the next phase; Phase 2C does not claim that every alternate form is already selectable in live battles.

Original ROM files are never stored in GitHub.