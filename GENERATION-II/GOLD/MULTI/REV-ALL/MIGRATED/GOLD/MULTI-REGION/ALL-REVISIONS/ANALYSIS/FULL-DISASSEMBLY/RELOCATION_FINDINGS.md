# Relocation findings

## European bank $27

English Gold bank `$27` is all-zero. Spanish/German/French/Italian Gold populate the beginning of `$27`. A unique 6-byte anchor scan maps this content to English logical bank `$24`; the opening routine has the same opcode skeleton as English bank `$24` around CPU `$6355`, with relocated pointer bases. English bank `$24` contains phone, RTC time-set, Pokégear, landmarks, fishing and slot-machine code/data.

This is therefore treated as a localization overflow/relocation bank, not an independent English-style bank `$27` role.

## European bank $58

English Gold bank `$58` is all-zero. All four European localized ROMs populate `$58`. Unique-anchor analysis maps the bank to English logical bank `$56` (Map Scripts 21). The first decoded text is the localized Route 32–Ruins of Alph Gate dialogue/sign text (e.g. `RUINAS ALFA`, `ALPH-RUINEN`, `RUINES D'ALPHA`, `ROVINE D'ALFA`).

Thus `$58` is a second localization overflow/relocation bank used for map-script/text content.

## Korean high banks

Relative to English, Korean Gold uniquely populates `$71`, `$72`, `$78`, `$79`, `$7A`, `$7B`; it leaves `$6A/$6B` zero because the Pokédex is packed into `$68/$69`. Current semantic labels: `$72` DMG error screen, `$78–$7A` Hangul tables, `$7B` diploma GFX, `$71` unresolved Korean-specific content.
