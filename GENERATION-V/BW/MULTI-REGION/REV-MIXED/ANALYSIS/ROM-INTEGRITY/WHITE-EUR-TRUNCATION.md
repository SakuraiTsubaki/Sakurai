# Pokémon White EUR source-image integrity audit — correction

Date: 2026-09-10

## Superseding result

The earlier conclusion that `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds` was physically truncated at 63 MiB was incorrect and is superseded by a direct full-file recheck.

The currently mounted source image is **268,435,456 bytes (256 MiB)** and contains all 484 FAT entries through the end of the NitroFS data region.

The previously reported SHA-1 `9337c23adfa0d200ebbf59bc46e3a1a75061a9b7` is not the full-file SHA-1. It is the SHA-1 of exactly the first `0x03F00000` bytes (63 MiB) of the current complete image. The earlier audit accidentally treated that prefix boundary as physical EOF.

No ROM binary is stored in GitHub.

## Current direct measurements

- game code: `IRAO`
- physical file size: `268,435,456` bytes (`0x10000000`, 256 MiB)
- full-file CRC32: `EDCD5161`
- full-file MD5: `8dfef9a099e1269af5c1fcf9d7736a11`
- full-file SHA-1: `f94d4578956487c09fee20809a591e858017769e`
- first-63-MiB SHA-1: `9337c23adfa0d200ebbf59bc46e3a1a75061a9b7`
- header device-capacity code: 11
- header logical ROM capacity: `268,435,456` bytes (256 MiB)
- header used-ROM-size field: `0x0C3B9400` (`205,231,104` bytes)
- FNT offset/size: `0x002F0E00 / 0x410`
- FAT offset/size: `0x002F1400 / 0xF20`
- FAT entry count: 484
- maximum FAT-referenced end: `0x0BFD9C3C`
- ARM9 overlay table offset/size: `0x00073A00 / 0x1DA0`
- ARM9 overlay count: 237

All FAT-referenced files are physically present in the current image.

## External checksum classification

The current White CRC32 `EDCD5161` is documented by public ROM-hacking/checksum references as the SweeTnDs-era USA/Europe image and is also marked `[b]` (bad dump/non-canonical image) by GameHacking.org. GameTDB lists a different 256 MiB IRAO checksum for a canonical image.

Therefore the project should distinguish two questions:

1. **physical completeness** — current source image is complete;
2. **archival/canonical dump identity** — current source is not checksum-identical to the canonical GameTDB entry and should remain identified by its exact supplied checksum.

This does not prevent binary analysis of the supplied project source, but findings must be tied to this specific image/revision identity.

## Hypothetical 63-MiB truncation donor test

Because the complete White image is now available, the previous hypothetical 63-MiB truncation can be tested exactly against Black as a donor.

Cut boundary used for the test: `0x03F00000`.

White FAT files FID 246–483 lie partly or wholly after that boundary. Comparing those 238 files against Black by logical FAT file ID shows:

- 233 files are byte-identical between Black and White;
- 5 files differ.

The five differing files are:

| FID | Path | Black size | White size | Member-level difference |
|---:|---|---:|---:|---|
| 268 | `a/0/2/6` | 22,228 | 22,528 | 8 of 15 NARC members differ |
| 328 | `a/0/8/6` | 3,356 | 3,356 | 1 of 1 member differs |
| 368 | `a/1/2/6` | 35,284 | 35,284 | 29 of 112 members differ |
| 420 | `a/1/7/8` | 168,792 | 168,792 | 26 of 649 members differ |
| 473 | `a/2/3/1` | 1,208,900 | 1,210,248 | 2 of 73 members differ |

`a/0/2/6` is independently documented as the version/title-screen graphics archive. `a/1/2/6` is independently documented for BW as wild encounter data. The exact BW semantics of `a/0/8/6`, `a/1/7/8`, and `a/2/3/1` remain unresolved in this audit and must not be guessed from B2W2 path maps.

### Raw-tail splice safety

A blind raw-byte append of Black from `0x03F00000` onward would not be a valid exact White reconstruction.

The range `0x03F00000–0x06AA6600` is byte-identical between the supplied Black and White images, so that contiguous region could be recovered exactly from Black.

At FID 268 (`a/0/2/6`, start `0x06AA6600`) the versions first diverge after the hypothetical cut.

A later structural mismatch is especially important at FID 473: White's file is 1,348 bytes larger than Black's, and FIDs 474–483 begin `0x400` bytes later in White. Therefore copying the remaining Black tail at the same raw ROM offsets would make White's own FAT point into the wrong data for those final files.

### Correct donor strategy if a White source were truly truncated

A reconstruction should be file-aware, not a raw tail concatenation:

- preserve the White header/FNT/FAT/overlays and all surviving White bytes;
- copy only files proven byte-identical by FID/content comparison from Black;
- place donor file payloads at the offsets expected by White's FAT or rebuild NitroFS consistently;
- mark the five version-different files as unresolved unless genuine White copies are available;
- never label a Black-substituted version-specific file as original White data.

A hybrid that substitutes Black versions for the five differing files may be useful for controlled experimentation, but it is **not an archival restoration of Pokémon White**.

## Current project handling rule

Status for the supplied White image: `PHYSICALLY_COMPLETE / SUPPLIED_SCENE_DUMP / NON-CANONICAL-CHECKSUM`.

The previous `INCOMPLETE_SOURCE_IMAGE` classification is retired.
