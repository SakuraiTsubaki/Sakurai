# Pokémon Silver supplied-ROM comparison

Generated from the eight project source ROM images; original ROM binaries are not committed.

- All eight pass Game Boy header and global checksums.
- JP HV0/HV1 are 1 MiB (64 × 16 KiB); Western/Korean supplied images are 2 MiB (128 banks).
- Korean HV0 is CGB-only (`0xC0`) with SGB disabled (`0x00`); the others use CGB-enhanced `0x80` and SGB `0x03`.
- JP HV0 vs HV1: 48/64 same-offset banks identical; 19,150/1,048,576 bytes differ (1.826286%).
- US/EU EN HV0 vs KR HV0: 29/128 same-offset banks identical; 882,326/2,097,152 bytes differ (42.072582%).

These are dump-level observations and do not by themselves prove source-code lineage.
