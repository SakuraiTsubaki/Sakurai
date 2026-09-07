# RUBY GitHub Auto-Upload Policy

이 프로젝트에서는 Pokémon Ruby 확장/분석 작업으로 생성되는 **배포 가능한 안전한 산출물**을 생성 시 GitHub에 함께 반영한다.

## Repository routing

- `SakuraiTsubaki/Sakurai`
  - 분석 보고서
  - 조사 결과
  - 검증 로그
  - 기계 판독용 분석 JSON
  - 매니페스트
  - 설계/연구 문서

- `SakuraiTsubaki/Tsubaki`
  - 빌더/도구 소스
  - 패치 생성 소스
  - 재현 가능한 작업 자산

## Canonical hierarchy

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

Ruby AXVE v0 기준 경로는 `GENERATION-III/RUBY/USA/REV-0/...` 이다.

## Never upload

- 원본 Pokémon ROM 바이너리 (`.gba` 등)
- 원본 ROM을 그대로 포함하거나 사실상 대체 배포하는 바이너리
- 저작권상 재배포하면 안 되는 원본 추출물

## Allowed outputs

- 분석/주소/구조 보고서
- JSON/CSV 메타데이터
- 검증 결과
- 소스 코드와 빌더
- 원본 데이터를 포함하지 않는 패치 및 재현 자료

## Current Ruby target

- National Species: 1025
- Pokémon varieties: 1351
- Pokémon Form records: 1579
- 향후 Generation 10 이상을 고려하여 ID/테이블 구조는 확장 가능하게 설계한다.
