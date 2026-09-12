# GB/GBC technical release IDs — v6

When bytes `0x013F-0x0142` are verified to expose a stable four-byte product token, v6 prefers that token over market/language fallback labels. Header version remains an independent `HV<n>` suffix.

Direct verification against the currently supplied ROM inputs establishes the following canonical technical IDs:

| Game / supplied image | token | header version | canonical release ID |
|---|---|---:|---|
| Pocket Monsters Geum (Korea) | `AAUK` | 0 | `AAUK-HV0` |
| Pocket Monsters Eun (Korea) | `AAXK` | 0 | `AAXK-HV0` |
| Pocket Monsters Crystal (Japan) | `BXTJ` | 0 | `BXTJ-HV0` |
| Pokémon Crystal USA/Europe | `BYTE` | 0 | `BYTE-HV0` |
| Pokémon Crystal USA/Europe Rev A | `BYTE` | 1 | `BYTE-HV1` |
| Pokémon Kristall-Edition (Germany) | `BYTD` | 0 | `BYTD-HV0` |
| Pokémon Version Cristal (France) | `BYTF` | 0 | `BYTF-HV0` |
| Pokémon Versione Cristallo (Italy) | `BYTI` | 0 | `BYTI-HV0` |
| Pokémon Edición Cristal (Spain) | `BYTS` | 0 | `BYTS-HV0` |

Rules:

- The technical token must be read directly from the ROM header; it is never guessed from filename, language, or region.
- `HV<n>` is the header version byte and is independent of preservation-set labels such as `Rev A`.
- Market/language labels remain metadata and may be used as path fallbacks only when no stronger verified technical token exists.
- Once a technical token is verified, the market/language fallback path becomes a migration alias only and must not remain a second live release owner.
- Exact observed files remain separate `DUMPS/<DUMP-ID>` children of the canonical release.
