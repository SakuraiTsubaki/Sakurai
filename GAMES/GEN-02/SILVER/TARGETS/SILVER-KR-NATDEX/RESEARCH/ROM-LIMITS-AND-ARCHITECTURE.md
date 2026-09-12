# SILVER KR 확장 엔진 — 원본 ROM 한계 및 최신 아키텍처

> 상태: CURRENT
> 기준일: 2026-09-07
> Source lock: `SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c`

## 1. 기준

한국판 Gold/Silver 디스어셈블리 구현 기준은 `SakuraiTsubaki/pokegold-kr`다. 원본 Silver ROM은 저장소에 포함하지 않으며 사용자가 보유한 base ROM을 빌드 입력으로 사용한다.

## 2. 데이터셋 / ID 목표

- Species: 1025
- Battle Variety / Pokémon records: 1351
- Form records: 1579
- Generation 10+: 기존 ID 재배치 없이 append-only

```text
Species
  -> Variety / Battle Profile
      -> Form / Appearance Record
```

최종 ID는 Species/Variant 16-bit를 기준으로 하고 EGG는 Species namespace 밖의 개체 상태로 분리한다.

## 3. 원본 8-bit 한계

Gen II는 `MON_SPECIES`, `wCurSpecies`, 파티/박스 빠른 species 목록, 야생/트레이너/진화/링크 등에서 species를 1 byte로 취급한다. BaseData만 늘리는 것으로는 해결되지 않으며 모든 8-bit copy/index/compare 경로를 감사해야 한다.

## 4. BoxMon / SRAM

원본 BoxMon은 32 bytes이고 Pokerus 뒤, Level 앞 2 bytes unused 영역이 있다. 확장 ID/form metadata 후보로 활용하되 BoxMon 32-byte 크기는 가능한 한 유지한다. 빠른 species list, Hall of Fame, daycare 등의 별도 1-byte truncation 경로도 패치 대상이다.

## 5. BaseData / Pokédex

고정 BaseData 용량 자체는 주된 병목이 아니다. 핵심은 원본 `GetBaseData`의 8-bit index + 단일 bank 전제이며, multi-bank + extended-ID lookup으로 일반화해야 한다.

Seen/Caught bitset도 용량 자체보다 WRAM/save 위치, count 루틴, UI index의 251-era 전제가 문제다.

## 6. Move / Item / 이름

Move ID와 Item ID도 8-bit다. 특히 BoxMon의 4개 move slot을 단순 u16화하면 SRAM 비용이 커지므로 Species 확장과 별도 설계 단계로 관리한다.

고정 이름 길이 역시 현대 공식명 전체 표시를 위해 포인터/가변 길이 렌더링 또는 언어별 확장 UI 검토가 필요하다.

## 7. ROM 용량 / Mapper 실측

Silver는 MBC3 + RTC 구조다.

- 일본 Silver 계열: 1 MiB / 64 banks
- 국제/한국 Silver 계열: 2 MiB / 128 banks
- SRAM: 32 KiB

8개 Silver ROM 비교에서 국제/한국 2 MiB 6개 빌드에 공통으로 완전히 0인 bank가 20개(320 KiB) 확인되었다. 일본 1 MiB 두 개까지 2 MiB로 zero-padding하면 8개 모두 공통으로 비어 있는 bank는 11개(176 KiB)다.

## 8. 그래픽 구조

```text
Species / Variant / Form
        -> GraphicSetID
        -> front/back
        -> palette
        -> icon
        -> animation/metadata
```

동일 그래픽 자산은 deduplicate한다. 1351 variety / 1579 form의 전체 그래픽·애니메이션·팔레트·아이콘·cry까지 포함하면 2 MiB가 병목이 될 가능성이 높다.

## 9. 구현 순서

1. Species/Variant 16-bit ID API
2. EGG 분리
3. party/box/temp/battle species 전달 확장
4. wild/trainer/evolution/daycare/Hall of Fame/link 확장
5. BaseData multi-bank lookup
6. names/cries/icon/sprite/palette lookup 일반화
7. Pokédex seen/caught 저장/UI 확장
8. 1025 Species / 1351 Variant 데이터 주입
9. 1579 Form mapping
10. 그래픽 실측 후 MBC3 2 MiB 유지 여부 재판정

## Provenance

Role-split copy derived from `pokegold-kr/docs/silver-natdex/SILVER_ROM_LIMITS_AND_ARCHITECTURE.md`. Engine implementation remains canonical in `SakuraiTsubaki/pokegold-kr`; this file is the Sakurai research/specification owner.
