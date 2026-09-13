# Ruby migration to repository architecture v11

Canonical release data: `GEN-03/RUBY/RELEASES/GBA-AGB/CART/<RELEASE-ID>/`.

Legacy `GEN-03/RUBY/SOURCE/GBA/...` and `GEN-03/RUBY/SOURCE/GBA-AGB/...` are migration-only. Known mappings include `SOURCE/GBA-AGB/CART/AXVJ-HV0/` → `RELEASES/GBA-AGB/CART/AXVJ-HV0/` and `SOURCE/GBA-AGB/CART/AXVE-HV2/` → `RELEASES/GBA-AGB/CART/AXVE-HV2/`.

New dump IDs use `DUMP-SHA256-<first-16-uppercase-hex>`. Keep legacy files until their non-ROM contents are reclassified and verified; never migrate the ROM image itself.
