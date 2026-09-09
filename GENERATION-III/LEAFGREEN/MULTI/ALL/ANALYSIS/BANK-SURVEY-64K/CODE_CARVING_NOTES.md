# Code-carving notes

First-pass candidate generation uses two independent Thumb signals:

- aligned 32-bit ROM words whose value is an in-ROM address with bit 0 set (Thumb function/callback pointer candidate), and
- Thumb-1 `BL` instruction-pair patterns whose decoded destination falls inside the ROM.

These are **candidate** signals only. Random data can mimic a `BL`, so targets in known fill ranges are rejected and the next pass scores targets by incoming-reference count, plausible function prologue, neighboring decoded control flow, and cross-version correspondence.

The reset vector and startup block are handled separately as ARM before the `BX` transition into Thumb code.
