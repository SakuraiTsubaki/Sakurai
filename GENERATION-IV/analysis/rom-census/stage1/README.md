# Generation IV ROM 전수 구조조사 — 1차 원장

대상 ROM 5개:
- Pokémon Diamond USA (`ADAE`, Rev 5)
- Pokémon Pearl USA (`APAE`, Rev 5)
- Pokémon Platinum Korea (`CPUK`, Rev 0)
- Pokémon HeartGold Korea (`IPKK`, Rev 0)
- Pokémon SoulSilver Korea (`IPGK`, Rev 0)

## 조사 방법
- NDS 헤더/ARM9/ARM7/FNT/FAT/Overlay table 직접 파싱
- NitroFS의 모든 FAT 엔트리 SHA-1/CRC32/크기/경로/매직 수집
- 모든 NARC를 직접 파싱해 내부 멤버 인덱스/크기/SHA-1/매직 수집
- ROM간 경로 동일성 및 바이트 동일성 비교
- HGSS 번호형 `a/x/x/x` 파일을 DPPt 명명 파일과 exact hash로 역매핑
- HG/SS 차이 NARC는 내부 멤버 단위까지 diff

> 원본 ROM 바이트를 복제한 결과물은 포함하지 않고, 구조/메타데이터/해시 원장만 저장한다.

## 전체 구조 요약

| ROM | 물리 크기 | Header used size | 0xFF tail padding | FAT | Named files | Dirs | ARM9 overlays | NARC | NARC members |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Diamond USA | 67,108,864 | 61,169,344 | 5,939,520 | 356 | 269 | 69 | 87 | 149 | 33,953 |
| Pearl USA | 67,108,864 | 61,169,344 | 5,939,520 | 356 | 269 | 70 | 87 | 149 | 33,953 |
| Platinum KOR | 134,217,728 | 102,630,460 | 31,587,268 | 461 | 339 | 105 | 122 | 215 | 53,505 |
| HeartGold KOR | 134,217,728 | 124,639,804 | 9,577,924 | 511 | 382 | 46 | 129 | 308 | 56,674 |
| SoulSilver KOR | 134,217,728 | 124,639,804 | 9,577,924 | 511 | 382 | 46 | 129 | 308 | 56,674 |

모든 tail padding은 Header used size 이후 ROM EOF까지 전 바이트가 `FF`임을 확인했다.

## 코드 영역

### Diamond ↔ Pearl
- ARM7: 완전 동일
- ARM9: 서로 다름
- ARM9 Overlay: 87개 중 69개 동일, 18개 다름
- Overlay 차이 ID: 5, 6, 7, 8, 11, 12, 16, 17, 18, 48, 54, 62, 63, 64, 80, 81, 83, 84

### HeartGold ↔ SoulSilver
- ARM7: 완전 동일
- ARM9: 서로 다름
- ARM9 Overlay: 129개 중 11개 동일, 118개 다름
- 서로 다른 Overlay 중 29개는 압축 바이너리 크기도 달라짐

## Diamond ↔ Pearl 파일시스템
- 공통 named path: 268
- 공통 268개는 **모두 바이트 완전 동일**
- Diamond-only path: `poketool/personal/personal.narc`
- Pearl-only path: `poketool/personal_pearl/personal.narc`
- FAT 356개 중 exact-hash 공유: 337개
- 즉 FAT 차이는 **18 Overlay + personal NARC 1개 = 19개**

### D/P personal 차이
두 personal archive는 각각 501 records. 다른 레코드는 6개뿐:
- 125, 126, 239, 240, 466, 467

각 레코드에서 달라지는 바이트는 12–15뿐이며, Gen IV personal 구조상 두 held-item 필드 위치다. 즉 D/P personal 차이는 이 6개 슬롯의 소지 아이템 슬롯 배열 차이로 국소화된다.

## Platinum 확장
Diamond와 비교:
- 공통 named path 239
- byte-identical path 166
- same path but different 73
- Diamond-only 30
- Platinum-only 100
- DP Overlay ID 0–86 중 3개만 byte-identical, 84개 변경
- Platinum은 Overlay 87–121, 총 35개 추가

주요 archive 확장:

| 데이터 | DP | Platinum |
|---|---:|---:|
| Personal | 501 | `pl_personal` 508 |
| Evolution | 501 | 508 |
| Level-up learnset | 501 | 508 |
| Move table | 471 | 471 |
| Item data | 442 | `pl_item_data` 446 |
| Trainer data | 850 | 928 |
| Trainer party | 850 | 928 |
| Field scripts | 1,051 | 1,124 |
| Zone events | 512 | 534 |
| Land data | 578 | 666 |
| Map matrix | 245 | 289 |
| Main/legacy messages | DP `msg` 624 | Pt `msg` 612 + `pl_msg` 714 |
| Font | 8 | 10 + `pl_font` 10 |

Platinum에는 `resource/kor/` 아래 한국어 전용 리소스가 32개 존재한다.

## HGSS 핵심 archive 매핑

| HGSS path | decomp logical role | entries |
|---|---|---:|
| `a/0/0/2` | Pokémon personal | 508 |
| `a/0/0/3` | growth table | 8 |
| `a/0/0/4` | Pokémon battle graphics | 2,964 |
| `a/0/1/1` | move table | 471 |
| `a/0/1/2` | field scripts | 965 |
| `a/0/1/6` | main font | 13 |
| `a/0/1/7` | item data | 514 |
| `a/0/1/8` | item icons | 797 |
| `a/0/2/0` | Pokémon icons | 551 |
| `a/0/2/7` | main messages | 822 |
| `a/0/3/0` | name input assets | 277 |
| `a/0/3/2` | zone events | 491 |
| `a/0/3/3` | level-up learnsets | 508 |
| `a/0/3/4` | evolutions | 508 |
| `a/0/3/7` | Gold encounter data | 142 |
| `a/0/4/1` | map matrix | 288 |
| `a/0/5/5` | trainer data | 738 |
| `a/0/5/6` | trainer parties | 738 |
| `a/0/6/5` | land data | 676 |
| `a/0/7/4` | Pokédex data | 102 |
| `a/0/7/5` | Pokédex height/weight data | 2 |
| `a/1/3/3` | Pokédex encounter/location data | 3,962 |
| `a/1/3/6` | Silver encounter data | 142 |
| `a/1/3/8` | Johto Pokédex data | 1 |
| `a/1/4/1` | following-Pokémon parameter data | 566 |
| `a/1/6/9` | Pokémon performance data | 554 |
| `a/2/2/9` | egg move list | 1 |
| `a/2/5/2` | Headbutt encounter data | 540 |
| `a/2/5/4` | photo data | 93 |

## HeartGold ↔ SoulSilver 일반 파일 차이
382개 named paths 중 379개 exact identical. 다른 것은 단 3개:

1. `a/0/7/5` — Pokédex height/weight data
   - 2 members
   - member #1만 다름
2. `a/1/3/3` — Pokédex encounter/location data
   - 3,962 members
   - 130 members 다름
3. `a/2/5/2` — Headbutt encounter data
   - 540 members
   - 33 members 다름

즉 HG/SS의 named NitroFS 차이는 Pokédex/출현 정보와 박치기 출현표에 극도로 집중되어 있다. 실행 코드 차이는 ARM9/Overlay에 별도로 크게 존재한다.

## DPPt → HGSS 자산 재사용
- HGSS의 번호형 `a/...` 가운데 **73개 경로**가 DPPt의 명명 파일과 바이트 단위 exact match.
- 서로 다른 파일명까지 포함해 exact-hash object group **96개가 5 ROM 모두에서 발견**됨.
- HGSS `pbr/`에는 DPPt 계열 호환/잔존 리소스가 별도 묶음으로 존재하며, 다음과 같은 자산이 DPPt와 exact match한다:
  - `sound_data.sdat`
  - `personal.narc` (501)
  - `waza_tbl.narc` (471)
  - `poke_icon.narc` (540)
  - `pokegra.narc` (2,964)
  - `msg.narc` (612)
  - `font.narc` (10)
  - battle background/object resources 등

## 한국어 폰트 계보
- Platinum `graphic/font.narc`: 10 members, 759,840 bytes
- Platinum `graphic/pl_font.narc`: 10 members, 759,912 bytes
- HGSS main `a/0/1/6`: 13 members, 1,201,508 bytes
- HGSS `pbr/font.narc`: Platinum `graphic/font.narc`와 exact match

HGSS 메인 폰트는 DPPt 호환 폰트와 분리되어 별도 확장되어 있다.

## 생성 원장
- `all_files.csv`: FAT 전체 2,195개 object
- `all_narc_members.csv`: NARC 내부 234,759개 member
- ROM별 `*_files.csv`: 경로/FAT/해시/형식/NARC count
- ROM별 `*_narcs.json`: NARC block metadata
- ROM별 `*_overlays.json`: Overlay table
- `pairwise.json`: ROM pairwise exact comparison
- `same_path_narc_diffs.json`: 동일 경로 NARC 멤버 diff
- `hgss_outer_diffs.json`: HG/SS 3개 파일 member-level diff
- `hgss_exact_named_mappings.json`: HGSS 번호 path → DPPt exact-match name
- `shared_objects.json`: ROM간 exact binary object reuse index
- `overlay_comparisons.json`: Overlay 차이 원장
- `overlay_manifest.json`: 전체 Overlay 해시/크기/메모리 매핑

# 2차: 고정 레코드 필드 디코딩

pret/pokeheartgold의 현재 구조체 정의와 ROM 실데이터 크기를 교차해 다음 핵심 테이블을 필드 단위 CSV로 디코딩했다.

## Personal 44-byte schema
- Base stats: HP/Atk/Def/Speed/SpAtk/SpDef
- type1/type2
- catch rate / EXP yield / EV yields
- held item slot 1/2
- gender ratio / egg cycles / friendship / growth rate
- egg groups
- ability 1/2
- Great Marsh rate field (HGSS에서 실제 의미/사용 여부는 별도 코드 검증 필요)
- color / sprite flip bit
- TM/HM compatibility 128-bit bitset

### D/P field-level difference
D/P에서 다른 personal record는 정확히 6개이며, 차이는 held-item 필드뿐이다.
- 125: item 322가 slot1 ↔ slot2
- 126: item 323가 slot2 ↔ slot1
- 239: item 322가 slot1 ↔ slot2
- 240: item 323가 slot2 ↔ slot1
- 466: item 322가 slot1 ↔ slot2
- 467: item 323가 slot2 ↔ slot1

## Move 16-byte schema
- effect (u16)
- category
- power
- type
- accuracy
- PP
- effect chance
- range/target mask
- priority
- unkB
- unkC
- contest type
- unkE

### Move table revisions
- Diamond/Pearl move tables: identical
- Diamond → Platinum: common 471 moves 중 **1 record만 변경**
  - move index 95: accuracy `70 → 60`
- Platinum → HGSS: common 471 moves 중 **1 record만 변경**
  - move index 258: `unkB 2 → 0`
- HG ↔ SS: move table 완전 동일

## Evolution
- record size 44 bytes
- 7 × `(method u16, param u16, target u16)` + tail 2 bytes
- DP common 501 records → Platinum 508 records
- Platinum 508 ↔ HGSS 508: **전 레코드 완전 동일**
- HG ↔ SS: 완전 동일

## Item 34-byte schema
- price
- held effect / parameter
- Pluck effect
- Fling effect / power
- Natural Gift power / type
- prevent-toss / selectable flags
- field/battle pocket
- field/battle use function
- party-use flag and party-effect parameter block

### Item revisions
- DP 442 → Platinum 446
- Platinum 446 → HGSS 514
- Platinum↔HGSS 공통 446개 중 29개가 변경
  - field-use function 차이: 28 records
  - selectable 차이: 12 records
  - party parameter block 차이: 4 records
- HG ↔ SS: 514 records 전부 동일

## Trainer 20-byte schema
- trainerType
- trainerClass
- unused/unknown byte
- party count
- four held battle items
- AI flags
- double-battle flag

### Trainer tables
- DP: 850
- Platinum: 928
- HGSS: 738
- HG ↔ SS trainer headers: 738 전부 동일
- HG ↔ SS trainer party NARC도 outer SHA-1이 동일하므로 파티 데이터도 동일

## HGSS version-data packaging observation
- HG와 SS 양쪽 ROM에 Gold encounter archive와 Silver encounter archive가 **둘 다 들어 있음**:
  - Gold `a/0/3/7` — 142 × 196 bytes
  - Silver `a/1/3/6` — 142 × 196 bytes
- 두 archive 모두 HG/SS ROM 사이에서 exact-identical.
- 따라서 일반 야생 출현 데이터는 양 버전에 함께 포함되고 실행 코드가 버전에 맞춰 선택하는 구조다.
- 반면 Headbutt archive `a/2/5/2`는 HG/SS 자체가 서로 달라 33 map/member가 다르다.

## 생성된 디코드 CSV
`decoded_core/` 아래 ROM별로:
- `*_personal.csv`
- `*_moves.csv`
- `*_evolutions.csv`
- `*_items.csv`
- `*_trainers.csv`
- `field_diffs.json`

이 단계까지 구조/고정 파라미터 계층은 ROM 바이트에서 직접 재구성 가능한 상태다.
