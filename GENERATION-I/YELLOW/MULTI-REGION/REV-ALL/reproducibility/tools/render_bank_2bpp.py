#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import sys
if len(sys.argv)<3: raise SystemExit('usage: render_bank_2bpp.py bank.bin out.png')
b=Path(sys.argv[1]).read_bytes(); tiles=len(b)//16; cols=32; rows=(tiles+cols-1)//cols
im=Image.new('L',(cols*8,rows*8),255); p=im.load(); shades=(255,170,85,0)
for t in range(tiles):
 d=b[t*16:t*16+16]; x0=(t%cols)*8; y0=(t//cols)*8
 for y in range(8):
  lo,hi=d[y*2:y*2+2]
  for x in range(8):
   bit=7-x; p[x0+x,y0+y]=shades[((lo>>bit)&1)|(((hi>>bit)&1)<<1)]
im.save(sys.argv[2])
