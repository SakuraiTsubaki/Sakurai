# Integrated disassembly status

The bank survey is now an integrated reverse-engineering pass rather than a statistics-only pass. Bank 00 is the first anchored bank: GBA reset starts in ARM state at `0x08000000`, branches past the cartridge header to startup code at `0x08000204`, and later switches to Thumb through `BX` using an odd target address. The same anchored procedure is propagated bank-by-bank.

Generated artifacts distinguish **confirmed entry/root**, **high-confidence function target**, **candidate target**, **data**, and **fill** so that non-code is not presented as executable assembly.
