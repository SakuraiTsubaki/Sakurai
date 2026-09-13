# Pokémon Emerald v10 direct-ROM census — 2026-09-13

The seven supplied filenames collapse to six byte-unique 16 MiB GBA images. The two English filenames are SHA-256-identical and therefore share one exact dump identity.

| Release | Dump | Aligned pointer refs | Pointer targets | LZ77 structural | LZ77 pointer-referenced | Padding runs >=256 |
|---|---|---:|---:|---:|---:|---:|
| BPEJ-HV0 | DUMP-SHA256-33F5610B9186B4AD | 92,327 | 64,668 | 4,596 | 4,254 | 241 |
| BPEE-HV0 | DUMP-SHA256-A9DEC84DFE7F62AB | 91,646 | 64,650 | 4,578 | 4,255 | 264 |
| BPED-HV0 | DUMP-SHA256-7C599C56849EFEEB | 91,448 | 64,568 | 4,574 | 4,256 | 264 |
| BPEF-HV0 | DUMP-SHA256-E79B40E6189550B4 | 91,672 | 64,661 | 4,578 | 4,256 | 264 |
| BPEI-HV0 | DUMP-SHA256-63CBFF3500B657CB | 91,493 | 64,580 | 4,575 | 4,256 | 264 |
| BPES-HV0 | DUMP-SHA256-E32C82BD10F174CF | 91,547 | 64,665 | 4,575 | 4,256 | 264 |

All six GBA header complement checksums verify with `(-sum(0xA0..0xBC) - 0x19) & 0xff`.

Across the six dumps, 25,533 pointer-referenced valid BIOS-LZ77 occurrences decompress to 4,514 SHA-256-unique payloads. Tsubaki tracks the full derived corpus with complete occurrence mapping; exact duplicate payloads are stored once by hash. Structural LZ77 validity is not a semantic asset classification.

The canonical production counterpart is `Tsubaki:GEN-03/EMERALD/PROJECTS/ROM-ASSET-CORPUS/`. ROM binaries are not committed.
