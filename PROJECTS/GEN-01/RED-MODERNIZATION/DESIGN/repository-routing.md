# RED v6 routing

Every RED artifact has exactly one truthful owner.

| Artifact | Canonical owner |
|---|---|
| official release identity | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/IDENTITY/` |
| exact observed ROM/dump fact | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/DUMPS/<DUMP-ID>/` |
| platform-native bank/layout research | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/NATIVE/` |
| semantic source research | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/DOMAINS/` |
| same-game release comparison | `LIBRARY/GEN-01/RED/COMPARE/<COMPARISON-ID>/` |
| reusable game parser/schema | `LIBRARY/GEN-01/RED/SHARED/` |
| external disassembly/reference | `LIBRARY/GEN-01/RED/REFERENCE/<REFERENCE-ID>/` |
| modernization/localization inputs | `PROJECTS/GEN-01/RED-MODERNIZATION/INPUTS/` |
| latest-official crosswalk | `PROJECTS/GEN-01/RED-MODERNIZATION/CROSSWALK/` |
| modernization design | `PROJECTS/GEN-01/RED-MODERNIZATION/DESIGN/` |
| derived-target verification | `PROJECTS/GEN-01/RED-MODERNIZATION/VERIFICATION/` |
| production assets/patch/build | Tsubaki `PROJECTS/GEN-01/RED-MODERNIZATION/...` |
| repository-wide registry/schema/tooling | `INFRA/REGISTRIES`, `INFRA/SCHEMAS`, `INFRA/TOOLING` |
| pre-v6 unmigrated material | `LEGACY/PRE-V6-2026-09-12/` (read-only) |

Canonical RED releases: `JP-JA-HV0`, `JP-JA-HV1`, `US-EU-EN-HV0`, `EU-DE-HV0`, `EU-FR-HV0`, `EU-IT-HV0`, `EU-ES-HV0`.

Original ROM binaries and byte-exact whole-bank payload archives are never committed.
