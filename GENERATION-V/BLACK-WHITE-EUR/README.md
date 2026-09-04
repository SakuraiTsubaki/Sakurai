# Pokémon Black / White EUR — Current Project ROM Census

> Generated directly from the current project ROM files. No ROM bytes were modified.

## ROM identity

| Field | Black | White |
|---|---:|---:|
| Physical file size | 268,435,456 B | 232,521,728 B |
| Header-declared capacity | 268,435,456 B | 268,435,456 B |
| Used ROM size (header) | 205,229,568 B | 205,231,104 B |
| Physically trimmed | False | True |
| Internal title | `POKEMON B` | `POKEMON W` |
| Game code | `IRBO` | `IRAO` |
| SHA-1 | `a68b3bedf5c1e53556e41e59cdf396c20b331896` | `8f1bede1ac7eda570ced765b72a6d8fa5d49ed29` |
| SHA-256 | `2e40416b8e8183d936084c7be0adeaab4fa3f786a68f90d7291ab77d340f0c1d` | `f7267ab3852bfdf31c79518ac92aa361776f70cffef8c8824d783d4494e94f9a` |

## Structural census

- FAT files: Black **484**, White **484**
- Named NitroFS files: Black **247**, White **247**
- Directories: Black **31**, White **31**
- ARM9 overlays: Black **237**, White **237**
- NARC archives: Black **237**, White **237**
- NARC inner members: Black **54,054**, White **54,054**

## Black ↔ White byte comparison

- FAT files identical: **299** / 484
- FAT files different: **185**
- ARM9 overlays identical: **57** / 237
- ARM9 overlays different: **180**
- NARC inner members identical: **53,988** / 54,054
- NARC inner members different: **66**

### Different NARC archives

| Path | Members B/W | Size B | Size W |
|---|---:|---:|---:|
| `/a/0/2/6` | 15/15 | 22228 | 22528 |
| `/a/0/8/6` | 1/1 | 3356 | 3356 |
| `/a/1/2/6` | 112/112 | 35284 | 35284 |
| `/a/1/7/8` | 649/649 | 168792 | 168792 |
| `/a/2/3/1` | 73/73 | 1208900 | 1210248 |

## Trim/padding observation

Black physically occupies the full header-declared 256 MiB image. White currently occupies **232,521,728 bytes**, while its DS header still declares **268,435,456 bytes** capacity and **205,231,104 bytes** used ROM data.
All FAT entries referenced by the current White image are present, so the missing tail is outside the used NitroFS data region and is consistent with a trimmed padding tail rather than missing game files.

## Reproduction

Run:

```bash
python3 scripts/bw_rom_census.py BLACK.nds WHITE.nds output_dir
```

ROM originals must not be committed to GitHub.
