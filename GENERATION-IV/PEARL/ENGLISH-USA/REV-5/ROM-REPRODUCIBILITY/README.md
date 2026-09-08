# PEARL ROM reproducibility workspace

- Game code: `APAE`
- Revision: `5`
- ROM size: `67108864` bytes
- Source SHA-256: `2dcc471033d1757ee572415f5773a77af67b350ad59e2aeb3fc28c1402c3a84c`
- FAT files: **356**
- NARC archives: **149**
- ARM9 overlays: **87**
- Exact extraction/rebuild round-trip: **PASS**

No ROM bytes or extracted copyrighted payloads are committed.

`repro_index.json.xz.b64` is the complete metadata/index set: parsed NDS header, layout, every FAT file path/offset/size/SHA-256/signature, NARC inventory, overlays, pairwise Diamond/Pearl differences, and round-trip verification. Decode it with:

```bash
base64 -d repro_index.json.xz.b64 | xz -d > repro_index.json
```

`nds_repro.py.xz.b64` is the reproducibility tool. Decode it with:

```bash
base64 -d nds_repro.py.xz.b64 | xz -d > nds_repro.py
```

Then run `analyze`, `extract`, `rebuild`, and `verify` against the original ROM. The local extraction workspace is byte-preserving and rebuilds to the source SHA-256 exactly.
