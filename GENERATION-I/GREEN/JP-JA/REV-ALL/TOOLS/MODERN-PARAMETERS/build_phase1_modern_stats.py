#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT = Path('/mnt/data')
OUT = ROOT / 'green_modern_params_phase1' / 'implementation'
OUT.mkdir(parents=True, exist_ok=True)
ROMS = {
    'REV-0': ROOT / 'Pocket Monsters - Midori (Japan) (SGB Enhanced).gb',
    'REV-A': ROOT / 'Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb',
}
EXPECTED_SHA1 = {
    'REV-0': '82c0eef40a5e2423699d9fd8ba15dfaa8b51d196',
    'REV-A': '4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b',
}
CHANGES = [
    (15, 'Beedrill', 'attack', 2, 80, 90, 'Gen VI'),
    (18, 'Pidgeot', 'speed', 4, 91, 101, 'Gen VI'),
    (24, 'Arbok', 'attack', 2, 85, 95, 'Gen VII'),
    (25, 'Pikachu', 'defense', 3, 30, 40, 'Gen VI'),
    (26, 'Raichu', 'speed', 4, 100, 110, 'Gen VI'),
    (31, 'Nidoqueen', 'attack', 2, 82, 92, 'Gen VI'),
    (34, 'Nidoking', 'attack', 2, 92, 102, 'Gen VI'),
    (51, 'Dugtrio', 'attack', 2, 80, 100, 'Gen VII'),
    (62, 'Poliwrath', 'attack', 2, 85, 95, 'Gen VI'),
    (76, 'Golem', 'attack', 2, 110, 120, 'Gen VI'),
    (83, "Farfetch'd", 'attack', 2, 65, 90, 'Gen VII'),
    (85, 'Dodrio', 'speed', 4, 100, 110, 'Gen VII'),
    (101, 'Electrode', 'speed', 4, 140, 150, 'Gen VII'),
]

def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()
def gb_global_checksum(data): return (sum(data[:0x14E]) + sum(data[0x150:])) & 0xFFFF
def header_checksum(data):
    x=0
    for b in data[0x134:0x14D]: x=(x-b-1)&0xFF
    return x

def make_ips(source,target):
    out=bytearray(b'PATCH'); i=0
    while i<len(source):
        if source[i]==target[i]: i+=1; continue
        start=i; chunk=bytearray()
        while i<len(source) and source[i]!=target[i] and len(chunk)<0xFFFF:
            chunk.append(target[i]); i+=1
        out += start.to_bytes(3,'big') + len(chunk).to_bytes(2,'big') + chunk
    return bytes(out+b'EOF')

for rev,path in ROMS.items():
    src=path.read_bytes(); assert sha1(src)==EXPECTED_SHA1[rev]
    dst=bytearray(src)
    for dex,name,field,field_off,old,new,gen in CHANGES:
        rec=0x38000+(dex-1)*28; off=rec+field_off
        assert dst[rec]==dex and dst[off]==old
        dst[off]=new
    dst[0x14E:0x150]=gb_global_checksum(dst).to_bytes(2,'big')
    assert dst[0x14D]==header_checksum(dst)
    tag='rev0' if rev=='REV-0' else 'reva'
    (OUT/f'green_{tag}_modern_stats_phase1.gb').write_bytes(dst)
    (OUT/f'green_{tag}_modern_stats_phase1.ips').write_bytes(make_ips(src,dst))
