#!/usr/bin/env python3
"""Minimal Pokémon Emerald Gen III text decoder used by extraction tools.

It preserves unhandled control bytes as explicit <XX> tokens rather than dropping data.
"""
from __future__ import annotations

EOS = 0xFF

WESTERN = {
    0x00:' ',0x01:'À',0x02:'Á',0x03:'Â',0x04:'Ç',0x05:'È',0x06:'É',0x07:'Ê',0x08:'Ë',
    0x09:'Ì',0x0B:'Î',0x0C:'Ï',0x0D:'Ò',0x0E:'Ó',0x0F:'Ô',0x10:'Œ',0x11:'Ù',0x12:'Ú',
    0x13:'Û',0x14:'Ñ',0x15:'ß',0x16:'à',0x17:'á',0x19:'ç',0x1A:'è',0x1B:'é',0x1C:'ê',
    0x1D:'ë',0x1E:'ì',0x20:'î',0x21:'ï',0x22:'ò',0x23:'ó',0x24:'ô',0x25:'œ',0x26:'ù',
    0x27:'ú',0x28:'û',0x29:'ñ',0x2A:'º',0x2B:'ª',0x2C:'<SUPER_ER>',0x2D:'&',0x2E:'+',
    0x34:'<LV>',0x35:'=',0x36:';',0x51:'¿',0x52:'¡',0x5A:'Í',0x5B:'%',0x5C:'(',0x5D:')',
    0x68:'â',0x6F:'í',0x77:'<SPACER>',0x79:'↑',0x7A:'↓',0x7B:'←',0x7C:'→',0x84:'<SUPER_E>',
    0x85:'<',0x86:'>',0xA0:'<SUPER_RE>',0xA1:'0',0xA2:'1',0xA3:'2',0xA4:'3',0xA5:'4',
    0xA6:'5',0xA7:'6',0xA8:'7',0xA9:'8',0xAA:'9',0xAB:'!',0xAC:'?',0xAD:'.',0xAE:'-',
    0xAF:'·',0xB0:'…',0xB1:'“',0xB2:'”',0xB3:'‘',0xB4:'’',0xB5:'♂',0xB6:'♀',0xB7:'¥',
    0xB8:',',0xB9:'×',0xBA:'/',0xEF:'▶',0xF0:':',0xF1:'Ä',0xF2:'Ö',0xF3:'Ü',0xF4:'ä',
    0xF5:'ö',0xF6:'ü',0xFA:'\\l',0xFB:'\\p',0xFE:'\\n',
}
for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 0xBB): WESTERN[i] = ch
for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz', 0xD5): WESTERN[i] = ch

HIRAGANA = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっ'
KATAKANA = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ'
JAPANESE = {0x00:'　',0xAB:'！',0xAC:'？',0xAD:'。',0xAE:'ー',0xB0:'⋯',0xB5:'♂',0xB6:'♀',0xFA:'\\l',0xFB:'\\p',0xFE:'\\n'}
for i, ch in enumerate(HIRAGANA, 1): JAPANESE[i] = ch
for i, ch in enumerate(KATAKANA, 0x51): JAPANESE[i] = ch
for k, v in WESTERN.items():
    if k >= 0xA1 and k not in JAPANESE:
        JAPANESE[k] = v

MULTI = {
    (0x53, 0x54): '<PKMN>',
    (0x55, 0x56, 0x57, 0x58, 0x59): '<POKEBLOCK>',
}


def decode(raw: bytes, japanese: bool = False, variant: str | None = None) -> tuple[str, list[int]]:
    table = JAPANESE if japanese else WESTERN
    out: list[str] = []
    unknown: list[int] = []
    i = 0
    while i < len(raw):
        b = raw[i]
        if b == EOS:
            break
        if not japanese:
            matched = False
            multi = dict(MULTI)
            if variant == 'ITA':
                multi[(0x5E, 0x5F, 0x60, 0x61, 0x63)] = '<POKEMELLE>'
            for seq, token in sorted(multi.items(), key=lambda kv: -len(kv[0])):
                if raw[i:i+len(seq)] == bytes(seq):
                    out.append(token); i += len(seq); matched = True; break
            if matched:
                continue
        ch = table.get(b)
        if ch is None:
            out.append(f'<{b:02X}>')
            unknown.append(b)
        else:
            out.append(ch)
        i += 1
    return ''.join(out), unknown


def read_terminated(data: bytes, offset: int, max_len: int = 1024) -> bytes:
    if not 0 <= offset < len(data):
        raise ValueError(f'offset outside ROM: 0x{offset:X}')
    end = data.find(bytes([EOS]), offset, min(len(data), offset + max_len))
    if end < 0:
        raise ValueError(f'no EOS within {max_len} bytes at 0x{offset:X}')
    return data[offset:end + 1]
