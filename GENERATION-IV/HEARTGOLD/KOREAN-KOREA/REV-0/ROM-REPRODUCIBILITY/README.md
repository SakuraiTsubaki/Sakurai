# HEARTGOLD ROM reproducibility workspace

- Game code: `IPKK`
- Revision: `0`
- ROM size: `134217728` bytes
- Source SHA-256: `659f20ca1d4f43b8b675d3c47217bb875a4f14c62438b08fa42f60467e2bed43`
- FAT files: **511**
- NARC archives: **308**
- ARM9 overlays: **129**
- Exact extraction/rebuild round-trip: **PASS**

No ROM bytes or extracted copyrighted payloads are committed.

`repro_index.json.xz.b64` is the complete metadata/index set: parsed NDS header, layout, every FAT file path/offset/size/SHA-256/signature, NARC inventory, overlays, pairwise HeartGold/SoulSilver differences, and round-trip verification. Decode it with:

```bash
base64 -d repro_index.json.xz.b64 | xz -d > repro_index.json
```

`nds_repro.py.xz.b64` is the reproducibility tool. Decode it with:

```bash
base64 -d nds_repro.py.xz.b64 | xz -d > nds_repro.py
```

Then run `analyze`, `extract`, `rebuild`, and `verify` against the original ROM. The local extraction workspace is byte-preserving and rebuilds to the source SHA-256 exactly.
