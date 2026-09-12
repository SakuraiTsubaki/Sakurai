# GS Korean 한글 글리프 전체 추출 검증

한국 정식판 `Pocket Monsters Geum (Korea).gbc` 및 `Pocket Monsters Eun (Korea).gbc`의 한글 폰트 영역을 전수 추출했다.

## 확정 구조

- 폰트 뱅크: `0x78`–`0x7A`
- 1bpp 테이블: 11개
- 테이블당 크기: `0x1000` bytes
- 테이블당 슬롯: 256
- 글리프 셀: 8×16
- 글리프당 데이터: 16 bytes
- 전체 결합 데이터: 45,056 bytes
- 전체 결합 SHA-256: `4a9151fb06807d0727fb40dd5779479f9cc9546610c2a4cd162ed185562d3d60`
- 금/은 대응 폰트 영역: byte-identical

## 저장 위치

실제 재사용 가능한 폰트 자산은 Tsubaki의 다음 경로에 저장한다.

`GENERATION-II/POCKET-MONSTERS-GOLD-SILVER/KOREA/REV-COMMON/FONT/`

`hangul_font_11tables.1bpp.gz`를 압축 해제하면 11개 테이블을 순서대로 결합한 45,056-byte 원본 1bpp 글리프 데이터가 나온다. 각 테이블은 `0x1000` byte 단위로 분할한다.

이 폰트는 GS Korean의 한국어 구현 기술 자료이며, 타 작품 번역문의 직접 원문으로 취급하지 않는다. ROM 전체 바이너리는 저장하지 않는다.
