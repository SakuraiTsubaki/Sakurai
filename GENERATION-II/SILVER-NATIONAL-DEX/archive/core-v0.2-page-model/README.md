# Core v0.2 page-model prototype — superseded

This directory preserves the earlier working prototype that encoded battle slots as 251-entry pages and used the two BoxMon unused bytes as page/form metadata.

It is **not the current canonical ID architecture**.

The project has since adopted a future-proof design based on stable append-only 16-bit Species and Variant identities, with Egg outside the normal species namespace. These files remain useful as ROM-location research, bank-layout evidence, checksums, and a reproducible prototype of the first engine hook.

Do not treat the `251-per-page` encoding as a permanent save-format contract.

No ROM binary is included.
