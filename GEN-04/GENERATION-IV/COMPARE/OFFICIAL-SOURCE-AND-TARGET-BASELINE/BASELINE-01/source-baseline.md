# Generation IV → ポケットモンスター: Source Baseline 01

작성 기준일: 2026-09-12 UTC

## 결론

현재 첨부된 16개 ROM은 모두 헤더 검증을 통과했다. Generation IV 직접 원본은 5개 작품이 모두 존재하며 미국 영어판과 한국어판으로 구성된다. 이 다섯 파일은 모두 동등한 공식 조사 원본이다.

일본판은 여러 공식 언어·지역판 가운데 하나이며 우선·유일 기준이 아니다. 특정 언어판의 부재를 이유로 확보된 다른 공식판을 보조본으로 격하하지 않는다.

| 작품 | 내부 코드 | 언어·지역 | 리비전 | 용량 | 역할 |
|---|---:|---|---:|---:|---|
| Pokémon Diamond | ADAE | 미국/영어 | 5 | 64 MiB | 공식 조사 원본·동등 지위 |
| Pokémon Pearl | APAE | 미국/영어 | 5 | 64 MiB | 공식 조사 원본·동등 지위 |
| Pokémon Platinum | CPUK | 한국/한국어 | 0 | 128 MiB | 공식 조사 원본·동등 지위 |
| Pokémon HeartGold | IPKK | 한국/한국어 | 0 | 128 MiB | 공식 조사 원본·동등 지위 |
| Pokémon SoulSilver | IPGK | 한국/한국어 | 0 | 128 MiB | 공식 조사 원본·동등 지위 |

Diamond와 Pearl의 SHA-1은 `pret/pokediamond`가 빌드 대상으로 명시한 미국판 해시와 일치한다. 이 두 파일은 단순 파일명 추정이 아니라 내부 코드, 리비전 바이트, 헤더 CRC, 전체 SHA-1이 서로 일치한다.

## 역이식 대상 후보

일본어 GBA판은 다음 5개가 존재한다.

| 작품 | 내부 코드 | 리비전 | 용량 |
|---|---:|---:|---:|
| Pocket Monsters Ruby | AXVJ | 0 | 8 MiB |
| Pocket Monsters Sapphire | AXPJ | 0 | 8 MiB |
| Pocket Monsters Emerald | BPEJ | 0 | 16 MiB |
| Pocket Monsters FireRed | BPRJ | 1 | 16 MiB |
| Pocket Monsters LeafGreen | BPGJ | 0 | 16 MiB |

이들은 모두 Gen III 일본어판 `ポケットモンスター`이며, Generation IV 조사 원본이 아니라 역이식·확장·통합 대상 ROM 후보다. 서로 다른 엔진 계통과 게임 콘텐츠를 가진 독립 후보이므로 하나를 임의로 대표 대상으로 선택하지 않는다.

## 비교 원본

- 영어 GBA: Ruby Rev 2, Sapphire Rev 2, Emerald Rev 0, FireRed Rev 1, LeafGreen Rev 1
- 한국어 GBC: Gold Rev 0

이 6개는 언어·리비전 또는 이전 세대 구조를 비교하는 자료로 분리한다. 일본어 GBA 대상 원본과 합치거나 덮어쓰지 않는다.

## 미확보 조사 커버리지

현재 일본어판 Diamond, Pearl, Platinum, HeartGold, SoulSilver는 첨부되어 있지 않다. 다음 항목은 일본어판 원본이 확보될 때 별도 공식 원본으로 추가 조사한다.

- Generation IV 당시의 일본어 고유 명칭·대사·문자 인코딩·폰트
- 일본판만의 스크립트, 배포, 통신, 검열 및 리비전 차이
- 일본판과 미국·한국판 사이의 파일 배치 및 데이터 차이

이 미확보 상태는 현재 미국판·한국판 NDS 조사를 중단시키거나 그 공식 원본 지위를 낮추지 않는다. 현재 5개 NDS로 시스템·구조·그래픽·사운드와 영어·한국어 현지화를 즉시 조사하며, 일본어판 관련 주장만 `미확보/미검증`으로 제한한다. 이후 유럽 각 언어판과 다른 공식 지역·리비전도 같은 방식으로 커버리지 원장에 추가한다.

## 후속 작업 게이트

1. 확보된 NDS 5종의 ARM9/ARM7, overlay, NitroFS, NARC, banner 구조를 작품·언어·지역·리비전별로 추출한다.
2. DP 공통·버전 고유, Pt 수정·확장, HGSS 재구축 요소를 분리하고 언어·지역판 차이 열을 유지한다.
3. 미확보된 공식 언어·지역·리비전은 커버리지 원장에 누락 상태로 기록하고, 확보 시 동등한 원본으로 추가한다.
4. 일본어 Gen III 대상 후보 5종 각각의 엔진, ROM 여유 공간, 포인터·테이블 한계를 조사한다.
5. 사용자가 최종 대상 게임 또는 다중 대상 정책을 확정한 뒤에만 구현 브랜치를 만든다.
6. 원본 바이트는 변경하지 않고, 모든 구현은 별도 작업본·패치·소스에서 수행한다.

## 검증 산출물

- `manifest/rom_inventory.json`: 전체 필드와 SHA-256을 포함한 기계 판독 원장
- `manifest/rom_inventory.csv`: 필터·비교용 평면 원장
- `tools/build_rom_inventory.py`: 동일 원장을 재생성하는 읽기 전용 도구

ROM 파일은 이 패키지에 포함하지 않는다.
