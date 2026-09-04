# Pokémon Black/White EUR — Egg Move census

- Archive: `a/1/2/3`
- Members: **650**, indexed by species ID 0..649.
- Record format: **u16 count + count × u16 move ID**.
- Local length validation: **650/650 pass, 0 exceptions**.
- Total move-ID entries across the archive: **2,773**.
- Maximum egg moves on one species entry: **16**.
- Zero-count entries: **390 including species-ID 0 placeholder; 389 actual species entries**.

The companion `a/0/2/0` archive contains 650 × 2-byte base/baby-species mapping entries and participates in breeding-family routing.

Historical BW research independently identifies `a/1/2/3` as the Egg Move NARC and describes the leading u16 as the number of following move IDs. The complete local ROM census confirms that structure for every member.
