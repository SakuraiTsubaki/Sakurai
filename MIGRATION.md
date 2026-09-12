# Repository Migration — v5

## Status

v5 is canonical. No new work may be written to legacy `GENERATION-*`, standalone `GEN-*`, `GAMES/`, v4 `LIBRARY/GEN-XX/<PLATFORM>/<GAME>/RELEASES/...`, `_SHARED`, `MULTI`, `REV-ALL`, `ALL`, `MULTI-REGION`, `MISC`, `OTHER`, `GENERAL`, or `REV-UNKNOWN` paths.

Canonical source ownership:

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/...
```

Same-game comparisons:

```text
LIBRARY/GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/...
```

Cross-game generation comparisons:

```text
LIBRARY/GEN-XX/COMPARE/<COMPARISON-ID>/...
```

Derived work:

```text
PROJECTS/<PROJECT-ID>/...
```

## Classification before moving

Every legacy file is classified by meaning before relocation:

- official source-release fact -> `SOURCE/<PLATFORM>/<PACKAGE>/<RELEASE>/`
- exact supplied/observed dump fact -> `.../<RELEASE>/DUMPS/<DUMP-ID>/`
- native ROM structure research -> `.../<RELEASE>/NATIVE/`
- normalized game-domain research -> `.../<RELEASE>/DOMAINS/`
- same-game release relationship -> `<GAME>/COMPARE/`
- cross-game relationship -> `GEN-XX/COMPARE/`
- truly identity-independent material -> `SHARED/`
- external/secondary material -> `REFERENCE/`
- port/integration/modernization/localization/rebuild -> `PROJECTS/`
- repository-wide schema/registry/validator -> `INFRA/`

Do not bulk-rename mixed legacy trees.

## Generation V current source migration

v4 Black:

```text
LIBRARY/GEN-05/NDS/BLACK/RELEASES/IRBO-R0/
```

becomes:

```text
LIBRARY/GEN-05/BLACK/SOURCE/NDS-TWL/CART/IRBO-HV0/
```

v4 White:

```text
LIBRARY/GEN-05/NDS/WHITE/RELEASES/IRAO-R0/
```

becomes:

```text
LIBRARY/GEN-05/WHITE/SOURCE/NDS-TWL/CART/IRAO-HV0/
```

Dump IDs are preserved:

```text
SWEETNDS-a68b3bed
SWEETNDS-f94d4578
```

The old comparison:

```text
LIBRARY/GEN-05/NDS/_SHARED/COMPARISONS/BLACK-IRBO-R0--WHITE-IRAO-R0/
```

becomes:

```text
LIBRARY/GEN-05/COMPARE/BLACK-IRBO-HV0--WHITE-IRAO-HV0/
```

No `_SHARED` pseudo-game remains.

## Native-vs-domain split

ROM-physical observations must be separated from semantic interpretation during migration.

Examples:

```text
header fields / ARM binaries / overlays / FNT / FAT / NitroFS / NARC path maps
-> NATIVE/

Pokemon / moves / maps / trainers / text / events / graphics meaning / unused content / bugs
-> DOMAINS/
```

A raw path such as `a/0/2/6` stays a native identifier even when research associates it with a semantic role. `DOMAINS` links back to the raw path; it does not rename away the source identity.

## SweeTnDs safety rule

The current Black/White SweeTnDs images are dump observations with an external bad/incomplete preservation classification. During migration:

1. preserve exact hashes and provenance;
2. keep TWL/DSi-sensitive conclusions dump-scoped;
3. promote only conclusions verified to be safe at release level;
4. revalidate TWL-specific structure against a verified full clean dump when available;
5. never create a fake release merely to represent a bad dump.

## Dedup rule

Black/White contain both heavy sharing and heavy executable divergence. Identical files stay owned by their releases and are recorded as equal in comparison indexes. Do not physically relocate them into `SHARED` just because their hashes match.

`SHARED` is for identity-independent schemas/tools/terminology, not a dumping ground for duplicate assets.

## Project migration

Cross-generation work remains project-owned:

```text
PROJECTS/GEN5-TO-POCKET-MONSTERS/
├── MANIFESTS/
├── CROSSWALK/
├── DESIGN/
├── IMPLEMENTATION/
├── PATCHES/
├── BUILD/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

Project release locks must be rewritten to the new v5 canonical source paths before old live paths are deleted.

## Migration order

1. Freeze all legacy and v4 source paths for new writes.
2. Register v5 release identities and dump identities.
3. Create v5 Generation V Black/White source roots.
4. Copy identity and dump manifests first; verify all hashes.
5. Split ROM-native material into `NATIVE` and semantic research into `DOMAINS`.
6. Move Black/White relationship material to generation-level `COMPARE`.
7. Rewrite project release locks and internal references.
8. Migrate remaining generations using the same platform/package/release grammar.
9. Verify file counts, hashes, links, and project target bindings.
10. Add CI/path validation for v5 and reject new legacy names.
11. Remove obsolete live copies only after equivalence checks pass; Git history remains the archive.

## Non-destructive invariant

A redesign is not permission to destroy provenance. Until the equivalence check for a legacy tree passes, keep it frozen and readable. Delete only redundant live copies after the v5 owner and references are verified.