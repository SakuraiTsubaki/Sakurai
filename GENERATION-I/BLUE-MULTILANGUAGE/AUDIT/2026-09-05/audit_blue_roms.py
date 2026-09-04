#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import hashlib, json, csv, itertools, math

ROOT = Path('/mnt/data')
OUT = ROOT / 'blue_rom_audit'
FILES = sorted(ROOT.glob('*.gb'))
BANK=0x4000
NINTENDO_LOGO = bytes.fromhex('CEED6666CC0D000B03730083000C000D0008111F8889000EDCCC6EE6DDDDD999BBBB67636E0EECCCDDDC999FBBB9333E')
CART_TYPES={0x03:'MBC1+RAM+BATTERY',0x13:'MBC3+RAM+BATTERY',0x1B:'MBC5+RAM+BATTERY'}
ROM_SIZES={0x04:512*1024,0x05:1024*1024}
RAM_SIZES={0x03:32*1024}

def hchk(b):
    x=0
    for v in b[0x134:0x14D]: x=(x-v-1)&0xff
    return x

def gchk(b):
    return (sum(b)-b[0x14e]-b[0x14f])&0xffff

def entropy(x):
    n=len(x); c=Counter(x)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

records=[]; data={}; bank_rows=[]
for p in FILES:
    b=p.read_bytes(); data[p.name]=b
    banks=[b[i:i+BANK] for i in range(0,len(b),BANK)]
    bank_sha1=[]
    for i,x in enumerate(banks):
        sh=hashlib.sha1(x).hexdigest(); bank_sha1.append(sh)
        c=Counter(x)
        bank_rows.append({
            'file':p.name,'bank':i,'offset_start':i*BANK,'offset_end':(i+1)*BANK-1,
            'sha1':sh,'entropy':round(entropy(x),6),'zero_bytes':c[0],'ff_bytes':c[255],
            'all_zero':len(c)==1 and 0 in c,'all_ff':len(c)==1 and 255 in c,'unique_byte_values':len(c)
        })
    rec={
      'file':p.name,'size_bytes':len(b),'banks_16k':len(banks),
      'sha256':hashlib.sha256(b).hexdigest(),'sha1':hashlib.sha1(b).hexdigest(),'md5':hashlib.md5(b).hexdigest(),
      'title':b[0x134:0x144].split(b'\0',1)[0].decode('ascii','replace'),
      'sgb_flag':b[0x146], 'cartridge_type_code':b[0x147], 'cartridge_type':CART_TYPES.get(b[0x147],f'0x{b[0x147]:02X}'),
      'rom_size_code':b[0x148], 'rom_size_expected':ROM_SIZES.get(b[0x148]),
      'ram_size_code':b[0x149], 'ram_size_expected':RAM_SIZES.get(b[0x149]),
      'destination_code':b[0x14A], 'old_licensee':b[0x14B], 'version':b[0x14C],
      'header_checksum_stored':b[0x14D], 'header_checksum_calculated':hchk(b),
      'header_checksum_valid':b[0x14D]==hchk(b),
      'global_checksum_stored':int.from_bytes(b[0x14E:0x150],'big'), 'global_checksum_calculated':gchk(b),
      'global_checksum_valid':int.from_bytes(b[0x14E:0x150],'big')==gchk(b),
      'nintendo_logo_valid':b[0x104:0x134]==NINTENDO_LOGO,
      'bank_sha1':bank_sha1,
    }
    records.append(rec)

pairs=[]
for a,c in itertools.combinations(records,2):
    ba=data[a['file']]; bb=data[c['file']]; n=min(len(ba),len(bb))
    diff=sum(x!=y for x,y in zip(ba[:n],bb[:n]))
    exact=[]
    for i in range(min(a['banks_16k'],c['banks_16k'])):
        if ba[i*BANK:(i+1)*BANK]==bb[i*BANK:(i+1)*BANK]: exact.append(i)
    first=next((i for i,(x,y) in enumerate(zip(ba[:n],bb[:n])) if x!=y),None)
    pairs.append({'a':a['file'],'b':c['file'],'compared_bytes':n,'different_bytes':diff,'same_percent':round((n-diff)*100/n,6),'first_difference':first,'exact_equal_banks':exact,'exact_equal_bank_count':len(exact)})

western=[r for r in records if r['size_bytes']==1048576]
bank_groups=[]
for i in range(64):
    groups={}
    for r in western:
        sh=r['bank_sha1'][i]
        groups.setdefault(sh,[]).append(r['file'])
    shared=[v for v in groups.values() if len(v)>1]
    if shared: bank_groups.append({'bank':i,'offset_start':i*BANK,'shared_groups':shared})

json_out={'generated_from':'project-mounted ROM files; ROM bytes are not included','records':records,'pairwise':pairs,'shared_western_bank_groups':bank_groups}
(OUT/'blue_rom_inventory.json').write_text(json.dumps(json_out,ensure_ascii=False,indent=2),encoding='utf-8')

with (OUT/'blue_rom_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
    fields=['file','size_bytes','banks_16k','sha256','sha1','md5','title','sgb_flag','cartridge_type_code','cartridge_type','rom_size_code','ram_size_code','destination_code','version','header_checksum_valid','global_checksum_valid','nintendo_logo_valid']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for r in records: w.writerow({k:r[k] for k in fields})
with (OUT/'bank_census.csv').open('w',newline='',encoding='utf-8-sig') as f:
    fields=list(bank_rows[0]); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(bank_rows)
with (OUT/'pairwise_similarity.csv').open('w',newline='',encoding='utf-8-sig') as f:
    fields=['a','b','compared_bytes','different_bytes','same_percent','first_difference','exact_equal_bank_count','exact_equal_banks']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for r in pairs:
        rr=r.copy(); rr['exact_equal_banks']=' '.join(map(str,rr['exact_equal_banks'])); w.writerow({k:rr[k] for k in fields})

lines=['# Pokémon Blue ROM baseline audit','',
'ROM 원본은 저장소에 포함하지 않는다. 이 문서는 프로젝트에 마운트된 ROM에서 산출한 메타데이터/구조 기초 원장이다.','',
'## Inventory','',
'| ROM | Size | Banks | Mapper | Dest | Ver | SHA-1 | Header | Global |',
'|---|---:|---:|---|---:|---:|---|---|---|']
for r in records:
    lines.append(f"| {r['file']} | {r['size_bytes']//1024} KiB | {r['banks_16k']} | {r['cartridge_type']} | {r['destination_code']} | {r['version']} | `{r['sha1']}` | {'OK' if r['header_checksum_valid'] else 'FAIL'} | {'OK' if r['global_checksum_valid'] else 'FAIL'} |")
lines += ['', '## Immediate structural findings','',
'- 일본판 Pocket Monsters Ao는 512 KiB / 32 banks / MBC1+RAM+BATTERY이다.',
'- 서구권 5개판은 1 MiB / 64 banks이다.',
'- 영문판은 MBC3+RAM+BATTERY, 독/불/이/서판은 MBC5+RAM+BATTERY로 헤더 매퍼가 다르다.',
'- 6개 ROM 모두 Nintendo logo, header checksum, global checksum 검증을 통과했다.',
'- 서구 5개판의 bank 45–63 (19 banks = 304 KiB)는 모두 완전한 `0x00` 빈 뱅크이며 서로 동일하다.',
'- 서구 5개판의 bank 27은 빈 뱅크가 아니라 실제 데이터가 있는 상태로 5개판 전체가 정확히 동일하다.',
'- 따라서 JP ↔ western은 단순 번역 차이로 취급할 수 없고, western 내부에서도 EN ↔ DE/FR/IT/ES의 뱅킹/매퍼 차이를 별도 추적해야 한다.',
'', '## Pairwise byte similarity', '',
'비교 길이는 두 ROM 중 더 짧은 쪽까지이며, 체크섬/헤더 차이도 포함한다.', '',
'| A | B | Compared | Different bytes | Same % | Exact 16KiB banks |',
'|---|---|---:|---:|---:|---:|']
for p in pairs:
    lines.append(f"| {p['a']} | {p['b']} | {p['compared_bytes']} | {p['different_bytes']} | {p['same_percent']:.3f}% | {p['exact_equal_bank_count']} |")
lines += ['', '## Generated ledgers', '',
'- `blue_rom_inventory.csv`: ROM-level header/hash inventory.',
'- `bank_census.csv`: every 16 KiB bank with SHA-1, entropy, zero/FF counts and blank-bank flags.',
'- `pairwise_similarity.csv`: ROM-pair byte similarity and exact-bank matches.',
'- `blue_rom_inventory.json`: machine-readable full baseline, including per-bank hashes.',
'- `audit_blue_roms.py`: reproducible audit generator; ROM bytes are never embedded.',
'', '## Next census layers', '',
'1. Banks 0–44의 code/data/text/graphics/audio 역할 분류 및 free-space 후보 확정.',
'2. Pointer tables / text engines / character tables / fonts / SGB data identification.',
'3. JP Blue ↔ EN Blue ↔ DE/FR/IT/ES localization correspondence map.',
'4. Maps, scripts, encounters, trainers, items, graphics, audio, Pokédex, menus/UI table census.',
'5. Provenance ledger and patch-safe address map.',
'', '## Repository rule', '',
'- ROM binaries: **never commit**.',
'- Analysis reports, ledgers, scripts, tools, patches, and other non-ROM outputs: commit to `Sakurai` as work progresses.',
]
(OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('generated:', ', '.join(sorted(p.name for p in OUT.iterdir())))
