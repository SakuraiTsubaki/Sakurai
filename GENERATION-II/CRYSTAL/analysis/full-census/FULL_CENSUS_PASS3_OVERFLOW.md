# European localization overflow-bank audit

## Exact ROM findings
- EN Rev0 and EN RevA banks `75`, `76`, `79`, `7A` are completely `0x00`.
- DE/FR/IT/ES all populate `75`, `76`, and `79`; bank `7A` remains completely zero in every international image.
- This is direct evidence that the European localizations consume extra ROM banks that are unused in English.

## Structural alignment back to English
Unique same-offset-independent 12-byte samples were searched from the European overflow banks against EN Rev0. The strongest source-bank alignments are:
- overflow `75` → EN `1A` (Map Scripts 5) and EN `26` (Map Scripts 11)
- overflow `76` → EN `27` (Map Scripts 12)
- overflow `79` → EN `66` (Map Scripts 19)

The matching samples are mostly script/control structure rather than translated prose, so they survive localization and provide strong relocation evidence. Full counts and sample offsets are in `european_overflow_alignment.csv`.

## Consequence for localization work
- Pointers must be tracked per language. A bank/address pair valid in EN is not guaranteed to identify the corresponding localized object in DE/FR/IT/ES.
- `75/76/79` cannot be treated as general free space in European builds.
- `7A` is the only whole all-zero bank shared by EN/DE/FR/IT/ES in this four-bank group; it still requires reference checks before being designated safe expansion space.
