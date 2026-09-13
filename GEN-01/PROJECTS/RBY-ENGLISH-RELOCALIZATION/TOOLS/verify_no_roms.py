#!/usr/bin/env python3
import sys
from pathlib import Path
F={'.gb','.gbc','.gba','.nds','.3ds','.cia','.xci','.nsp','.sfc','.smc','.iso','.rvz','.wbfs'}
r=Path(sys.argv[1] if len(sys.argv)>1 else '.');bad=[p for p in r.rglob('*') if p.is_file() and p.suffix.lower() in F]
for p in bad:print(p)
raise SystemExit(bool(bad))
