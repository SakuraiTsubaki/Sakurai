# Pokémon Sapphire ROM Inventory

Generated from the uploaded read-only ROM set for the SAPPHIRE project.

- Generation: III
- Game: SAPPHIRE
- Work type: ANALYSIS
- Original ROM binaries: **not stored in GitHub**
- Purpose: identification, revision tracking, checksum verification, and routing of future work products

## Verified ROMs

| Language / Region | Revision | File | Size | Game code | Header version | SHA-1 | MD5 |
|---|---:|---|---:|---|---:|---|---|
| Japanese / Japan | REV-0 | Pocket Monsters - Sapphire (Japan).gba | 8,388,608 | AXPJ | 0 | 3233342c2f3087e6ffe6c1791cd5867db07df842 | 5323f95f70f5d4f21bed6ec000332bda |
| German / Germany | REV-1 | Pokemon - Saphir-Edition (Germany) (Rev 1).gba | 16,777,216 | AXPD | 1 | 7e6e034f9cdca6d2c4a270fdb50a94def5883d17 | 9d816b369343d39b94af9a8b0ce7f63b |
| English / Europe | REV-1 | Pokemon - Sapphire Version (Europe) (Rev 1).gba | 16,777,216 | AXPE | 1 | 4722efb8cd45772ca32555b98fd3b9719f8e60a9 | 3a32fd98b065283d09eeba1ce0542888 |
| English / USA | REV-0 | Pokemon - Sapphire Version (USA).gba | 16,777,216 | AXPE | 0 | 3ccbbd45f8553c36463f13b938e833f652b793e4 | f34e91399c719812e66e2c828a2e93d7 |
| English / USA-Europe | REV-2 | Pokemon - Sapphire Version (USA, Europe) (Rev 2).gba | 16,777,216 | AXPE | 2 | 89b45fb172e6b55d51fc0e61989775187f6fe63c | 9bc2b765ca6997175fac51e6cdc29089 |
| French / France | REV-0 | Pokemon - Version Saphir (France).gba | 16,777,216 | AXPF | 0 | c269b5692b2d0e5800ba1ddf117fda95ac648634 | 2e6e9e3b87f99f04a1ac44b01bfa6ecd |
| French / France | REV-1 | Pokemon - Version Saphir (France) (Rev 1).gba | 16,777,216 | AXPF | 1 | 860e93f5ea44f4278132f6c1ee5650d07b852fd8 | c59c79d8bfacd27a1c3fafda2bd801d0 |
| Italian / Italy | REV-0 | Pokemon - Versione Zaffiro (Italy).gba | 16,777,216 | AXPI | 0 | f729dd571fb2c09e72c5c1d68fe0a21e72713d34 | f42847fa81d5d1cf30d1dd5b64924561 |
| Italian / Italy | REV-1 | Pokemon - Versione Zaffiro (Italy) (Rev 1).gba | 16,777,216 | AXPI | 1 | 73edf67b9b82ff12795622dca412733755d2c0fe | b075dcf2b63a992e10204b553800ff40 |

## Header observations

All nine ROMs identify as `POKEMON SAPP` in the GBA header and use maker code `01`.

The revision routing convention is derived from the header version byte:

- `0` → `REV-0`
- `1` → `REV-1`
- `2` → `REV-2`

The Japanese dump is 8 MiB; the other eight dumps are 16 MiB.

## Repository routing rule

All future project outputs must use this hierarchy:

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

Examples:

- `GENERATION-III/SAPPHIRE/JAPANESE-JAPAN/REV-0/ANALYSIS/`
- `GENERATION-III/SAPPHIRE/ENGLISH-USA/REV-0/SOURCE/`
- `GENERATION-III/SAPPHIRE/FRENCH-FRANCE/REV-1/PATCH/`
- `GENERATION-III/SAPPHIRE/ITALIAN-ITALY/REV-1/EXTRACT/`

Original copyrighted ROM binaries remain read-only local inputs and are never committed. Analysis documents, source code, patches, metadata, checksums, and distributable extracted/derived assets may be committed according to their work type.
