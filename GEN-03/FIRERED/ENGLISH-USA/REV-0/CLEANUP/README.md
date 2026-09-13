# FireRed English USA Rev 0 ROM cleanup

## Result

The uploaded 16 MiB `BPRE` revision 0 source dump differed from the clean target only at the final two ROM bytes.

- Affected offset range: `0x00FFFFFE-0x00FFFFFF`
- Before: `00 19`
- Restored padding: `FF FF`
- Bytes changed: `2`
- All other bytes: unchanged

## Fingerprints

### Source dump before cleanup

- CRC32: `07C5CC23`
- MD5: `17C9CC8267F0210A8170A830C10C60F2`
- SHA-1: `D3B806453369B4B086C792EB3C05A02F00057F50`

### Verified clean result

- CRC32: `DD88761C`
- MD5: `E26EE0D44E809351C8CE2D73C7400CDD`
- SHA-1: `41CB23D8DCCC8EBD7C649CD8FBB58EEACE6E2FDC`

## Repository policy

No ROM binary is stored in this repository. The cleanup is represented only by reproducible metadata, documentation, and tooling.
