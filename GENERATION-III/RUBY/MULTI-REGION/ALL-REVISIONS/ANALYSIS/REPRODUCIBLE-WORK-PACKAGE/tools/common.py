from __future__ import annotations
from pathlib import Path
import hashlib, math, struct

LANG = {'J':('JAPANESE','JAPAN'),'E':('ENGLISH','USA-EUROPE'),'D':('GERMAN','GERMANY'),'F':('FRENCH','FRANCE'),'I':('ITALIAN','ITALY'),'S':('SPANISH','SPAIN')}

def hashes(data: bytes):
    return {
        'md5': hashlib.md5(data).hexdigest(),
        'sha1': hashlib.sha1(data).hexdigest(),
        'sha256': hashlib.sha256(data).hexdigest(),
    }

def gba_header(data: bytes):
    if len(data) < 0xC0: raise ValueError('ROM too small')
    title=data[0xA0:0xAC].rstrip(b'\0').decode('ascii','replace')
    code=data[0xAC:0xB0].decode('ascii','replace')
    maker=data[0xB0:0xB2].decode('ascii','replace')
    version=data[0xBC]
    complement=data[0xBD]
    calc=(-sum(data[0xA0:0xBD])-0x19)&0xFF
    entry_word=struct.unpack_from('<I', data, 0)[0]
    entry_target=None
    if (entry_word >> 24) & 0xFF == 0xEA:
        imm24=entry_word & 0xFFFFFF
        if imm24 & 0x800000: imm24 -= 1<<24
        entry_target=(8 + (imm24<<2)) & 0xFFFFFFFF
    suffix=code[-1:] if code else ''
    lang,region=LANG.get(suffix,('UNKNOWN','UNKNOWN'))
    return {
        'title': title, 'game_code': code, 'maker_code': maker,
        'software_version': version, 'header_complement': complement,
        'header_complement_calculated': calc,
        'header_checksum_ok': complement==calc,
        'fixed_value': data[0xB2], 'unit_code': data[0xB3], 'device_type': data[0xB4],
        'entry_word_le': f'{entry_word:08X}', 'entry_target_rom_offset': entry_target,
        'language': lang, 'region': region,
    }

def shannon_entropy(block: bytes):
    if not block: return 0.0
    counts=[0]*256
    for x in block: counts[x]+=1
    n=len(block)
    return -sum((c/n)*math.log2(c/n) for c in counts if c)

def trailing_run(data: bytes, value: int):
    i=len(data)
    while i and data[i-1]==value: i-=1
    return len(data)-i

def pointer_count(block: bytes, rom_size: int):
    lo=0x08000000; hi=lo+rom_size
    c=0
    for i in range(0,len(block)-3,4):
        v=struct.unpack_from('<I',block,i)[0]
        if lo <= v < hi: c+=1
    return c

def parse_lz77(data: bytes, off: int):
    # GBA BIOS LZ77 type 0x10. Return (decompressed_size, compressed_span) or None.
    if off+4>len(data) or data[off]!=0x10: return None
    out_len=data[off+1] | (data[off+2]<<8) | (data[off+3]<<16)
    if not (1 <= out_len <= 0x2000000): return None
    p=off+4; out=0
    try:
        while out < out_len:
            flags=data[p]; p+=1
            for bit in range(7,-1,-1):
                if out >= out_len: break
                if flags & (1<<bit):
                    if p+2>len(data): return None
                    a,b=data[p],data[p+1]; p+=2
                    disp=((a & 0x0F)<<8)|b
                    length=(a>>4)+3
                    if disp+1 > out: return None
                    out += length
                else:
                    if p>=len(data): return None
                    p+=1; out+=1
                if p>len(data): return None
        return out_len, p-off
    except IndexError:
        return None
