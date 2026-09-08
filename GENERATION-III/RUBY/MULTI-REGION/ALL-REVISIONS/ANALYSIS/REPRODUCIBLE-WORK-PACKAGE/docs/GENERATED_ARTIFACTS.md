# Generated Artifact Policy

The local work package retains generated reports such as `page_fingerprints_64k.csv` and `lz77_candidates.csv`. The source-of-truth for reproducibility is the original ROM hash manifest plus the deterministic tools in `tools/`.

Large derived indexes may be regenerated with `./run_analysis.sh ROM_DIR` instead of being duplicated across every repository path. This keeps GitHub binary-free and avoids storing massive data that is mechanically reproducible from the verified originals.
