from pathlib import Path
import json
import hashlib
from hangul_glyph_gen import decompose_hangul, HANGUL_START, HANGUL_END

ROOT = Path(__file__).parent / 'out' / 'full_modern'

assert HANGUL_END - HANGUL_START + 1 == 11172
assert decompose_hangul('가') == (0, 0, 0)
assert decompose_hangul('각') == (0, 0, 1)
assert decompose_hangul('힣') == (18, 20, 27)

summary = json.loads((ROOT / 'build_summary.json').read_text(encoding='utf-8'))
assert summary['glyph_count'] == 11172

expected_sizes = {
    'glyphs_8x8_1bpp.bin': 11172 * 8,
    'glyphs_8x8_gb2bpp.bin': 11172 * 16,
    'glyphs_16x16_1bpp.bin': 11172 * 32,
    'glyphs_16x16_gb2bpp.bin': 11172 * 64,
}
for name, size in expected_sizes.items():
    actual = (ROOT / name).stat().st_size
    assert actual == size, (name, actual, size)

m8 = json.loads((ROOT / 'mapping_8x8.json').read_text(encoding='utf-8'))
assert m8[0]['char'] == '가' and m8[0]['1bpp_offset'] == 0 and m8[0]['gb_2bpp_offset'] == 0
assert m8[-1]['char'] == '힣'
assert m8[-1]['1bpp_offset'] == (11172 - 1) * 8
assert m8[-1]['gb_2bpp_offset'] == (11172 - 1) * 16

print('ALL TESTS PASSED')
print('glyphs:', summary['glyph_count'])
for name in expected_sizes:
    b=(ROOT/name).read_bytes()
    print(name, len(b), hashlib.sha256(b).hexdigest())
