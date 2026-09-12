# Generation IV Phase 2 — Semantic Data Map

## 1. 단계 목적

Phase 1에서 확정한 Nintendo DS 파일시스템/FAT/FNT/overlay/NARC 인벤토리를 바탕으로, 각 NARC가 실제로 담당하는 데이터 의미와 내부 멤버 구조를 연결한 단계다. 원본 ROM의 바이트 구조, pret 계열 디컴파일의 런타임 NARC 표, 코드의 실제 로더 범위를 교차하여 `확정`, `고신뢰 구조 추론`, `참조 추적 보류`를 구분한다. 파일이 존재한다는 사실만으로 실사용 또는 미사용을 단정하지 않는다.

## 2. 전체 NARC 의미 지도 규모

| Game | NARC archives | Total members | Resolved/path-named | Numeric unresolved | High-inference |
|---|---:|---:|---:|---:|---:|
| diamond | 149 | 33953 | 149 | 0 | 0 |
| pearl | 149 | 33953 | 149 | 0 | 0 |
| platinum | 215 | 53505 | 215 | 0 | 0 |
| heartgold | 308 | 56674 | 110 | 198 | 2 |
| soulsilver | 308 | 56674 | 110 | 198 | 2 |

HGSS의 `numeric_unresolved`는 데이터가 미상이라는 뜻이 아니라, `a/x/y/z` 숫자형 파일의 **symbolic name이 아직 디컴파일에서 복구되지 않은 항목**이다. 런타임 NARC ID 자체는 numeric path에서 계산 가능하다. `a/0/0/0`과 `a/0/0/1`은 DPPt의 동일한 NARC ID 순서, 멤버 구조, 기술 스크립트의 468~500번 더미 꼬리 일치에 근거하여 각각 `battle/skill/waza_seq`, `battle/skill/sub_seq`로 고신뢰 구조 추론했다.

## 3. 핵심 데이터 구조 비교

| Game | Role | Path | Members | Uniform record | Min–Max | Confidence |
|---|---|---|---:|---:|---:|---|
| diamond | personal | `poketool/personal/personal.narc` | 501 | 44 | 44–44 | medium-high |
| diamond | growth | `poketool/personal/growtbl.narc` | 8 | 404 | 404–404 | medium-high |
| diamond | evolution | `poketool/personal/evo.narc` | 501 | 44 | 44–44 | medium-high |
| diamond | levelup_moves | `poketool/personal/wotbl.narc` | 501 | — | 4–44 | medium-high |
| diamond | move_table | `poketool/waza/waza_tbl.narc` | 471 | 16 | 16–16 | medium-high |
| diamond | move_scripts | `battle/skill/waza_seq.narc` | 501 | — | 4–24 | medium-high |
| diamond | item_data | `itemtool/itemdata/item_data.narc` | 442 | 34 | 34–34 | medium-high |
| diamond | trainer_data | `poketool/trainer/trdata.narc` | 850 | 20 | 20–20 | medium-high |
| diamond | trainer_parties | `poketool/trainer/trpoke.narc` | 850 | — | 8–96 | medium-high |
| diamond | field_scripts | `fielddata/script/scr_seq_release.narc` | 1051 | — | 0–8508 | medium-high |
| diamond | zone_events | `fielddata/eventdata/zone_event_release.narc` | 512 | — | 16–1660 | medium-high |
| diamond | land_data | `fielddata/land_data/land_data_release.narc` | 578 | — | 2710–66712 | medium-high |
| diamond | map_matrix | `fielddata/mapmatrix/map_matrix.narc` | 245 | — | 13–4508 | medium-high |
| diamond | messages | `msgdata/msg.narc` | 624 | — | 18–296818 | medium-high |
| pearl | personal | `poketool/personal_pearl/personal.narc` | 501 | 44 | 44–44 | medium-high |
| pearl | growth | `poketool/personal/growtbl.narc` | 8 | 404 | 404–404 | medium-high |
| pearl | evolution | `poketool/personal/evo.narc` | 501 | 44 | 44–44 | medium-high |
| pearl | levelup_moves | `poketool/personal/wotbl.narc` | 501 | — | 4–44 | medium-high |
| pearl | move_table | `poketool/waza/waza_tbl.narc` | 471 | 16 | 16–16 | medium-high |
| pearl | move_scripts | `battle/skill/waza_seq.narc` | 501 | — | 4–24 | medium-high |
| pearl | item_data | `itemtool/itemdata/item_data.narc` | 442 | 34 | 34–34 | medium-high |
| pearl | trainer_data | `poketool/trainer/trdata.narc` | 850 | 20 | 20–20 | medium-high |
| pearl | trainer_parties | `poketool/trainer/trpoke.narc` | 850 | — | 8–96 | medium-high |
| pearl | field_scripts | `fielddata/script/scr_seq_release.narc` | 1051 | — | 0–8508 | medium-high |
| pearl | zone_events | `fielddata/eventdata/zone_event_release.narc` | 512 | — | 16–1660 | medium-high |
| pearl | land_data | `fielddata/land_data/land_data_release.narc` | 578 | — | 2710–66712 | medium-high |
| pearl | map_matrix | `fielddata/mapmatrix/map_matrix.narc` | 245 | — | 13–4508 | medium-high |
| pearl | messages | `msgdata/msg.narc` | 624 | — | 18–296818 | medium-high |
| platinum | personal | `poketool/personal/pl_personal.narc` | 508 | 44 | 44–44 | medium-high |
| platinum | growth | `poketool/personal/pl_growtbl.narc` | 8 | 404 | 404–404 | medium-high |
| platinum | evolution | `poketool/personal/evo.narc` | 508 | 44 | 44–44 | medium-high |
| platinum | levelup_moves | `poketool/personal/wotbl.narc` | 508 | — | 4–44 | medium-high |
| platinum | move_table | `poketool/waza/pl_waza_tbl.narc` | 471 | 16 | 16–16 | medium-high |
| platinum | move_scripts | `battle/skill/waza_seq.narc` | 501 | — | 4–24 | medium-high |
| platinum | item_data | `itemtool/itemdata/pl_item_data.narc` | 446 | 34 | 34–34 | medium-high |
| platinum | trainer_data | `poketool/trainer/trdata.narc` | 928 | 20 | 20–20 | medium-high |
| platinum | trainer_parties | `poketool/trainer/trpoke.narc` | 928 | — | 8–108 | medium-high |
| platinum | field_scripts | `fielddata/script/scr_seq.narc` | 1124 | — | 4–9132 | medium-high |
| platinum | zone_events | `fielddata/eventdata/zone_event.narc` | 534 | — | 16–1660 | medium-high |
| platinum | land_data | `fielddata/land_data/land_data.narc` | 666 | — | 2972–64212 | medium-high |
| platinum | map_matrix | `fielddata/mapmatrix/map_matrix.narc` | 289 | — | 13–4508 | medium-high |
| platinum | messages | `msgdata/pl_msg.narc` | 714 | — | 18–160410 | medium-high |
| heartgold | personal | `a/0/0/2` | 508 | 44 | 44–44 | high |
| heartgold | growth | `a/0/0/3` | 8 | 404 | 404–404 | high |
| heartgold | evolution | `a/0/3/4` | 508 | 44 | 44–44 | high |
| heartgold | levelup_moves | `a/0/3/3` | 508 | — | 4–44 | high |
| heartgold | move_table | `a/0/1/1` | 471 | 16 | 16–16 | high |
| heartgold | move_scripts | `a/0/0/0` | 501 | — | 4–24 | high-inference |
| heartgold | item_data | `a/0/1/7` | 514 | 34 | 34–34 | high |
| heartgold | trainer_data | `a/0/5/5` | 738 | 20 | 20–20 | high |
| heartgold | trainer_parties | `a/0/5/6` | 738 | — | 8–108 | high |
| heartgold | field_scripts | `a/0/1/2` | 965 | — | 4–8728 | high |
| heartgold | zone_events | `a/0/3/2` | 491 | — | 16–1660 | high |
| heartgold | land_data | `a/0/6/5` | 676 | — | 2658–72696 | high |
| heartgold | map_matrix | `a/0/4/1` | 288 | — | 13–4003 | high |
| heartgold | messages | `a/0/2/7` | 822 | — | 20–100706 | high |
| soulsilver | personal | `a/0/0/2` | 508 | 44 | 44–44 | high |
| soulsilver | growth | `a/0/0/3` | 8 | 404 | 404–404 | high |
| soulsilver | evolution | `a/0/3/4` | 508 | 44 | 44–44 | high |
| soulsilver | levelup_moves | `a/0/3/3` | 508 | — | 4–44 | high |
| soulsilver | move_table | `a/0/1/1` | 471 | 16 | 16–16 | high |
| soulsilver | move_scripts | `a/0/0/0` | 501 | — | 4–24 | high-inference |
| soulsilver | item_data | `a/0/1/7` | 514 | 34 | 34–34 | high |
| soulsilver | trainer_data | `a/0/5/5` | 738 | 20 | 20–20 | high |
| soulsilver | trainer_parties | `a/0/5/6` | 738 | — | 8–108 | high |
| soulsilver | field_scripts | `a/0/1/2` | 965 | — | 4–8728 | high |
| soulsilver | zone_events | `a/0/3/2` | 491 | — | 16–1660 | high |
| soulsilver | land_data | `a/0/6/5` | 676 | — | 2658–72696 | high |
| soulsilver | map_matrix | `a/0/4/1` | 288 | — | 13–4003 | high |
| soulsilver | messages | `a/0/2/7` | 822 | — | 20–100706 | high |

### 구조적으로 확정되는 공통 단위

- Pokémon personal/base stats 레코드: D/P 501개, Pt/HGSS 508개, **각 44바이트**.
- 성장표: 8개 × 404바이트.
- 진화표: 종/폼 슬롯별 **44바이트**.
- 기술 데이터: 471개 × **16바이트**.
- 아이템 데이터: D/P 442개, Pt 446개, HGSS 514개 × **34바이트**.
- 트레이너 헤더: D/P 850, Pt 928, HGSS 738 × **20바이트**.
- 기술 습득표·트레이너 파티·필드 스크립트·이벤트·land/map matrix는 가변 길이 멤버다.

## 4. Diamond ↔ Pearl 실제 데이터 차이 — personal 6종

D/P의 버전별 personal archive는 501 × 44바이트이며 전체 중 **6개 species 레코드만 다르다**. 차이는 BaseStats의 0x0C~0x0F, 즉 `item1`/`item2` 두 u16 필드에만 존재한다.

| ID | Species | Diamond item1 / item2 | Pearl item1 / item2 |
|---:|---|---|---|
| 125 | Electabuzz | Electirizer / None | None / Electirizer |
| 126 | Magmar | None / Magmarizer | Magmarizer / None |
| 239 | Elekid | Electirizer / None | None / Electirizer |
| 240 | Magby | None / Magmarizer | Magmarizer / None |
| 466 | Electivire | Electirizer / None | None / Electirizer |
| 467 | Magmortar | None / Magmarizer | Magmarizer / None |

Electirizer는 item ID 322, Magmarizer는 323이다. 일반 held-item odds 테이블에서는 item1과 item2가 서로 다른 확률 슬롯이므로 이 교환은 단순 정렬 차이가 아니라 버전별 야생 소지 확률 차이를 만든다. 정확한 확률 모드 의미는 호출부까지 계속 추적하되, ROM과 코드에서 odds 두 세트 `{45,95}` / `{20,80}` 및 item1/item2 분기 자체는 확인됐다.

## 5. Platinum 확장 구조와 한국어 리소스 계층

Platinum은 D/P의 핵심 구조를 그대로 대체하는 것이 아니라, 다수의 `pl_*` 아카이브와 신규 시스템 아카이브를 **병렬 추가**한다. 예: `pl_personal` 508, `pl_waza_tbl` 471, `pl_item_data` 446, `pl_enc_data` 183, Frontier·Distortion World 관련 자원 등.

한국판 Pt에는 `resource/kor/` 아래 **32개 NARC, 총 2,801개 멤버**가 별도 존재한다. 가방, 배틀 오브젝트, 박스, 콘테스트, Frontier, 이름 입력, Pokétch, 타이틀/오프닝, 상태창, Trainer Case, VS 데모, Wi-Fi Lobby, 도감 등 시각·UI·현지화 자원이 분리되어 있다.

### D/P와 바이트 단위로 동일하게 남아 있는 Pt 병렬 아카이브

| Path | Identical to Diamond | Usage classification |
|---|---|---|
| `poketool/personal/personal.narc` | true | parallel-legacy-archive-reference-tracing-pending |
| `poketool/personal/growtbl.narc` | true | parallel-legacy-archive-reference-tracing-pending |
| `poketool/waza/waza_tbl.narc` | true | parallel-legacy-archive-reference-tracing-pending |
| `itemtool/itemdata/item_data.narc` | true | parallel-legacy-archive-reference-tracing-pending |
| `poketool/pokegra/otherpoke.narc` | true | parallel-legacy-archive-reference-tracing-pending |
| `poketool/pokeanm/pokeanm.narc` | true | parallel-legacy-archive-reference-tracing-pending |
| `pokeanime/poke_anm.narc` | true | parallel-legacy-archive-reference-tracing-pending |

이 일치만으로 `unused`라고 확정하지 않는다. Platinum의 실제 코드 참조/직접 경로 접근까지 추적한 뒤 `active / compatibility / leftover / unused`를 분리한다.

## 6. HeartGold ↔ SoulSilver 데이터 차이 축

Phase 1의 공통 경로 비교에서 일반 NitroFS 데이터 NARC 차이는 정확히 3개로 좁혀졌으며 Phase 2에서 내부 멤버까지 확정했다.

| Runtime NARC ID | Path | Semantic role | Different members |
|---:|---|---|---:|
| 75 | `a/0/7/5` | application/zukanlist/zkn_data/zukan_hw_data | 1 |
| 133 | `a/1/3/3` | application/zukanlist/zkn_data/zukan_enc | 130 |
| 254 | `a/2/5/2` | arc/headbutt | 33 |

합계 **164개 멤버**가 다르다: Pokédex height/weight 계열 1개, Pokédex encounter 계열 130개, Headbutt 계열 33개. 실행 overlay 차이는 별도의 코드 차이 축으로 유지한다.

### HGSS 런타임 NARC ID 주의점

`sNarcFileList`에는 numeric `a/x/y/z` 흐름 중 runtime ID 194·195에 `pbr/pokegra.narc`, `pbr/otherpoke.narc`가 삽입된다. 따라서 numeric code 194 이상은 runtime NARC ID가 +2 이동한다. 예를 들어 egg move list는 ID 231=`a/2/2/9`, Headbutt는 ID 254=`a/2/5/2`, photo data는 ID 256=`a/2/5/4`다.

## 7. 확인된 미사용·더미 기술 슬롯

기술의 정상 ID 상한은 Shadow Force #467이며 정상 move loader는 `(NUM_MOVES + 1)`개, 즉 **0~467의 468개 레코드**만 읽는다. 그런데 다섯 ROM 모두 move table에는 471개의 16바이트 레코드가 있어 **468, 469, 470** 세 레코드는 정상 기술 ID 경로 밖에 남는다.

또한 다섯 ROM 모두 `waza_seq`에 501개 멤버가 있고, 정상 전투에서는 현재 move ID를 멤버 번호로 사용한다. **468~500의 33개 멤버는 전부 동일한 4바이트 `24 00 00 00`**이며 정상 move ID로 도달할 수 없다.

- move-table unreachable records: 5 × 3 = **15**
- move-script dummy records: 5 × 33 = **165**
- 현재 이 범주에서 확인된 합계: **180 records**

이 항목들은 프로젝트의 “unused를 정상 콘텐츠화” 단계에서 가장 먼저 안전한 신규 슬롯 후보로 검토할 수 있다. 단, 기존 sentinel/guard가 아닌지 호출부를 한 번 더 확인한 후 새 ID·테이블 한계를 함께 확장해야 한다.

## 8. 런타임 NARC 표 밖의 파일 — 아직 unused가 아님

D/P에는 표준 NarcId path table 밖에 `data/trapmark.narc`, `data/ug_radar.narc`, `resource/eng/trial/trial.narc` 3개가 각각 존재한다. HGSS에는 `sNarcFileList` 밖의 NARC가 버전당 **41개** 있다. 이들은 직접 경로 접근, overlay 내부 참조, 호환성/잔존 자원일 수 있으므로 현재 상태는 전부 `reference-tracing-pending`이다.

## 9. HeartGold 작업 사본 무결성 주의

Phase 1에서 해시를 고정한 HeartGold 기준본은 128 MiB였지만 현재 런타임의 `/mnt/data/포켓몬스터 하트골드.nds`는 약 114.1 MB에서 끊긴 사본이다. FAT가 가리키는 후반 PBR 자원 12개가 현재 파일 끝 이후에 있다. Phase 2 인벤토리에서는 Phase 1에서 SoulSilver와 SHA-1 동일성이 확인된 해당 12개 항목의 구조 프로필만 SoulSilver에서 대리 복원하고 `high-proxy`로 표시했다. 이 현상을 원본 HeartGold의 결손으로 취급하지 않는다.

## 10. 산출물

- `semantic_narc_map.csv`: 5개 ROM 전체 NARC 의미/근거/신뢰도 지도
- `archive_member_profiles.csv`: 전체 NARC의 멤버 수·크기 분포·SHA-1 프로필
- `core_structure_matrix.csv`: 핵심 게임 데이터 구조 비교
- `dp_personal_version_diffs.csv`: D/P 6종 personal 차이
- `hgss_version_narc_member_diffs.csv`: HG/SS 164개 차이 멤버
- `platinum_korean_resource_map.csv`: 한국 Pt 전용 32개 리소스 NARC
- `platinum_parallel_legacy_archives.csv`: Pt에 남은 D/P 동일 병렬 아카이브
- `runtime_narc_table_exceptions.csv`: 런타임 NARC 표 밖 자원과 조사 상태
- `confirmed_unused_move_slots.csv`: 정상 move ID로 도달 불가한 180개 레코드

## 11. Phase 3 진입 기준

다음 단계는 **개별 레코드 완전 디코딩**이다. personal 508계열 → 진화 508계열 → 기술 468개 정상 항목 → 아이템 → 트레이너 → 조우 → field script/event → map/land 순으로 ID별 원장을 만들고, D/P/Pt/HG/SS 값 차이를 한 행에서 비교한다. 폼용 추가 personal/moveset 슬롯과 Pt/HGSS의 확장 슬롯도 base species와 분리하여 연결한다.
