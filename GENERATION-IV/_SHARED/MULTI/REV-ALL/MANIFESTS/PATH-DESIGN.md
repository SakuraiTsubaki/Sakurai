# Generation IV Path Design

## Ownership rule

Generation IV uses the repository-wide canonical path:

`GENERATION-IV / GAME / LANGUAGE-REGION / REV / WORK-TYPE / SUBJECT...`

The first five levels express ownership. Everything after WORK TYPE expresses only the technical subject.

## Game ownership

Use `DIAMOND`, `PEARL`, `PLATINUM`, `HEARTGOLD`, or `SOULSILVER` when a result belongs to one title. Use `_SHARED` only for a result that intentionally compares or models multiple Generation IV titles.

Examples:

- Diamond US Rev 5 ROM identity: `DIAMOND/US-EN/REV-5/MANIFESTS/ROM-IDENTITY.md`
- Platinum Korean Rev 0 archive analysis: `PLATINUM/KR-KO/REV-0/STRUCTURE/ARCHIVES/...`
- Diamond/Pearl US Rev 5 comparison: `_SHARED/US-EN/REV-5/DIFFS/DIAMOND-PEARL/...`
- five-ROM census spanning US and Korean builds: `_SHARED/MULTI/REV-ALL/...`

## Work-type routing

- `MANIFESTS`: hashes, ROM identity, provenance
- `STRUCTURE`: NitroFS, NARC, record layouts, capacity and limits
- `DATA`: decoded normalized game records and semantic maps
- `DIFFS`: game/version/locale/revision comparisons
- `CENSUS`: unused/dummy/reserved/bug inventory
- `REPORTS`: phase reports and status summaries
- `ANALYSIS`: interpretive/system/cross-generation research that is not better represented by a narrower type
- `VERIFICATION`: validation and reproducibility outputs
- `TOOLS`: analysis scripts
- `MAPS`, `TEXT`, `SYMBOLS`, `DISASSEMBLY`, `LOCALIZATION`, `TESTS`: use directly when applicable

## Phase migration

Phase history is preserved in report filenames or secondary subject folders. It is not a structural owner.

- Phase 1 filesystem material → `STRUCTURE/FILESYSTEM`, `DIFFS/FILESYSTEM`, `VERIFICATION/ROM-AUDIT`, `TOOLS/NDS`
- Phase 2 semantic map → `DATA/SEMANTIC-MAP`, with unused findings in `CENSUS/UNUSED` and version comparisons in `DIFFS`
- Phase 3 record decode → `DATA/RECORDS`, `DIFFS/ENCOUNTERS`, `CENSUS/UNUSED`, with the narrative report in `REPORTS/PHASES`
- Phase 4 and later follow the same rule: put each artifact in its semantic owner rather than creating `PHASE-4` as a mixed bucket.

## Cross-generation material

Cross-generation studies use `ANALYSIS/CROSS-GENERATION/<SUBJECT>`. The subject folder is descriptive only; source/target generation, game, locale, revision and hashes belong in a manifest. Implementation artifacts should eventually be owned by their actual target game where a single target exists.

## Removed legacy patterns

The following are not live Generation IV path structures after semantic normalization:

- `DPPt-HGSS/MULTI-REGION/REV-MIXED/ANALYSIS`
- `DIAMOND-PEARL/USA/REV-UNKNOWN/ANALYSIS`
- `GENERATION-IV-TO-POCKET-MONSTERS/MULTI-REGION/MULTI-REV/ANALYSIS`
- `ANALYSIS/KOREA/...`
- `ANALYSIS/KO-KR/...`
- `SOURCE/LEGACY-PLATINUM/KOREA/REV-0/...`

Their historical spellings remain available in Git history; they are not duplicated in the current tree.

## Phase 4 continuation

Generation IV relational world mapping continues semantically as:

- shared normalized identifiers/record relations → `_SHARED/MULTI/REV-ALL/DATA/RELATIONAL-MAP/`
- per-game map headers and map linkage → each game/locale/revision under `MAPS/`
- cross-game map/encounter differences → `_SHARED/MULTI/REV-ALL/DIFFS/MAPS/` and `DIFFS/ENCOUNTERS/`
- unused/unreachable maps, events or records → `_SHARED/MULTI/REV-ALL/CENSUS/UNUSED/`
- Phase 4 narrative status/report → `_SHARED/MULTI/REV-ALL/REPORTS/PHASES/`
