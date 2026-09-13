# FireRed English USA/Europe Rev 1 ROM cleanup

## Result

The uploaded 16 MiB `BPRE` revision 1 source dump differed from the clean target only at the final two ROM bytes.

- Affected offset range: `0x00FFFFFE-0x00FFFFFF`
- Before: `00 18`
- Restored padding: `FF FF`
- Bytes changed: `2`
- All other bytes: unchanged

## Fingerprints

### Source dump before cleanup

- CRC32: `29A4CDDF`
- MD5: `84CEA5F7A46531213C7A27BC3D72DE95`
- SHA-1: `C4D0119D9BCB36687F41A8F7CA72AB7AF60558E4`

### Verified clean result

- CRC32: `84EE4776`
- MD5: `51901A6E40661B3914AA333C802E24E8`
- SHA-1: `DD5945DB9B930750CB39D00C84DA8571FEEBF417`

## Repository policy

No ROM binary is stored in this repository. The cleanup is represented only by reproducible metadata, documentation, and tooling.
