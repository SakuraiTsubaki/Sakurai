# Silver v4 -> v5 migration

Canonical root: `LIBRARY/GEN-02/SILVER/SOURCE/GBC/CART/<RELEASE-ID>/`.

For these supplied Silver ROMs, the stable four-byte technical token observed at header bytes `0x013F-0x0142` is used with the header-version byte. This is only used when actually observed; it is not generalized to every GB/GBC title.

Mapping: `JP-JA-HV0` -> `AAXJ-HV0`; `JP-JA-HV1` -> `AAXJ-HV1`; `US-EU-EN-HV0` -> `AAXE-HV0`; `EU-DE-HV0` -> `AAXD-HV0`; `EU-FR-HV0` -> `AAXF-HV0`; `EU-IT-HV0` -> `AAXI-HV0`; `EU-ES-HV0` -> `AAXS-HV0`; `KR-KO-HV0` -> `AAXK-HV0`.

Old live Silver v4 paths under `LIBRARY/GEN-02/GBC/SILVER/` are removed after equivalent v5 identities, dump metadata, comparison data, and project bindings are recreated. Git history remains the archive.
