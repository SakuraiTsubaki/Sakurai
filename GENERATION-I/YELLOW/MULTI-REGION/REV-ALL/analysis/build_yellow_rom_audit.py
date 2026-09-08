#!/usr/bin/env python3
from pathlib import Path
import hashlib, csv, json, collections, itertools

ROOT = Path('/mnt/data')
OUT = ROOT / 'yellow_rom_audit'
OUT.mkdir(exist_ok=True)

ROM_GLOBS = ('*.gb','*.gbc')
paths=[]
for g in ROM_GLOBS:
    paths.extend(ROOT.glob(g))
paths=sorted(paths, key=lambda p:p.name)

NINTENDO_LOGO = bytes.fromhex(
    'CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D '
    '00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99 '
    'BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E')

def hsum(b):
    x=0
    for i in range(0x134,0x14D):
        x=(x-b[i]-1)&0xff
    return x

def gsum(b):
    return (sum(b[:0x14E])+sum(b[0x150:]))&0xffff

def sha(alg,b):
    h=hashlib.new(alg); h.update(b); return h.hexdigest()

def parse(p):
    b=p.read_bytes()
    cgb=b[0x143]
    # Header title/game-ID layout varies across cartridge generations. Preserve neutral views
    # instead of assuming bytes 013F-0142 are always a manufacturer code.
    title_legacy=b[0x134:0x143].rstrip(b'\0').decode('ascii','replace')
    title_11=b[0x134:0x13F].rstrip(b'\0').decode('ascii','replace')
    tail_013f_0142=b[0x13F:0x143].rstrip(b'\0').decode('ascii','replace')
    return {
        'filename':p.name,
        'size_bytes':len(b),
        'md5':sha('md5',b),
        'sha1':sha('sha1',b),
        'sha256':sha('sha256',b),
        'header_0134_0143_hex':b[0x134:0x144].hex().upper(),
        'title_legacy_0134_0142':title_legacy,
        'title_11_0134_013E':title_11,
        'tail_013F_0142_ascii':tail_013f_0142,
        'tail_013F_0142_hex':b[0x13F:0x143].hex().upper(),
        'cgb_flag':f'0x{cgb:02X}',
        'new_licensee':b[0x144:0x146].decode('ascii','replace'),
        'sgb_flag':f'0x{b[0x146]:02X}',
        'cartridge_type':f'0x{b[0x147]:02X}',
        'rom_size_code':f'0x{b[0x148]:02X}',
        'ram_size_code':f'0x{b[0x149]:02X}',
        'destination_code':f'0x{b[0x14A]:02X}',
        'old_licensee':f'0x{b[0x14B]:02X}',
        'header_version':b[0x14C],
        'header_checksum_stored':f'0x{b[0x14D]:02X}',
        'header_checksum_calc':f'0x{hsum(b):02X}',
        'header_checksum_valid':hsum(b)==b[0x14D],
        'global_checksum_stored':f'0x{int.from_bytes(b[0x14E:0x150],"big"):04X}',
        'global_checksum_calc':f'0x{gsum(b):04X}',
        'global_checksum_valid':gsum(b)==int.from_bytes(b[0x14E:0x150],"big"),
        'nintendo_logo_valid':b[0x104:0x134]==NINTENDO_LOGO,
    }, b

records=[]; blobs={}
for p in paths:
    r,b=parse(p); records.append(r); blobs[p.name]=b

# Exact duplicate groups by SHA-1
by_sha=collections.defaultdict(list)
for r in records: by_sha[r['sha1']].append(r['filename'])
dup_groups=[]
for s,names in sorted(by_sha.items()):
    dup_groups.append({'sha1':s,'count':len(names),'filenames':sorted(names)})

# Canonical representative: prefer verbose .gb dump name when duplicate; otherwise only file.
def rep_name(names):
    gb=[n for n in names if n.endswith('.gb')]
    if gb: return sorted(gb, key=lambda x:(-len(x),x))[0]
    return sorted(names)[0]
unique=[]
for s,names in by_sha.items():
    n=rep_name(names)
    unique.append((n,blobs[n],s))
unique.sort(key=lambda x:x[0])

# Manifest CSV/JSON
fields=list(records[0].keys()) if records else []
with (OUT/'rom_manifest.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(records)
(OUT/'rom_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'duplicate_groups.json').write_text(json.dumps(dup_groups,ensure_ascii=False,indent=2),encoding='utf-8')

# Bank hashes for unique ROMs
with (OUT/'bank_sha1.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['rom','sha1','bank_dec','bank_hex','offset_start','offset_end','bank_sha1'])
    for n,b,s in unique:
        for bank in range(len(b)//0x4000):
            chunk=b[bank*0x4000:(bank+1)*0x4000]
            w.writerow([n,s,bank,f'{bank:02X}',f'0x{bank*0x4000:06X}',f'0x{(bank+1)*0x4000-1:06X}',sha('sha1',chunk)])

# Pairwise byte-diff / bank-diff summary for 9 unique images
pair_rows=[]
for (na,a,sa),(nb,b,sb) in itertools.combinations(unique,2):
    diff_positions=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    diff_banks=sorted({i//0x4000 for i in diff_positions})
    pair_rows.append({
        'rom_a':na,'sha1_a':sa,'rom_b':nb,'sha1_b':sb,
        'diff_bytes':len(diff_positions),
        'same_bytes':len(a)-len(diff_positions),
        'diff_percent':round(100*len(diff_positions)/len(a),6),
        'different_banks':len(diff_banks),
        'identical_banks':64-len(diff_banks),
        'different_bank_list':' '.join(f'{x:02X}' for x in diff_banks),
        'first_diff':f'0x{diff_positions[0]:06X}' if diff_positions else '',
        'last_diff':f'0x{diff_positions[-1]:06X}' if diff_positions else '',
    })
with (OUT/'pairwise_diff_summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(pair_rows[0].keys())); w.writeheader(); w.writerows(pair_rows)

# compact identity table for unique ROMs
unique_records=[]
for n,b,s in unique:
    r=next(r for r in records if r['filename']==n)
    aliases=sorted(by_sha[s])
    unique_records.append({**r,'aliases':aliases})
(OUT/'unique_roms.json').write_text(json.dumps(unique_records,ensure_ascii=False,indent=2),encoding='utf-8')

# Human-readable README
jp=[r for r in unique_records if r['filename'].startswith('Pocket Monsters')]
intl=[r for r in unique_records if not r['filename'].startswith('Pocket Monsters')]
lines=[]
lines += ['# Pokémon Yellow ROM audit','',
          'This package contains only hashes, header metadata, bank hashes, and comparison summaries. No ROM bytes are redistributed.','',
          '## Inventory','',
          f'- Uploaded files scanned: **{len(records)}**',
          f'- Byte-unique ROM images: **{len(unique_records)}**',
          f'- Exact duplicate filename pairs/groups: **{sum(1 for g in dup_groups if g["count"]>1)}**',
          f'- Japanese unique revisions: **{len(jp)}**',
          f'- International unique language builds: **{len(intl)}**','',
          '## Common hardware/header facts','',
          '- All images are 1,048,576 bytes (1 MiB / 64 × 16 KiB ROM banks).',
          '- All declare 32 KiB external RAM.',
          '- All have valid Nintendo logo, header checksum, and global checksum.',
          '- All are Super Game Boy enhanced (`SGB flag = 0x03`).',
          '- Japanese revisions are DMG/SGB (`CGB flag = 0x00`) and use cartridge type `0x13` (MBC3+RAM+BATTERY).',
          '- International builds are CGB-compatible (`CGB flag = 0x80`) and use cartridge type `0x1B` (MBC5+RAM+BATTERY).','',
          '## Exact duplicate aliases','']
for g in dup_groups:
    if g['count']>1:
        lines.append(f'- `{g["sha1"]}`')
        for n in g['filenames']: lines.append(f'  - `{n}`')
lines += ['', '## Japanese revision identity','']
for r in sorted(jp,key=lambda x:x['header_version']):
    lines.append(f'- header version {r["header_version"]}: `{r["filename"]}` — SHA-1 `{r["sha1"]}`')
lines += ['', '## Files','',
          '- `rom_manifest.csv` / `rom_manifest.json`: all 14 uploaded filenames and parsed header/checksum metadata.',
          '- `unique_roms.json`: 9 byte-unique ROM images with alias lists.',
          '- `duplicate_groups.json`: exact SHA-1 duplicate groups.',
          '- `bank_sha1.csv`: SHA-1 for each 16 KiB bank of every unique image.',
          '- `pairwise_diff_summary.csv`: byte-level and bank-level pairwise comparison of all 9 unique images.',
          '- `inspect_yellow_roms.py`: standalone re-runnable inspector.',
          '',
          '## Interpretation note','',
          'Filename extensions (`.gb` vs `.gbc`) are not evidence of different ROM content. The duplicate groups above are byte-identical, so one canonical image per SHA-1 is sufficient for analysis.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# standalone inspect script copied from a simpler embedded implementation
script='''#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

def header_checksum(b):
    x=0
    for i in range(0x134,0x14D): x=(x-b[i]-1)&0xff
    return x

def global_checksum(b): return (sum(b[:0x14E])+sum(b[0x150:]))&0xffff

def inspect(path):
    b=Path(path).read_bytes()
    return {
      "filename":Path(path).name,"size":len(b),
      "md5":hashlib.md5(b).hexdigest(),"sha1":hashlib.sha1(b).hexdigest(),"sha256":hashlib.sha256(b).hexdigest(),
      "cgb_flag":f"0x{b[0x143]:02X}","sgb_flag":f"0x{b[0x146]:02X}","cartridge_type":f"0x{b[0x147]:02X}",
      "rom_size_code":f"0x{b[0x148]:02X}","ram_size_code":f"0x{b[0x149]:02X}","destination_code":f"0x{b[0x14A]:02X}",
      "header_version":b[0x14C],"header_checksum_valid":header_checksum(b)==b[0x14D],
      "global_checksum_valid":global_checksum(b)==int.from_bytes(b[0x14E:0x150],"big")
    }

if __name__=="__main__":
    import sys
    print(json.dumps([inspect(p) for p in sys.argv[1:]],indent=2))
'''
(OUT/'inspect_yellow_roms.py').write_text(script,encoding='utf-8')

print(OUT)
print('files:',*[p.name for p in sorted(OUT.iterdir())],sep='\n- ')
