# GREEN path migration to v11

The canonical GREEN layout follows repository structure v11.

- `SOURCE/GB/CART/<RELEASE>` → `RELEASES/GB/CART/<RELEASE>/DUMPS/<content-addressed DUMP-ID>/...`
- `COMPARE/<scope>` → `COMPARES/<scope>`
- `TARGET/<project>` → `PROJECTS/<project>`
- `REFERENCE/<reference>` → `KNOWLEDGE/REFERENCES/<reference>`
- exact pre-v11 trees are retained under `KNOWLEDGE/LEGACY-V10/` for provenance and migration audit.

Canonical dump IDs:

- JP-JA-HV0: `DUMP-SHA256-6576B4E0979E93D4`
- JP-JA-HV1: `DUMP-SHA256-3F0DC460CA8D06BE`

The legacy top-level `SOURCE`, `COMPARE`, `TARGET`, and `REFERENCE` roots are retired after their content is attached to canonical v11 coordinates or retained under `KNOWLEDGE/LEGACY-V10`. Original and modified playable ROM images are not committed.
