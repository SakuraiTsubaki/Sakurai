# pokegold-kr upstream snapshot

Canonical project coordinate: `GEN-02/PROJECTS/POKEGOLD-KR/`.

Pinned upstream: `SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c`.

Pinned upstream tree: `fe50ec090dbf514da2aaa80f331ceedbb30f3197`.

The upstream builds Korean Pokémon Gold and Silver from the corresponding base ROMs. ROM images themselves are not committed to Sakurai or Tsubaki.

Under repository architecture v11, Tsubaki is the complete non-ROM superset and mirrors all 4,126 tracked upstream files at `GEN-02/PROJECTS/POKEGOLD-KR/IMPLEMENTATION/`. The import verification found zero tracked ROM files in the pinned upstream tree, so the mirrored implementation subtree is byte-for-byte tree-identical to the upstream tree.

Sakurai stores the research/control subset: release and dump identity, provenance, reverse-engineering findings, analyses, reports, schemas, and verification evidence. Any newly generated non-ROM research artifact tracked here is also expected in Tsubaki at the same semantic coordinate.
