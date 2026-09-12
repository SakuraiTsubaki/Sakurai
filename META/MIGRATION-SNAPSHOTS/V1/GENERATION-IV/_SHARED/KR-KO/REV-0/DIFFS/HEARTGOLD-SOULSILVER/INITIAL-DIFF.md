# HeartGold KO-KR Rev 0 vs SoulSilver KO-KR Rev 0 — initial raw filesystem diff

## Scope
Byte-level comparison of the uploaded Korean retail ROMs at Nintendo DS FAT/NitroFS file-entry level. This is an initial structural baseline, not the final gameplay-difference catalog.

## Result
- FAT entries in each ROM: 511
- Identical entries: 390
- Differing entries: 121
- Named NitroFS paths present in both versions: same path set in this pass
- Named files that differ byte-for-byte: 3
  - `a/0/7/5`
  - `a/1/3/3`
  - `a/2/5/2`
- The remaining differing entries are currently non-FNT/unnamed entries and require overlay/container-role mapping before interpretation.

## Interpretation
HeartGold and SoulSilver have the same high-level filesystem layout but substantially more binary-level divergence than Diamond/Pearl in this raw pass. The three numbered NARC/data paths above are priority targets for semantic identification; the unnamed differences must be resolved against ARM9/ARM7 overlay tables and other DS file-table roles before any gameplay conclusion is drawn.

## Next decomposition
1. Resolve all 511 FAT IDs to FNT/overlay/other roles.
2. Identify the semantic names of `a/0/7/5`, `a/1/3/3`, and `a/2/5/2` using decompilation mappings and direct archive parsing.
3. Parse NARC members and compare HG/SS version-exclusive data at member level.
4. Build Johto/Kanto encounter, trainer, script, graphics, text, and event difference catalogs separately.
