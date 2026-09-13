#!/usr/bin/env python3
"""Generate non-ROM observation/catalog artifacts from a local GB/GBC/GBA image.
The input ROM remains local and is never copied to the output tree.
"""
import argparse, hashlib, json, math, zlib
from pathlib import Path

def entropy(data):
    if not data: return 0.0
    counts = [0] * 256
    for b in data: counts[b] += 1
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in counts if c)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('rom')
    p.add_argument('--chunk-size', type=lambda x:int(x,0), required=True)
    a = p.parse_args()
    data = Path(a.rom).read_bytes()
    print(json.dumps({'size':len(data),'md5':hashlib.md5(data).hexdigest(),'sha1':hashlib.sha1(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest()}, sort_keys=True))
    for i in range(0, len(data), a.chunk_size):
        c=data[i:i+a.chunk_size]
        print(json.dumps({'index':i//a.chunk_size,'offset':i,'size':len(c),'sha256':hashlib.sha256(c).hexdigest(),'crc32':f'{zlib.crc32(c)&0xffffffff:08x}','entropy':round(entropy(c),6)}, sort_keys=True))
if __name__=='__main__': main()
