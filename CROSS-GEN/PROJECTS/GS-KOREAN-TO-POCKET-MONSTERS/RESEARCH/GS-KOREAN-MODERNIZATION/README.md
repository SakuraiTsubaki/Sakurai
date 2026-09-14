# GS Korean Modernization

한국 정식판 『포켓몬스터 금』과 『포켓몬스터 은』을 읽기 전용 원본으로 잠그고, 한국어 텍스트와 공식 명칭을 현재 공식 기준으로 전면 현대화하는 Generation II 다중 게임 타깃이다.

## Canonical routing

```text
Gold source   GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0/
Silver source GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0/
Comparison    GEN-02/COMPARE/GOLD-AAUK-HV0--SILVER-AAXK-HV0/
Target        GEN-02/TARGET/GS-KOREAN-MODERNIZATION/
```

ROM 바이너리는 저장하지 않는다. 해시, 헤더, 구조 분석, 추출 데이터, 코덱, 매핑, 검증 결과와 재현 가능한 도구만 버전 관리한다.

## Sakurai ownership

- 릴리스/덤프 식별과 provenance
- ROM 구조와 뱅크 분석
- 한국어 문자표와 UTF-8 디코드 자료
- 6C 명칭 추출 및 공식 명칭 대조 원장
- 번역·교정 정책과 최신 공식 명칭 적용 규칙
- Gold/Silver 비교 근거와 회귀 검증

생산용 자산, 변환 결과, 구현, 패치와 빌드 메타데이터는 동일 ID 체계를 사용하는 Tsubaki가 소유한다.

## Canonical Phase 2 artifacts

격리된 pre-v8 migration snapshot에 있던 검증 산출물을 바이트 변경 없이 v9 경로로 승격했다.

```text
INPUTS/ROM-DERIVED/TEXT/bank_6c_names_utf8.csv
INPUTS/ROM-DERIVED/TEXT/bank_6c_names_utf8.json
INPUTS/ROM-DERIVED/TEXT/korean_charmap.csv
INPUTS/ROM-DERIVED/TEXT/korean_charmap.json
MAPPINGS/official_name_comparison_master.csv
MAPPINGS/official_name_comparison_master.json
TOOLS/gs_korean_codec.py
REPORTS/GS_KOREAN_IMPLEMENTATION_PHASE2_KO.md
REPORTS/phase2_summary.json
```

다음 작업은 `official_name_comparison_master`의 미검증 항목을 최신 공식 한국어 명칭으로 전수 대조한 뒤, 뱅크 68–69 도감 설명문 추출·현대화로 이어간다.
