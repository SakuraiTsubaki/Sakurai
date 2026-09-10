# Pokémon White EUR source-image integrity audit

Date: 2026-09-10

## Result

The currently supplied `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds` image is **incomplete/truncated**. It is not a normal NDS image with only unused tail padding removed.

No ROM binary is stored in this repository.

## Direct measurements

- game code: `IRAO`
- physical file size: `66,060,288` bytes
- physical EOF: `0x03F00000`
- SHA-1: `9337c23adfa0d200ebbf59bc46e3a1a75061a9b7`
- header device-capacity code: 11
- header logical ROM capacity: `268,435,456` bytes (256 MiB)
- header used-ROM-size field: `0x0C3B9400` (`205,231,104` bytes)
- FNT offset/size: `0x002F0E00 / 0x410`
- FAT offset/size: `0x002F1400 / 0xF20`
- FAT entry count: 484
- maximum FAT-referenced end: `0x0BFD9C3C`
- ARM9 overlay table offset/size: `0x00073A00 / 0x1DA0`
- ARM9 overlay count: 237

## First truncation point

The last fully present FAT file is ID 245, path `a/0/0/3`.

FAT file ID 246 is:

- path: `a/0/0/4`
- start: `0x038E3200`
- expected end: `0x04069398`
- physical EOF: `0x03F00000`
- expected file size: 7,889,304 bytes
- missing tail from this member: 1,479,576 bytes

Therefore the physical image terminates **inside** `a/0/0/4`, not between files and not after the final used file.

`a/0/0/4` is independently identified in Generation-V filesystem documentation as the Pokémon battle sprite / `pokegra` archive. Its NARC header is present and declares 14,285 members, but the archive body is incomplete in the supplied White image.

## Files beyond EOF

Of the 484 FAT entries, 238 are partly or wholly outside the physical image. FID 246 crosses EOF; FIDs 247–483 are absent from the physical image.

Immediate FNT mapping around the cut:

| FID | Path | State |
|---:|---|---|
| 242 | `a/0/0/0` | complete |
| 243 | `a/0/0/1` | complete |
| 244 | `a/0/0/2` | complete |
| 245 | `a/0/0/3` | complete |
| 246 | `a/0/0/4` | partial / cut at EOF |
| 247 | `a/0/0/5` | absent |
| 248 | `a/0/0/6` | absent |
| 249 | `a/0/0/7` | absent |

Consequently this source cannot be used for a complete White-vs-Black NitroFS, graphics, text, map, or UI-resource audit.

## Overlay code remains usable

All 237 ARM9 overlay files are stored before the cut and were successfully extracted. White Overlay 91, the Pokémon-list/party subsystem, decompresses correctly to 35,648 bytes and contains the expected embedded original source module names (`pokelist.c`, `plist_plate.c`, `plist_message.c`, `plist_menu.c`, `plist_battle.c`, `plist_demo.c`).

Therefore the current White image may still be used for **code/overlay comparison** where the referenced overlay itself lies before EOF. It must not be treated as a complete White resource baseline.

## Project handling rule

Status for this image: `INCOMPLETE_SOURCE_IMAGE`.

Until replaced by a complete White dump:

- use the supplied Black image as the complete BW resource baseline;
- use White only for verified pre-EOF code/overlay regions;
- do not report absent post-EOF files as genuine Black/White version differences;
- do not synthesize missing White assets from Black and label them original White data;
- once a complete White image is available, repeat FNT/FAT/NARC hashes and version-delta comparisons from scratch.
