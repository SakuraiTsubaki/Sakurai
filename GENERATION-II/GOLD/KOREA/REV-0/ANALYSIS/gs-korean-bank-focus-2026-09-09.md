# GS Korean Bank Focus — Verified and Structural Evidence

Date: 2026-09-09

This supplements the exhaustive 16 KiB survey. Semantic labels are only assigned where previous direct GS Korean extraction/reassembly already verified the role. All other banks remain unlabeled until code/pointer/reference tracing is complete.

## Verified Korean-resource banks

| Bank | Verified role | KR Gold/Silver exact? | EN Gold at same bank | JP Gold bank exists? |
|---:|---|:---:|---|:---:|
| `$68` | Pokédex description text | no | populated | no |
| `$69` | Pokédex description text | no | populated | no |
| `$6C` | Korean name/string tables | yes | populated | no |
| `$78` | Hangul table/font resource block | yes | whole-bank `00` fill | no |
| `$79` | Hangul table/font resource block | yes | whole-bank `00` fill | no |
| `$7A` | Hangul table/font resource block | yes | whole-bank `00` fill | no |

## Evidence

- `$68–$69`: previously extracted as Pokédex description text banks.
- `$6C`: previous lossless extraction/reassembly verified 830 records: item names 256, trainer-class names 67, Pokémon-name slots 256, move names 251.
- `$78–$7A`: previous Hangul-resource work verified the block containing 11 Hangul tables and 2,419 two-byte codes. The block is populated and byte-identical in Korean Gold/Silver.
- EN Gold/Silver banks `$78–$7A` are complete `00` fill banks in the present binaries.
- JP Gold/Silver are 1 MiB ROMs and end at bank `$3F`, so `$78–$7A` do not exist there.

The `$78–$7A` pattern is therefore especially strong evidence of Korean-specific use of the expanded 2 MiB address space.

## Gold/Silver relationship

Korean Gold and Silver share 92 of 128 physical banks byte-for-byte. Their 36 changed aligned bank indices contain 264,639 differing bytes. The most changed aligned bank is `$15` with 16,160 differing bytes.

The large common-bank set is useful for isolating shared Korean implementation code/data from version-specific game content.

## Safety rule

A whole-bank `00`/`FF` result or long fill run is only a relocation-space candidate. It is not approved free space until cross-bank bank-switch, direct/far pointer, call/jump, table and resource reference tracing shows it to be unreferenced.
