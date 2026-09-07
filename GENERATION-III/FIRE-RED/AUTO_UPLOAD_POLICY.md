# FIRE RED GitHub Auto-Upload Policy

이 프로젝트에서는 Pokémon FireRed 확장/분석 작업으로 생성되는 **배포 가능한 안전한 산출물**을 생성 시 GitHub에 함께 반영한다.

## Repository routing

- `SakuraiTsubaki/Sakurai`
  - 분석 보고서
  - 조사 결과
  - 검증 로그
  - 기계 판독용 분석 JSON
  - 설계 문서
  - 공통 엔진 분석은 `GENERATION-III/FIRE-RED/analysis/...`
  - 특정 언어/리비전 전용 분석은 `GENERATION-III/FIRE-RED/<LANG>/REV-<N>/analysis/...`

- `SakuraiTsubaki/Tsubaki`
  - 빌더/도구 소스
  - 매니페스트
  - 패치 생성 소스
  - 재현 가능한 작업 자산
  - 그래픽/팔레트/아이콘/기타 재사용 자산

## Never upload

- 원본 Pokémon ROM 바이너리 (`.gba` 등)
- 작업용 전체 ROM 복사본
- `.sav` 등 원본/플레이 세이브 바이너리
- 원본 ROM을 그대로 포함하거나 사실상 대체 배포하는 바이너리
- 저작권상 재배포하면 안 되는 원본 추출물

## Current FireRed target

- National Species: 1025 current, base-species ID space reserved through 4095
- Pokémon varieties reference set: 1351
- Pokémon Form records reference set: 1579
- Base Species rule: `SPECIES_* ID == National Dex number` for the reserved base range
- Gameplay varieties start at `0x1000`
- `SPECIES_EGG = 0xFFFE`, `SPECIES_INVALID = 0xFFFF`

## Upload discipline

Before every write, inspect the target repository and the relevant game directory. Common analysis and version-specific analysis must not be mixed. Manifests/build assets must not be committed to Sakurai when they belong in Tsubaki.
