# Generation IV → ポケットモンスター

이 작업공간은 출발점인 Generation IV와 도착점인 「ポケットモンスター」 양쪽의 모든 공식 작품·언어·지역·리비전 원본을 분리하여 조사하는 초기 기준점이다.

## 고정 원칙

- 모든 첨부 ROM은 읽기 전용 원본으로 취급한다.
- 원본 ROM이나 수정된 전체 ROM은 산출물에 포함하거나 공개 저장소에 올리지 않는다.
- 출발점과 도착점 어느 쪽에서도 일본판을 우선 또는 유일한 기준으로 두지 않는다. 모든 공식 언어·지역·리비전을 동등한 조사 원본으로 취급한다.
- 원본 차이는 `DP`, `Pt`, `HGSS` 작품군과 언어·지역·리비전별로 보존한다.
- 조사·설계·구현·검증 자료에는 원본, 역이식, 통합 수정, 프로젝트 신규 요소를 구분한다.
- Generation IV 조사 원본과 여러 세대·언어의 역이식 대상 ROM을 혼동하지 않는다.
- 대상 ROM은 사용자가 하나를 확정하기 전까지 후보끼리 합치거나 대표본으로 간주하지 않는다.

## 현재 확인된 입력

- Generation IV official research sources: Diamond (USA Rev 5), Pearl (USA Rev 5), Platinum (Korea Rev 0), HeartGold (Korea Rev 0), SoulSilver (Korea Rev 0)
- Target-side official research sources: Japanese and English GBA Ruby, Sapphire, Emerald, FireRed, LeafGreen; Korean GBC Gold

첨부된 대상 측 ROM 11개도 모두 공식 조사 원본이며, 일본어판 5개만 우선 대상으로 삼지 않는다. 현재 없는 언어·지역·리비전은 미확보 커버리지로 추가 관리하며, 확보된 다른 공식판의 지위를 낮추거나 작업을 정지시키지 않는다.

## 생성 파일

- `manifest/rom_inventory.json`: 전체 헤더·체크섬·역할 정보
- `manifest/rom_inventory.csv`: 표 계산 및 필터링용 동일 자료
- `tools/build_rom_inventory.py`: 원본 바이트를 변경하지 않는 재현 가능한 인벤토리 생성기
