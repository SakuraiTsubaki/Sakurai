# Emerald v4 -> v6 migration

Canonical source ownership is now `LIBRARY/GEN-03/EMERALD/SOURCE/GBA/CART/<RELEASE-ID>/` using `BPEJ-HV0`, `BPEE-HV0`, `BPED-HV0`, `BPEF-HV0`, `BPEI-HV0`, and `BPES-HV0`. Exact observed dumps are `UPLOAD-<sha1-prefix>` and remain below their release. Same-game localization research moved to `LIBRARY/GEN-03/EMERALD/COMPARE/REV0-LOCALIZATION-SET/`. The seven supplied filenames resolve to six unique byte identities; the two English filenames are aliases of `UPLOAD-f3ae0881`. No ROM binary is committed.

Pre-v6 release IDs `BPE*-R0`, dump IDs `PROJECT-*`, platform-first `LIBRARY/GEN-03/GBA/EMERALD`, flat project roots, `INFRA/REGISTRY`, and `INFRA/TOOLS` are noncanonical for new Emerald work.
