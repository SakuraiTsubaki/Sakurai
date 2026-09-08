# White reproducibility tools

Pokémon Black and White EUR REV-0 use the same Nintendo DS reproducibility workflow in this project.

The canonical stdlib-only extractor/chunker/rebuilder/validator is stored at:

`GENERATION-V/BLACK/EN-USA-EUR/REV-0/repro-tools/nds_repro.py`

It was tested independently against the White source (`IRAO`) as well as Black. The White no-change rebuild matched CRC32, MD5, SHA-1 and SHA-256 exactly, including the source-independent `base_chunks` rebuild path.

Keeping one canonical copy avoids needless script duplication while the path remains documented under the White hierarchy.
