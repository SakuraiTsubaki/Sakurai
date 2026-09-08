# Reproduction runbook

## 1. Place the source ROM dumps in one directory

The builder identifies ROMs by cryptographic hash; filenames are secondary. Duplicate `.gb` / `.gbc` aliases are automatically collapsed.

## 2. Build the workspace

Use the local reproducibility builder against the source ROM directory. The build uses only Python standard-library modules.

## 3. Verify the generated dataset

Expected result for this exact input set:

- 14 input filenames
- 9 byte-unique canonical ROMs
- 576 bank files
- 9/9 exact split/rebuild matches
- 8/8 exact IPS relationship rebuilds

## 4. Reconstruct a canonical ROM from its 64 private bank slices

Use `rebuild_from_banks.py` against the desired `private/banks/<ROM_ID>` directory. For `EN-US-EU_REV-0`, the result must have SHA-1 `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`.

## 5. Source-control boundary

Commit reproducibility scripts, manifests, hashes, reports and verification tables. Keep literal ROM bank slices and ROM-derived patch bytes outside public repositories.

## 6. External semantic reference

For symbol/data interpretation of the canonical English build, use the exact `pret/pokeyellow` revision recorded in `reference/pret_pokeyellow.lock.json`; do not silently follow upstream `master`.