# Generation IV → Gen II / Gen III — Phase 1 numeric move patch

Scope: all Gen II / Gen III ROMs currently uploaded to this project (14 targets).

## What is changed
Only numeric move parameters safely representable in each original move table:
- Power
- Accuracy
- PP

Source profile: HGSS active move table (NDS file ID 140), established in the Phase 1 inspection.

## What is deliberately not changed yet
- Move effect IDs / scripts
- Physical / Special / Status category
- Target masks
- Priority semantics
- Contact / Protect / Mirror Move / King's Rock etc. flags
- New Gen IV moves
- Abilities, held-item battle hooks, evolution logic, save/UI expansion

These require engine-level work and are not treated as numeric byte replacements.

## Target handling
- Gen II move entries are 7 bytes. Accuracy uses the 0..255 encoding.
- Gen III move entries are 12 bytes. Accuracy is direct percent.
- Every target ROM is scanned independently for the move-table signature; region offsets are not reused blindly.
- Gen II global checksums are recalculated after modification.
- Original uploaded ROM files are never modified.

## Verification
- 14/14 targets located independently.
- 248 numeric field changes total.
- Each patch was reapplied to the original bytes and compared byte-for-byte with the verified working copy.
- Gen II header/global checksum validity checked after patching.

Full modified ROMs are not distributed or committed. Portable artifacts are IPS patches plus manifests.