# GOLD KR 확장 엔진 — 원본 ROM 한계 및 최신 아키텍처

> 상태: CURRENT / Stage 0 프로토타입 설계를 대체하는 최신 기준
> Source lock: `SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c`

## 1. 기준 ROM

- SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`
- 크기: 2 MiB (`128 × 16 KiB ROM banks`)
- 카트리지: MBC3 + RTC + RAM + Battery
- SRAM: 32 KiB (`4 × 8 KiB`)
- 원본 ROM은 저장소에 포함하지 않는다.

## 2. 현재 데이터셋 목표

- Species: 1025
- Battle Variety / Pokemon record: 1351
- Form record: 1579
- 10세대 이후: 기존 ID를 재배치하지 않고 append-only 확장

```text
Species ID : uint16
Variety ID : uint16
Form ID    : uint16
```

EGG는 species namespace에서 분리하고, 최종 목표에서 `SPECIES_* ID == National Dex species number`를 유지한다.

## 3. 원본 ROM의 확실한 빈 공간

128개 ROM bank 실측에서 다음 24개 bank가 통째로 `00`이다.

```text
13 22 27 28 29 2C 2D 2F
34 35
58
63 67
6A 6B 6F
73 74 75 76 77
7C 7D 7E
```

합계 24 banks = 393,216 bytes = 384 KiB. 부분 빈 bank는 링커 맵/실행 경로 검증 후 사용한다.

## 4. 16-bit 전환 감사 대상

원본 `MON_SPECIES`와 Pokémon 상수는 8-bit/251종 전제를 가진다. 따라서 다음 경로를 16-bit-safe하게 감사한다.

- party / box species access
- wild encounter / trainer party / evolution targets
- names / base data / cries
- sprites / palettes / icons
- Pokédex indexing
- breeding / daycare / Hall of Fame
- link/trade compatibility layer

## 5. BaseData / SRAM

원본 BaseData는 32 bytes/record이다. 1351 battle profile도 고정 파라미터 용량 자체는 핵심 병목이 아니다.

원본 `BOXMON_STRUCT_LENGTH`는 32 bytes이며 14개 박스가 32 KiB SRAM 구조에 빡빡하게 배치된다. `MON_POKERUS` 뒤, `MON_LEVEL` 앞의 예약 2바이트는 확장 메타데이터 후보로 사용할 수 있다. BoxMon 크기는 가능한 한 유지한다.

## 6. Move / Item namespace

Move ID와 Item ID도 8-bit다. Move는 개체당 4개 필드라 단순 uint16 전환 시 SRAM 비용이 크다. 후보 설계는 8-bit local dictionary + 16-bit master ID, side table, versioned extended slots 등이다.

## 7. Pokédex / Variety / Form

Seen/Caught bitset 용량 자체보다 UI·count·index 경로의 8-bit 전제가 문제다.

```text
Species (National Dex identity)
  └─ Variety / Battle Profile
       └─ Form / Appearance record
```

Ability, Nature, move category, modern EV, evolution methods, regional/form mechanics는 기존 BaseData를 무작정 키우지 않고 별도 확장 테이블로 둔다.

## 8. 실제 용량 병목

1. front/back sprite data
2. form-specific graphics
3. move data + animations
4. Pokédex text
5. cries/audio

바이트 동일 그래픽은 deduplicate한다.

## 9. Mapper 확장

현재 MBC3 / 2 MiB / 128 banks / 32 KiB SRAM. 2 MiB가 부족하면 우선 MBC30 4 MiB / 256-bank 경로를 검토한다. 8 MiB MBC5는 9번째 ROM-bank bit 때문에 bank API 자체 확장이 필요하다.

## 10. 결론

핵심 하드캡은 단순한 “251 Pokémon”이 아니라 8-bit Species/Move/Item namespace, 32-byte BoxMon + 32 KiB SRAM, MBC3 2 MiB 구조다.

최종 설계는 native 16-bit Species/Variety/Form을 기준으로 한다. Stage 0의 `0xFC + ext16 species` sentinel 방식은 재현 가능한 초기 프로토타입으로만 보존한다.

## Provenance

Role-split copy derived from `pokegold-kr/docs/gold-natdex/GOLD_ROM_LIMITS_AND_ARCHITECTURE.md`. Engine implementation remains canonical in `SakuraiTsubaki/pokegold-kr`; this file is the Sakurai research/specification owner.
