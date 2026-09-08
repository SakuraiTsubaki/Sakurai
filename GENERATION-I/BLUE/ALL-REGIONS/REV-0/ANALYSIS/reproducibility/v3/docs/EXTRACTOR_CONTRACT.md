# Extractor contract

Every future semantic extractor should expose four operations:

1. **identify** — confirm the exact compatible ROM hash/revision.
2. **extract** — emit structured editable data plus an address/source manifest.
3. **encode** — turn that structured data back into the exact encoded byte representation.
4. **verify** — reinsert the encoded bytes and prove whole-ROM SHA-256 equality.

Required metadata per extracted record: ROM code/revision; bank and CPU address; absolute file offset; encoded length; checksum where practical; semantic type; pointer/reference provenance; extractor version; verification state.

Generated raw binary assets belong under a local ignored directory. Reusable source code, manifests and non-infringing metadata belong in version control.
