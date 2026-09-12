# RED v4.1 routing

Every new RED artifact is classified by semantic ownership before a path is chosen.

| Artifact | Canonical owner |
|---|---|
| official build identity | `LIBRARY/GEN-01/GB/RED/RELEASES/<RELEASE-ID>/MANIFESTS/` |
| exact supplied file observation | `LIBRARY/GEN-01/GB/RED/RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/` |
| release-specific research | `LIBRARY/GEN-01/GB/RED/RELEASES/<RELEASE-ID>/<DOMAIN>/` |
| cross-release comparison | `LIBRARY/GEN-01/GB/RED/COMPARISONS/<COMPARISON-ID>/` |
| game-wide parser/schema | `LIBRARY/GEN-01/GB/RED/SHARED/` |
| modernization/localization design | `PROJECTS/RED-MODERNIZATION/DESIGN/` |
| crosswalk/latest-official mapping | `PROJECTS/RED-MODERNIZATION/CROSSWALK/` |
| research verification of derived target | `PROJECTS/RED-MODERNIZATION/VERIFICATION/` |
| production assets/patch/build | Tsubaki `PROJECTS/RED-MODERNIZATION/...` |
| repository-wide schema/registry/migration tooling | `INFRA/` |

Legacy `GAMES/`, `GENERATION-*`, standalone `GEN-*`, `META/`, `MULTI`, `REV-ALL`, `ALL`, and `MULTI-REGION` paths are frozen migration inputs and receive no new RED work.

The seven canonical RED source release IDs are `JP-JA-HV0`, `JP-JA-HV1`, `US-EU-EN-HV0`, `EU-DE-HV0`, `EU-FR-HV0`, `EU-IT-HV0`, and `EU-ES-HV0`.
