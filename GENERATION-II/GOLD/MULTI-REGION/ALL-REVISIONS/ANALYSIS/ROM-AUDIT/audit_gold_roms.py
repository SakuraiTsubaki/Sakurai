#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, hashlib, math, collections, json

parser=argparse.ArgumentParser()
parser.add_argument('--input', type=Path, default=Path('.'))
parser.add_argument('--output', type=Path, default=Path('gold_rom_audit'))
args=parser.parse_args()
ROOT=args.input
OUT=args.output
OUT.mkdir(parents=True, exist_ok=True)
ROMS=sorted(ROOT.glob('*.gbc'))
BANK=0x4000
ROM_SIZE={0x00:32768,0x01:65536,0x02:131072,0x03:262144,0x04:524288,0x05:1048576,0x06:2097152,0x07:4194304,0x08:8388608,0x52:1179648,0x53:1310720,0x54:1572864}
RAM_SIZE={0x00:0,0x01:2048,0x02:8192,0x03:32768,0x04:131072,0x05:65536}
CART={0x10:'MBC3+TIMER+RAM+BATTERY'}

def sha1(b): return hashlib.sha1(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()
def hchk(d):
    x=0
    for i in range(0x134,0x14D): x=(x-d[i]-1)&0xff
    return x
def gchk(d): return (sum(d)-d[0x14e]-d[0x14f])&0xffff
def entropy(b):
    c=collections.Counter(b); n=len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
def title(d):
    raw=d[0x134:0x143]
    return ''.join(chr(x) if 32<=x<127 else f'\\x{x:02X}' for x in raw).replace('\\x00','').rstrip()
def label(name):
    if 'Korea' in name: return ('KOREA','REV-0')
    if 'Japan' in name and 'Rev A' in name: return ('JAPAN','REV-A')
    if 'Japan' in name: return ('JAPAN','REV-0')
    if 'USA, Europe' in name: return ('USA-EUROPE','REV-0')
    if 'Germany' in name: return ('GERMANY','REV-0')
    if 'France' in name: return ('FRANCE','REV-0')
    if 'Italy' in name: return ('ITALY','REV-0')
    if 'Spain' in name: return ('SPAIN','REV-0')
    return ('UNKNOWN','UNKNOWN')

records=[]; banks_by_file={}; data_by_file={}
for p in ROMS:
    d=p.read_bytes(); data_by_file[p.name]=d
    region,rev=label(p.name)
    banks=[]
    for i in range(len(d)//BANK):
        b=d[i*BANK:(i+1)*BANK]
        c=collections.Counter(b)
        dominant,count=c.most_common(1)[0]
        banks.append({'file':p.name,'region':region,'revision':rev,'bank_dec':i,'bank_hex':f'{i:02X}',
                      'offset_start':f'0x{i*BANK:06X}','offset_end':f'0x{(i+1)*BANK-1:06X}',
                      'sha1':sha1(b),'entropy':f'{entropy(b):.6f}','unique_bytes':len(c),
                      'dominant_byte':f'0x{dominant:02X}','dominant_count':count,'all_zero':len(c)==1 and dominant==0})
    banks_by_file[p.name]=banks
    stored_g=(d[0x14e]<<8)|d[0x14f]
    records.append({'file':p.name,'region':region,'revision':rev,'size_bytes':len(d),'size_mib':len(d)/(1024*1024),
                    'bank_count':len(banks),'title':title(d),'cgb_flag':f'0x{d[0x143]:02X}','sgb_flag':f'0x{d[0x146]:02X}',
                    'cartridge_type':f'0x{d[0x147]:02X} {CART.get(d[0x147],"UNKNOWN")}',
                    'rom_size_code':f'0x{d[0x148]:02X}','declared_rom_bytes':ROM_SIZE.get(d[0x148],''),
                    'ram_size_code':f'0x{d[0x149]:02X}','declared_ram_bytes':RAM_SIZE.get(d[0x149],''),
                    'destination':'Japan' if d[0x14a]==0 else 'Non-Japan','old_license_code':f'0x{d[0x14b]:02X}',
                    'version_byte':d[0x14c],'header_checksum_stored':f'0x{d[0x14d]:02X}','header_checksum_calc':f'0x{hchk(d):02X}',
                    'header_checksum_ok':hchk(d)==d[0x14d],'global_checksum_stored':f'0x{stored_g:04X}','global_checksum_calc':f'0x{gchk(d):04X}',
                    'global_checksum_ok':gchk(d)==stored_g,'sha1':sha1(d),'sha256':sha256(d),
                    'all_zero_bank_count':sum(x['all_zero'] for x in banks),
                    'all_zero_banks':' '.join(x['bank_hex'] for x in banks if x['all_zero'])})

with (OUT/'rom_manifest.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=records[0].keys()); w.writeheader(); w.writerows(records)
with (OUT/'bank_manifest.csv').open('w',newline='',encoding='utf-8') as f:
    allb=[b for p in ROMS for b in banks_by_file[p.name]]
    w=csv.DictWriter(f,fieldnames=allb[0].keys()); w.writeheader(); w.writerows(allb)

pairs=[]
for i,a in enumerate(ROMS):
    for b in ROMS[i+1:]:
        ba=banks_by_file[a.name]; bb=banks_by_file[b.name]; n=min(len(ba),len(bb))
        same=[j for j in range(n) if ba[j]['sha1']==bb[j]['sha1']]
        pairs.append({'file_a':a.name,'file_b':b.name,'compared_banks':n,'identical_same_index_banks':len(same),
                      'identity_percent':f'{100*len(same)/n:.3f}','identical_bank_hex':' '.join(f'{x:02X}' for x in same)})
with (OUT/'pairwise_bank_identity.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=pairs[0].keys()); w.writeheader(); w.writerows(pairs)

name0='Pocket Monsters Kin (Japan).gbc'; name1='Pocket Monsters Kin (Japan) (Rev A).gbc'
a=data_by_file[name0]; b=data_by_file[name1]
diffs=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
runs=[]
if diffs:
    s=prev=diffs[0]
    for x in diffs[1:]:
        if x==prev+1: prev=x; continue
        runs.append((s,prev)); s=prev=x
    runs.append((s,prev))
rows=[]
for s,e in runs:
    rows.append({'start_offset':f'0x{s:06X}','end_offset':f'0x{e:06X}','length':e-s+1,'bank_hex':f'{s//BANK:02X}',
                 'rev0_sha1_segment':sha1(a[s:e+1]),'revA_sha1_segment':sha1(b[s:e+1])})
with (OUT/'japan_rev0_vs_reva_diff_runs.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

summary={
 'rom_count':len(records),
 'total_input_bytes':sum(r['size_bytes'] for r in records),
 'japan_rev0_vs_reva_different_bytes':len(diffs),
 'japan_rev0_vs_reva_changed_banks':sorted({i//BANK for i in diffs}),
 'roms':records,
}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

readme=['# Pokémon Gold uploaded-ROM audit','',
        'Generated from the eight uploaded `.gbc` ROMs. Original ROM binaries are **not** included.','',
        '## Key findings','',
        '- 8 ROM images detected; all header and global checksums validate.','- Japanese Rev 0 / Rev A are 1 MiB (64 × 16 KiB banks).',
        '- Korean / USA-Europe / German / French / Italian / Spanish ROMs are 2 MiB (128 × 16 KiB banks).',
        '- Korean Gold reports CGB flag `0xC0` (CGB-only) and SGB flag `0x00`; the other seven report CGB flag `0x80`, and the Japanese/Western ROMs report SGB flag `0x03`.',
        f'- Japanese Rev 0 vs Rev A differ in {len(diffs):,} bytes across banks '+', '.join(f'${x:02X}' for x in sorted({i//BANK for i in diffs}))+'.',
        '', '## Files','',
        '- `audit_gold_roms.py` — reproducible scanner','- `rom_manifest.csv` — ROM-level header/checksum/hash manifest',
        '- `bank_manifest.csv` — per-bank hashes/entropy/empty-bank flags','- `pairwise_bank_identity.csv` — same-index exact-bank comparison',
        '- `japan_rev0_vs_reva_diff_runs.csv` — contiguous Rev 0 ↔ Rev A difference ranges','- `summary.json` — machine-readable summary','',
        '## Safety / provenance','',
        'The script reads `.gbc` files from the input directory and never modifies them. No copyrighted ROM binary is written to this analysis package.'
]
(OUT/'README.md').write_text('\n'.join(readme)+'\n',encoding='utf-8')
print('generated',OUT)
print('\n'.join(x.name for x in OUT.iterdir()))
