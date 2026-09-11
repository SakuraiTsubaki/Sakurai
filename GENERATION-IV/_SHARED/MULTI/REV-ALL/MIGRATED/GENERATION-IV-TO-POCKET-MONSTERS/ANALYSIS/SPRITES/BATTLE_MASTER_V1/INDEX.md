# Generation IV Battle Sprite Master v1 — GitHub index

## Master counts

- Logical sprite records: 25,136
- Unique 64×64 target assets after SHA-256 deduplication: 11,947
- Atlas pages: 24
- `otherpoke` members inventoried: 727

## Uploaded now

- `README.md`
- `summary.json`
- `build_gen4_sprite_master.py`
- `decode_manifests.py`
- `otherpoke_unreferenced.csv`

## Present in project workspace but not yet stored in this repository through the current connector

- full `logical_slots.csv` (4,194,193 bytes)
- full `asset_index.csv` (998,573 bytes)
- full `atlas_map.csv` (306,982 bytes)
- full `otherpoke_member_inventory.csv` (66,397 bytes)
- 24 PNG atlas pages
- `gen4_battle_sprite_master_v1.zip`

The current GitHub connector exposes UTF-8 text writes but no local binary-file upload action. Binary PNG/ZIP files are therefore tracked by SHA-256 in the Tsubaki `BINARY_MANIFEST.json` rather than being falsely marked as uploaded.
