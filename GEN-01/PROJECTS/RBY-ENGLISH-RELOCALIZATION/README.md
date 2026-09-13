# RBY English Relocalization

Canonical Generation I project coordinate for re-translating and re-implementing Japanese **Pocket Monsters Red, Green, Blue, and Pikachu** in English.

Japanese ROMs are the translation originals. Existing English Red/Blue/Yellow are implementation references for font, encoding, text engine, UI, pointers, banks, and other English-support machinery; their legacy translations are not automatically authoritative.

## Repository behavior

Tsubaki is the complete non-ROM superset. Sakurai stores the knowledge/control subset. ROM binaries never enter either repository.

## Current observed corpus

12 byte-exact dumps are pinned in `PROJECT.json`: 9 Japanese translation-source revisions and 3 English implementation-reference releases.
