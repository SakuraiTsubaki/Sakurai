# Source-level bridge: pret/pokecrystal ↔ supplied Crystal ROMs

This workpack has two distinct reproducibility layers:

1. **Binary-forensic reproducibility for all seven supplied ROMs** — deterministic manifests, address maps, cross-version equivalence data and an exact split→reassemble roundtrip test.
2. **Assembler/source reproducibility for the two USA/Europe English revisions** — bridged to the public `pret/pokecrystal` disassembly.

## Pinned upstream reference

- Repository: `pret/pokecrystal`
- Pinned observed commit: `7a7881d0d62e0ddbd82dcf10e7116807487ac651`
- Observed commit date: 2026-08-13
- Upstream installation documentation recommends RGBDS 1.0.3.

The pin is intentional: future upstream changes must not silently alter the reconstruction baseline.

## Exact English identities

| Workpack target | Upstream build target | SHA-1 |
| --- | --- | --- |
| USA-EUROPE_REV0 | `make` → `pokecrystal.gbc` | `f4cd194bdee0d04ca4eac29e09b8e4e9d818c133` |
| USA-EUROPE_REV1 | `make crystal11` → `pokecrystal11.gbc` | `f2f52230b536214ef7c9924f483392993e226cfb` |

Those two SHA-1 values exactly match the two supplied English ROMs in this project.

Use `tools/verify_pokecrystal_bridge.py` against a checkout/build directory to verify the resulting binaries. The source repository itself is not bundled into this workpack.

## Regional reconstruction strategy

JP/DE/ES/FR/IT are kept as independent verified targets. They are **not** represented as raw ROM blobs or giant byte patches in the distributable repository.

For those versions, reconstruction proceeds by:

- using the English disassembly as the semantic map where structures are shared;
- using `same_offset_bank_equivalence.csv` and `same_offset_page_equivalence.csv` to identify byte-identical regions;
- progressively assigning ownership to code/data/text/graphics/audio/save structures;
- extracting each localized structure with a typed decoder;
- proving exact extract→reinsert or exact assembler rebuild against each target hash.

A regional target is not marked source-complete until every ROM byte has exactly one declared owner and the rebuild hash matches the verified source ROM.
