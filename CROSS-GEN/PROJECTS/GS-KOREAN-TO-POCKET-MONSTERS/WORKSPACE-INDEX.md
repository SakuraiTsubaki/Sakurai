# GS Korean -> Pocket Monsters — Workspace Index

Canonical project root:

`CROSS-GEN/PROJECTS/GS-KOREAN-TO-POCKET-MONSTERS/`

**이 프로젝트의 현재 작업물은 이 루트 한 곳에서만 찾는다.** 같은 작업물을 버전별·마이그레이션별 경로에 복제하지 않는다.

## Research / analysis

- `RESEARCH/GS-KOREAN-MODERNIZATION/` — ROM-derived text tables, Hangul charmap data, mappings, tools, reports, manifests, verification material
- `RESEARCH/GS-KOREAN-MODERNIZATION/WORKPACKAGES/` — GS Korean phase work packages consolidated from prior layouts

## Project control

- `MANIFESTS/`
- `VERIFICATION/`
- `PROJECT.json`
- `ROUTING.md`

## Version-up rule

새 구조 버전으로 이동할 때는 **유일한 작업물을 새 canonical 경로에 병합하고 검증한 뒤 구경로를 삭제한다.** 별도의 PRE-V, quarantine, migration snapshot 또는 redirect 복제본은 만들지 않는다. 과거 상태가 필요하면 Git history를 사용한다.

Complete playable ROM image files are not stored here.
