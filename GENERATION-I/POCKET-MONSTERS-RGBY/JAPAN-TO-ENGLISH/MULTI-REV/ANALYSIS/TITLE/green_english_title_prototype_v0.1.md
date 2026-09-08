# Pocket Monsters Green → Pokémon Green Version title prototype

## Result

- The Japanese Green ROM remains the base ROM.
- The Japanese title logo block at `0x010419–0x010B18` (0x700 bytes) is replaced with the Pokémon logo data from the provided English Pokémon Red ROM.
- Japanese Green already contains a native `Green Version` title graphic in its shared 0x50-byte version graphics block at `0x068000`.
- The Green title selector at `0x0049DA` uses tiles `62 63 64 7F 65 66 67 68 69 50`, which selects `Green Version`.
- Therefore no invented/custom Green lettering is required.
- ROM size remains 512 KiB.
- Only the title logo and the two-byte global checksum change.

## Revisions

### Rev 0
- Source SHA-1: `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196`
- Output SHA-256: `7862c4d0d8a5f273b38ea98b46f7bc17497ab3eb1e11b1d10a26549cda067565`
- Global checksum: `0x4261`
- IPS SHA-256: `cdcf70b7986114e1ac211b4c0e741445223ca3051bf70eb5fc8383334e002ed4`

### Rev A
- Source SHA-1: `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b`
- Output SHA-256: `bb1d0bdc344977095df5efe2d8da32e24dcf06cc70fedbd04b7e76b21d85912d`
- Global checksum: `0x59D3`
- IPS SHA-256: `0becd16cf8cb7d5f1772970051e9cc7df37c1ac3b0ea289ec8ee60051ad73fd7`

## Verification

- IPS was reapplied to each clean source ROM and reproduced the patched ROM byte-for-byte.
- The original ROMs were not modified.
- No ROM binary is stored in GitHub; only patches and documentation are project artifacts.
