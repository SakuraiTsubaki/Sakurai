# GB/GBC technical release IDs — v6

When bytes `0x013F-0x0142` are verified to expose a stable four-byte product token, v6 prefers that token over market/language fallback labels. Header version remains an independent `HV<n>` suffix.

Direct verification on the current Generation V → ポケットモンスター ROM inputs established:

| Game / supplied image | token | header version | canonical release ID |
|---|---|---:|---|
| Pocket Monsters Geum (Korea) | `AAUK` | 0 | `AAUK-HV0` |
| Pocket Monsters Eun (Korea) | `AAXK` | 0 | `AAXK-HV0` |
| Pocket Monsters Crystal (Japan) | `BXTJ` | 0 | `BXTJ-HV0` |
| Pokémon Crystal USA/Europe Rev A | `BYTE` | 1 | `BYTE-HV1` |

This does not authorize guessing tokens for other GB/GBC releases. A token must be observed and verified per release. Market/language labels remain metadata and are valid path fallbacks only when no stronger native identifier has been established.
