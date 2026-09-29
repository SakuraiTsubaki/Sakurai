# Hangul Glyph Generator — Generation IV source-first 8×8 / 16×16

현대 한글 완성형 `U+AC00..U+D7A3` 11,172자를 대상으로 하는 한글 글리프 빌드 도구입니다.

현재 원칙은 **공식 원본 우선, 프로젝트 생성 보충**입니다.

- Generation IV 한국어판에서 확인된 16×16 글리프는 원본 2bpp 픽셀을 그대로 사용합니다.
- 공식 Gen IV에 없는 현대 한글 음절만 벡터 폰트에서 프로젝트 파생 글리프로 생성합니다.
- 8×8은 Gen IV에 대응 원본이 없으므로 프로젝트 파생입니다.
- ROM 자체는 입력으로만 사용하고 저장소에 넣지 않습니다.

## Generation IV source pack

`extract-gen4-korean-font.py`가 한국판 Gen IV retail ROM에서 재현 가능한 source pack을 만듭니다.

확인된 HGSS 한국판 기준:

- archive: `a/0/1/6`
- principal members: `0, 1, 2, 4, 10`
- source glyph: 16×16, 2bpp, 64 bytes/glyph
- 확정 매핑: Wansung 2350 + compatibility jamo 51 = 2401 glyphs
- 미확정 slot `3427/3428`은 source pack에서 의도적으로 제외합니다.

16×16 현대 한글 전체 빌드에서는 Wansung 2350자가 `gen4_official`, 나머지 8822자가 `project_derived_vector`입니다.

## Gen IV 원본 우선 빌드

예: HGSS MESSAGE / FontID 1 / member 1을 16×16 기준 소스로 사용합니다.

```bash
python hangul_glyph_gen.py \
  --sizes 16 \
  --gen4-source-dir /path/to/gen4_font_pack \
  --gen4-member 1 \
  -o out/full_gen4_message
```

지원 member:

- `0` — SYSTEM / 11px Korean fixed advance
- `1` — MESSAGE / 12px
- `2` — SUBSCREEN / 13px
- `4` — HGSS application/UI / 12px
- `10` — HGSS Pokéwalker compact UI / 11px

member 10을 Emerald `FONT_NARROW`의 소스로 쓰는 것은 **프로젝트 매핑**이며, 원본 HGSS의 전역 narrow-font 역할을 뜻하지 않습니다.

## 출력과 보존 수준

각 크기마다:

- `atlas_8x8.png`, `atlas_16x16.png`
- `glyphs_*_1bpp.bin`
- `glyphs_*_gb2bpp.bin`
- `mapping_*.json/.csv`
- `charset.txt`
- `build_summary.json`

16×16 빌드에는 추가로:

- `glyphs_16x16_semantic2bpp.bin`

이 파일의 `gen4_official` 항목은 Generation IV source pack의 64-byte 2bpp 글리프와 **byte-for-byte 동일**합니다. 값의 의미는 Gen IV renderer 기준으로 `0=zero/transparent, 1=foreground, 2=shadow, 3=background`입니다.

반면 다음 출력은 변환 산출물입니다.

- `1bpp`: Gen IV foreground+shadow를 ink로 합치는 lossy projection
- `gb2bpp`: Game Boy/GBC tile format으로 변환한 파생본
- 벡터 생성 글리프의 semantic 2bpp: 프로젝트 생성 픽셀을 foreground index 1로 패킹한 파생본

따라서 **원본 보존 검증에는 `semantic2bpp`와 source pack을 비교**해야 합니다.

## source provenance

각 `mapping_16x16.*` 레코드에 다음 필드가 기록됩니다.

- `source_kind=gen4_official`
- `source_member`
- `source_slot`
- `source_class`

공식 원본이 없는 경우:

- `source_kind=project_derived_vector`

수동 override가 적용된 경우:

- `source_kind=project_override`

공식 데이터와 프로젝트 파생 데이터를 같은 것으로 취급하지 않습니다.

## 벡터 보충 빌드

Gen IV source pack을 지정하지 않으면 기존과 동일하게 전체 현대 한글을 벡터 래스터로 생성합니다.

```bash
python hangul_glyph_gen.py -o out/full
```

폰트 파일은 프로젝트에 포함하지 않습니다.

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

동일 문자는 한 번만 수록하고 최초 등장 순서를 보존합니다.

## 수동 보정 override

자동 생성된 프로젝트 파생 글리프는 픽셀 override가 가능합니다. 공식 Gen IV 글리프에 override를 적용하면 그 결과는 더 이상 원본이 아니므로 `source_kind=project_override`로 재분류됩니다.

## Unicode 한글 분해

```text
S = codepoint - 0xAC00
L = S // 588
V = (S % 588) // 28
T = S % 28
```

이 파이프라인은 원본 Gen IV 픽셀을 우선 보존하면서 최신 한국어 텍스트에 필요한 현대 한글 전체 범위를 별도 프로젝트 파생 글리프로 확장하기 위한 기반입니다.
