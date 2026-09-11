# Generation IV Battle Sprite Master v1 — GitHub text index

This directory mirrors the full local master metadata. Large manifests are split only to satisfy GitHub Contents API size limits; no logical scope is intentionally omitted.

## Master counts

- Logical sprite records: 25,136
- Unique 64×64 target assets after SHA-256 deduplication: 11,947
- Atlas pages: 24
- `otherpoke` members inventoried: 727

## Text artifacts

- `summary.json`
- `build_gen4_sprite_master.py`
- `logical_slots_compact_part_01.tsv` … `logical_slots_compact_part_03.tsv`
- `asset_index_part_01.csv` … `asset_index_part_02.csv`
- `atlas_map.csv`
- `otherpoke_member_inventory.csv`

The binary PNG atlas pages and ZIP master are not converted into fake text files. The current GitHub connector can write UTF-8 text only, so binary assets remain in the project workspace until a binary-capable repository upload path is available.
