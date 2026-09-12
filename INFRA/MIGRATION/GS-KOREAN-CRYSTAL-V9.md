# GS Korean project — Crystal source identity cutover (v9)

Status: **canonical cutover** — 2026-09-13.

The GS Korean -> Pocket Monsters project uses Generation II technical release identities as canonical source owners. Crystal previously accumulated both language-label and technical-ID directories for the same bytes. New work must not fork those into separate releases.

## Canonical mapping

```text
GEN-02/CRYSTAL/SOURCE/GBC/CART/JP-JA-HV0/
  -> GEN-02/CRYSTAL/SOURCE/GBC/CART/BXTJ-HV0/

GEN-02/CRYSTAL/SOURCE/GBC/CART/US-EU-EN-HV0/
  -> GEN-02/CRYSTAL/SOURCE/GBC/CART/BYTE-HV0/

GEN-02/CRYSTAL/SOURCE/GBC/CART/US-EU-EN-HV1/
  -> GEN-02/CRYSTAL/SOURCE/GBC/CART/BYTE-HV1/
```

Canonical dump bindings:

```text
BXTJ-HV0/DUMPS/UPLOAD-95127b90
BYTE-HV0/DUMPS/UPLOAD-f4cd194b
BYTE-HV1/DUMPS/UPLOAD-f2f52230
```

## Rules

1. `BXTJ` and `BYTE` are the stable technical release identities for these Crystal builds.
2. The old language-label directories are legacy aliases/read-only compatibility paths; do not add new analysis beneath them.
3. Existing references may be migrated incrementally. Do not delete alias trees until all inbound references have been repaired and unique blobs checked.
4. A dump ID is an opaque established identity. Do not rename it merely to normalize historical `UPLOAD`, `USER-UPLOAD`, or `PROJECT` prefixes.
5. ROM binaries remain local and are never committed.
6. Project manifests must reference only the canonical technical paths after this cutover.

This migration changes ownership/routing only. It does not claim that Japanese and English texts are equivalent; each source remains an independent translation target.
