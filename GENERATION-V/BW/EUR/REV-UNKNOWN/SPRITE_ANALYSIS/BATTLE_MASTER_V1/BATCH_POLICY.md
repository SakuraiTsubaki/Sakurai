# Small-batch publication policy

Battle-sprite assets are published in small, reviewable batches rather than as one unreviewable bulk dump.

Each batch must contain a closed validation unit:

- source-role manifest rows
- source hashes
- source reconstruction PNG(s)
- 64×64 final PNG(s)
- Generation III palette data
- Generation III 4bpp data
- Generation III compressed graphics
- final hash set
- logical-slot → canonical-asset mapping
- visual comparison/review result
- validator result

A batch may be published only when every referenced binary exists in Tsubaki and every Tsubaki asset resolves back to Sakurai provenance.

Rendered duplicates are not republished. They resolve to an existing canonical asset by final rendered-pixel SHA-256 while retaining all new logical references in the manifest.
