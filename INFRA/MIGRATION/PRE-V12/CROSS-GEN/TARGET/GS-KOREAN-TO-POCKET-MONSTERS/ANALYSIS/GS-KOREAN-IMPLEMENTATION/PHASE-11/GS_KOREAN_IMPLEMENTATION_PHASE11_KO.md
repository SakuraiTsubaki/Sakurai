# GS Korean 구현 분석 11단계 — 트레이너 분류 67개 현대화

## 결론

- 한국판 표는 금·은 클래스 ID 1–66과 Crystal의 67번 `MYSTICALMAN`용 후행 문자열 1개로 구성된다.
- 한국판 금·은의 원본 표 영역은 완전히 동일하며 Phase 2 추출 데이터로 바이트 단위 재구성된다.
- 67개 중 18개를 수정 후보로 확정하고 49개는 유지한다.
- 모든 최종 문자열은 기존 GS Korean 문자표로 인코딩된다.
- 최장 표시 폭은 원본 9타일, 수정안 9타일이다.
- 논리 테이블은 681바이트에서 707바이트로 +26바이트 변한다.
- ROM은 쓰지 않았다. 다음 단계에서 배치·참조 방식을 검증한 뒤 후보 데이터를 만든다.

## 변경 목록

| ID | 내부 클래스 | 기존 한국어 | 최종 후보 | 분류 |
|---:|---|---|---|---|
| 10 | `POKEMON_PROF` | 포켓몬박사 | 포켓몬 박사 | ORTHOGRAPHY_AND_CURRENT_NAME |
| 20 | `SCIENTIST` | 괴짜 연구원 | 연구원 | CURRENT_OFFICIAL_CLASS_NAME |
| 23 | `SCHOOLBOY` | 학원끝난 아이 | 학원 끝난 아이 | ORTHOGRAPHY_NORMALIZATION |
| 25 | `LASS` | 짧은치마 | 짧은 치마 | ORTHOGRAPHY_NORMALIZATION |
| 27 | `COOLTRAINERM` | 엘리트트레이너 | 엘리트 트레이너 | ORTHOGRAPHY_NORMALIZATION |
| 28 | `COOLTRAINERF` | 엘리트트레이너 | 엘리트 트레이너 | ORTHOGRAPHY_NORMALIZATION |
| 31 | `GRUNTM` | 로켓단 | 로켓단 조무래기 | ROLE_RESTORATION |
| 33 | `SKIER` | 스키선수 | 스키어 | LATER_OFFICIAL_CLASS_NAME |
| 36 | `BUG_CATCHER` | 곤충채집 | 곤충채집소년 | CURRENT_OFFICIAL_CLASS_NAME |
| 38 | `SWIMMERM` | 수영팬티 소년 | 수영팬티소년 | ORTHOGRAPHY_NORMALIZATION |
| 49 | `JUGGLER` | 집시저글러 | 저글러 | OUTDATED_EXONYM_REMOVAL |
| 51 | `EXECUTIVEM` | 로켓단 | 로켓단 간부 | ROLE_RESTORATION |
| 53 | `PICNICKER` | 피크닉 걸 | 피크닉걸 | ORTHOGRAPHY_NORMALIZATION |
| 55 | `EXECUTIVEF` | 로켓단 | 로켓단 간부 | ROLE_RESTORATION |
| 56 | `SAGE` | 중 | 수행자 | LATER_OFFICIAL_CLASS_NAME |
| 59 | `POKEFANM` | 애호가 클럽 | 애호가클럽 | ORTHOGRAPHY_NORMALIZATION |
| 62 | `POKEFANF` | 애호가 클럽 | 애호가클럽 | ORTHOGRAPHY_NORMALIZATION |
| 66 | `GRUNTF` | 로켓단 | 로켓단 조무래기 | ROLE_RESTORATION |

## 중요한 판정

- `GRUNTM/GRUNTF`와 `EXECUTIVEM/EXECUTIVEF`는 기존 한국판에서 모두 ‘로켓단’으로 합쳐졌으나,
  내부 역할을 보존해 각각 ‘로켓단 조무래기’와 ‘로켓단 간부’로 분리한다.
- `MYSTICALMAN`용 ‘수수께끼의 청년’은 금·은의 유효 클래스 ID가 아니라 후행 호환 문자열이다.
  Crystal 이식 자료로 가치가 있으므로 삭제하지 않고 보존한다.
- `JUGGLER`의 ‘저글러’는 최신 공식 명칭이라고 단정하지 않는 프로젝트 편집 판정이다.
- 현대 명칭 자료는 추출·미러 자료이므로 모든 행의 직접 1차 공식 검증 표시는 `false`로 유지한다.

## 구조 경계

- 뱅크: `0x6C`
- 시작: CPU `0x49A1` / 파일 `0x1B09A1`
- 다음 표: CPU `0x4C4A` / 파일 `0x1B0C4A`
- 종료 바이트: `0x50`
- 한국판 금·은 원본 표 일치: 예
- ROM 출력: 없음
