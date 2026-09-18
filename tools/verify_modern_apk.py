#!/usr/bin/env python3
import argparse
import json
import struct
import zipfile
from pathlib import Path

PT_LOAD = 1
EM_AARCH64 = 183

def elf_info(data: bytes):
    if len(data) < 64 or data[:4] != b"\x7fELF":
        return None
    cls = data[4]
    endian = data[5]
    if endian == 1:
        e = "<"
    elif endian == 2:
        e = ">"
    else:
        return None
    machine = struct.unpack_from(e + "H", data, 18)[0]
    if cls == 2:
        phoff = struct.unpack_from(e + "Q", data, 32)[0]
        phentsize = struct.unpack_from(e + "H", data, 54)[0]
        phnum = struct.unpack_from(e + "H", data, 56)[0]
        align_off = 48
        align_fmt = "Q"
    elif cls == 1:
        phoff = struct.unpack_from(e + "I", data, 28)[0]
        phentsize = struct.unpack_from(e + "H", data, 42)[0]
        phnum = struct.unpack_from(e + "H", data, 44)[0]
        align_off = 28
        align_fmt = "I"
    else:
        return None

    loads = []
    for n in range(phnum):
        off = phoff + n * phentsize
        if off + phentsize > len(data):
            break
        p_type = struct.unpack_from(e + "I", data, off)[0]
        if p_type == PT_LOAD:
            align = struct.unpack_from(e + align_fmt, data, off + align_off)[0]
            loads.append(align)
    return {
        "class": 64 if cls == 2 else 32,
        "machine": machine,
        "load_alignments": loads,
        "min_load_alignment": min(loads) if loads else None,
    }

def zip_data_offset(fp, info: zipfile.ZipInfo):
    fp.seek(info.header_offset)
    header = fp.read(30)
    if len(header) != 30 or header[:4] != b"PK\x03\x04":
        return None
    name_len, extra_len = struct.unpack_from("<HH", header, 26)
    return info.header_offset + 30 + name_len + extra_len

def main():
    ap = argparse.ArgumentParser(description="Check ARM64 + 16 KiB native-library compatibility in an APK")
    ap.add_argument("apk")
    ap.add_argument("--require-arm64", action="store_true")
    ap.add_argument("--require-16k", action="store_true")
    args = ap.parse_args()

    apk = Path(args.apk)
    report = {"apk": str(apk), "libraries": [], "ok": True, "notes": []}
    arm64_count = 0

    with apk.open("rb") as raw, zipfile.ZipFile(raw) as z:
        for info in z.infolist():
            if not (info.filename.startswith("lib/") and info.filename.endswith(".so")):
                continue
            parts = info.filename.split("/")
            abi = parts[1] if len(parts) > 2 else "?"
            data = z.read(info)
            elf = elf_info(data)
            row = {
                "path": info.filename,
                "abi": abi,
                "compression": "stored" if info.compress_type == zipfile.ZIP_STORED else "compressed",
                "zip_data_offset": zip_data_offset(raw, info),
                "elf": elf,
            }
            if abi == "arm64-v8a":
                arm64_count += 1
                if not elf or elf["class"] != 64 or elf["machine"] != EM_AARCH64:
                    row["error"] = "arm64-v8a entry is not ELF64 AArch64"
                    report["ok"] = False
                if args.require_16k and (not elf or not elf["load_alignments"] or any(a < 0x4000 for a in elf["load_alignments"])):
                    row["error"] = "PT_LOAD alignment is below 16 KiB"
                    report["ok"] = False
                if info.compress_type == zipfile.ZIP_STORED:
                    off = row["zip_data_offset"]
                    row["zip_16k_aligned"] = (off is not None and off % 0x4000 == 0)
                    if args.require_16k and not row["zip_16k_aligned"]:
                        row["warning"] = "uncompressed .so is not 16 KiB ZIP-aligned"
                        report["ok"] = False
            report["libraries"].append(row)

    if args.require_arm64 and arm64_count == 0:
        report["ok"] = False
        report["notes"].append("No lib/arm64-v8a/*.so found")

    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["ok"] else 1)

if __name__ == "__main__":
    main()
