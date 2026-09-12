# ROM Binary Exclusion Policy

Canonical rule: **ROM images are the only project artifacts categorically excluded from GitHub.**

Do not commit original or modified/playable ROM images. For the currently registered Nintendo handheld corpus this includes `.gb`, `.gbc`, `.gba`, `.nds`, `.3ds`, `.cci`, `.cia`, `.xci`, and `.nsp` images/containers when they constitute game dumps or install images.

Track the work around those binaries instead: hashes, release/dump manifests, reverse-engineering notes, scripts, source, tables, CSV/JSON/YAML/Markdown, logs, comparisons, extracted/normalized assets, patches, build recipes, verification output, and reproducibility metadata.

A build directory may contain manifests and logs describing a locally produced ROM, but the playable ROM itself must remain outside Git.
