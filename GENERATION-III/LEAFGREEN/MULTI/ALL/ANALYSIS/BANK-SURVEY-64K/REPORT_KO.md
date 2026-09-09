# Pokémon LeafGreen 7개 ROM — 64 KiB 뱅크 전수조사 1차 보고서

## 조사 기준

GBA ROM은 GB/GBC처럼 하드웨어 뱅크 스위칭을 사용하는 구조가 아니다. 이 보고서에서 **뱅크**는 비교와 추적을 위한 고정 분석 단위이며, 크기는 `0x10000` (65,536 bytes, 64 KiB)로 정의했다. 16 MiB ROM 한 개는 `00`–`FF`, 총 256개 분석 뱅크로 나뉜다.

대상은 업로드된 LeafGreen 7개 정식 ROM이다: 일본 Rev0, 영어 Rev0, 영어 Rev1, 독일/스페인/프랑스/이탈리아 Rev0. 원본 ROM은 읽기 전용으로 분석했으며 수정하지 않았다.

## 완료 범위

- 7 ROM × 256 banks = **1,792개 뱅크 레코드** 전수 해시/통계
- 각 뱅크 CRC32 / SHA-1
- Shannon entropy, FF/00 비율, ASCII 비율
- 순수/준수 fill 뱅크 판정
- aligned 32-bit ROM 포인터 후보의 뱅크별 inbound/outbound 집계
- 전체 포인터 후보의 source-bank → target-bank 그래프
- `0x10` GBA LZ77 헤더 후보 밀도
- 7판 동일 뱅크 판정
- 서양 Rev0 5개판 동일 뱅크 판정
- EN Rev0 ↔ EN Rev1 뱅크별 차이 바이트 수 및 전체 연속 차이 구간
- 서로 다른 위치에 존재하는 64 KiB 완전 동일 데이터 뱅크 탐색
- 4 KiB 이상 연속 FF/00 구간 탐색
- ROM 끝의 정확한 trailing-FF 영역 계산

## 핵심 결과

### 1. EN Rev0 ↔ Rev1 변경 범위

영어 Rev0과 Rev1은 **뱅크 `00`–`71`의 114개 뱅크에서만 차이**가 검출되었다. `72`–`FF`는 두 영어 리비전에서 뱅크 단위로 모두 동일하다.

단, `00`–`71` 내부에서는 삽입/재배치의 연쇄 영향 때문에 대부분의 뱅크가 광범위하게 달라진다. 단순히 각 다른 바이트를 독립 패치 포인트로 해석하면 안 된다.

### 2. 7개 ROM에서 같은 위치·같은 내용인 뱅크

**84 / 256개 뱅크**가 7개 ROM에서 SHA-1까지 완전히 동일하다.

주요 동일 범위는 `72`–`BF`, `EC`–`EF`, `FE`–`FF`이며, 다수는 순수 `FF` 여유 공간이다. 따라서 “동일 뱅크 수” 자체를 공통 게임 데이터 양으로 해석하면 안 된다.

### 3. 대형 연속 여유 공간

- EN Rev0: `0x719B18–0xCFFFFF` = **6,186,216 bytes** 연속 FF
- EN Rev1: `0x719B88–0xCFFFFF` = **6,186,104 bytes** 연속 FF
- DE Rev0: `0x717DAC–0xCFFFFF` = **6,193,748 bytes** 연속 FF
- ES Rev0: `0x7104DC–0xCFFFFF` = **6,224,676 bytes** 연속 FF
- FR Rev0: `0x70F2E0–0xCFFFFF` = **6,229,280 bytes** 연속 FF
- IT Rev0: `0x70D600–0xCFFFFF` = **6,236,672 bytes** 연속 FF
- JP Rev0: `0x6C7B7C–0xBFFFFF` = **5,473,412 bytes** 연속 FF

일본판은 그 뒤 `C0–D9`와 `F0–FD`에 다시 실데이터가 나타나므로, 중간 FF 블록을 ROM 끝의 자유 공간과 동일하게 취급하면 안 된다.

### 4. 정확한 ROM 끝 trailing FF

- JP Rev0: 마지막 non-FF `0xFDFFFE`; trailing FF **131,073 bytes (0.125 MiB)**
- EN Rev0 / Rev1: 마지막 non-FF `0xEB0E13`; trailing FF **1,372,652 bytes (1.309 MiB)**
- DE Rev0: 마지막 non-FF `0xEB2337`; trailing FF **1,367,240 bytes (1.304 MiB)**
- ES Rev0: 마지막 non-FF `0xEB2387`; trailing FF **1,367,160 bytes (1.304 MiB)**
- FR Rev0: 마지막 non-FF `0xEB2317`; trailing FF **1,367,272 bytes (1.304 MiB)**
- IT Rev0: 마지막 non-FF `0xEB244B`; trailing FF **1,366,964 bytes (1.304 MiB)**

### 5. 일본판 → 영어판 후반 블록 재배치

64 KiB 전체가 완전히 동일한 상태로 **정확히 `+0x100000` 이동**한 사례가 다수 확인되었다.

대표 매핑: JP `C2→D2`, `C3→D3`, `C4→D4`, `C5→D5`, `C6→D6`, `C7→D7`, `C9→D9`, `CA→DA`, `CB→DB`, `CC→DC`, `CD→DD`, `CE→DE`, `CF→DF`, `D0→E0`, `D1→E1`, `D2→E2`, `D3→E3`.

또 `C0→D0`은 약 92.27%, `C1→D1`은 약 98.77%, `C8→D8`은 약 99.98%가 동일해, 이 구간 역시 같은 계열 데이터가 재배치되면서 일부만 지역판별로 변한 것으로 보인다.

### 6. 일본판 `F0–FD`는 실제 참조 데이터

일본판 `F0–FD`에는 대량의 00/FF가 섞여 있지만 순수 패딩이 아니다. 정렬된 32-bit ROM 포인터 후보의 inbound 수가 지속적으로 존재한다. 예: JP `FC`에는 **101개**의 inbound ROM 포인터 후보가 검출되었다. 따라서 이 구간을 확장용 빈 공간으로 덮어쓰는 것은 금지해야 한다.

### 7. 포인터 집중 뱅크

EN Rev0에서 inbound ROM 포인터 후보가 특히 많은 뱅크는 `3E`(2625), `3A`(2383), `16`(2290), `23`(2250), `41`(1930) 등이다. JP Rev0에서는 `1F`(2278), `3A`(2196), `00`(2046), `36`(1886), `19`(1599) 등이 상위다.

이 수치는 **후보 포인터 통계**이며, 코드/데이터/그래픽의 실제 심볼 의미를 확정한 값은 아니다. 다음 패스에서 디스어셈블리 심볼 및 실제 데이터 구조와 결합해야 한다.

## 다음 의미 분석 패스

고정 64 KiB 통계 지도 위에 디스어셈블리의 심볼/섹션을 결합하여 각 뱅크를 `code`, `scripts`, `text`, `maps`, `Pokemon data`, `trainer data`, `graphics`, `audio`, `wireless/mystery gift`, `font`, `padding/free space` 등으로 세분화한다. 특히 `00–71`, JP `C0–D9`, Western `D0–EB`, JP `F0–FD`를 우선 해부한다.
