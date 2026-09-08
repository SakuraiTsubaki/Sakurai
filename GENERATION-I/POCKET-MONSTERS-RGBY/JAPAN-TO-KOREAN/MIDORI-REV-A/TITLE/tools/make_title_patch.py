from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json

SRC = Path('/mnt/data/Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb')
OUTDIR = Path('/mnt/data/gs_korean_title_prototype_green_reva')
OUTDIR.mkdir(exist_ok=True)
ROM = bytearray(SRC.read_bytes())
OFF = 0x10400
W, H = 128, 48
TILES_X, TILES_Y = 16, 6
LENGTH = TILES_X * TILES_Y * 16
assert LENGTH == 0x600
original = bytes(ROM[OFF:OFF + LENGTH])


def unpack_2bpp(raw):
    image = Image.new('L', (W, H), 255)
    pixels = image.load()
    palette = [255, 170, 85, 0]
    for tile_index in range(TILES_X * TILES_Y):
        tile_x = tile_index % TILES_X
        tile_y = tile_index // TILES_X
        tile = raw[tile_index * 16:(tile_index + 1) * 16]
        for y in range(8):
            lo = tile[y * 2]
            hi = tile[y * 2 + 1]
            for x in range(8):
                bit = 7 - x
                value = ((lo >> bit) & 1) | (((hi >> bit) & 1) << 1)
                pixels[tile_x * 8 + x, tile_y * 8 + y] = palette[value]
    return image


def pack_2bpp(values):
    raw = bytearray()
    for tile_y in range(TILES_Y):
        for tile_x in range(TILES_X):
            for y in range(8):
                lo = 0
                hi = 0
                for x in range(8):
                    value = values[tile_y * 8 + y][tile_x * 8 + x]
                    bit = 7 - x
                    lo |= (value & 1) << bit
                    hi |= ((value >> 1) & 1) << bit
                raw += bytes([lo, hi])
    return bytes(raw)


original_image = unpack_2bpp(original)
original_image.resize((W * 4, H * 4), Image.Resampling.NEAREST).save(
    OUTDIR / 'original_title_logo_4x.png'
)

# Rasterized only. Font files are never exported with the artifact.
font_file = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
scale = 4
hires = Image.new('L', (W * scale, H * scale), 0)
draw = ImageDraw.Draw(hires)
font_main = ImageFont.truetype(font_file, 22 * scale, index=1)
font_sub = ImageFont.truetype(font_file, 14 * scale, index=1)
main_text = '포켓몬스터'
sub_text = '그린'


def center_text(text, font, y):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (W * scale - text_width) // 2 - bbox[0]
    draw.text((x, y * scale), text, font=font, fill=255)


center_text(main_text, font_main, 0)
bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
sub_width = bbox[2] - bbox[0]
sub_x = (W * scale - sub_width) // 2 - bbox[0]
sub_y = 27 * scale
draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=255)
line_y = 36 * scale
line_gap = 6 * scale
left_end = sub_x - line_gap
right_start = sub_x + sub_width + line_gap
draw.rectangle((10 * scale, line_y, max(10 * scale, left_end), line_y + scale), fill=255)
draw.rectangle((min(W * scale - 10 * scale, right_start), line_y, W * scale - 10 * scale, line_y + scale), fill=255)

lowres = hires.resize((W, H), Image.Resampling.LANCZOS)
values = [[0] * W for _ in range(H)]
pixels = lowres.load()
for y in range(H):
    for x in range(W):
        values[y][x] = 3 if pixels[x, y] >= 96 else 0

for y in range(1, H - 1):
    for x in range(1, W - 1):
        if values[y][x] == 3:
            neighbors = sum(
                values[yy][xx] == 3
                for yy in range(y - 1, y + 2)
                for xx in range(x - 1, x + 2)
            ) - 1
            if neighbors == 0:
                values[y][x] = 0

new_raw = pack_2bpp(values)
assert len(new_raw) == LENGTH
new_image = unpack_2bpp(new_raw)
new_image.resize((W * 4, H * 4), Image.Resampling.NEAREST).save(
    OUTDIR / 'korean_title_logo_4x.png'
)

patched = bytearray(ROM)
patched[OFF:OFF + LENGTH] = new_raw
(OUTDIR / '_local_verification_only_Pocket_Monsters_Midori_RevA_KR_Title.gb').write_bytes(patched)

ips = bytearray(b'PATCH')
ips += OFF.to_bytes(3, 'big') + LENGTH.to_bytes(2, 'big') + new_raw + b'EOF'
(OUTDIR / 'Pocket_Monsters_Midori_JP_RevA_Korean_Title_Prototype.ips').write_bytes(ips)
(OUTDIR / 'korean_title_logo.2bpp').write_bytes(new_raw)

manifest = {
    'project': 'GS Korean -> Pocket Monsters Korean localization/new translation',
    'target': 'Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced)',
    'change': 'Title-screen large logo prototype: 포켓몬스터 / 그린',
    'source_sha256': hashlib.sha256(SRC.read_bytes()).hexdigest(),
    'source_sha1': hashlib.sha1(SRC.read_bytes()).hexdigest(),
    'rom_size': len(ROM),
    'logo_offset_start': f'0x{OFF:05X}',
    'logo_offset_end_inclusive': f'0x{OFF + LENGTH - 1:05X}',
    'logo_length': LENGTH,
    'tile_format': 'Game Boy 2bpp, 16 x 6 tiles, row-major',
    'tile_count': TILES_X * TILES_Y,
    'original_block_sha256': hashlib.sha256(original).hexdigest(),
    'new_block_sha256': hashlib.sha256(new_raw).hexdigest(),
    'patched_working_copy_sha256': hashlib.sha256(patched).hexdigest(),
}
(OUTDIR / 'manifest.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
)
