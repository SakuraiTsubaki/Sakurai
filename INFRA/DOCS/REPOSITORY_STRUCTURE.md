# Repository Structure

`/STRUCTURE.md` is the authoritative canonical architecture. This document explains where the Decompilation-style operating layer lives without changing that model.

```text
README.md
STRUCTURE.md
CONTRIBUTING.md
.editorconfig
.gitattributes
.github/
GEN-XX/
CROSS-GEN/
INFRA/
├── DOCS/          repository-wide documentation hub
└── MANIFESTS/     repository-wide manifest conventions/examples
```

Project/release/comparison/reference material must continue to live at its truthful canonical owner path under the v12 model. `INFRA/DOCS` and `INFRA/MANIFESTS` are repository-wide operating metadata, not alternate project ownership roots.

Do not create empty directory trees solely for symmetry with other repositories.
