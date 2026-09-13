# Emerald cutover to Repository Structure v10

Date: 2026-09-13

Canonical Emerald ownership is now:

- releases and exact observations: `GEN-03/EMERALD/RELEASES/GBA/CART/<RELEASE-ID>/DUMPS/<DUMP-ID>/`
- same-game comparison/reverse engineering: `GEN-03/EMERALD/COMPARES/HV0-LOCALIZATION-SET/`
- production projects in Tsubaki: `GEN-03/EMERALD/PROJECTS/...`

Retired Emerald ownership branches `GEN-03/EMERALD/SOURCE/` and `GEN-03/EMERALD/COMPARE/` are removed from the active tree after their verified research artifacts are re-homed. Git history preserves the original paths.

Dump IDs are re-keyed from old SHA-1-derived `UPLOAD-*`/`DUMP-*` forms to the v10 SHA-256 form `DUMP-SHA256-<first-16-uppercase-hex>`.

The obsolete `GBA-AGB` platform alias is not carried forward; the platform coordinate is `GBA`.

No ROM binary is committed.
