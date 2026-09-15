# Generation I — Completion Matrix

This matrix prevents representative coverage from being mistaken for full Generation I coverage.

Legend: `NS` not started · `INV` inventory · `IP` in progress · `OBS` observed · `REP` reproduced · `MATCH` byte/data matched · `N/A` not applicable.

| Category | Aka R0 | Aka R1 | Midori R0 | Midori R1 | Ao | Pikachu R0 | Pikachu R1 | Pikachu R2 | Pikachu R3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ROM identity / hashes | MATCH | MATCH | MATCH | MATCH | INV | INV | INV | INV | INV |
| Bank inventory | MATCH | MATCH | MATCH | MATCH | IP | IP | IP | IP | IP |
| Bank 00 code reconstruction | IP | IP | IP | IP | IP | IP | IP | IP | IP |
| Banks 01+ code reconstruction | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Symbols / address map | IP | IP | IP | IP | IP | IP | IP | IP | IP |
| Pokémon / internal IDs / base data | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Evolutions / learnsets / TM-HM | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Moves / effects | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Types / effectiveness | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Items / TM-HM / key items | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Maps / interiors | NS | NS | NS | NS | IP | NS | NS | NS | NS |
| Blocks / tilesets / collision | NS | NS | IP | IP | NS | NS | NS | NS | NS |
| Connections / warps | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| NPCs / objects | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Trainers / parties / AI | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Wild encounters | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Gifts / trades / fixed encounters | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Events / scripts / flags | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Progression dependencies | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Text encoding / fonts / control codes | NS | NS | IP | IP | NS | NS | NS | NS | NS |
| Dialogue / menus / UI | NS | NS | IP | IP | NS | NS | NS | NS | NS |
| Pokémon graphics | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Trainer / overworld graphics | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Tiles / title / battle UI / effects | NS | NS | IP | IP | NS | NS | NS | NS | NS |
| BGM / SFX / cries | NS | NS | IP | IP | NS | IP | IP | IP | IP |
| Battle system | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Field system | IP | IP | IP | IP | IP | IP | IP | IP | IP |
| Save / SRAM | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Link trade / battle | NS | NS | IP | IP | NS | NS | NS | NS | NS |
| Unused / dummy / debug | NS | NS | NS | NS | IP | IP | IP | IP | IP |
| Bugs / glitches / special behavior | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Version/revision differences | IP | IP | IP | IP | INV | IP | IP | IP | IP |
| Regional/localization comparison | INV | INV | INV | INV | INV | INV | INV | INV | INV |
| Later Kanto/system comparison | NS | NS | NS | NS | NS | NS | NS | NS | NS |
| Integration candidate classification | NS | NS | NS | NS | NS | NS | NS | NS | NS |

## Current Bank 00 boundaries

- Aka Rev 0 / Rev 1: reconstructed through `$01C3`; next `$01C4`.
- Midori Rev 0 / Rev 1: reconstructed through `$0BF0`; next `$0BF1`.
- Ao: reconstructed through `$035E`; next `$035F`.
- Pikachu Rev 0 / 1 / 2 / 3: reconstructed through `$01AE`; next `$01AF`.

## Update rule

A cell advances only when evidence exists for that exact target. Similarity to another RGBY version is never sufficient by itself. Regional/localized releases will receive additional columns after their ROM identities/revisions are fully inventoried.
