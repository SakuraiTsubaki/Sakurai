# Pokémon Crystal 7-ROM Semantic Bank Census

This is the second-pass bank census: it keeps the 128-bank byte survey, but adds semantic role, reconstruction status, nearest exact-source anchor for German/Italian, and work priority. English roles are anchored to pret/pokecrystal; Japanese to PikalaxALT/pokekuristaru; Spanish to erosunica/pokecrystal-es; French to qwilvove/pokecrystal-fr. Banks 75/76/79 are confirmed EU map-script expansions from the exact Spanish and French layouts.

## Executive findings

- 128 banks × 7 ROMs = 896 bank images surveyed.
- All-seven byte-identical banks (9): 30, 31, 37, 3B, 3C, 3D, 4B, 4C, 7A
- English Rev0→RevA changed banks (8): 00(4B), 10(9B), 11(2B), 3E(8B), 47(1B), 5C(546B), 7E(2B), 7F(12B)
- EU-only expansion: 75 = Map Scripts 26, 76 = Map Scripts 27, 79 = Map Scripts 28; 7A is all-zero in all seven.
- DE/IT have no exact semantic source repository confirmed in this survey, so per-bank nearest-anchor matching is used to prioritize reconstruction.
- Priority: A = relocation/revision-critical; B = code/script/text semantic reconstruction; C = graphics/audio/data alignment; D = byte-identical or directly reusable structure.

## Class counts

- audio: 5
- battle/code-data: 8
- engine/mixed: 16
- graphics/data: 42
- map-block: 3
- map-script: 25
- map-script (EU relocation): 3
- mobile/special: 11
- phone/script-text: 3
- text: 11
- unused/zero: 1

## Full 00–7F status

|Bank|Semantic role|Class|EN0→EN1 diff|DE nearest exact-source anchor|IT nearest exact-source anchor|Priority|
|---:|---|---|---:|---|---|:---:|
|00|ROM0: RST/interrupt vectors, Header, Home|engine/mixed|4|ES0 (8880 bytes)|ES0 (10426 bytes)|B|
|01|bank1: link/OAM/map objects/intro/learn/math/items/NPC/events|engine/mixed|0|FR0 (11783 bytes)|ES0 (6038 bytes)|B|
|02|bank2: player object/sine/predef/color|engine/mixed|0|ES0 (94 bytes)|ES0 (145 bytes)|B|
|03|bank3: time/specials/HP/overworld/items/step/PC/item effects|battle/code-data|0|EN0 (6886 bytes)|ES0 (13959 bytes)|B|
|04|bank4: pack/time/TMHM/naming/menu/events/party corrections|engine/mixed|0|FR0 (14082 bytes)|FR0 (11035 bytes)|B|
|05|bank5: RTC/overworld/save/map setup/PC/mart/mom/daycare/breeding|engine/mixed|0|ES0 (7696 bytes)|ES0 (6297 bytes)|B|
|06|Tileset Data 1|graphics/data|0|EN0/ES0/FR0 (80 bytes)|EN0 (40 bytes)|C|
|07|Roofs + Tileset Data 2 + Extra Songs 1|graphics/data|0|ES0 (0 bytes)|EN0/ES0/FR0 (2 bytes)|C|
|08|Clock Reset + Tileset Data 3 + Egg Moves|graphics/data|0|ES0 (12 bytes)|ES0 (13 bytes)|C|
|09|bank9: menus/battle menu/trainer card/decorations/move effects|battle/code-data|0|FR0 (8166 bytes)|FR0 (11469 bytes)|B|
|0A|bankA + Trainer Backpics|graphics/data|0|ES0 (12007 bytes)|ES0 (11876 bytes)|C|
|0B|bankB: trainer HUDs/class names/TMHM/start battle/etc|battle/code-data|0|FR0 (10918 bytes)|FR0 (10690 bytes)|B|
|0C|Tileset Data 4|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|0D|Effect Commands|battle/code-data|0|ES0 (7075 bytes)|EN0 (7020 bytes)|B|
|0E|Enemy Trainers / battle AI trainer data|battle/code-data|0|FR0 (8300 bytes)|ES0 (8214 bytes)|B|
|0F|Battle Core + effect command pointers|battle/code-data|0|ES0 (8782 bytes)|ES0 (2006 bytes)|B|
|10|Pokédex + move data + evolution engine + Evolutions/Attacks|engine/mixed|9|ES0 (12881 bytes)|FR0 (12099 bytes)|B|
|11|fruit trees/battle AI/Pokédex 2/mail|battle/code-data|2|ES0 (470 bytes)|FR0 (508 bytes)|B|
|12|Crystal Features 1 / mobile / Celebi / main menu|mobile/special|0|ES0 (7257 bytes)|FR0 (7561 bytes)|B|
|13|map palettes/collision/save/link/stats/evolution movie/etc|engine/mixed|0|FR0 (4232 bytes)|ES0 (4640 bytes)|B|
|14|party menu/events/types/stats/base stats/Pokémon names|engine/mixed|0|ES0 (13893 bytes)|ES0 (14983 bytes)|B|
|15|Map Scripts 1|map-script|0|FR0 (13745 bytes)|ES0 (12855 bytes)|B|
|16|Map Scripts 2|map-script|0|EN0 (15074 bytes)|EN0 (13566 bytes)|B|
|17|Map Scripts 3|map-script|0|EN0 (12666 bytes)|FR0 (11864 bytes)|B|
|18|Map Scripts 4|map-script|0|FR0 (8579 bytes)|FR0 (6776 bytes)|B|
|19|Crystal Phone Text|text|0|ES0 (13492 bytes)|EN0/ES0 (12503 bytes)|B|
|1A|Map Scripts 5|map-script|0|FR0 (12428 bytes)|ES0 (10687 bytes)|B|
|1B|Map Scripts 6|map-script|0|EN0 (14602 bytes)|FR0 (13150 bytes)|B|
|1C|Map Scripts 7|map-script|0|EN0 (14908 bytes)|FR0 (13234 bytes)|B|
|1D|Map Scripts 8|map-script|0|FR0 (13398 bytes)|EN0 (12480 bytes)|B|
|1E|Map Scripts 9|map-script|0|EN0 (14872 bytes)|FR0 (12958 bytes)|B|
|1F|Map Scripts 10|map-script|0|FR0 (14768 bytes)|EN0 (13165 bytes)|B|
|20|player movement/engine flags/variables/battle text|text|0|ES0 (7754 bytes)|FR0 (7354 bytes)|B|
|21|printer + battle animation gfx + Hall of Fame|graphics/data|0|ES0 (1002 bytes)|ES0 (1008 bytes)|C|
|22|Crystal Features 2 / Kurt/player gfx/mobile/Unown walls/Battle Tower rules|graphics/data|0|EN0 (12184 bytes)|FR0 (12102 bytes)|C|
|23|timeofday palettes/battle transition/field moves/sprite anims/icons|graphics/data|0|ES0 (64 bytes)|EN0 (82 bytes)|C|
|24|phone/RTC/Pokégear/fishing/slot machine|phone/script-text|0|FR0 (13440 bytes)|FR0 (13176 bytes)|B|
|25|Maps + Events|engine/mixed|0|FR0 (1887 bytes)|ES0 (5041 bytes)|B|
|26|Map Scripts 11|map-script|0|ES0 (11136 bytes)|ES0 (10194 bytes)|B|
|27|Map Scripts 12|map-script|0|FR0 (5129 bytes)|ES0 (4420 bytes)|B|
|28|Phone Scripts 1|phone/script-text|0|ES0 (5509 bytes)|EN0 (4967 bytes)|B|
|29|Phone Text|text|0|EN0 (9586 bytes)|EN0 (8925 bytes)|B|
|2A|Map Blocks 1|map-block|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|2B|Map Blocks 2|map-block|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|2C|Map Blocks 3|map-block|0|ES0 (46 bytes)|ES0 (39 bytes)|C|
|2D|Tileset Data 5|graphics/data|0|EN0/ES0/FR0 (40 bytes)|EN0 (20 bytes)|C|
|2E|map-name/hidden items/trees/radio/mail|engine/mixed|0|ES0 (5719 bytes)|ES0 (5296 bytes)|B|
|2F|Phone Scripts 2 + trainer scripts|phone/script-text|0|FR0 (8579 bytes)|EN0 (6507 bytes)|B|
|30|Sprites 1|graphics/data|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|31|Sprites 2|graphics/data|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|32|battle anim bg/effects + move animations ptr/The End|battle/code-data|0|ES0/FR0 (186 bytes)|ES0/FR0 (141 bytes)|B|
|33|Move Animations + Extra Songs 2|audio|0|ES0 (14923 bytes)|FR0 (13601 bytes)|C|
|34|Pic Animations 1|graphics/data|0|ES0 (1 bytes)|EN0/ES0/FR0 (20 bytes)|C|
|35|Pic Animations 2|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|36|Font Inversed + Pic Animations 3|graphics/data|0|FR0 (0 bytes)|ES0 (0 bytes)|D|
|37|Tileset Data 6|graphics/data|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|38|Unown/card flip/puzzle/memory/Bill PC|engine/mixed|0|ES0 (11206 bytes)|FR0 (11243 bytes)|B|
|39|Copyright + options/splash/intro|engine/mixed|0|FR0 (14027 bytes)|ES0 (14007 bytes)|B|
|3A|Audio + Songs 1|audio|0|EN0/ES0/FR0 (6 bytes)|EN0/ES0/FR0 (6 bytes)|C|
|3B|Songs 2|audio|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|3C|Songs 3 + SFX + cries|audio|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|3D|Songs 4|audio|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|3E|font/time capsule/name rater/new dex/Unown dex/Hidden Power|graphics/data|8|FR0 (110 bytes)|ES0 (80 bytes)|B|
|3F|tileset animations/NPC trade/mom phone|graphics/data|0|ES0 (140 bytes)|EN0 (118 bytes)|C|
|40|Mobile 40|mobile/special|0|FR0 (3192 bytes)|ES0 (4077 bytes)|B|
|41|DMA/emotes/warp/mystery gift/used move text/mobile/font|text|0|ES0 (827 bytes)|EN0 (6897 bytes)|B|
|42|Mobile 42 + Intro Logo + Credits|mobile/special|0|ES0 (2071 bytes)|ES0 (2210 bytes)|B|
|43|Title|engine/mixed|0|ES0 (110 bytes)|ES0/FR0 (169 bytes)|B|
|44|Mobile Adapter SDK|mobile/special|0|EN0/ES0/FR0 (1 bytes)|EN0/ES0/FR0 (1 bytes)|B|
|45|Mobile Adapter SDK Mail + Mobile 45|mobile/special|0|ES0 (53 bytes)|FR0 (92 bytes)|B|
|46|Mobile 46|mobile/special|0|FR0 (4903 bytes)|FR0 (6454 bytes)|B|
|47|Battle Tower|mobile/special|1|ES0 (250 bytes)|ES0 (215 bytes)|B|
|48|Pic pointers + Pics 1|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|49|Unown pic pointers + Pics 2|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|4A|Trainer pic pointers + Pics 3|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|4B|Pics 4|graphics/data|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|4C|Pics 5|graphics/data|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|4D|Pics 6|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|4E|Pics 7|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|4F|Pics 8|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|50|Pics 9|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|51|Pics 10|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|52|Pics 11|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|53|Pics 12|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|54|Pics 13|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|55|Pics 14|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|56|Pics 15|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|57|Pics 16|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|58|Pics 17|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|59|Pics 18|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|5A|Pics 19|graphics/data|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|5B|link trade/mobile + Pics 20|graphics/data|0|ES0 (424 bytes)|ES0 (428 bytes)|C|
|5C|Mobile 5C + Pics 21|graphics/data|546|FR0 (209 bytes)|FR0 (210 bytes)|A|
|5D|Crystal Phone Text 2 + Pics 22|text|0|EN0 (14025 bytes)|FR0 (12687 bytes)|B|
|5E|Battle HUD/Songs 5/Crystal SFX/Mobile 5E + Pics 23|graphics/data|0|ES0 (12 bytes)|ES0 (26 bytes)|C|
|5F|Mobile 5F + Pics 24|graphics/data|0|EN0 (7447 bytes)|EN0 (10422 bytes)|C|
|60|Map Scripts 13 + Pokédex Entries 001-064|map-script|0|EN0 (12325 bytes)|FR0 (11422 bytes)|B|
|61|Map Scripts 14|map-script|0|FR0 (9932 bytes)|FR0 (8927 bytes)|B|
|62|Map Scripts 15|map-script|0|JP0 (14991 bytes)|JP0 (13255 bytes)|B|
|63|Map Scripts 16|map-script|0|JP0 (14009 bytes)|ES0 (12874 bytes)|B|
|64|Map Scripts 17|map-script|0|JP0 (14526 bytes)|JP0 (12904 bytes)|B|
|65|Map Scripts 18|map-script|0|FR0 (14930 bytes)|EN0 (13264 bytes)|B|
|66|Map Scripts 19|map-script|0|FR0 (13555 bytes)|ES0 (12020 bytes)|B|
|67|Map Scripts 20|map-script|0|JP0 (15439 bytes)|ES0 (13429 bytes)|B|
|68|Map Scripts 21|map-script|0|JP0 (13353 bytes)|FR0 (11079 bytes)|B|
|69|Map Scripts 22|map-script|0|JP0 (14326 bytes)|EN0 (12664 bytes)|B|
|6A|Map Scripts 23|map-script|0|FR0 (14070 bytes)|FR0 (12588 bytes)|B|
|6B|Map Scripts 24|map-script|0|FR0 (10448 bytes)|ES0 (9457 bytes)|B|
|6C|Phone Text 2 + Map Scripts 25|map-script|0|EN0 (10424 bytes)|FR0 (9397 bytes)|B|
|6D|Special Phone Text|text|0|EN0 (13759 bytes)|FR0 (12664 bytes)|B|
|6E|Pokédex Entries 065-128|engine/mixed|0|FR0 (6605 bytes)|FR0 (6385 bytes)|B|
|6F|Text 1|text|0|JP0 (8714 bytes)|JP0 (7222 bytes)|B|
|70|Text 2|text|0|FR0 (8605 bytes)|JP0 (7515 bytes)|B|
|71|Text 3|text|0|EN0 (8948 bytes)|JP0 (6455 bytes)|B|
|72|Misc text: item names/move names/landmarks|text|0|EN0 (11121 bytes)|FR0 (10977 bytes)|B|
|73|Pokédex Entries 129-192|engine/mixed|0|FR0 (6623 bytes)|FR0 (6392 bytes)|B|
|74|Pokédex Entries 193-251|engine/mixed|0|EN0/FR0 (6150 bytes)|FR0 (5836 bytes)|B|
|75|Map Scripts 26 (ES/FR exact; DE/IT EU-localized)|map-script (EU relocation)|0|FR0 (8708 bytes)|FR0 (7444 bytes)|A|
|76|Map Scripts 27 (ES/FR exact; DE/IT EU-localized)|map-script (EU relocation)|0|FR0 (10834 bytes)|EN0/JP0 (8687 bytes)|A|
|77|Unown font/Print Party/Tileset Data 7/Pokégear GFX/European Mail|graphics/data|0|ES0 (10705 bytes)|ES0 (9419 bytes)|C|
|78|Debug Room (conditional) + Tileset Data 8|graphics/data|0|FR0 (836 bytes)|FR0 (752 bytes)|C|
|79|Map Scripts 28 (ES/FR exact; DE/IT EU-localized)|map-script (EU relocation)|0|FR0 (2490 bytes)|ES0 (2320 bytes)|A|
|7A|Unused / all-zero in all seven ROMs|unused/zero|0|EN0/ES0/FR0/JP0 (0 bytes)|EN0/ES0/FR0/JP0 (0 bytes)|D|
|7B|Battle Tower Text|text|0|EN0 (4391 bytes)|FR0 (3628 bytes)|B|
|7C|Battle Tower Trainer Data|mobile/special|0|EN0/ES0/FR0 (0 bytes)|EN0/ES0/FR0 (0 bytes)|D|
|7D|Mobile News Data|mobile/special|0|ES0 (2 bytes)|ES0/FR0 (10 bytes)|B|
|7E|Crystal Events / Battle Tower load + Odd Egg|mobile/special|2|EN0 (500 bytes)|EN0 (406 bytes)|B|
|7F|Stadium 2 checksums at $7DE0-$7FFF|mobile/special|12|ES0 (325 bytes)|FR0 (318 bytes)|B|

## Interpretation

A nearest-anchor byte count is not a claim that the target bank is derived from that language; it is a reconstruction heuristic. Exact source repos provide semantic boundaries and labels, while local DE/IT ROM bytes remain the authority for their final addresses and content.

The next deep pass should begin with Bank 00 (vectors/header/home code) and, in parallel, Banks 75/76/79 because they expose the European relocation model needed to understand later pointer movement.
