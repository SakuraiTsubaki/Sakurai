# Reproducibility completeness matrix

| Layer | Status | Evidence / regeneration path |
|---|---|---|
| ROM identity / headers / hashes | COMPLETE | `data/manifests/` |
| Exact 64-bank split and rebuild | COMPLETE (9/9) | `data/banks/lossless_rebuild_results.json` |
| Cross-version exact patch edges | COMPLETE (8/8) | `data/diffs/patch_verification.json`, private IPS cache |
| 64-bank semantic section placement | COMPLETE for canonical EN layout | `data/semantic/section_layout.csv`, pinned `layout.link` |
| Exact EN section ranges and symbols | REPRODUCIBLE FROM PINNED SOURCE | `tools/sync_pret_reference.py` + `tools/parse_pret_symbols.py`; `.map/.sym` Git blob hashes pinned |
| Cross-version bank role transfer | COMPLETE at bank granularity | `data/semantic/bank_atlas.csv` + exact bank hashes |
| Revision/localization changed-byte metrics by bank | COMPLETE | `data/semantic/relationship_bank_diffs.csv` |
| Text candidates | COMPLETE heuristic inventory | `data/text/*_candidates.csv.gz` |
| Pointer candidates | COMPLETE heuristic inventory | `data/pointers/pointer_candidates_full.csv.gz` |
| Literal 00/FF free-space candidates | COMPLETE heuristic inventory | `data/free_space/` (not equivalent to linker-certified free space) |
| Raw 2bpp visual inspection atlas | COMPLETE, all unique bank hashes | private `visual/tiles/`, public manifest |
| Whole-ROM relationship heatmaps | COMPLETE | private `visual/diffs/`, public manifest |
| Map/script/audio object-level decoding for non-EN builds | NOT YET SEMANTICALLY PROVEN | Requires transferring exact EN symbols/ranges and validating each changed range against JP/EU builds |
| Native source rebuild of every non-EN localization | NOT YET COMPLETE | Current exact path is bank reconstruction + verified IPS graph; full localized source disassemblies remain future work |

`COMPLETE` here means deterministic and regression-verifiable for the stated layer. Heuristic inventories are deliberately labeled heuristic and are not promoted to semantic truth without a source/range proof.
