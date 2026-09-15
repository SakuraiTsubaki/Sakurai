# BW EUR `/a/0/0/4` battle archive inventory — first verified pass

This file records the first direct inventory pass against the uploaded read-only EUR Pokémon Black/White ROM sources.

## Source identity

| Field | Black | White |
|---|---:|---:|
| Game code | `IRBO` | `IRAO` |
| Header ROM version | `0` | `0` |
| ROM size | `268435456` bytes | `268435456` bytes |
| ROM SHA-256 | `2e40416b8e8183d936084c7be0adeaab4fa3f786a68f90d7291ab77d340f0c1d` | `93e4f473ce9a0543bccf2e689ecd07ab4fcc39dd00fb4f194343cbd5e70e17ed` |
| `/a/0/0/4` file ID | `246` | `246` |
| `/a/0/0/4` ROM offset | `59650560` | `59650560` |
| archive size | `7889304` bytes | `7889304` bytes |
| archive SHA-256 | `0ef9595f7924f533985515f159c35bdb8fd8015ef50bef2a2f0e08219ed3487e` | same |
| NARC members | `14285` | `14285` |

The complete Black and White `/a/0/0/4` archives are byte-identical in these two supplied EUR ROMs. Black and White nevertheless remain separate logical game identities in provenance and slot manifests.

## Standard block arithmetic

`14285 = 714 × 20 + 5`.

The archive therefore contains 714 complete 20-member blocks plus 5 trailing members. This arithmetic is only a structural fact; block-to-species/form identity and the semantics of the 5 tail members must be proven separately rather than inferred solely from position.

## Decoded Nitro resource census

The first pass decodes Nintendo LZ-compressed members where valid and classifies the resulting resources. The major resource counts are:

| Decoded resource | Count |
|---|---:|
| NCGR | 3234 |
| NCLR | 1457 |
| NCER | 1426 |
| NANR | 1426 |
| NMCR | 1426 |
| NMAR | 1426 |
| empty members | 2464 |

The remaining auxiliary members include small non-Nitro-header records and compressed/auxiliary records. They are retained for later semantic resolution and must not be discarded as junk merely because their type is not yet named.

## Verified source canvas families

Direct NCGR header inspection shows two dominant dimensions:

- static battle NCGRs: `96×96` source canvas
- multipart animated-parts NCGRs: `256×128` raw source canvas

These observations match the active BATTLE_MASTER_V1 split: dedicated static NCGRs feed the Generation III 64×64 static insertion master, while multipart animation resources are preserved independently.

## Current conclusions

- The historical directory label `REV-UNKNOWN` must not be used as a substitute for source provenance; both supplied source headers explicitly report version byte `0`.
- `/a/0/0/4` is shared byte-for-byte between the supplied EUR Black and White ROMs.
- Deduplication may therefore share canonical extracted/converted assets, but logical Black/White references must remain distinct.
- All 14285 members remain in scope, including empty slots, auxiliary records, complete 20-member blocks, and the 5 trailing members.
- No National Dex-only truncation is allowed.

## Next inventory gates

The next verified passes must resolve:

1. every 20-member block to species/form/logical role;
2. all female-empty/shared alias behavior;
3. the 5 trailing members;
4. every auxiliary `+8/+17` record type and semantics;
5. exact normal/shiny palette associations;
6. source-index rendering and Generation III 64×64 conversion for every static logical role;
7. full source/intermediate/final SHA-256 chain and global rendered-pixel dedup mapping.
