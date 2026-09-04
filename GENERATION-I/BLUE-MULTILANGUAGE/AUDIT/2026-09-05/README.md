# Pokémon Blue ROM baseline audit

ROM 원본은 저장소에 포함하지 않는다. 이 문서는 프로젝트에 마운트된 ROM에서 산출한 메타데이터/구조 기초 원장이다.

## Inventory

| ROM | Size | Banks | Mapper | Dest | Ver | SHA-1 | Header | Global |
|---|---:|---:|---|---:|---:|---|---|---|
| Pocket Monsters - Ao (Japan) (SGB Enhanced).gb | 512 KiB | 32 | MBC1+RAM+BATTERY | 0 | 0 | `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` | OK | OK |
| Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | 1 | 0 | `20e72dc6f41493eee1fdd0cef54214e6c3389688` | OK | OK |
| Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb | 1024 KiB | 64 | MBC3+RAM+BATTERY | 1 | 0 | `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` | OK | OK |
| Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | 1 | 0 | `7715e7b133e8634df48918b9138374110212a108` | OK | OK |
| Pokemon - Version Bleue (France) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | 1 | 0 | `47faa910d0e073c600665bf9c83b6bd17babdf8a` | OK | OK |
| Pokemon - Versione Blu (Italy) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | 1 | 0 | `f69ed1a1332f04c24c7db899a09019bb045fa8b3` | OK | OK |

## Immediate structural findings

- 일본판 Pocket Monsters Ao는 512 KiB / 32 banks / MBC1+RAM+BATTERY이다.
- 서구권 5개판은 1 MiB / 64 banks이다.
- 영문판은 MBC3+RAM+BATTERY, 독/불/이/서판은 MBC5+RAM+BATTERY로 헤더 매퍼가 다르다.
- 6개 ROM 모두 Nintendo logo, header checksum, global checksum 검증을 통과했다.
- 서구 5개판의 bank 45–63 (19 banks = 304 KiB)는 모두 완전한 `0x00` 빈 뱅크이며 서로 동일하다.
- 서구 5개판의 bank 27은 빈 뱅크가 아니라 실제 데이터가 있는 상태로 5개판 전체가 정확히 동일하다.
- 따라서 JP ↔ western은 단순 번역 차이로 취급할 수 없고, western 내부에서도 EN ↔ DE/FR/IT/ES의 뱅킹/매퍼 차이를 별도 추적해야 한다.

## Pairwise byte similarity

비교 길이는 두 ROM 중 더 짧은 쪽까지이며, 체크섬/헤더 차이도 포함한다.

| A | B | Compared | Different bytes | Same % | Exact 16KiB banks |
|---|---|---:|---:|---:|---:|
| Pocket Monsters - Ao (Japan) (SGB Enhanced).gb | Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb | 524288 | 308811 | 41.099% | 1 |
| Pocket Monsters - Ao (Japan) (SGB Enhanced).gb | Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb | 524288 | 295428 | 43.652% | 1 |
| Pocket Monsters - Ao (Japan) (SGB Enhanced).gb | Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb | 524288 | 295595 | 43.620% | 1 |
| Pocket Monsters - Ao (Japan) (SGB Enhanced).gb | Pokemon - Version Bleue (France) (SGB Enhanced).gb | 524288 | 308897 | 41.083% | 1 |
| Pocket Monsters - Ao (Japan) (SGB Enhanced).gb | Pokemon - Versione Blu (Italy) (SGB Enhanced).gb | 524288 | 308036 | 41.247% | 1 |
| Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb | Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb | 1048576 | 283051 | 73.006% | 20 |
| Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb | Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb | 1048576 | 280172 | 73.281% | 20 |
| Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb | Pokemon - Version Bleue (France) (SGB Enhanced).gb | 1048576 | 275774 | 73.700% | 20 |
| Pokemon - Blaue Edition (Germany) (SGB Enhanced).gb | Pokemon - Versione Blu (Italy) (SGB Enhanced).gb | 1048576 | 280512 | 73.248% | 20 |
| Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb | Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb | 1048576 | 265135 | 74.715% | 20 |
| Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb | Pokemon - Version Bleue (France) (SGB Enhanced).gb | 1048576 | 280224 | 73.276% | 20 |
| Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb | Pokemon - Versione Blu (Italy) (SGB Enhanced).gb | 1048576 | 270592 | 74.194% | 20 |
| Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb | Pokemon - Version Bleue (France) (SGB Enhanced).gb | 1048576 | 274027 | 73.867% | 20 |
| Pokemon - Edicion Azul (Spain) (SGB Enhanced).gb | Pokemon - Versione Blu (Italy) (SGB Enhanced).gb | 1048576 | 264060 | 74.817% | 20 |
| Pokemon - Version Bleue (France) (SGB Enhanced).gb | Pokemon - Versione Blu (Italy) (SGB Enhanced).gb | 1048576 | 270164 | 74.235% | 20 |

## Generated ledgers

- `blue_rom_inventory.csv`: ROM-level header/hash inventory.
- `pairwise_similarity.csv`: ROM-pair byte similarity and exact-bank matches.
- `banks/JP_AO.csv`: JP Blue 32-bank census.
- `banks/EN_BLUE.csv`, `banks/DE_BLUE.csv`, `banks/FR_BLUE.csv`, `banks/IT_BLUE.csv`, `banks/ES_BLUE.csv`: western 64-bank censuses.
- `shared_western_bank_groups.json`: exact 16 KiB bank groups shared across western versions.
- `audit_blue_roms.py`: reproducible audit generator; ROM bytes are never embedded.

Each bank census records SHA-1, entropy, zero/FF byte counts, blank-bank flags and unique-byte-value counts.

## Next census layers

1. Banks 0–44의 code/data/text/graphics/audio 역할 분류 및 free-space 후보 확정.
2. Pointer tables / text engines / character tables / fonts / SGB data identification.
3. JP Blue ↔ EN Blue ↔ DE/FR/IT/ES localization correspondence map.
4. Maps, scripts, encounters, trainers, items, graphics, audio, Pokédex, menus/UI table census.
5. Provenance ledger and patch-safe address map.

## Repository rule

- ROM binaries: **never commit**.
- Analysis reports, ledgers, scripts, tools, patches, and other non-ROM outputs: commit to `Sakurai` as work progresses.
