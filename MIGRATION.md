# Repository Migration

## Status

Canonical migration is complete.

The repository follows:

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

Legacy bundle names, locale aliases, revision aliases, and temporary `MIGRATED` compatibility buckets have been promoted into canonical paths. Where an old bundle cannot be truthfully reduced to one game, locale, or revision, its provenance label is retained below an allowed WORK TYPE such as `ANALYSIS`, `LOCALIZATION`, `DIFFS`, or `SOURCE` rather than being used as a structural level.

`MIGRATED` is forbidden for new and existing canonical paths. The repository structural validator enforces this rule.

Git history remains available for historical path recovery; migration changes the current tree, not past commits.
