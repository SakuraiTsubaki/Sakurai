#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROMS={
 'JP':'/mnt/data/Pocket Monsters - Emerald (Japan).gba',
 'EN':'/mnt/data/Pokemon - Emerald Version (U).gba',
 'FR':'/mnt/data/Pokemon - Version Emeraude (France).gba',
 'DE':'/mnt/data/Pokemon - Smaragd-Edition (Germany).gba',
 'IT':'/mnt/data/Pokemon - Versione Smeraldo (Italy).gba',
 'ES':'/mnt/data/Pokemon - Edicion Esmeralda (Spain).gba',
}
D={k:Path(v).read_bytes() for k,v in ROMS.items()}

# Anchors verified against pret/pokeemerald-jp funcmap_us.txt / funcmap_jp.txt.
EN_LAST_MAIN=0x1DB620
JP_LAST_MAIN=0x1DAB78
EN_LIB_START=0x2DED70
JP_LIB_START=0x28D2F8
EN_STRCPY=0x2E94E4
JP_LAST_LIB_FUNC=0x29BD74


def unique_find(data,sig):
    first=data.find(sig)
    if first<0: return None
    if data.find(sig,first+1)>=0: raise RuntimeError('signature not unique')
    return first

out={'anchors':{},'regions':{}}
for lang in ROMS:
    assert D[lang][0x3A4:0x3A8]

main_sig=D['EN'][EN_LAST_MAIN:EN_LAST_MAIN+28]
main_starts={'EN':EN_LAST_MAIN,'JP':JP_LAST_MAIN}
for lang in ['FR','DE','IT','ES']:
    p=unique_find(D[lang][0x180000:0x200000],main_sig)
    if p is None: raise RuntimeError(f'{lang}: last-main anchor not found')
    main_starts[lang]=0x180000+p

main_ends={}
for lang,s in main_starts.items():
    if lang=='JP':
        main_ends[lang]=0x1DABA4
    else:
        d=D[lang]
        end=None
        for o in range(s,s+0x100,2):
            if int.from_bytes(d[o:o+2],'little')==0x4700:
                end=o+2
                break
        if end is None: raise RuntimeError(f'{lang}: last-main return not found')
        main_ends[lang]=end

lib_sig=D['EN'][EN_LIB_START:EN_LIB_START+256]
lib_starts={}
for lang,d in D.items():
    p=unique_find(d,lib_sig)
    if p is None: raise RuntimeError(f'{lang}: library start anchor not found')
    lib_starts[lang]=p
assert lib_starts['JP']==JP_LIB_START

strcpy_sig=D['EN'][EN_STRCPY:EN_STRCPY+64]
strcpy_starts={}
for lang,d in D.items():
    p=unique_find(d,strcpy_sig)
    if p is None: raise RuntimeError(f'{lang}: strcpy anchor not found')
    strcpy_starts[lang]=p
lib_ends={lang:(s+0x4A) for lang,s in strcpy_starts.items() if lang!='JP'}
lib_ends['JP']=0x29BDA0

out['anchors']={
 'main_entry_common':'0x0003A4',
 'main_last_function_start':{k:f'0x{v:06X}' for k,v in main_starts.items()},
 'library_GameCubeMultiBoot_Hash':{k:f'0x{v:06X}' for k,v in lib_starts.items()},
 'strcpy_anchor':{k:f'0x{v:06X}' for k,v in strcpy_starts.items()},
 'signature_sha256':{
   'western_last_main_28':hashlib.sha256(main_sig).hexdigest(),
   'library_start_256':hashlib.sha256(lib_sig).hexdigest(),
   'strcpy_64':hashlib.sha256(strcpy_sig).hexdigest(),
 }
}
for lang in ROMS:
    out['regions'][lang]=[
      {'kind':'ARM_STARTUP','start':'0x000204','end_exclusive':'0x0003A4'},
      {'kind':'THUMB_MAIN','start':'0x0003A4','end_exclusive':f'0x{main_ends[lang]:06X}'},
      {'kind':'LIBRARY_CODE','start':f'0x{lib_starts[lang]:06X}','end_exclusive':f'0x{lib_ends[lang]:06X}'},
    ]

p=Path('/mnt/data/emerald_bank_audit/disassembly/boundary_evidence.json')
p.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(p)
print(json.dumps(out['anchors'],indent=2))
