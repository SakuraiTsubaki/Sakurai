# Korean Gold/Silver layout reference — pokegold-kr

Source lock: `SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c`

This note records GSCRGBY-relevant ROM/disassembly constraints only. The NatDex expansion prototype in the source repository is not itself a GSCRGBY deliverable.

## ROM identities

| Game | Release ID | SHA-1 | Size | Banks |
| --- | --- | --- | ---: | ---: |
| Korean Gold | `AAUK-HV0` | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | 2 MiB | 128 |
| Korean Silver | `AAXK-HV0` | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` | 2 MiB | 128 |

Both use the Korean Gold/Silver MBC3-era layout represented by the `pokegold-kr` disassembly. Full ROM images remain local inputs and are not stored here.

## Gold observations useful to extraction work

The Korean Gold audit reports 24 complete 16 KiB banks containing only `00`:

```text
13 22 27 28 29 2C 2D 2F
34 35
58
63 67
6A 6B 6F
73 74 75 76 77
7C 7D 7E
```

This is 384 KiB of observed fully-zero bank space in that exact Gold image. Treat it as release-specific evidence, not a universal Gen II layout rule.

The source also confirms 8-bit-era assumptions around species indexing, `GetBaseData`, BoxMon, Pokédex, move IDs, and item IDs. For GSCRGBY these are useful when distinguishing semantic game data from engine-specific storage constraints.

## Silver observations useful to extraction work

The Silver architecture audit records:

- Japanese Silver builds: 1 MiB / 64 banks;
- international/Korean Silver builds: 2 MiB / 128 banks;
- 20 completely zero banks common to the six inspected 2 MiB international/Korean builds;
- after zero-padding the two 1 MiB Japanese builds to 2 MiB, 11 banks are empty across all eight inspected Silver images.

The common-empty-bank observations are comparison evidence. They do not authorize assuming identical offsets across versions.

## Canonical routing

Current project work lives under:

```text
CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/INPUTS/
CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/ANALYSIS/
CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/TOOLS/
```

Stable format descriptors, normalized portable data, and validated difference tables are kept in Sakurai; Tsubaki retains the complete non-ROM production/evidence superset.
