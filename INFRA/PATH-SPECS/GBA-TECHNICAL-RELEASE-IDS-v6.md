# GBA technical release IDs — v6

Canonical GBA source release ID: `<GAME-CODE>-HV<HEADER-VERSION>`.

Path:
`LIBRARY/<GENERATION>/<GAME-ID>/SOURCE/GBA/CART/<RELEASE-ID>/`

Locale is manifest metadata, not an extra path segment.

If two materially distinct builds share the same game code and header version, the non-retail build appends a factual build qualifier. Example: Ruby retail `AXVD-HV0` and German debug `AXVD-HV0-DEBUG`.

Exact observed files are separate dump identities under `DUMPS/<DUMP-ID>/`. No original ROM binary is committed.
