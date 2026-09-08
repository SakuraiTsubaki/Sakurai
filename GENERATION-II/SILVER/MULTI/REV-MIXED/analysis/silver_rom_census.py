from pathlib import Path
from collections import Counter
import hashlib

BANK = 0x4000
ROM_DIR = Path('/mnt/data')
FILES = [
    'Pocket Monsters Gin (Japan).gbc',
    'Pocket Monsters Gin (Japan) (Rev A).gbc',
    'Pokemon - Silver Version (USA, Europe).gbc',
    'Pokemon - Silberne Edition (Germany).gbc',
    'Pokemon - Version Argent (France).gbc',
    'Pokemon - Versione Argento (Italy).gbc',
    'Pokemon - Edicion Plata (Spain).gbc',
    'Pocket Monsters Eun (Korea).gbc',
]

def header_checksum(data):
    x = 0
    for i in range(0x134, 0x14D):
        x = (x - data[i] - 1) & 0xff
    return x == data[0x14D]

def global_checksum(data):
    calc = (sum(data) - data[0x14E] - data[0x14F]) & 0xffff
    stored = (data[0x14E] << 8) | data[0x14F]
    return calc == stored

def full_zero_banks(data):
    return [i for i in range(len(data)//BANK) if data[i*BANK:(i+1)*BANK] == bytes(BANK)]

for name in FILES:
    p = ROM_DIR / name
    b = p.read_bytes()
    title = b[0x134:0x143].rstrip(b'\0').decode('latin1')
    zero = full_zero_banks(b)
    print(name)
    print(' size=', len(b), 'banks=', len(b)//BANK, 'title=', title)
    print(' cgb=0x%02X cart=0x%02X romsize=0x%02X ramsize=0x%02X dest=%d rev=%d' %
          (b[0x143], b[0x147], b[0x148], b[0x149], b[0x14A], b[0x14C]))
    print(' header_checksum=', header_checksum(b), 'global_checksum=', global_checksum(b))
    print(' sha256=', hashlib.sha256(b).hexdigest())
    print(' full_zero_banks=', ' '.join(f'{x:02X}' for x in zero), f'({len(zero)} banks / {len(zero)*BANK} bytes)')
    print()

r0 = (ROM_DIR / FILES[0]).read_bytes()
ra = (ROM_DIR / FILES[1]).read_bytes()
diffs = [i for i,(a,b) in enumerate(zip(r0,ra)) if a != b]
bybank = Counter(i//BANK for i in diffs)
print('JP Rev0 vs RevA')
print(' differing_bytes=', len(diffs))
print(' first=0x%X last=0x%X' % (diffs[0], diffs[-1]))
print(' by_bank=', ' '.join(f'{k:02X}:{v}' for k,v in sorted(bybank.items())))
