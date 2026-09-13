# Repository Migration — v11

Status: **active cutover** — 2026-09-13.

v11 is canonical. It keeps release-centric, content-addressed dump identity and makes Tsubaki the complete non-ROM project superset.

## Path mapping

```text
GEN-XX/<GAME>/SOURCE/<PLATFORM>/<PACKAGE>/<RELEASE>/...
  → GEN-XX/<GAME>/RELEASES/<PLATFORM>/<PACKAGE>/<RELEASE>/...
GEN-XX/<GAME>/TARGET/<PROJECT-ID>/...
  → GEN-XX/<GAME>/PROJECTS/<PROJECT-ID>/...
GEN-XX/<GAME>/COMPARE/<COMPARE-ID>/...
  → GEN-XX/<GAME>/COMPARES/<COMPARE-ID>/...
GEN-XX/<GAME>/REFERENCE/<REFERENCE-ID>/...
  → GEN-XX/<GAME>/REFERENCES/<REFERENCE-ID>/...
```

## Cutover rules

1. Do not create new legacy ownership roots.
2. Register ROM observations under `RELEASES/.../DUMPS/DUMP-SHA256-<16HEX>` without ROM bytes.
3. Reattach verified existing Git objects under canonical coordinates before removing legacy paths.
4. Keep legacy paths read-only until references and CI consumers have been checked.
5. Tsubaki receives all new non-ROM artifacts; Sakurai receives the research/control subset.
6. Keep pair IDs and shared relative paths identical across repositories.
7. Never commit an original, modified, rebuilt, patched, or otherwise playable ROM image, nor a lossless whole-ROM chunk decomposition.

Detailed rules: [INFRA/ARCHITECTURE/MIGRATION-V11.md](INFRA/ARCHITECTURE/MIGRATION-V11.md).
