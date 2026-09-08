# PLATINUM ROM reproducibility workspace

- Game code: `CPUK`
- Revision: `0`
- ROM size: `134217728` bytes
- Source SHA-256: `51050f65776f402f86b8b2b2d3b84ab5bbe80dbec75129c86f8bd9b447f11d7b`
- FAT files: **461**
- NARC archives: **215**
- ARM9 overlays: **122**
- Exact extraction/rebuild round-trip: **PASS**

No ROM bytes or extracted copyrighted payloads are committed.

`repro_index.json.xz.b64` is the complete metadata/index set: parsed NDS header, layout, every FAT file path/offset/size/SHA-256/signature, NARC inventory, overlays, and round-trip verification. Decode it with:

```bash
base64 -d repro_index.json.xz.b64 | xz -d > repro_index.json
```

`nds_repro.py.xz.b64` is the reproducibility tool. Decode it with:

```bash
base64 -d nds_repro.py.xz.b64 | xz -d > nds_repro.py
```

Then run `analyze`, `extract`, `rebuild`, and `verify` against the original ROM. The local extraction workspace is byte-preserving and rebuilds to the source SHA-256 exactly.
