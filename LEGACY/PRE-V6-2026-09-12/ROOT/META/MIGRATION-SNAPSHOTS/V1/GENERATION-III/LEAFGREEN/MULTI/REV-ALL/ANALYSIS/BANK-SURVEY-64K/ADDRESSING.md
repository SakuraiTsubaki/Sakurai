# Addressing convention

- ROM file offset `0x000000` maps to GBA bus address `0x08000000`.
- 64 KiB analysis bank `NN` maps to offsets `NN0000`–`NNFFFF` and bus addresses `0x08NN0000`–`0x08NNFFFF` for `NN=00`–`FF`.
- Thumb function pointers store the bus address with bit 0 set; listings normalize the target to an even instruction address and retain the Thumb-state annotation.
