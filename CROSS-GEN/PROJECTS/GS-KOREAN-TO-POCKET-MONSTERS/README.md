# GS Korean → Pocket Monsters

**Canonical active project root:** `CROSS-GEN/PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/`

이 디렉터리가 GS Korean → CRGBY 프로젝트의 단일 현행 연구/분석 루트다. `INFRA/MIGRATION/**` 및 `INFRA/QUARANTINE/**`은 과거 저장소 구조의 보존 스냅샷일 뿐이며, 현행 작업물을 찾기 위해 들어갈 필요가 없다. 새 작업도 그 경로에 기록하지 않는다.

## 바로 찾기

- `ANALYSIS/GS-KOREAN-IMPLEMENTATION/PHASE-01` ~ `PHASE-11`: 세션에서 진행한 GS Korean 구현 분석 단계 전체
- `GS-KOREAN-FOUNDATION/`: 한국판 금·은 Bank 6C UTF-8 추출, 한글 문자표, 공식 명칭 대조 원장, 코덱, Phase 2 기반 자료
- `CROSSWALK/`: CRGBY 적용용 교차대조
- `DESIGN/`: 통합 설계
- `REPORTS/`: 소스 ingest 및 ROM 구조 감사 보고서
- `TOOLS/`: 재현·분석 도구
- `MANIFESTS/`: 현재 입력/대상 및 프로젝트 매니페스트
- `VERIFICATION/`: 현재 검증 자료

## 저장 원칙

Sakurai는 분석·조사·비교·검증·문서·테이블·재현 도구의 현행본을 이 프로젝트 루트 아래에 둔다. Tsubaki의 대응 production 루트도 동일한 경로 `CROSS-GEN/PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/`를 사용한다. ROM 바이너리는 커밋하지 않는다.

2026-09-14에 PRE-V8/PRE-V12에 흩어져 있던 Phase 01~11 및 GS Korean foundation 작업물을 이 현행 루트로 승격했다. 과거 위치는 이력 보존용이다.
