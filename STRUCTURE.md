# Repository Structure v8

Status: **canonical redesign candidate** — 2026-09-12.

v8 replaces the detached top-level `LIBRARY/` + `PROJECTS/` ownership model with generation/game ownership.

## 1. Canonical roots

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

Root documentation and `.github` metadata are also allowed. Top-level `LIBRARY/`, `PROJECTS/`, and `LEGACY/` are retired after cutover.

## 2. Game ownership

Every game may own exactly these semantic branches:

```text
GEN-XX/<GAME-ID>/
├── SOURCE/
├── TARGET/
├── COMPARE/
├── SHARED/
└── REFERENCE/
```

A branch is created only when content exists; empty placeholders are not required.

## 3. SOURCE grammar

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

The order is fixed:

```text
generation → game → source → platform → package/distribution → technical release identity
```

`RELEASE-ID` is the registered official release/build identity. Do **not** create extra `LANGUAGE`, `REGION`, `REV`, `BUILD`, or `VERSION` folders when those facts are already encoded by the registered release identity or manifest. They remain explicit manifest fields and may be part of the release ID where required for uniqueness.

Typical Sakurai release leaf:

```text
<RELEASE-ID>/
├── IDENTITY/
├── DUMPS/<DUMP-ID>/
├── NATIVE/
├── DOMAINS/
├── TEXT/
├── CODE/
├── MAPS/
├── TOOLS/
├── REPORTS/
└── VERIFICATION/
```

An exact dump observation never creates a fake release. Modified/bad/trimmed/overdumped/incomplete images remain dump observations under the correct release or an explicit unresolved identity record.

## 4. TARGET grammar

Single-game derived work belongs with its owner game:

```text
GEN-XX/<GAME-ID>/TARGET/<TARGET-ID>/
```

Only targets that intentionally span multiple games in one generation use:

```text
GEN-XX/TARGET/<TARGET-ID>/
```

Targets spanning generations use:

```text
CROSS-GEN/TARGET/<TARGET-ID>/
```

A target manifest locks exact source release IDs and dump IDs when required. A derived project never masquerades as `SOURCE`.

## 5. COMPARE / SHARED / REFERENCE

Same-game comparisons:

```text
GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
```

Same-generation cross-game comparisons:

```text
GEN-XX/COMPARE/<COMPARISON-ID>/
```

Cross-generation comparisons:

```text
CROSS-GEN/COMPARE/<COMPARISON-ID>/
```

`SHARED` is only for genuinely identity-independent reusable schemas, parsers, terminology maps, or equivalent resources. Byte-identical release-owned artifacts remain under each release and equality is recorded by hashes/catalogs.

`REFERENCE` contains external or secondary sources and never overrides facts observed from official software.

## 6. CROSS-GEN

```text
CROSS-GEN/
├── TARGET/
├── COMPARE/
├── SHARED/
└── REFERENCE/
```

No game-local source release is stored here.

## 7. INFRA and quarantine

Repository-wide architecture, registries, schemas, validators, migration maps, and generic tooling belong under `INFRA/`.

Pre-v8 unique or not-yet-semantic-migrated material may remain read-only under:

```text
INFRA/QUARANTINE/PRE-V8/
```

Quarantine is never a destination for new work. Git history is the permanent archive.

## 8. Repository pair invariant

Sakurai and Tsubaki use identical values for:

- generation ID
- game ID
- platform ID
- package kind
- release ID
- dump ID
- target ID
- comparison ID
- reference/resource ID

Sakurai owns identity/research/specification/verification. Tsubaki owns verified production assets/conversions/implementation/patch/build outputs.

## 9. Forbidden canonical labels

Outside quarantine, new canonical paths must not introduce ambiguous ownership labels such as:

```text
MULTI
REV-ALL
ALL
ALL-RELEASES
MULTI-REGION
_SHARED
MISC
OTHER
GENERAL
REV-UNKNOWN
MIGRATED
```

Unknown facts are manifest state, not directory identities.

## 10. Routing examples

```text
GEN-01/GREEN/TARGET/GREEN-MODERNIZATION/
GEN-02/SILVER/TARGET/SILVER-MODERNIZATION/
GEN-03/FIRERED/TARGET/FIRERED-MODERNIZATION/
GEN-03/LEAFGREEN/TARGET/LEAFGREEN-PAST-PARADOX-001-386/
GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/
CROSS-GEN/TARGET/<CROSS-GENERATION-PROJECT>/
```
