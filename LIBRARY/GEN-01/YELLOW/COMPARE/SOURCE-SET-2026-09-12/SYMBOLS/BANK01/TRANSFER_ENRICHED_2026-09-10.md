# Bank 01 symbol transfer — exact + opcode-normalized

Pass 1 required a unique exact 12–32 byte window. Pass 2 fills unresolved function starts by matching 6–14 decoded instruction opcodes while ignoring immediate operands/addresses. A mapping is accepted only when the opcode signature occurs exactly once in the target bank.

| Symbol | EN | JPD | FR | DE | IT | ES | JP0A | JPB | JPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PrintSafariZoneBattleText | `$4111` | `$4111` | `$4111` (exact24) | `$4111` (exact24) | `$4111` (exact24) | `$4111` (exact24) | `$4111` (exact24) | `$4111` (exact32) | `$4111` (exact32) |
| PrepareTitleScreen | `$414B` | `$416A` | `$414B` (opcode14) | `$414B` (opcode14) | `$414B` (opcode14) | `$414B` (opcode14) | `$416A` (exact32) | `$416A` (exact32) | `$416A` (exact32) |
| DisplayTitleScreen | `$4171` | `$4190` | `$4171` (opcode14) | `$4171` (opcode14) | `$4171` (opcode14) | `$4171` (opcode14) | `$4190` (opcode14) | `$4190` (exact32) | `$4190` (exact32) |
| LoadMonData_ | `$442B` | `$4438` | `$442C` (opcode14) | `$442C` (opcode14) | `$442C` (opcode14) | `$442C` (opcode14) | `$4438` (exact24) | `$4438` (exact32) | `$4438` (exact32) |
| PrepareOAMData | `$499B` | `$48F7` | `$4A17` (opcode14) | `$4996` (opcode14) | `$49EB` (opcode14) | `$49D4` (opcode14) | `$48F7` (exact12) | `$48F7` (exact32) | `$48F7` (exact32) |
| PrintWaitingText | `$4B89` | `$4AD7` | `$4C05` (opcode12) | `$4B84` (opcode12) | `$4BD9` (opcode12) | `$4BC2` (opcode12) | `$4AD7` (exact12) | `$4AD7` (exact32) | `$4AD7` (exact32) |
| _UpdateSprites | `$4BB7` | `$4B05` | `$4C32` (exact16) | `$4BB4` (exact16) | `$4C06` (exact16) | `$4BF0` (exact16) | `$4B05` (exact32) | `$4B05` (exact32) | `$4B05` (exact32) |
| DetectCollisionBetweenSprites | `$4BF7` | `$4B45` | `$4C72` (exact12) | `$4BF4` (exact12) | `$4C46` (exact12) | `$4C30` (exact12) | `$4B45` (exact32) | `$4B45` (exact32) | `$4B45` (exact32) |
| PickUpItem | `$4D55` | `$4CA3` | `$4DD0` (opcode14) | `$4D52` (opcode14) | `$4DA4` (opcode14) | `$4D8E` (opcode14) | `$4CA3` (opcode14) | `$4CA3` (exact32) | `$4CA3` (exact32) |
| UpdatePlayerSprite | `$4DA5` | `$4D08` | `$4E20` (exact32) | `$4DA2` (exact32) | `$4DF4` (exact32) | `$4DDE` (exact32) | `$4D08` (exact32) | `$4D08` (exact32) | `$4D08` (exact32) |
| CableClub_DoBattleOrTrade | `$53A5` | `$52FB` | `$5420` (opcode14) | `$53A2` (opcode14) | `$53F4` (opcode14) | `$53DE` (opcode14) | `$52FB` (opcode14) | `$52FB` (exact32) | `$52FB` (exact32) |
| MainMenu | `$5BA6` | `$5ACC` | `$5C22` (opcode14) | `$5BAE` (opcode14) | `$5BEF` (opcode14) | `$5BE3` (opcode14) | `$5ACC` (exact16) | `$5ACC` (exact32) | `$5ACC` (exact32) |
| PrepareOakSpeech | `$5E27` | `$5D86` | `$5EB0` (opcode14) | `$5E3C` (opcode14) | `$5E76` (opcode14) | `$5E6E` (opcode14) | `$5D86` (exact24) | `$5D86` (exact32) | `$5D86` (exact32) |
| OakSpeech | `$5E85` | `$5DE4` | `$5F0E` (opcode14) | `$5E9A` (opcode14) | `$5ED4` (exact12) | `$5ECC` (opcode14) | `$5DE4` (opcode14) | `$5DE4` (exact32) | `$5DE4` (exact32) |
| PrepareForSpecialWarp | `$6042` | `$60E6` | `$60CB` (opcode14) | `$6057` (opcode14) | `$6091` (opcode14) | `$6089` (opcode14) | `$60E6` (opcode14) | `$60E6` (exact32) | `$60E6` (exact32) |
| AskName | `$625D` | `$6301` | `$62E6` (opcode14) | `$6272` (opcode14) | `$62AC` (opcode14) | `$62A4` (opcode14) | `$6301` (opcode14) | `$6301` (exact32) | `$6301` (exact32) |
| DisplayNamingScreen | `$6307` | `$63BB` | `$6390` (opcode14) | `$631C` (opcode14) | `$6356` (opcode14) | `$634E` (opcode14) | `$63BB` (opcode14) | `$63BB` (exact32) | `$63BB` (exact32) |
| PrintAlphabet | `$64ED` | `$6585` | `$6576` (opcode14) | `$6502` (opcode14) | `$653C` (opcode14) | `$6534` (opcode14) | `$6585` (exact32) | `$6585` (exact32) | `$6585` (exact32) |
| ChoosePlayerName | `$66DB` | `$675F` | `$675E` (opcode14) | `$66F1` (opcode14) | `$671F` (opcode14) | `$6722` (opcode14) | `$675F` (exact32) | `$675F` (exact32) | `$675F` (exact32) |
| HandleItemListSwapping | `$68C9` | `$6966` | `$6942` (opcode14) | `$68CB` (opcode14) | `$6901` (opcode14) | `$6914` (opcode14) | `$6966` (opcode14) | `$6966` (exact32) | `$6966` (exact32) |
| DisplayPokemartDialogue_ | `$69A5` | `$6A42` | `$6A1E` (opcode14) | `$69A7` (opcode14) | `$69DD` (opcode14) | `$69F0` (opcode14) | `$6A42` (opcode14) | `$6A42` (exact32) | `$6A42` (exact32) |
| LearnMove | `$6BC8` | `$6D36` | `$6C41` (opcode14) | `$6BCA` (opcode14) | `$6C00` (opcode14) | `$6C13` (opcode14) | `$6D36` (opcode14) | `$6D36` (exact32) | `$6D36` (exact32) |
| DisplayPokemonCenterDialogue_ | `$6D97` | `$6FD8` | `$6E10` (opcode14) | `$6D99` (opcode14) | `$6DCF` (opcode14) | `$6DE2` (opcode14) | `$6FD8` (opcode14) | `$6FD8` (exact32) | `$6FD8` (exact32) |
| DisplayTextIDInit | `$6F0E` | `$71D5` | `$6F87` (opcode14) | `$6F10` (opcode14) | `$6F46` (opcode14) | `$6F59` (opcode14) | `$71D5` (exact32) | `$71D5` (exact32) | `$71D5` (exact32) |
| DrawStartMenu | `$6F80` | `$7247` | `$6FF9` (opcode14) | `$6F82` (opcode14) | `$6FB8` (opcode14) | `$6FCB` (opcode14) | `$7247` (exact16) | `$7247` (exact32) | `$7247` (exact32) |
| CableClubNPC | `$7035` | `$72F0` | `$70B2` (opcode14) | `$7039` (opcode14) | `$706E` (opcode14) | `$7084` (opcode14) | `$72F0` (opcode14) | `$72F0` (exact32) | `$72F0` (exact32) |
| DisplayTextBoxID_ | `$71BF` | `$7544` | `$723C` (opcode14) | `$71C3` (opcode14) | `$71F8` (opcode14) | `$720E` (opcode14) | `$7544` (exact32) | `$7544` (exact32) | `$7544` (exact32) |
| DisplayMoneyBox | `$738F` | `$7715` | `$73D7` (opcode10) | `$735C` (opcode14) | `$738F` (opcode14) | `$73A9` (opcode10) | `$7715` (opcode14) | `$7715` (exact32) | `$7715` (exact32) |
| DoBuySellQuitMenu | `$73BE` | `$774D` | `$740F` (opcode14) | `$7383` (opcode14) | `$73B6` (opcode14) | `$73E1` (opcode14) | `$774D` (exact16) | `$774D` (exact32) | `$774D` (exact32) |
| DisplayTwoOptionMenu | `$742D` | `$77BC` | `$747E` (opcode14) | `$73F2` (opcode14) | `$7425` (opcode14) | `$7450` (opcode14) | `$77BC` (exact32) | `$77BC` (exact32) | `$77BC` (exact32) |
| DisplayFieldMoveMonMenu | `$758A` | `$7906` | `$75DF` (exact12) | `$7554` (exact12) | `$7579` (exact12) | `$75AA` (exact12) | `$7906` (exact24) | `$7906` (exact32) | `$7906` (exact32) |
| DrainHPEffect_ | `$76E7` | `$7A10` | `$773A` (opcode14) | `$76C2` (opcode14) | `$76DA` (opcode14) | `$7715` (opcode14) | `$7A10` (exact32) | `$7A10` (exact32) | `$7A10` (exact32) |
| PlayerPC | `$778E` | `$7ACD` | `$77E1` (opcode14) | `$7769` (opcode14) | `$7781` (opcode14) | `$77BC` (opcode14) | `$7ACD` (opcode14) | `$7ACD` (exact32) | `$7ACD` (exact32) |
| _RemovePokemon | `$7A0F` | `$7DED` | `$7A69` (opcode14) | `$79F2` (opcode14) | `$7A0C` (opcode14) | `$7A43` (opcode14) | `$7DED` (exact32) | `$7DED` (exact32) | `$7DED` (exact32) |
| _DisplayPokedex | `$7ABF` | `$7E9D` | `$7B19` (opcode14) | `$7AA2` (opcode14) | `$7ABC` (opcode14) | `$7AF3` (opcode14) | — | `$7E9D` (exact32) | `$7E9D` (exact32) |
