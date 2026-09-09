# Symbol propagation summary: Bank $20-$2F

- Mapping rows: 648 (81 English anchors × 8 ROMs)
- Source CSV SHA-256: `1e002f9f7d71a9dabe6d8cd1fd0c314b683dfd925f783983616ff0d33025701b`

| Region | High | Medium | Low | Unmapped |
|---|---:|---:|---:|---:|
| EN | 81 | 0 | 0 | 0 |
| KR | 63 | 5 | 3 | 10 |
| JP-Rev0 | 56 | 9 | 5 | 11 |
| JP-RevA | 56 | 9 | 5 | 11 |
| ES | 73 | 6 | 0 | 2 |
| DE | 74 | 5 | 0 | 2 |
| FR | 72 | 7 | 0 | 2 |
| IT | 73 | 6 | 0 | 2 |

Matching method: 48-byte English baseline windows are decomposed into non-trivial six-byte anchors. Candidate positions vote for a consistent target origin; byte equality and vote margin determine confidence. EU English-bank $24 anchors also search regional bank $27 to detect localization relocation. Low/unmapped results are not treated as semantic identity.
