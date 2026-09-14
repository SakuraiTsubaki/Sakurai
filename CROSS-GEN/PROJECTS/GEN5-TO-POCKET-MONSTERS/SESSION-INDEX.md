# Generation V project session → artifact index

이 파일은 ChatGPT `Generation V` 프로젝트에서 진행한 주요 세션이 GitHub의 어디에 반영되어 있는지 찾기 위한 인덱스다. 현재 작업물의 단일 진입점은 이 디렉터리(`CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS/`)다.

| 프로젝트 세션 / 작업 축 | 현재 정규 위치 | 상태 |
|---|---|---|
| 세대5 원본 조사 / BW 전수조사 시작 | `BLACK/`, `WHITE/`, `SHARED/` | Black/White release identity, inventory, native structure, tools를 프로젝트 루트에서 바로 탐색 |
| 포켓몬 화이트 ROM 검사 / 화이트 집중 완전 해체 | `WHITE/RELEASES/NDS-TWL/CART/IRAO-HV0/` | W1–W5, `DOMAINS/`, `NATIVE/`, `TOOLS/`, `VERIFICATION/`, dump provenance 복구 완료 |
| White W1–W5 보고서 | `WHITE/RELEASES/NDS-TWL/CART/IRAO-HV0/REPORTS/` | `WHITE-W1-DIRECT-ROM-STRUCTURE.md` ~ `WHITE-W5-COMPLETE-DECONSTRUCTION.md` |
| Generation V 비교 분석 | `COMPARES/BLACK-IRBO-HV0--WHITE-IRAO-HV0/` | Black/White structural/component/NitroFS delta 및 비교 보고서 |
| 롬 재현 작업 자료 만들기 | `MANIFESTS/`, `TOOLS/`, `VERIFICATION/` | source/target lock, provenance, audit/revalidation 도구와 검증 자료. 실제 build/implementation 산출물은 Tsubaki의 같은 프로젝트 루트에 존재 |
| 롬 확장 규모 검토 | `DESIGN/`, `REPORTS/`, `MANIFESTS/` | 설계·기준 자료 축으로 통합; 세션별 독립 파일명으로 분리하지 않은 항목은 여기서 추적 |
| Generation V 버그·글리치·오류 조사 | `REPORTS/`, `DESIGN/`, `VERIFICATION/` | 조사/검증 축. 개별 버그가 ROM 직접 검증되지 않은 경우 확정 사실로 승격하지 않음 |
| unused / dummy 정상화 | `DESIGN/`, `MANIFESTS/`, `VERIFICATION/` | 미사용 요소를 삭제하지 않고 reachability/정상화 검증 대상으로 유지하는 프로젝트 정책 축 |
| 최신 공식 사양으로 현대화 | `DESIGN/`, `CROSSWALK/`, `MANIFESTS/` | 원본 조사와 현대화 설계를 분리하여 관리 |
| 롬 글리프 / 텍스트 분석 | `WHITE/RELEASES/NDS-TWL/CART/IRAO-HV0/DOMAINS/text/` 및 W5 보고서 | BW1 text archive/bank 구조 및 검증된 text-bank 자료 |
| 스프라이트 픽셀 분석 / 이미지 업로드 원칙 | Tsubaki `CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS/TOOLS/SPRITES/` | 생산·변환·이미지 자산 쪽은 Tsubaki가 정규 소유. 스프라이트 작업 시 사람이 확인 가능한 이미지도 포함 |
| 디스어셈블리 / 완전 해체 | `WHITE/.../NATIVE/`, `DOMAINS/`, `TOOLS/`, `REPORTS/` | 현재는 재현 가능한 구조적 deconstruction까지. ARM9/overlay 함수·심볼 수준 완전 disassembly는 W5에서 명시한 후속 미완료 층 |
| 경로 재설계 / GitHub 업로드 원칙 | `README.md`, `STRUCTURE.md`, `.github/validate_structure.py` | 프로젝트는 현재 정규 경로 하나만 사용. 버전 변경 시 같은 트리를 직접 갱신하고 옛 경로·별도 이력 트리는 만들지 않음 |

## White deep-deconstruction quick path

`WHITE/RELEASES/NDS-TWL/CART/IRAO-HV0/REPORTS/WHITE-W5-COMPLETE-DECONSTRUCTION.md`

## Production repository

Sakurai는 조사·기준·검증 자료의 프로젝트 진입점이다. 실제 추출 비-ROM 바이너리, build/implementation, 변환 자산과 sprite 생산물은 `SakuraiTsubaki/Tsubaki`의 동일한 프로젝트 경로에 함께 정리한다:

`CROSS-GEN/PROJECTS/GEN5-TO-POCKET-MONSTERS/`

완전한 플레이 가능 ROM 이미지만 GitHub에서 제외한다. 그 외 프로젝트 산출물은 정규 프로젝트 경로에서 찾을 수 있어야 한다.
