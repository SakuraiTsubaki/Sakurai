#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib

MOVE_TABLE = 0x39658
EXPECTED_SHA1 = {
    'rev0': '82c0eef40a5e2423699d9fd8ba15dfaa8b51d196',
    'reva': '4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b',
}
EFFECT_CHANGES = [
    (44, 0x1F, 0x25), (59, 0x23, 0x05), (67, 0x25, 0x00),
    (81, 0x14, 0x3C), (87, 0x06, 0x24), (126, 0x22, 0x04),
    (157, 0x00, 0x25),
]
CHANCE_PATCH = {
    'rev0': (0x3F8C8, 0x55, 0x1A),
    'reva': (0x3F8CD, 0x55, 0x1A),
}
PRIORITY = {
    'rev0': dict(start=0x3C31C, cpu=0x431C, enemy=0x4374, player=0x43B4, stringcmp=0x3AD8, random=0x718D),
    'reva': dict(start=0x3C31E, cpu=0x431E, enemy=0x4376, player=0x43B6, stringcmp=0x3AC6, random=0x7192),
}

def jr(op, pc, target):
    d = target - (pc + 2)
    if not -128 <= d <= 127:
        raise ValueError((hex(pc), hex(target), d))
    return bytes((op, d & 0xFF))


def priority_block(s):
    start=s['cpu']; helper=start+21; table=helper+19; compare=start+52
    out=bytearray(); pc=start
    def emit(x):
        nonlocal pc
        out.extend(x); pc += len(x)
    emit(bytes((0xFA,0xDC,0xCC))); emit(bytes((0xCD,helper&255,helper>>8))); emit(b'\x47')
    emit(bytes((0xFA,0xDD,0xCC))); emit(bytes((0xCD,helper&255,helper>>8))); emit(b'\xB8')
    emit(jr(0x28,pc,compare)); emit(bytes((0xDA,s['player']&255,s['player']>>8))); emit(jr(0x18,pc,s['enemy']))
    emit(bytes((0x21,table&255,table>>8,0x06,0x06))); loop=pc
    emit(b'\xBE'); zpos=pc; emit(b'\x28\x00'); emit(bytes((0x23,0x23,0x05))); emit(jr(0x20,pc,loop))
    emit(bytes((0x3E,0x02,0xC9))); found=pc; out[zpos-start+1]=(found-(zpos+2))&255; emit(bytes((0x23,0x7E,0xC9)))
    emit(bytes((0x12,0,0x2E,0,0x44,1,0x62,3,0x64,0,0x75,3)))
    emit(bytes((0x11,0x10,0xD0,0x21,0xE1,0xCF,0x0E,2,0xCD,s['stringcmp']&255,s['stringcmp']>>8)))
    tie=compare+17; emit(jr(0x28,pc,tie)); emit(jr(0x30,pc,s['player'])); emit(jr(0x18,pc,s['enemy']))
    emit(bytes((0xCD,s['random']&255,s['random']>>8,0x47,0xF0,0xAA,0xFE,2,0x78,0x20,1,0x2F,0xFE,0x80)))
    emit(jr(0x38,pc,s['player'])); emit(jr(0x18,pc,s['enemy'])); emit(b'\x00')
    assert len(out) == 88 and pc == s['enemy']
    return bytes(out)


def checksum(buf):
    value=(sum(buf[:0x14E])+sum(buf[0x150:]))&0xFFFF
    buf[0x14E]=value>>8; buf[0x14F]=value&255


def ips(old,new):
    p=bytearray(b'PATCH'); i=0
    while i < len(old):
        if old[i] == new[i]: i += 1; continue
        start=i
        while i < len(old) and old[i] != new[i] and i-start < 0xFFFF: i += 1
        data=new[start:i]
        p += start.to_bytes(3,'big') + len(data).to_bytes(2,'big') + data
    return bytes(p+b'EOF')


def build(rev, source, numeric_csv, output_rom, output_ips):
    original=Path(source).read_bytes()
    assert hashlib.sha1(original).hexdigest() == EXPECTED_SHA1[rev]
    rom=bytearray(original)
    with open(numeric_csv,newline='') as f:
        for row in csv.DictReader(f):
            off=int(row['rom_offset'],16); old=int(row['old_raw']); new=int(row['new_raw'])
            assert rom[off] == old
            rom[off] = new
    for move,old,new in EFFECT_CHANGES:
        off=MOVE_TABLE+(move-1)*6+1
        assert rom[off] == old
        rom[off] = new
    off,old,new=CHANCE_PATCH[rev]; assert rom[off] == old; rom[off] = new
    spec=PRIORITY[rev]; rom[spec['start']:spec['start']+88] = priority_block(spec)
    checksum(rom)
    Path(output_rom).write_bytes(rom)
    Path(output_ips).write_bytes(ips(original,bytes(rom)))

if __name__ == '__main__':
    raise SystemExit('Import build() and provide exact Rev 0/Rev A source paths; originals are never modified in place.')
