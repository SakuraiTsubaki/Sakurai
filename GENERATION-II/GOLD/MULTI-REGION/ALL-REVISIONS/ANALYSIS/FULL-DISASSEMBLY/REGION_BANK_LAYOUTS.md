# Region-specific bank layout notes

## English / western baseline (`pret/pokegold`)

Uploaded English Gold exactly matches the documented `pret/pokegold` Gold build target. Important regions: `$00` vectors/header/home; `$0D` effect commands; `$0E` enemy trainers; `$0F` battle core; `$10` evolutions/attacks; `$12-$20` pictures; `$25` maps/events; `$30-$31` sprites; `$3A-$3D` audio; `$40` standard scripts; `$41` phone scripts; `$42-$62` map scripts; `$64-$66` text; `$68-$6B` Pokédex; `$6C` names; `$6D` move descriptions; `$6E` item descriptions; `$70` tileset/Pokégear/credits; `$7F` Stadium 2 checksum tail.

German/French/Italian/Spanish use this as the working structural baseline, with offsets verified against each ROM rather than assumed.

## Japanese Gold Rev 0 / Rev A (`Narishma-gb/pokesilver`)

Japanese Gold is 64 banks (`$00-$3F`) and is packed differently from the 2 MiB western layout. Notable roles: `$11` Pokédex entries + Pokémon Mail; `$13` map scripts 1; `$22` map scripts 2; `$26-$29` map scripts 3-6; `$2C-$2D` map scripts 7-8; `$2F` map scripts 9; `$34-$35` map scripts 10-11; `$36` standard scripts + phone scripts + map scripts 12; `$39` copyright/title/options/inverted font/intro; `$3A-$3D` audio; `$3F` final bank.

## Korean Gold (`Narishma-gb/pokegold-kr`)

Korean Gold is 128 banks and follows much of the western layout but adds/relocates Korean-specific data. `$25` holds maps/events (WIP layout places Events at CPU `$65F9`); `$40-$53` identified script banks; `$54-$62` unresolved/commented in the WIP layout; `$68` Pokédex 001-128; `$69` Pokédex 129-251; `$6C` names; `$6D` move descriptions; `$6E` item descriptions; `$71` unresolved Korean bank; `$72` DMG error screen; `$78-$7A` Hangul tables; `$7B` Diploma GFX; `$7F` Korean-specific tail handling.
