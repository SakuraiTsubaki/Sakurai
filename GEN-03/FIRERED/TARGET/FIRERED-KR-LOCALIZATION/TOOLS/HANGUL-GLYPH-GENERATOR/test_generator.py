from pathlib import Path
import json
import hashlib

from hangul_glyph_gen import (
    HANGUL_END,
    HANGUL_START,
    decode_nds_glyph_2bpp,
    decompose_hangul,
    nds_glyph_to_mask,
    pack_nds_glyph_2bpp_from_mask,
)

ROOT = Path(__file__).parent / "out" / "full_modern"

assert HANGUL_END - HANGUL_START + 1 == 11172
assert decompose_hangul("가") == (0, 0, 0)
assert decompose_hangul("각") == (0, 0, 1)
assert decompose_hangul("힣") == (18, 20, 27)

# NDS tile ordering regression: a foreground-only 16x16 mask must survive the
# semantic 2bpp pack/decode path without transposition or half-row reversal.
from PIL import Image
probe = Image.new("L", (16, 16), 0)
px = probe.load()
for x, y in ((0, 0), (7, 1), (8, 2), (15, 3), (3, 8), (12, 15)):
    px[x, y] = 255
packed = pack_nds_glyph_2bpp_from_mask(probe)
decoded = nds_glyph_to_mask(packed)
assert list(probe.getdata()) == list(decoded.getdata())
assert len(packed) == 64
assert len(decode_nds_glyph_2bpp(packed)) == 16

summary = json.loads((ROOT / "build_summary.json").read_text(encoding="utf-8"))
assert summary["glyph_count"] == 11172

expected_sizes = {
    "glyphs_8x8_1bpp.bin": 11172 * 8,
    "glyphs_8x8_gb2bpp.bin": 11172 * 16,
    "glyphs_16x16_1bpp.bin": 11172 * 32,
    "glyphs_16x16_gb2bpp.bin": 11172 * 64,
}
for name, size in expected_sizes.items():
    actual = (ROOT / name).stat().st_size
    assert actual == size, (name, actual, size)

m8 = json.loads((ROOT / "mapping_8x8.json").read_text(encoding="utf-8"))
assert m8[0]["char"] == "가" and m8[0]["1bpp_offset"] == 0 and m8[0]["gb_2bpp_offset"] == 0
assert m8[-1]["char"] == "힣"
assert m8[-1]["1bpp_offset"] == (11172 - 1) * 8
assert m8[-1]["gb_2bpp_offset"] == (11172 - 1) * 16

print("ALL TESTS PASSED")
print("glyphs:", summary["glyph_count"])
for name in expected_sizes:
    b = (ROOT / name).read_bytes()
    print(name, len(b), hashlib.sha256(b).hexdigest())
