# LeafGreen v4 migration and repository split

Status: canonical for LeafGreen. **v4.1 ownership extension active** via `INFRA/ROUTING/LEAFGREEN-REPOSITORY-SPLIT-v4.1.md` and `INFRA/ROUTING/LEAFGREEN-ARTIFACT-OWNERSHIP.json`.

## Canonical source root
`LIBRARY/GEN-03/GBA/LEAFGREEN/`

Official builds are releases, exact supplied files are dumps. The seven current releases are `BPGJ-R0`, `BPGE-R0`, `BPGE-R1`, `BPGD-R0`, `BPGF-R0`, `BPGI-R0`, and `BPGS-R0`.

## Replace legacy owners
Legacy paths containing `GENERATION-III/LEAFGREEN`, standalone `GEN-03/LEAFGREEN`, `GAMES/GEN-03/LEAFGREEN`, `MULTI`, or `REV-ALL` are migration inputs only. New files must not be added there.

- source-release fact -> `LIBRARY/GEN-03/GBA/LEAFGREEN/RELEASES/<RELEASE-ID>/...`
- exact uploaded-file observation -> `.../RELEASES/<RELEASE-ID>/DUMPS/<DUMP-ID>/...`
- all-build bank/revision/localization comparison -> `.../COMPARISONS/<COMPARISON-ID>/...`
- release-independent LeafGreen parser/schema -> `.../SHARED/...`
- modernization, Past Paradox, BW-direct-params, or any other modification -> top-level `PROJECTS/<PROJECT-ID>/...`

## Sakurai / Tsubaki ownership
Sakurai is authoritative for release identity, dump provenance, reverse engineering, text/data structure, comparisons, design, and verification. Tsubaki uses exactly the same release IDs and owns production assets, conversion indices, build inputs, patches, and generated implementation resources.

The v4.1 extension makes this split machine-readable and adds ROM-derived bank sharing evidence. Research-level bank identity stays in Sakurai; production reuse/dedup summaries derived from that evidence stay in Tsubaki.

Original `.gba` files stay outside GitHub.
