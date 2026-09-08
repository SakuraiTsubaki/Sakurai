from pathlib import Path
import csv, hashlib, json

ROOT = Path('/mnt/data')
FILES = sorted(list(ROOT.glob('*.gb')) + list(ROOT.glob('*.gbc')))
ROM_SIZE = {0x00:32768,0x01:65536,0x02:131072,0x03:262144,0x04:524288,0x05:1048576,0x06:2097152,0x07:4194304,0x08:8388608,0x52:1179648,0x53:1310720,0x54:1572864}
RAM_SIZE = {0x00:0,0x01:2048,0x02:8192,0x03:32768,0x04:131072,0x05:65536}
CART = {0x03:'MBC1+RAM+BATTERY',0x13:'MBC3+RAM+BATTERY',0x1B:'MBC5+RAM+BATTERY'}

def header(p):
    b=p.read_bytes()
    title=b[0x134:0x143].split(b'\0')[0].decode('ascii','replace')
    hc=0
    for x in b[0x134:0x14D]: hc=(hc-x-1)&0xFF
    gc=(sum(b[:0x14E])+sum(b[0x150:]))&0xFFFF
    gs=int.from_bytes(b[0x14E:0x150],'big')
    return {
        'file':p.name,'bytes':len(b),'size_kib':len(b)//1024,
        'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),
        'title':title,'cgb_flag':f'0x{b[0x143]:02X}','sgb_flag':f'0x{b[0x146]:02X}',
        'cart_type':f'0x{b[0x147]:02X}','cart':CART.get(b[0x147],f'unknown 0x{b[0x147]:02X}'),
        'rom_size_code':f'0x{b[0x148]:02X}','rom_size_declared':ROM_SIZE.get(b[0x148]),
        'ram_size_code':f'0x{b[0x149]:02X}','ram_size_declared':RAM_SIZE.get(b[0x149]),
        'destination':'Japan' if b[0x14A]==0 else 'Non-Japan',
        'version':b[0x14C],
        'header_checksum':f'0x{b[0x14D]:02X}','header_ok':hc==b[0x14D],
        'global_checksum':f'0x{gs:04X}','global_ok':gc==gs,
    }

rows=[header(p) for p in FILES]
with open(ROOT/'rby_rom_inventory_2026-09-09.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

def diff(a,b):
    aa=(ROOT/a).read_bytes(); bb=(ROOT/b).read_bytes()
    n=min(len(aa),len(bb)); positions=[i for i in range(n) if aa[i]!=bb[i]]
    banks=sorted({i//0x4000 for i in positions})
    exact=[]
    for bank in range(n//0x4000):
        s=bank*0x4000;e=s+0x4000
        if aa[s:e]==bb[s:e]: exact.append(bank)
    return {'from':a,'to':b,'diff_bytes':len(positions)+abs(len(aa)-len(bb)),'changed_banks':banks,'exact_banks':exact}

comparisons=[
 diff('Pocket Monsters - Aka (Japan) (SGB Enhanced).gb','Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb'),
 diff('Pocket Monsters - Midori (Japan) (SGB Enhanced).gb','Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb'),
 diff('Pocket Monsters - Pikachu (Japan) (Rev 0A) (SGB Enhanced).gb','Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb'),
 diff('Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb','Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb'),
 diff('Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb','Pocket Monsters - Pikachu (Japan) (Rev D) (SGB Enhanced).gb'),
 diff('Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb','Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb'),
]
with open(ROOT/'rby_rom_revision_diffs_2026-09-09.json','w',encoding='utf-8') as f: json.dump(comparisons,f,ensure_ascii=False,indent=2)
