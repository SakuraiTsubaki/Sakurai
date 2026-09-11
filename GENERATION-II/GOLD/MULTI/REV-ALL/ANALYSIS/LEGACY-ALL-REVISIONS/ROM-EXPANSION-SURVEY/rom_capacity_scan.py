#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT = Path('/mnt/data')
roms = sorted(ROOT.glob('*.gbc'))
out=[]
for p in roms:
    b=p.read_bytes(); banks=len(b)//0x4000
    full_blank=[]; large_run_bytes=0; max_run=0
    for bi in range(banks):
        x=b[bi*0x4000:(bi+1)*0x4000]
        if len(set(x)) == 1 and x[0] in (0x00,0xff):
            full_blank.append(bi)
        i=0
        while i < len(x):
            v=x[i]
            if v not in (0x00,0xff):
                i += 1; continue
            j=i+1
            while j < len(x) and x[j] == v:
                j += 1
            n=j-i
            if n >= 0x100:
                large_run_bytes += n
                max_run=max(max_run,n)
            i=j
    out.append({
        'file':p.name,
        'size_bytes':len(b),
        'size_mib':len(b)/1048576,
        'banks_16k':banks,
        'cart_type':b[0x147],
        'rom_size_code':b[0x148],
        'ram_size_code':b[0x149],
        'version':b[0x14c],
        'md5':hashlib.md5(b).hexdigest(),
        'sha1':hashlib.sha1(b).hexdigest(),
        'sha256':hashlib.sha256(b).hexdigest(),
        'full_blank_16k_banks':[f'{i:02X}' for i in full_blank],
        'full_blank_bytes':len(full_blank)*0x4000,
        'large_00_ff_runs_ge_256_bytes':large_run_bytes,
        'max_large_run_bytes':max_run,
    })
print(json.dumps(out, indent=2, ensure_ascii=False))
