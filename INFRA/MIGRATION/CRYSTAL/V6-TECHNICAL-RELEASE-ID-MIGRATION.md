# Pokémon Crystal v6 technical release-ID migration

The seven supplied Crystal ROMs were re-read directly. Their verified four-byte header tokens at `0x013F–0x0142` are now the canonical release identity spine.

| legacy live ID | canonical v6 ID | observed SHA-1 |
|---|---|---|
| `JP-JA-HV0` | `BXTJ-HV0` | `95127b901bbce2407daf43cce9f45d4c27ef635d` |
| `US-EU-EN-HV0` | `BYTE-HV0` | `f4cd194bdee0d04ca4eac29e09b8e4e9d818c133` |
| `US-EU-EN-HV1` | `BYTE-HV1` | `f2f52230b536214ef7c9924f483392993e226cfb` |
| `EU-DE-HV0` | `BYTD-HV0` | `accb584293ba056152f1fd908439b019017ff2fe` |
| `EU-FR-HV0` | `BYTF-HV0` | `c055992b16b7399c687647725cdd1f4f13a2f75c` |
| `EU-IT-HV0` | `BYTI-HV0` | `6cee05e5b95beeae74b8365ad18ec4a07a8c4af8` |
| `EU-ES-HV0` | `BYTS-HV0` | `889a06fc0bb863666865aa69def0adf97945ac2a` |

The old market/language directories are migration aliases only. They must not coexist as second release owners after this migration. Market and language remain metadata in each canonical release identity.

The exact observed files remain under `DUMPS/UPLOAD-<SHA1-8>` beneath the canonical release. No original ROM binary or whole raw-bank dump is committed.

Comparison material is rewritten to the canonical IDs. Project locks for Crystal localization and downstream integrations must resolve to the technical IDs.
