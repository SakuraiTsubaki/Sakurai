# Version and Release Coordinates

Sakurai tracks identity through semantic coordinates rather than a single global version list.

A release coordinate may include:

- generation
- game ID
- platform ID
- package kind
- release ID
- region
- language
- revision/update
- dump identity
- cryptographic hashes
- provenance/source
- verification level

Canonical release ownership follows:

```text
GEN-XX/<GAME-ID>/RELEASES/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

Exact dump observations should use stable hash-derived identities where the project schema requires them. Do not invent region, language, revision, platform, package, or release values when evidence is missing; use explicit unknown/TBD fields in manifests until verified.
