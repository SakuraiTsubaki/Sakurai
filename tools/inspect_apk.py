#!/usr/bin/env python3
import sys, zipfile, hashlib, struct, json
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def elf(path_bytes):
    if path_bytes[:4] != b"\x7fELF":
        return None
    cls={1:"ELF32",2:"ELF64"}.get(path_bytes[4],str(path_bytes[4]))
    machine=struct.unpack_from("<H",path_bytes,18)[0]
    return {"class":cls,"machine":machine}

def main(p):
    p=Path(p)
    out={"file":p.name,"sha256":sha256(p),"size":p.stat().st_size,"native":[]}
    with zipfile.ZipFile(p) as z:
        out["entries"]=len(z.infolist())
        for n in z.namelist():
            if n.startswith("lib/") and n.endswith(".so"):
                parts=n.split("/")
                out["native"].append({"abi":parts[1],"path":n,**(elf(z.read(n)) or {})})
        out["hasManifest"]="AndroidManifest.xml" in z.namelist()
    print(json.dumps(out,indent=2))
if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: inspect_apk.py app.apk")
    main(sys.argv[1])
