# Classification and confidence policy

`EXACT`: proven directly by the supplied ROM (for example a 100% blank bank) or by an exact canonical source identity/reference mapping.

`HIGH`: strong exact-byte cross-version alignment covering a large fraction of the bank.

`MEDIUM`: useful exact-byte cross-version evidence, but insufficient for automatic semantic promotion by itself.

`LOW` / `NONE`: no semantic claim; the bank remains unresolved.

`HEURISTIC`: candidate discovery only. Pointer-shaped values, opcode-shaped values, text-like byte runs, and tile statistics may contain false positives and must never be treated as decoded source without independent verification.

The physical byte-exact scaffold is always authoritative until extract → reinsert → SHA-256 equality succeeds.
