# Pokémon Silver KR Stage 5 — Charset & Core Text Census

## Result
The Korean two-byte character system has now been reconstructed from the ROM's own Hangul graphics tables and checked against the public `pokegold-kr` charmap/source.

- Two-byte codes defined: **2,419**
- Hangul codes under lead bytes `01`–`0A`: **2,353**
  - KS X 1001 syllables actually present: **2,348**
  - Added non-Wansung syllables: **5**
- Special two-byte table `0B`: **66** codes
- KS X 1001 syllables intentionally absent: **2** (`댜`, `돐`)

This yields the exact **2,419 two-byte code definitions** used by the KR build.

## Custom Hangul deviations
- Removed: `02:F4 = 댜`, `03:1B = 돐`
- Added: `03:D0 = 뢔`, `06:2F = 쌰`, `06:30 = 쎼`, `06:A0 = 쓔`, `08:30 = 쬬`

The five additions and two omissions explain why a naive KS X 1001 decoder drifts even though most of the table follows Wansung order.

## Full decoded corpora
- Names bank `6C`: **830 records** = 256 items + 67 stored trainer-class strings (66 official classes + 1 unused `MYSTICALMAN`) + 256 Pokémon slots + 251 moves.
- Item/move descriptions: **512 records**.
- Pokédex: **251 records**.
- Unknown/unmapped codes across all three corpora: **0**.

## Binary layout
The KR Names bank contains 830 stored records. The exact bank-6C boundaries are:
- Items: `6C:0000–09A0`
- Trainer-class strings including unused `수수께끼의 청년`: `6C:09A1–0C49`
- Pokémon fixed-width table: `6C:0C4A–1649`
- Moves: `6C:164A–1EE0`
- Remaining bank `6C:1EE1–3FFF`: zero-filled.

The Western EN/DE/FR/IT/ES name corpus remains **829 records** because those builds store only the 66 official trainer classes.

## Cross-validation
All five source checks pass, including:
- `이상해씨`
- Master Ball: `포켓몬을 반드시 잡을 수 있는 / 최고의 볼`
- Bulbasaur category `씨앗`
- Bulbasaur Pokédex description beginning `태어날 때부터 등에 씨앗을…`

## Outputs
- `kr_two_byte_charmap_2419.csv`
- `kr_charmap_anomalies.csv`
- `kr_name_inventory_830.csv`
- `kr_description_inventory_512.csv`
- `kr_pokedex_inventory_251.csv`
- `kr_decode_unknowns.csv`
- `kr_decoder_cross_validation.csv`
- `kr_charset_text_summary.csv`
- `stage5_kr_charset_text_census.py`
