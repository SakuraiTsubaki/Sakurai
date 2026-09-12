# Pokémon Red uploaded ROM audit

Read-only identification and bank-layout baseline for all uploaded Red-family Game Boy ROMs. Original ROM binaries are not included.

## Inventory

| File | Size | Banks | Cart | Region | Rev | SHA-256 | Checksums |
|---|---:|---:|---|---|---:|---|---|
| Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb | 512 KiB | 32 | MBC1+RAM+BATTERY | Japan | 1 | `751abb1fb2b2d6b91dc631fa10ed36bd07f682cb5c3febe6c8f0e3dabc1fae1c` | header/global OK |
| Pocket Monsters - Aka (Japan) (SGB Enhanced).gb | 512 KiB | 32 | MBC1+RAM+BATTERY | Japan | 0 | `392ce450d708c8d127aaed7afc20001a48625bd83a5fa5325be82f5c0972ccfa` | header/global OK |
| Pokemon - Edicion Roja (Spain) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | Non-Japan | 0 | `a756cf7ad888aa46de4b9699a177a0edf1775e59eb6330014c6f5c139be9c45d` | header/global OK |
| Pokemon - Red Version (USA, Europe) (SGB Enhanced) - 복사본.gb | 1024 KiB | 64 | MBC3+RAM+BATTERY | Non-Japan | 0 | `5ca7ba01642a3b27b0cc0b5349b52792795b62d3ed977e98a09390659af96b7b` | header/global OK |
| Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb | 1024 KiB | 64 | MBC3+RAM+BATTERY | Non-Japan | 0 | `5ca7ba01642a3b27b0cc0b5349b52792795b62d3ed977e98a09390659af96b7b` | header/global OK |
| Pokemon - Rote Edition (Germany) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | Non-Japan | 0 | `9cd186b288dbcd52413d561ae449f1f700c32b45af56dbf849095d4a0c8637a6` | header/global OK |
| Pokemon - Version Rouge (France) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | Non-Japan | 0 | `23766290f3b2347f815f1e8977c3b84047ed880cadda8c4f1a3595a633daa303` | header/global OK |
| Pokemon - Versione Rossa (Italy) (SGB Enhanced).gb | 1024 KiB | 64 | MBC5+RAM+BATTERY | Non-Japan | 0 | `e805d00b0002156d38b96efd57c823b0db3a3ef4cd32f98bd9bb4779bda3dd5b` | header/global OK |

## Key findings

- 8 uploaded files resolve to 7 distinct ROM byte images because the English USA/Europe copy is byte-identical to the original English file (same SHA-256).
- Japanese Red Rev 0 and Rev A are 512 KiB / 32 banks / MBC1+RAM+BATTERY. Header revision is 0 and 1 respectively.
- English Red is 1 MiB / 64 banks / MBC3+RAM+BATTERY; German, French, Italian and Spanish Red are 1 MiB / 64 banks / MBC5+RAM+BATTERY.
- All eight files have valid Game Boy header and global checksums.
- In every 1 MiB localized ROM, banks 0x2D-0x3F are entirely zero-filled: 19 full banks = 304 KiB of unambiguous empty ROM area.
- Bank 0x2C is partially used; its trailing zero run is roughly 14.3-14.8 KiB depending on language, but this is not counted as guaranteed free space without pointer/reference analysis.
- Bank 0x1B is byte-identical across both Japanese revisions and all localized ROMs.
- Japanese Rev 0 vs Rev A differ by 46,167 bytes. Only bank 0x1B is wholly identical between them.
