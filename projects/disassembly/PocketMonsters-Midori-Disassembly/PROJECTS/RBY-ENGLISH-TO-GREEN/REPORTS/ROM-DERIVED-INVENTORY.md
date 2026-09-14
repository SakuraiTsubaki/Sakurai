# Green ROM-derived inventory for RBY ENGLISH → G

## Verified Green source pair

| Release | Dump | Size | SHA-1 | SHA-256 | Header ver. | Status |
|---|---|---:|---|---|---:|---|
| `JP-JA-HV0` | `USER-UPLOAD-82c0eef4` | 524288 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | `6576b4e0979e93d4a6fa02db893c294b7aeab3b841b1acc8658bc10b3554f33c` | 0 | PASS |
| `JP-JA-HV1` | `USER-UPLOAD-4b97cd44` | 524288 | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` | `3f0dc460ca8d06be1c9ac96307c939c0ea7baa366b40c2f1f4ad63242b6c4816` | 1 | PASS |

Both are 32 × 16 KiB banks. Original ROM binaries stay local and are not committed.

## Already canonical in Sakurai

- `GEN-01/GREEN/SOURCE/GB/CART/JP-JA-HV0/IDENTITY/release.json`
- `GEN-01/GREEN/SOURCE/GB/CART/JP-JA-HV0/DUMPS/USER-UPLOAD-82c0eef4/IDENTITY/dump.json`
- `GEN-01/GREEN/SOURCE/GB/CART/JP-JA-HV0/NATIVE/ROM/rom-observation.json`
- `GEN-01/GREEN/SOURCE/GB/CART/JP-JA-HV0/NATIVE/ROM/bank-analysis.csv`
- `GEN-01/GREEN/SOURCE/GB/CART/JP-JA-HV0/NATIVE/ROM/bank-map.json`
- equivalent `JP-JA-HV1` records
- `GEN-01/GREEN/COMPARE/JP-JA-HV0--JP-JA-HV1/ANALYSIS/revision-summary.json`
- `GEN-01/GREEN/COMPARE/JP-JA-HV0--JP-JA-HV1/DATA/bank-diff-summary.csv`
- `GEN-01/GREEN/REFERENCE/POKEGREEN-DISASSEMBLY/reference.json`

## Shared RBY English system research

Generation-wide English text engine, character-map, font/UI and relocation research remains under `GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION`. Green-specific comparison and application evidence belongs to this target.

## Production side in Tsubaki

- per-release ROM bank production indexes
- source references and source locks
- range-extraction schema and verified-range extraction tool
- per-revision implementation roots

These production artifacts are consumed by `GEN-01/GREEN/TARGET/RBY-ENGLISH-TO-GREEN` in Tsubaki. Their factual source identity remains Sakurai-owned.

## Next ROM-derived domains to populate

Green text/encoding observations, text pointers and dispatchers, maps/events/NPCs, trainers/wild/items, battle/system messages, menus/UI, name entry, Pokédex, save/link structures, graphics/tile/sprite indexes, unused/dummy text/data, and per-domain HV0↔HV1 deltas.
