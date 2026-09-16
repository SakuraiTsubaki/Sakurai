# Bank audit summary

## Coverage
- Japanese Red Rev0: banks `00-1F` (32 banks)
- Japanese Red RevA: banks `00-1F` (32 banks)
- English/German/French/Italian/Spanish Red: banks `00-3F` (64 banks each)
- Total unique-ROM banks audited: 384

## International layout reference
- `00`: vectors / header / home
- `01-1F`: engine, audio, maps, graphics, battle systems and support data
- `20-2A`: text banks 1-11
- `2B`: Pokédex text
- `2C`: move names
- `2D-3F`: zero-filled unused banks in all five uploaded international builds

## Strong cross-language invariants
- Bank `1B` is byte-for-byte identical across EN/DE/FR/IT/ES.
- Banks `2D-3F` are byte-for-byte identical and entirely zero-filled across EN/DE/FR/IT/ES: 19 banks = 304 KiB.
- Bank `1F` has 16,381 / 16,384 bytes identical at the same offsets across all five international builds (99.9817%).
- Bank `02` has 16,370 / 16,384 bytes identical (99.9146%).
- Bank `0A` has 16,368 / 16,384 bytes identical (99.9023%).
- Bank `0B` has 16,355 / 16,384 bytes identical (99.8230%).
- Bank `0C` has 16,364 / 16,384 bytes identical (99.8779%).
- Bank `19` has 16,346 / 16,384 bytes identical (99.7681%).

## Language-heavy banks
International text banks `20-29` have low same-offset identity because localization changes string lengths and pointer placement. `2B` (Pokédex text) is likewise highly language-dependent. `2A` and `2C` retain much higher commonality because large portions of those banks remain structurally shared or unused.

## Japanese layout differences
Japanese Rev0/RevA use 32-bank MBC1 ROMs. Their bank roles largely correspond to the international engine/map/audio organization, but names/text placement differs substantially: for example Move Names are in Japanese bank `04`, while international Move Names are in bank `2C`. Japanese banks also preserve explicit garbage/padding regions that are useful for revision archaeology.

## Verification
All 384 generated bank scaffolds were re-read from their emitted `db` directives. Concatenating them reproduced each of the seven source ROMs byte-for-byte and matched the recorded SHA-256 values.
