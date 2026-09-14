# GS Korean → Pocket Monsters — Research Index

**현행 연구/분석 루트는 이 디렉터리 하나다:**

`CROSS-GEN/PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/`

이제 `INFRA/MIGRATION/**`, `INFRA/QUARANTINE/**`, 옛 `CROSS-GEN/TARGET/**`를 찾아다닐 필요가 없다. 그 경로들은 역사 보존용이다.

## 현재 작업 위치

- `ANALYSIS/GS-KOREAN-IMPLEMENTATION/PHASE-01` ~ `PHASE-11` — 세션에서 진행한 GS Korean 구현 분석 단계 전체
- `RESEARCH/GS-KOREAN-MODERNIZATION/` — Bank 6C UTF-8 추출, 한글 문자표, 공식 명칭 대조 원장, 코덱, Phase 2 기반 자료
- `CROSSWALK/` — CRGBY 적용용 교차대조
- `DESIGN/` — 통합 설계
- `REPORTS/` — 소스 ingest 및 ROM 구조 감사 보고서
- `TOOLS/` — 재현·분석 도구
- `MANIFESTS/` — 입력/대상 및 프로젝트 매니페스트
- `VERIFICATION/` — 검증 자료

Tsubaki의 대응 production 루트도 동일한 프로젝트 경로를 사용한다. 새 GS Korean → CRGBY 작업은 이 canonical project root 밖의 retired/migration 경로에 기록하지 않는다. ROM 바이너리는 커밋하지 않는다.
