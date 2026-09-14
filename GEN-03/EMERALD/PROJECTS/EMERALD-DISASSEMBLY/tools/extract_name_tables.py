#!/usr/bin/env python3
"""Extract and decode Emerald species/move fixed-width name tables."""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path

SPECIES_RECORDS = 412
MOVE_RECORDS = 355
EOS = 0xFF

WESTERN = {
    0x00:' ', 0x01:'À',0x02:'Á',0x03:'Â',0x04:'Ç',0x05:'È',0x06:'É',0x07:'Ê',0x08:'Ë',
    0x09:'Ì',0x0B:'Î',0x0C:'Ï',0x0D:'Ò',0x0E:'Ó',0x0F:'Ô',0x10:'Œ',0x11:'Ù',0x12:'Ú',
    0x13:'Û',0x14:'Ñ',0x15:'ß',0x16:'à',0x17:'á',0x19:'ç',0x1A:'è',0x1B:'é',0x1C:'ê',
    0x1D:'ë',0x1E:'ì',0x20:'î',0x21:'ï',0x22:'ò',0x23:'ó',0x24:'ô',0x25:'œ',0x26:'ù',
    0x27:'ú',0x28:'û',0x29:'ñ',0x2A:'º',0x2B:'ª',0x2D:'&',0x2E:'+',0x35:'=',0x36:';',
    0x51:'¿',0x52:'¡',0x5A:'Í',0x5B:'%',0x5C:'(',0x5D:')',0x68:'â',0x6F:'í',
    0xA1:'0',0xA2:'1',0xA3:'2',0xA4:'3',0xA5:'4',0xA6:'5',0xA7:'6',0xA8:'7',0xA9:'8',0xAA:'9',
    0xAB:'!',0xAC:'?',0xAD:'.',0xAE:'-',0xAF:'·',0xB0:'…',0xB1:'“',0xB2:'”',0xB3:'‘',0xB4:'’',
    0xB5:'♂',0xB6:'♀',0xB7:'¥',0xB8:',',0xB9:'×',0xBA:'/',0xEF:'▶',0xF0:':',
    0xF1:'Ä',0xF2:'Ö',0xF3:'Ü',0xF4:'ä',0xF5:'ö',0xF6:'ü',
}
for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 0xBB): WESTERN[i] = ch
for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz', 0xD5): WESTERN[i] = ch

HIRAGANA = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっ'
KATAKANA = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッ'
JAPANESE = {0x00:'　', 0xAB:'！',0xAC:'？',0xAD:'。',0xAE:'ー',0xB0:'⋯',0xB5:'♂',0xB6:'♀'}
for i, ch in enumerate(HIRAGANA, 1): JAPANESE[i] = ch
for i, ch in enumerate(KATAKANA, 0x51): JAPANESE[i] = ch
for k, v in WESTERN.items():
    if k >= 0xA1 and k not in JAPANESE:
        JAPANESE[k] = v


def decode_name(raw: bytes, japanese: bool):
    table = JAPANESE if japanese else WESTERN
    out=[]; unknown=[]; eos=None
    for i,b in enumerate(raw):
        if b == EOS:
            eos = i
            break
        ch=table.get(b)
        if ch is None:
            unknown.append(b)
            out.append(f'<{b:02X}>')
        else:
            out.append(ch)
    return ''.join(out), unknown, eos


def verify_and_load(ref, rom_dir):
    path=rom_dir/ref['source_filename']
    data=path.read_bytes()
    got=hashlib.sha1(data).hexdigest()
    if got != ref['sha1']:
        raise ValueError(f"SHA-1 mismatch for {ref['id']}: {got}")
    return data


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom_dir', type=Path)
    ap.add_argument('--manifest', type=Path, default=Path('manifests/roms.json'))
    ap.add_argument('--headers', type=Path, default=Path('analysis/gf_rom_headers.json'))
    ap.add_argument('--out-dir', type=Path, default=Path('text/name_tables'))
    args=ap.parse_args()

    manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
    refs={r['id']:r for r in manifest['references']}
    headers=json.loads(args.headers.read_text(encoding='utf-8'))['records']
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary=[]

    for h in headers:
        rid=h['id']
        rom=verify_and_load(refs[rid], args.rom_dir)
        japanese=(rid=='JPN')
        species_width=6 if japanese else 11
        move_width=8 if japanese else 13
        gap=h['moveNames_rom_offset']-h['monSpeciesNames_rom_offset']
        if gap != SPECIES_RECORDS*species_width:
            raise ValueError(f'{rid}: species table gap {gap:#x} != {SPECIES_RECORDS}*{species_width}')

        for kind,root,count,width in [
            ('species',h['monSpeciesNames_rom_offset'],SPECIES_RECORDS,species_width),
            ('moves',h['moveNames_rom_offset'],MOVE_RECORDS,move_width),
        ]:
            lines=[]; unknown_total=[]; missing_eos=[]
            for index in range(count):
                raw=rom[root+index*width:root+(index+1)*width]
                text,unknown,eos=decode_name(raw,japanese)
                unknown_total.extend(unknown)
                if eos is None:
                    missing_eos.append(index)
                lines.append(f'{index:03d}\t{text}\n')
            (args.out_dir/f'{rid.lower()}_{kind}.txt').write_text(''.join(lines), encoding='utf-8')
            summary.append({
                'release':rid,'table':kind,'root_rom_offset':f'0x{root:08X}',
                'record_count':count,'record_width':width,
                'unknown_code_count':len(unknown_total),
                'unknown_codes':' '.join(f'{b:02X}' for b in sorted(set(unknown_total))),
                'missing_eos_count':len(missing_eos),
            })

    with (args.out_dir/'summary.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]))
        w.writeheader(); w.writerows(summary)

if __name__=='__main__':
    main()
