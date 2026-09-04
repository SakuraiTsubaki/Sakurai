# Pokémon Black / White EUR — Current Project ROM Census

> Generated directly from the current project ROM files. No ROM bytes were modified. Original ROM binaries are excluded from GitHub.

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

- FAT files: **484** each
- Named NitroFS files: **247** each
- Directories: **31** each
- ARM9 overlays: **237** each
- NARC archives: **237** each
- NARC inner members: **54,054** each

## Black ↔ White byte comparison

- FAT files identical: **299 / 484**
- FAT files different: **185**
- decompressed ARM9 overlays identical: **57 / 237**
- decompressed ARM9 overlays different: **180**
- NARC inner members identical: **53,988 / 54,054**
- NARC inner members different: **66**

Exactly five ordinary NARCs differ: `a/0/2/6`, `a/0/8/6`, `a/1/2/6`, `a/1/7/8`, and `a/2/3/1`.

## Completed deep-census phases

### Field subsystem

See `analysis/FIELD_SUBSYSTEM_CENSUS.md`.

Locally proven relationships for all **427 ZoneData records**:

- `a/0/1/2` = **427 × 48 B** ZoneData.
- `+0x06 = 2×zone` → executable field-script member in `a/0/5/7`.
- `+0x08 = 2×zone+1` → metadata member byte-identical to the corresponding overworld tail.
- `+0x14` → encounter index 0..111 or `FFFF`.
- `+0x16 = zone` → overworld/event-object member in `a/1/2/5`.
- locally validated executable script entry points: **2,589**.

### Core species / move / item / trainer data

See `analysis/CORE_GAME_DATA_CENSUS.md`.

- `a/0/1/6` Personal archive is composite:
  - member 0 special/placeholder
  - **1..649** base species PersonalInfo, 60 B each
  - **650..667** 18 alternate-form PersonalInfo records
  - member **668 = 1,300 B = 650×u16 Unova-Dex mapping**
- Unova-Dex sentinel = **999**; Victini #494→0, Snivy #495→1, Genesect #649→155.
- `a/0/1/9`: **668 × 42 B** evolution data, 7×6 B slots per member.
- `a/0/2/1`: **560 × 36 B** move parameters.
- `a/0/2/4`: **627 × 36 B** item parameters.
- trainer metadata/party: **616 + 616 members**, with all four party template sizes validated and **0 mismatches**.

### Egg moves

See `analysis/EGG_MOVE_CENSUS.md`.

- `a/1/2/3`: **650 species-indexed members**.
- record format: `u16 count + count × u16 move ID`.
- **650/650** length checks pass.
- **2,773** listed Egg Move IDs total.
- maximum **16** Egg Moves on one species entry.

## Current semantic policy

BW1 and B2W2 filesystem mappings are not treated as interchangeable. Historical mappings are used only as leads; BW1 paths are promoted to confirmed only after local structure/xref/byte-level verification. Unknown archives remain explicitly unknown rather than receiving guessed names.

## Trim/padding observation

Black physically occupies the full header-declared 256 MiB image. White currently occupies **232,521,728 bytes**, while its DS header declares **268,435,456 bytes** capacity and **205,231,104 bytes** used ROM data. All FAT entries referenced by White are present, so the removed tail is outside used NitroFS data and is consistent with trimmed padding.

## Reproduction

Base structural census:

```bash
python3 scripts/bw_rom_census.py BLACK.nds WHITE.nds output_dir
```

ROM originals must never be committed to GitHub. Analysis reports, ledgers, scripts, patches and other non-ROM outputs are committed as the census progresses.
