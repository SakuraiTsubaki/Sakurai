# Pokémon Crystal 7-ROM Bank Survey

All 7 uploaded ROMs are 2 MiB / 128 × 16 KiB banks. English semantic labels are anchored to pret/pokecrystal `layout.link`; non-English banks are provisional until symbol/address matching is completed.

|Bank|English semantic anchor|All 7 identical|JP diff|EN1 diff|ES diff|DE diff|FR diff|IT diff|
|---:|---|:---:|---:|---:|---:|---:|---:|---:|
|00|ROM0: RST/interrupt vectors, Header, Home||13645|4|11860|11824|11770|11680|
|01|bank1: link/OAM/map objects/intro/learn/math/items/NPC/events||8975|0|12903|12734|6268|12888|
|02|bank2: player object/sine/predef/color||10497|0|147|154|164|154|
|03|bank3: time/specials/HP/overworld/items/step/PC/item effects||15374|0|13998|6886|13506|14028|
|04|bank4: pack/time/TMHM/naming/menu/events/party corrections||15141|0|14526|14166|13144|14189|
|05|bank5: RTC/overworld/save/map setup/PC/mart/mom/daycare/breeding||15295|0|7938|7986|7955|7979|
|06|Tileset Data 1||15024|0|68|80|76|40|
|07|Roofs + Tileset Data 2 + Extra Songs 1||4|0|2|2|2|2|
|08|Clock Reset + Tileset Data 3 + Egg Moves||15081|0|20|21|20|21|
|09|bank9: menus/battle menu/trainer card/decorations/move effects||14427|0|7144|10857|10126|11563|
|0A|bankA + Trainer Backpics||14383|0|14190|14135|13860|13983|
|0B|bankB: trainer HUDs/class names/TMHM/start battle/etc||15832|0|11204|11185|11257|11236|
|0C|Tileset Data 4||10899|0|0|0|0|0|
|0D|Effect Commands||8199|0|7149|7312|7123|7020|
|0E|Enemy Trainers / battle AI trainer data||13503|0|7965|8445|8411|8236|
|0F|Battle Core + effect command pointers||15597|0|5857|12507|13061|5825|
|10|Pokédex + move data + evolution engine + Evolutions/Attacks||15565|9|13135|13109|12942|13070|
|11|fruit trees/battle AI/Pokédex 2/mail||15575|2|1753|1759|1740|1755|
|12|Crystal Features 1 / mobile / Celebi / main menu||13898|0|11018|10983|10931|10930|
|13|map palettes/collision/save/link/stats/evolution movie/etc||10027|0|7616|7490|7418|7785|
|14|party menu/events/types/stats/base stats/Pokémon names||15060|0|13333|14411|14058|15328|
|15|Map Scripts 1||15765|0|12430|13936|13615|12873|
|16|Map Scripts 2||15960|0|13627|15074|13688|13566|
|17|Map Scripts 3||15701|0|11508|12666|11876|11912|
|18|Map Scripts 4||15941|0|12415|12288|12299|12236|
|19|Crystal Phone Text||15784|0|12517|13494|12588|12503|
|1A|Map Scripts 5||15916|0|14339|14434|14451|14365|
|1B|Map Scripts 6||15921|0|13221|14602|13195|13217|
|1C|Map Scripts 7||15989|0|13076|14908|13456|13396|
|1D|Map Scripts 8||15794|0|12452|13462|12469|12480|
|1E|Map Scripts 9||15890|0|12875|14872|12982|13002|
|1F|Map Scripts 10||15890|0|13239|14776|13313|13165|
|20|player movement/engine flags/variables/battle text||7480|0|7674|7840|7347|7425|
|21|printer + battle animation gfx + Hall of Fame||10350|0|7666|7639|7653|7652|
|22|Crystal Features 2 / Kurt/player gfx/mobile/Unown walls/Battle Tower rules||14193|0|12771|12184|9927|12527|
|23|timeofday palettes/battle transition/field moves/sprite anims/icons||303|0|100|80|92|82|
|24|phone/RTC/Pokégear/fishing/slot machine||15561|0|13570|13781|13627|13535|
|25|Maps + Events||6703|0|5153|5642|5445|5328|
|26|Map Scripts 11||16000|0|14481|14583|14548|14414|
|27|Map Scripts 12||16034|0|14481|14708|14507|14704|
|28|Phone Scripts 1||10666|0|5116|5525|5130|4967|
|29|Phone Text||14099|0|9308|9586|8974|8925|
|2A|Map Blocks 1||6|0|0|0|0|0|
|2B|Map Blocks 2||14|0|0|0|0|0|
|2C|Map Blocks 3||122|0|54|58|45|51|
|2D|Tileset Data 5||7799|0|34|40|38|20|
|2E|map-name/hidden items/trees/radio/mail||8472|0|7144|7337|7253|7110|
|2F|Phone Scripts 2 + trainer scripts||14376|0|8889|9373|9090|6507|
|30|Sprites 1|✓|0|0|0|0|0|0|
|31|Sprites 2|✓|0|0|0|0|0|0|
|32|battle anim bg/effects + move animations ptr/The End||13875|0|172|207|175|189|
|33|Move Animations + Extra Songs 2||15304|0|164|14950|15450|15167|
|34|Pic Animations 1||397|0|20|20|20|20|
|35|Pic Animations 2||1714|0|0|0|0|0|
|36|Font Inversed + Pic Animations 3||7088|0|236|210|210|236|
|37|Tileset Data 6|✓|0|0|0|0|0|0|
|38|Unown/card flip/puzzle/memory/Bill PC||15938|0|13275|12440|13307|12603|
|39|Copyright + options/splash/intro||15056|0|14204|14170|6009|14140|
|3A|Audio + Songs 1||11|0|5|6|6|6|
|3B|Songs 2|✓|0|0|0|0|0|0|
|3C|Songs 3 + SFX + cries|✓|0|0|0|0|0|0|
|3D|Songs 4|✓|0|0|0|0|0|0|
|3E|font/time capsule/name rater/new dex/Unown dex/Hidden Power||12037|8|1081|1055|1052|1065|
|3F|tileset animations/NPC trade/mom phone||10077|0|121|142|140|118|
|40|Mobile 40||8196|0|3603|4125|4117|4093|
|41|DMA/emotes/warp/mystery gift/used move text/mobile/font||10004|0|9006|9017|7286|6897|
|42|Mobile 42 + Intro Logo + Credits||10315|0|2300|2285|2205|2357|
|43|Title||4073|0|135|145|127|172|
|44|Mobile Adapter SDK||2|0|1|1|1|1|
|45|Mobile Adapter SDK Mail + Mobile 45||1977|0|127|116|119|117|
|46|Mobile 46||14920|0|6421|6709|6718|6694|
|47|Battle Tower||13610|1|233|302|323|232|
|48|Pic pointers + Pics 1||500|0|0|0|0|0|
|49|Unown pic pointers + Pics 2||90|0|0|0|0|0|
|4A|Trainer pic pointers + Pics 3||495|0|0|0|0|0|
|4B|Pics 4|✓|0|0|0|0|0|0|
|4C|Pics 5|✓|0|0|0|0|0|0|
|4D|Pics 6||597|0|0|0|0|0|
|4E|Pics 7||1703|0|0|0|0|0|
|4F|Pics 8||9934|0|0|0|0|0|
|50|Pics 9||10129|0|0|0|0|0|
|51|Pics 10||16153|0|0|0|0|0|
|52|Pics 11||6168|0|0|0|0|0|
|53|Pics 12||9278|0|0|0|0|0|
|54|Pics 13||8201|0|0|0|0|0|
|55|Pics 14||11915|0|0|0|0|0|
|56|Pics 15||9767|0|0|0|0|0|
|57|Pics 16||12886|0|0|0|0|0|
|58|Pics 17||15985|0|0|0|0|0|
|59|Pics 18||10132|0|0|0|0|0|
|5A|Pics 19||10132|0|0|0|0|0|
|5B|link trade/mobile + Pics 20||765|0|442|441|447|444|
|5C|Mobile 5C + Pics 21||13322|546|9644|767|773|770|
|5D|Crystal Phone Text 2 + Pics 22||15501|0|13097|14025|13151|13105|
|5E|Battle HUD/Songs 5/Crystal SFX/Mobile 5E + Pics 23||141|0|32|32|34|30|
|5F|Mobile 5F + Pics 24||10834|0|3518|7447|9500|10422|
|60|Map Scripts 13 + Pokédex Entries 001-064||12425|0|11778|12325|11845|11895|
|61|Map Scripts 14||8900|0|9198|9940|8939|9011|
|62|Map Scripts 15||13592|0|13713|15168|13779|13748|
|63|Map Scripts 16||12713|0|13016|14231|13202|13017|
|64|Map Scripts 17||13189|0|13122|14656|13346|13339|
|65|Map Scripts 18||13346|0|13054|14950|13061|13264|
|66|Map Scripts 19||14444|0|14265|14316|14323|14193|
|67|Map Scripts 20||13255|0|13454|15529|13286|13485|
|68|Map Scripts 21||11859|0|11654|13413|11746|11726|
|69|Map Scripts 22||12579|0|12437|14402|12562|12664|
|6A|Map Scripts 23||13810|0|13815|14112|13738|13826|
|6B|Map Scripts 24||9641|0|9594|10470|9569|9467|
|6C|Phone Text 2 + Map Scripts 25||8213|0|9242|10424|9099|9406|
|6D|Special Phone Text||13449|0|13417|13759|13361|13363|
|6E|Pokédex Entries 065-128||6846|0|6901|6615|6563|6587|
|6F|Text 1||7956|0|8217|8794|8024|8017|
|70|Text 2||7572|0|7973|8626|7561|7557|
|71|Text 3||8196|0|8518|8948|8150|8158|
|72|Misc text: item names/move names/landmarks||11971|0|11819|11121|11521|11543|
|73|Pokédex Entries 129-192||6931|0|6825|6665|6689|6697|
|74|Pokédex Entries 193-251||6408|0|6200|6150|6185|6179|
|75|UNMAPPED||0|0|8096|9324|8025|7964|
|76|UNMAPPED||0|0|10090|10949|10314|8687|
|77|Unown font/Print Party/Tileset Data 7/Pokégear GFX/European Mail||11135|0|11602|11329|11104|11389|
|78|Debug Room (conditional) + Tileset Data 8||4096|0|844|856|812|844|
|79|UNMAPPED||0|0|2262|2506|2366|2340|
|7A|UNMAPPED|✓|0|0|0|0|0|0|
|7B|Battle Tower Text||3722|0|3682|4391|3710|3658|
|7C|Battle Tower Trainer Data||2365|0|0|0|0|0|
|7D|Mobile News Data||8836|0|11|11|11|11|
|7E|Crystal Events / Battle Tower load + Odd Egg||11243|2|800|500|533|406|
|7F|Stadium 2 checksums at $7DE0-$7FFF||438|12|351|350|346|346|
