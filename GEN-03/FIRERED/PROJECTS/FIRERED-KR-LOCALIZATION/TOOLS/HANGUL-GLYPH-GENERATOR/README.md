# Hangul Glyph Generator — 8×8 / 16×16

현대 한글 완성형 `U+AC00..U+D7A3` 11,172자를 8×8/16×16 비트맵으로 자동 생성하는 베이스라인 도구입니다.

## 출력

각 크기마다 다음을 생성합니다.

- `atlas_8x8.png`, `atlas_16x16.png` — 전체 글리프 아틀라스
- `glyphs_*_1bpp.bin` — 행 우선 1bpp packed bitmap
- `glyphs_*_gb2bpp.bin` — Game Boy/GBC 호환 8×8 tile 단위 2bpp planar data
  - 8×8 글리프 = 1 tile = 16 bytes
  - 16×16 글리프 = 4 tiles(TL, TR, BL, BR) = 64 bytes
- `mapping_*.json/.csv` — Unicode, 내부 ID, 초/중/종성 분해, ROM 데이터 offset
- `charset.txt` — 생성 순서의 문자 목록
- `build_summary.json` — 빌드 조건

## 전체 11,172자 생성

```bash
python hangul_glyph_gen.py -o out/full
```

폰트 파일은 프로젝트에 포함하지 않습니다. 시스템에서 한국어 폰트를 자동 탐지하며, 원하는 폰트가 있으면 직접 지정합니다.

```bash
python hangul_glyph_gen.py --font /path/to/font.ttf -o out/full
```

## 번역문 subset 생성

```bash
python hangul_glyph_gen.py \
  --subset translated_text.txt \
  --include-non-hangul \
  --extras "♂♀…·→←↑↓" \
  -o out/subset
```

동일 문자가 여러 번 나와도 한 번만 수록하며 텍스트에서 처음 등장한 순서를 보존합니다.

## 수동 보정 override

자동 래스터 결과 중 8×8에서 판독성이 나쁜 글자만 픽셀 단위로 교체할 수 있습니다. 이 구조를 쓰면 **자동 생성 → 판독성 테스트 → 문제 글자만 override** 방식으로 11,172자를 관리할 수 있습니다.

## Unicode 한글 분해

```text
S = codepoint - 0xAC00
L = S // 588
V = (S % 588) // 28
T = S % 28
```

현재 버전은 현대 벡터 한글 폰트를 픽셀 셀에 맞춰 자동 래스터하는 베이스라인 생성기입니다. 실제 게임용 8×8에서는 특정 복합 모음/겹받침의 pixel override가 필요할 수 있습니다. 폰트 파일 자체는 배포하지 않습니다.
