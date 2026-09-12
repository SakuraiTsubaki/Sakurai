# Repository Structure v9

Status: **canonical redesign candidate** — 2026-09-13.

v9 keeps generation/game ownership from v8, but makes the Sakurai/Tsubaki split explicit at every target leaf and defines one ROM-ingest rule for both repositories.

## 1. Canonical roots

```text
GEN-XX/
CROSS-GEN/
INFRA/
```

Root documentation and `.github` metadata are allowed. Historical roots such as `GENERATION-*`, `LIBRARY/`, `PROJECTS/`, and `LEGACY/` are non-canonical and must migrate or remain read-only under quarantine.

## 2. Pair roles

The repository pair shares the same IDs and semantic owner, but not the same payload.

- **Sakurai**: identity, provenance, research, specifications, mappings, reference metadata, and verification criteria/evidence.
- **Tsubaki**: production tooling, conversion logic, implementation, patch payloads, build recipes, generated manifests/reports, and reproducible build outputs that are safe to redistribute.
- **Local-only**: original ROM images, complete patched ROM images, and substantial extracted proprietary game content.

A private repository is not used as a substitute for a local ROM vault.

## 3. Source release ownership

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

`RELEASE-ID` is the registered official release/build identity. Language, region, revision, build, and version are manifest fields and appear in the ID only when needed for uniqueness.

Typical Sakurai source leaf:

```text
<RELEASE-ID>/
├── IDENTITY/
├── MANIFESTS/
├── DUMPS/<DUMP-ID>/          # hashes/metadata/observations, never ROM bytes
├── DOMAINS/
├── TEXT/
├── CODE/
├── MAPS/
├── RESEARCH/
├── REFERENCE/
└── VERIFICATION/
```

## 4. Target ownership

Single-game target:

```text
GEN-XX/<GAME-ID>/TARGET/<TARGET-ID>/
```

Same-generation multi-game target:

```text
GEN-XX/TARGET/<TARGET-ID>/
```

Cross-generation target:

```text
CROSS-GEN/TARGET/<TARGET-ID>/
```

A target that consumes Gen I and produces Gen II-compatible work is therefore `CROSS-GEN`, even when its geographic scope is only Kanto.

Typical **Sakurai** target leaf:

```text
<TARGET-ID>/
├── README.md
├── MANIFESTS/
├── SPEC/
├── MAPPING/
├── RESEARCH/
├── REFERENCE/
└── VERIFICATION/
```

Implementation code, patch payloads, staging assets, and build products belong in the matching Tsubaki target, not here.

## 5. COMPARE / SHARED / REFERENCE

Same-game comparison:

```text
GEN-XX/<GAME-ID>/COMPARE/<COMPARISON-ID>/
```

Same-generation cross-game comparison:

```text
GEN-XX/COMPARE/<COMPARISON-ID>/
```

Cross-generation comparison:

```text
CROSS-GEN/COMPARE/<COMPARISON-ID>/
```

`SHARED` is only for identity-independent reusable schemas, terminology maps, parsers, or equivalent resources. Release-owned facts remain with their semantic owner.

## 6. Infrastructure

Repository-wide registries, schemas, validators, routing rules, and migration maps belong under `INFRA/`.

```text
INFRA/
├── REGISTRY/
├── SCHEMAS/
├── ROUTING/
├── VALIDATION/
├── MIGRATION/
└── QUARANTINE/PRE-V9/
```

Quarantine is read-only and receives no new production work.

## 7. ROM-ingest invariant

Original images are never committed. The tracked handoff is:

```text
local ROM
  → identity/hash verification
  → Sakurai manifest/spec/mapping
  → Tsubaki extractor/converter/implementation
  → redistributable patch + verification report
```

See `INFRA/ROUTING/ROM-INGEST.md`.

## 8. Registered cross-generation target

The current project is registered as:

```text
CROSS-GEN/TARGET/RGBY-KANTO-TO-GSC/
```

This ID is identical in Sakurai and Tsubaki.

## 9. Forbidden canonical labels

Outside quarantine, do not create ambiguous owner IDs such as:

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

Unknown facts are manifest state, not directory identity.
