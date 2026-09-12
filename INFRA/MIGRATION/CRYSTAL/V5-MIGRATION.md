# Pokémon Crystal migration to repository structure v5

Canonical source root: `LIBRARY/GEN-02/CRYSTAL/SOURCE/GBC/CART/`.

Seven supplied Crystal images are represented as seven release identities plus seven exact `UPLOAD-<SHA1-8>` dump observations. The old v4 root `LIBRARY/GEN-02/GBC/CRYSTAL/` is removed from the live tree; Git history retains it.

Same-game research moved from `COMPARISONS` to `LIBRARY/GEN-02/CRYSTAL/COMPARE/RELEASE-MATRIX/`. Existing research and tooling blobs are retained while release and dump identity manifests are rewritten to v5.

Original ROM binaries are never committed.
