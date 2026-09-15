# Verified Input Requirements

This project can prepare tooling and public-source research without proprietary inputs, but binary-level decompilation requires verified local research material.

## Per title / per revision

Preferred local research tree:

- extracted `exefs/` when available;
- extracted `romfs/`;
- locally recorded title/update identity;
- locally measured SHA-256 hashes for the source package/tree where lawful and practical;
- platform variant noted explicitly (Nintendo Switch / Nintendo Switch 2 Edition where applicable).

## Never upload to GitHub

- retail game images;
- NSP/XCI/NCA or equivalent retail/update packages;
- console keys;
- raw decrypted proprietary executables;
- raw proprietary dumps solely copied from the game.

## Commit instead

- file inventories;
- hashes and sizes;
- format descriptions;
- schemas;
- parsers and analysis tooling;
- reconstructed/decompiled source where appropriate;
- symbol/function maps;
- comparison tables;
- test fixtures that are independently created/minimal and contain no proprietary content;
- verification reports and patch metadata.

## First command chain after local input is available

```text
inventory.py <extracted-tree> -> inventory.json
structure_report.py inventory.json -> structure-report.json
compare_inventories.py old.json new.json -> revision-diff.json
```

For Scarlet/Violet, equivalent-version inventories are additionally compared across titles. For Z-A, Switch/Switch 2 Edition and DLC/update boundaries are tracked independently.
