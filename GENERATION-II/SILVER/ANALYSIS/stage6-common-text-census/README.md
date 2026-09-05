# Pokémon Silver Stage 6 — Common Text Census

Direct binary grammar parse of localized common-text banks `64`–`66`.

## Results

| Language | Streams | Literals | Used bytes | Literal bytes | Unknown codes |
|---|---:|---:|---:|---:|---:|
| EN | 655 | 810 | 19,532 | 17,731 | 0 |
| DE | 659 | 800 | 21,812 | 20,011 | 0 |
| FR | 655 | 801 | 19,391 | 17,607 | 0 |
| IT | 655 | 807 | 19,641 | 17,868 | 0 |
| ES | 659 | 828 | 20,160 | 18,289 | 0 |
| KR | 641 | 874 | 23,361 | 21,430 | 0 |

Total: **3,924 text streams / 4,920 literal payloads**.

Every bank parses continuously from offset `0000` to its final text stream; remaining bank bytes are all zero padding. Parsing is stateful: bytes `01`–`16` are TX commands at command boundaries, while KR bytes `01`–`0B` are two-byte Hangul lead bytes inside literal payloads. `<DONE>` / `<PROMPT>` are accepted as text-stream terminals.

All six localized corpora decode with **zero unresolved character codes** after resolving language-specific compressed glyphs/tokens (`…`, French contractions, Italian `ì`, Spanish `¡`, etc.).

## Outputs
- `common_text_stream_inventory_6localized.csv`
- `common_text_literal_inventory_6localized.csv`
- `common_text_summary.csv`
- `common_text_command_counts.csv`
- `common_text_decode_unknowns.csv`
- `stage6_common_text_census.py`
