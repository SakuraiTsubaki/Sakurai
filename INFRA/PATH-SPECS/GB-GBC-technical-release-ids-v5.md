# GB/GBC technical release IDs in v5

v5 does not assume that every GB/GBC title exposes a universal four-character game-code field. It does, however, prefer a stable technical release key when one is actually present and verified.

For the currently supplied Pokémon Silver ROMs, bytes `0x013F-0x0142` consistently expose the four-byte tokens `AAXJ`, `AAXE`, `AAXD`, `AAXF`, `AAXI`, `AAXS`, and `AAXK`. The Japanese Rev A image retains `AAXJ` while header version changes from `0` to `1`.

Therefore the canonical Silver release IDs are `<TOKEN>-HV<HEADER-VERSION>`, for example `AAXJ-HV0`, `AAXJ-HV1`, `AAXE-HV0`, and `AAXK-HV0`.

This is an evidence-based Silver rule, not a blanket claim about all GB/GBC software. If a title lacks a trustworthy technical token, use another stable platform-appropriate release key and record the basis in `IDENTITY/`; market/language may be used as a fallback only when no stronger technical identity is supported.
