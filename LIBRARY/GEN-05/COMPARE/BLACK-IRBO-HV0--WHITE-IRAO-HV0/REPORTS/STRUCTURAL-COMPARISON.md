# Black / White supplied-ROM structural comparison

Generated directly from the two supplied ROM images. ROM bytes are not stored here.

## Identity

| Field | Black | White |
|---|---|---|
| Internal title | POKEMON B | POKEMON W |
| Game code | IRBO | IRAO |
| Header version | 0 | 0 |
| Unit code | 0x02 | 0x02 |
| Size | 268435456 | 268435456 |
| SHA-1 | `a68b3bedf5c1e53556e41e59cdf396c20b331896` | `f94d4578956487c09fee20809a591e858017769e` |
| SHA-256 | `2e40416b8e8183d936084c7be0adeaab4fa3f786a68f90d7291ab77d340f0c1d` | `93e4f473ce9a0543bccf2e689ecd07ab4fcc39dd00fb4f194343cbd5e70e17ed` |

## Structural counts

- FAT entries: 484 / 484
- ARM9 overlays: 237 / 237
- named NitroFS files: 247 / 247
- NARC containers among named NitroFS files: 237 / 237
- ARM7 overlay entries: 0 / 0

## Equality / delta counts

| Layer | Same | Different | Black-only | White-only |
|---|---:|---:|---:|---:|
| FAT by file ID | 299 | 185 | 0 | 0 |
| ARM9 overlay by overlay ID | 57 | 180 | 0 | 0 |
| NitroFS by native path | 242 | 5 | 0 | 0 |
| NARC by native path | 232 | 5 | 0 | 0 |

## Differing NitroFS paths

- `a/0/2/6` — Black 22228 bytes / White 22528 bytes
- `a/0/8/6` — Black 3356 bytes / White 3356 bytes
- `a/1/2/6` — Black 35284 bytes / White 35284 bytes
- `a/1/7/8` — Black 168792 bytes / White 168792 bytes
- `a/2/3/1` — Black 1208900 bytes / White 1210248 bytes

## Differing ARM9 overlay IDs

180 overlay IDs differ. Compact ranges/list:

`0-4, 6-65, 67-83, 88, 90-107, 109-112, 114-125, 127-129, 131-137, 168, 170-188, 194-199, 203-225, 227-228, 230-231`

## Repository consequence

Do not move byte-identical Black/White source files into `SHARED`; release ownership stays with each release. Equality and deltas are represented in `COMPARE`. Native paths remain native paths until semantic identity has been independently verified.
