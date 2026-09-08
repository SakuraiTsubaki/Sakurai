#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, json, re
BANK=0x4000
V3=Path(__file__).resolve().parents[1]
ROOT=V3.parent
ROM_DIR=Path('/mnt/data')
manifest=json.loads((V3/'reports/v3_manifest.json').read_text())
expected_total=0; expected_banks=0
for r in manifest['roms']:
    p=ROM_DIR/r['filename_reference']; d=p.read_bytes(); h=hashlib.sha256(d).hexdigest()
    assert len(d)==r['size'],(r['code'],'size')
    assert h==r['sha256'],(r['code'],'sha256')
    assert len(d)//BANK==r['banks'],(r['code'],'banks')
    expected_total+=len(d); expected_banks+=len(d)//BANK
assert expected_total==5767168,expected_total
assert expected_banks==352,expected_banks
with (V3/'reports/work_unit_registry.csv').open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
assert len(rows)==expected_banks
assert len({(r['rom_code'],r['bank_hex']) for r in rows})==expected_banks
for line in (V3/'reports/generated_report_checksums.sha256').read_text().splitlines():
    if not line.strip(): continue
    want,rel=line.split(None,1); q=V3/rel.strip()
    assert hashlib.sha256(q.read_bytes()).hexdigest()==want,q
for rom in manifest['roms']:
    bank_dir=ROOT/'scaffold'/rom['code']/'banks'; files=sorted(bank_dir.glob('bank_*.asm'))
    assert len(files)==rom['banks']
    for p in files:
        inc=re.findall(r'INCBIN\s+"baserom\.gb",\s*\$([0-9A-Fa-f]+),\s*\$0100',p.read_text(encoding='utf-8'))
        assert len(inc)==64,(p,len(inc))
print(f'PASS v3: {expected_banks} banks / {expected_total} bytes / six ROM hashes / all 0x100 scaffold chunks verified')
