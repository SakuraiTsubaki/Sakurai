# RED v5 routing

Every new RED artifact is classified by semantic ownership before a path is chosen.

| Artifact | Canonical owner |
|---|---|
| official build identity | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/IDENTITY/` |
| exact supplied file observation | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/DUMPS/<DUMP-ID>/` |
| platform-native structure research | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/NATIVE/` |
| semantic release research | `LIBRARY/GEN-01/RED/SOURCE/GB/CART/<RELEASE-ID>/DOMAINS/` |
| same-game release comparison | `LIBRARY/GEN-01/RED/COMPARE/<COMPARISON-ID>/` |
| game-wide parser/schema | `LIBRARY/GEN-01/RED/SHARED/` |
| external disassembly/reference | `LIBRARY/GEN-01/RED/REFERENCE/<REFERENCE-ID>/` |
| modernization/localization design | `PROJECTS/RED-MODERNIZATION/DESIGN/` |
| latest-official crosswalk | `PROJECTS/RED-MODERNIZATION/CROSSWALK/` |
| derived-target verification | `PROJECTS/RED-MODERNIZATION/VERIFICATION/` |
| production assets/patch/build | Tsubaki `PROJECTS/RED-MODERNIZATION/...` |
| repository-wide schema/registry/migration tooling | `INFRA/` |

Legacy `GAMES/`, `GENERATION-*`, standalone `GEN-*`, old v4 `LIBRARY/GEN-XX/<PLATFORM>/<GAME>/RELEASES/...`, `_SHARED`, `MULTI`, `REV-ALL`, `ALL`, `MISC`, `OTHER`, `GENERAL`, and `REV-UNKNOWN` receive no new RED work.

Canonical RED source releases: `JP-JA-HV0`, `JP-JA-HV1`, `US-EU-EN-HV0`, `EU-DE-HV0`, `EU-FR-HV0`, `EU-IT-HV0`, `EU-ES-HV0`.
