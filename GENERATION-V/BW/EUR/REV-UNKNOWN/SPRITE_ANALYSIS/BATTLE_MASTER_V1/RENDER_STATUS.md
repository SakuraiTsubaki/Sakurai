# Native renderer status

Direct NCGR/NCLR parsing has begun. Header-level dimensions and palette containers are verified, but the canonical source renderer is not yet accepted until tile/layout reconstruction is validated against the original game's sprite-loading behavior or a trusted independent decoder.

A visually scrambled intermediate render must not be promoted as a source PNG or used for Generation III conversion. The project contract requires layout validation before source reconstruction becomes canonical.
