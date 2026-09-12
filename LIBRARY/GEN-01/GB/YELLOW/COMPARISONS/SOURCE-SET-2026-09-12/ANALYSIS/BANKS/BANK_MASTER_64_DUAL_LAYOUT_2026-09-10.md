# 포켓몬스터 피카츄 / Pokémon Yellow — 64뱅크 전수조사 마스터

대상: JP Rev 0A/B/C/D + EN/FR/DE/IT/ES, 고유 ROM 9개. 모든 수치는 각 ROM에서 직접 읽은 0x4000-byte 뱅크의 동일 위치 바이트 비교다.

주의: 일본판과 해외판은 같은 뱅크 번호라도 배치가 다르다. `JP 역할`은 Narishma-gb/pokeyellow-jp의 layout.link, `해외판 역할`은 pret/pokeyellow의 canonical EN layout을 기준으로 하고, 실제 업로드 ROM 바이트 통계와 교차검증했다.

`JP Δ` = 0A→B / B→C / C→D changed bytes. `JPD→Intl` = Rev D와 EN/FR/DE/IT/ES의 changed bytes.

|Bank|JP 역할|해외판 역할|정확 동일 그룹|JP Δ|JPD→Intl (EN/FR/DE/IT/ES)|Intl Δ min–max|우선|핵심 메모|
|---|---|---|---|---:|---:|---:|---|---|
|`00`|ROM0: vectors/header/Home + Garbage 0|ROM0 / vectors / header / Home|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|15610/31/200|15800/15814/15826/15812/15831|5416–11580|P0||
|`01`|bank1 + Garbage 1|bank1: title, menus, overworld, naming, mart/center, Pokédex display|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|883/43/299|15534/15376/15537/15535/15561|13245–14150|P0||
|`02`|Audio 1 (SFX/music/audio engine)|Sound Effect Headers 1 / Music Headers 1 / Sound Effects 1 / Audio Engine 1 / Music 1|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|327/54/296|27/27/27/27/27|11–23|P2||
|`03`|bank3|bank3: joypad, overworld, item effects, flags, hidden events, math|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|15776/68/456|15095/15085/15081/15104/15099|7526–7892|P0||
|`04`|bank4 + NPC Sprites 1 + Battle Engine 1|font / status/party menus / player gfx / TM data / NPC Sprites 1 / Battle Engine 1|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|322/9/53|15353/15750/15494/15642/15650|2936–11019|P1||
|`05`|bank5 + NPC Sprites 2 + Battle Engine 2|Pokédex/map sprite gfx / NPC Sprites 2 / Battle Engine 2|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|415/67/349|608/609/610/610/609|47–115|P1||
|`06`|Maps 1–2 + Doors/Ledges + Garbage 6|Maps 1 / Maps 2 / Doors and Ledges|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|986/87/538|11615/11616/11617/11614/11618|421–916|P1||
|`07`|Maps 3–4 + Clear Save + Hidden Events 1 + Garbage 7|Maps 3 / bank7 / Maps 4 / Hidden Events 1|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|601/4/19|15525/15515/15530/15504/15510|785–5796|P1||
|`08`|Audio 2 + Low Health Alarm + Bill’s PC|Audio headers/SFX 2 / Low Health Alarm / Bill's PC / Audio Engine 2 / Music 2|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|2006/279/1595|9130/9059/8900/9128/9113|7444–8990|P2||
|`09`|Pics 1 + Battle Engine 3|Pics 1 / Battle Engine 3|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|325/40/280|502/471/488/521/507|355–444|P1||
|`0A`|Pics 2 + Battle Engine 4|Pics 2 / Battle Engine 4|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|495/74/448|193/193/193/193/193|4–26|P1||
|`0B`|Pics 3 + Battle Engine 5|Pics 3 / Battle Engine 5|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|414/72/342|304/304/304/304/304|10–27|P1||
|`0C`|Pics 4|Pics 4|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|682/89/606|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`0D`|Pics 5 + Slot Machines|Pics 5 / Slot Machines|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|131/5/56|2530/2531/2528/2531/2530|76–186|P1||
|`0E`|Battle Engine 6|Battle Engine 6 / moves/base stats/cries/evos|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|225/29/140|10629/10656/10644/10657/10643|393–8475|P0||
|`0F`|Battle Core + Garbage 15|Battle Core|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|518/4/28|15985/15987/15971/15976/15984|10293–11460|P0||
|`10`|bank10|Pokédex UI / trade/intro/options|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|2407/306/2054|13611/13573/13594/13600/13595|6087–7279|P0||
|`11`|Maps 5–6 + Pokédex Rating + Dungeon Warps + Garbage 17|Maps 5 / Pokédex Rating / Maps 6 / Dungeon Warps|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|1442/168/11204|14830/14828/14819/14825/14823|429–808|P1||
|`12`|Maps 7–8 + Garbage 18|Maps 7 / Maps 8|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|666/41/256|15701/15711/15713/15703/15714|549–6821|P1||
|`13`|Trainer Pics + Maps 9|Trainer Pics / Maps 9|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|235/34/233|87/87/87/87/87|2–7|P1||
|`14`|Maps 10 + Hidden Events 2|Maps 10 / Hidden Events 2|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|945/81/7007|12664/12662/12653/12657/12669|5393–5908|P1||
|`15`|Maps 11–12 + Battle Engine 7 + Diploma + Trainer Sight|Maps 11 / Battle Engine 7 / Maps 12 / Diploma / Trainer Sight|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|477/22/148|10833/10833/10834/10833/10834|610–1059|P1||
|`16`|Maps 13–14 + bank16 + Saffron Guards|Maps 13 / experience/status/oak aide / Maps 14 / Saffron Guards|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|489/21/122|12353/12353/12354/12354/12353|582–1038|P1||
|`17`|Maps 15–16 + Starter Dex + Hidden Events 3 + Garbage 23|Maps 15 / Starter Dex / Maps 16 / Hidden Events 3|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|947/89/2724|15240/15251/15252/15250/15262|3367–7170|P1||
|`18`|Maps 17–18 + Cinnabar Lab Fossils + Hidden Events 4 + Garbage 24|Maps 17 / Cinnabar Lab Fossils / Maps 18 / Hidden Events 4|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|520/31/124|14983/14983/14983/14982/14982|519–968|P1||
|`19`|Tilesets 1|Tilesets 1|JP0A=JPB=JPC=JPD / EN / FR / DE / IT / ES|0/0/0|39/41/59/39/37|6–38|P2|JP revisions exact|
|`1A`|Version Graphics + Tilesets 2|Version Graphics / Tilesets 2|EN=FR=DE=IT=ES / JP0A / JPB / JPC / JPD|16/4/16|19/19/19/19/19|0–0|P2|international 5 exact; JPD differs by 16–19 bytes|
|`1B`|Tilesets 3|Tilesets 3|JP0A=JPB=JPC=JPD=EN=FR=DE=IT=ES|0/0/0|0/0/0/0/0|0–0|P2|all 9 exact|
|`1C`|bank1C|hall of fame/healing/player anims/battle transitions/town map/icons/trades/palettes/save|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|6798/259/1327|14322/15312/15305/15496/15394|11350–14309|P0||
|`1D`|Maps 19–21 + Itemfinder + Vending Machine|Maps 19 / Itemfinder 1 / Maps 20 / Vending Machine / Maps 21 / Itemfinder 2|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|764/70/339|15607/15595/15578/15590/15596|6467–7961|P1||
|`1E`|bank1E|battle animations / cut/dust / fishing gfx / move animation data|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|206/19/86|15497/15496/15497/15497/15497|16–349|P1||
|`1F`|Audio 3 (SFX/music/audio engine)|Audio headers/SFX 3 / Audio Engine 3 / Music 3|EN=IT / JP0A / JPB / JPC / JPD / FR / DE / ES|1955/446/1903|7/7/7/7/7|0–6|P2|EN=IT; JPD differs from EN by 7 bytes|
|`20`|Surfing Pikachu Graphics|Audio headers/SFX 4 / Surfing Pikachu Graphics / Audio Engine 4 / Music 4|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|9081/1757/8949|14647/11307/11262/11435/11173|3181–6627|P2||
|`21`|Pikachu Cries 1|Pikachu Cries 1|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|5649/1033/5556|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`22`|Pikachu Cries 2|Pikachu Cries 2|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|4094/808/4018|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`23`|Pikachu Cries 3|Pikachu Cries 3|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|496/107/490|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`24`|Pikachu Cries 4|Pikachu Cries 4|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|6099/1153/5954|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`25`|Pikachu Cries 5|Pikachu Cries 5|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|4825/927/4788|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`26`|unused in Rev D; Rev 0A/B/C garbage region|Text 1|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16367/3139/16012|14676/12355/14087/12157/12732|12163–14527|P2|JP Rev D cleared/unused; older JP retains garbage|
|`27`|unused in Rev D; Rev 0A/B/C garbage region|Text 2|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16358/3203/16263|14900/12180/14060/12410/13203|12158–14660|P2|JP Rev D cleared/unused; older JP retains garbage|
|`28`|Audio 4 (SFX/music/audio engine)|Text 3|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|10748/1871/8855|15180/12355/14617/12264/12811|12033–14883|P2||
|`29`|bank29|Text 4|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|12717/1801/9441|13774/11789/14066/11417/11739|11531–13869|P2||
|`2A`|unused in Rev D; Rev 0A/B/C garbage region|Text 5|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16366/2640/13155|14955/12391/14387/12572/12484|12207–14720|P2|JP Rev D cleared/unused; older JP retains garbage|
|`2B`|unused in Rev D; Rev 0A/B/C garbage region|Text 6|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16378/2375/12372|14560/13204/14335/12262/12920|12674–14339|P2|JP Rev D cleared/unused; older JP retains garbage|
|`2C`|unused in Rev D; Rev 0A/B/C garbage region|Text 7|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16371/2426/12545|14279/13366/14322/12143/12848|12591–14072|P2|JP Rev D cleared/unused; older JP retains garbage|
|`2D`|unused in Rev D; Rev 0A/B/C garbage region|Text 8|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16377/2611/12802|12406/12571/14462/12843/13582|12379–14300|P2|JP Rev D cleared/unused; older JP retains garbage|
|`2E`|unused in Rev D; Rev 0A/B/C garbage region|Pokédex Text|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16377/2431/12269|14603/13621/14372/14371/13748|13113–14048|P2|JP Rev D cleared/unused; older JP retains garbage|
|`2F`|unused in Rev D; Rev 0A/B/C garbage region|Move Names / BG Map Attributes|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16372/2552/13032|4078/4146/4208/4177/4241|1548–1627|P1|JP Rev D cleared/unused; older JP retains garbage|
|`30`|bank30 + Pikachu Graphics 1 + Credits + Maps 22|garbage data (entire bank in canonical EN build)|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|12931/1102/9943|15761/10025/12165/10190/10781|10008–16212|P2|EN canonical garbage bank; JP contains real content; localized banks repurposed|
|`31`|Pikachu Cries 6|Pikachu Cries 6|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|826/73/644|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`32`|Pikachu Cries 7|Pikachu Cries 7|JP0A=JPB=JPC=JPD=EN=FR=DE=IT=ES|0/0/0|0/0/0/0/0|0–0|P2|all 9 exact|
|`33`|Pikachu Cries 8|Pikachu Cries 8|JPD=EN=FR=DE=IT=ES / JPB=JPC / JP0A|10/0/7|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`34`|Pikachu Cries 9|Pikachu Cries 9|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|6780/643/5288|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`35`|Pikachu Cries 10|Pikachu Cries 10|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|2557/288/2134|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`36`|Pikachu Cries 11|Pikachu Cries 11|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|160/21/140|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`37`|Pikachu Cries 12|Pikachu Cries 12|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|106/8/94|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`38`|Pikachu Cries 13|Pikachu Cries 13|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|264/15/219|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`39`|Pikachu Graphics 2|Pikachu Graphics 1|JPD=EN=FR=DE=IT=ES / JP0A / JPB / JPC|349/39/239|0/0/0/0/0|0–0|P2|JPD + all international exact|
|`3A`|Printer|Pokémon names / printer / NPC movement / diploma2|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|7948/635/12328|10447/10408/10504/10486/10484|6170–7297|P0||
|`3B`|Pikachu PCM|empty in canonical EN build|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|16112/1646/11707|254/11784/13337/11333/11876|11332–13335|P2|EN empty; JP uses Pikachu PCM; FR/DE/IT/ES use localization data|
|`3C`|Tilesets 4 + bank3C + Maps 23 + Hidden Events Core|Pikachu PCM / bank3C / Tilesets 4 / Pikachu movement/gfx / Credits / Maps 22 / Hidden Events Core|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|3654/223/2321|12508/12499/12500/12527/12518|2334–7178|P0||
|`3D`|Battle Engine 8 + Pics 7 + Battle Engine 9|Battle Engine 8 / Pics 7 / Battle Engine 9|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|9175/969/6670|9995/10001/9990/10000/9992|4296–9001|P0||
|`3E`|Surfing Minigame + Intro Graphics + Animated Objects|Surfing Minigame / intro yellow / animated objects|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|1086/84/731|14384/14266/14320/14208/14315|7404–11661|P0||
|`3F`|Overworld Pikachu + NPC Sprites 3 + Garbage 63|Overworld Pikachu / map songs/headers / Pikachu follow/status/emotions/movement / NPC Sprites 3|JP0A / JPB / JPC / JPD / EN / FR / DE / IT / ES|3452/359/3324|11487/11486/11485/11485/11485|91–421|P0||

## 핵심 결론

- **9개 전부 동일:** Bank `1B`, `32`.
- **일본 4리비전 전부 동일:** `19`, `1B`, `32`.
- **해외 5개 언어판 전부 동일:** `0C`, `1A`, `1B`, `21`–`25`, `31`–`39`.
- **JP Rev D + 해외 5개 언어판까지 전부 동일:** `0C`, `1B`, `21`–`25`, `31`–`39` (`32` 포함).
- JP Rev D는 `26`, `27`, `2A`–`2F`가 비어 있고, 이전 일본 Rev 0A/B/C에는 garbage가 남아 있다. 이는 공개 일본판 layout의 Rev.0–Rev.2 garbage 표기와 실제 ROM 통계가 일치한다.
- Bank `30`과 `3B`는 지역별 역할이 특히 크게 갈린다. EN `30`은 canonical garbage, EN `3B`는 empty지만 JP에서는 각각 실제 그래픽/크레딧/맵과 Pikachu PCM을 사용한다. FR/DE/IT/ES는 `30`/`3B`를 현지화 데이터로 활용한다.

## 디스어셈블리 권장 순서

1. **P0 코드 코어:** `00`, `01`, `03`, `0E`, `0F`, `10`, `1C`, `3A`, `3C`, `3D`, `3E`, `3F`.
2. **P1 혼합/맵/이벤트:** `04`–`07`, `09`–`0B`, `0D`, `11`–`18`, `1D`, `1E`, `2F`.
3. **P2 데이터 계열:** 오디오 `02/08/1F/20–25/28/31–38`, 그래픽 `0C/19–1B/30/39`, 해외 텍스트 `26`–`2F`, 지역별 여유/garbage 영역.
