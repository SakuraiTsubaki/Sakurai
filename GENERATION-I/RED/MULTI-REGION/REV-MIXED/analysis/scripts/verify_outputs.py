#!/usr/bin/env python3
from pathlib import Path
import tempfile, subprocess, sys, hashlib
if len(sys.argv)!=3: raise SystemExit("usage: verify_outputs.py INPUT_ROM_DIR PACKAGE_ROOT")
romdir=Path(sys.argv[1]).resolve(); expected=Path(sys.argv[2]).resolve(); analyzer=expected/'GENERATION-I/RED/MULTI-REGION/REV-MIXED/analysis/scripts/analyze_roms.py'
with tempfile.TemporaryDirectory() as td:
    actual=Path(td)/'analysis'; subprocess.run([sys.executable,str(analyzer),str(romdir),str(actual)],check=True)
    def files(root):
        return {p.relative_to(root):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '/scripts/' not in p.as_posix() and p.name not in {'package-manifest.sha256','README.md','NO_ROM_BINARIES.md'}}
    a=files(actual); e=files(expected); missing=sorted(set(e)-set(a)); extra=sorted(set(a)-set(e)); changed=sorted(k for k in set(a)&set(e) if a[k]!=e[k])
    if missing or extra or changed:
        print('FAIL'); print('missing:',*[str(x) for x in missing],sep='\n  '); print('extra:',*[str(x) for x in extra],sep='\n  '); print('changed:',*[str(x) for x in changed],sep='\n  '); raise SystemExit(1)
    print(f'OK: {len(a)} generated analysis files match exactly')
