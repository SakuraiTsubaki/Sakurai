# GS Korean -> Pocket Monsters — v9 routing

Canonical home: `CROSS-GEN/TARGET/GS-KOREAN-TO-POCKET-MONSTERS/`.

The project translates each Japanese source directly from Japanese and each English source directly from English. Official Korean Gold/Silver provide the Game Boy Korean implementation reference and are also independent language-audit targets.

## Source identity

Canonical source paths are:

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

The strongest stable technical release ID is canonical. Market/language/revision names are aliases/metadata when a stronger identifier exists. This collapses Crystal duplicates such as `JP-JA-HV0` vs `BXTJ-HV0` and `US-EU-EN-HV*` vs `BYTE-HV*` into one release identity.

Exact supplied ROM images are dump observations, never releases:

```text
<RELEASE-ID>/OBSERVATIONS/<DUMP-ID>/manifest.json
```

ROM binaries are not committed. `DUMP-ID` is hash-derived and the manifest stores the complete SHA-256/SHA-1, size and header facts.

## Current supplied set

`SOURCE-SET-23.csv` registers all 23 supplied ROM observations and their canonical routes. Generation I uses stable market/language IDs where no stronger technical key is established. Generation II uses `AAUJ/AAUE/AAUK`, `AAXJ/AAXE/AAXK`, `BXTJ`, and `BYTE` technical identities where available.

English Yellow remains `SOURCE/GB/...` even though the supplied filename ends in `.gbc`; file extension is not platform identity.

## Target variants

Every independently buildable source release gets a variant ID:

```text
<GAME>-<RELEASE-ID>-KO-KR
```

This preserves Japanese/English localization differences and revision differences rather than forcing one Korean text onto unlike originals.

## GS Korean implementation references

```text
GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0/
GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0/
```

Korean Gold/Silver are dual-role inputs: translation subjects and implementation references. Release-owned bytes stay owned by their source release. A deduplicated target production asset is allowed only when provenance lists every owning release and byte equality is verified.

## Repository split

**Sakurai** owns release/dump identity, bank fingerprints, reverse engineering, text/code/pointer analysis, translation crosswalks, UI/SRAM/relocation design, reports and verification.

**Tsubaki** owns extracted/normalized production assets, converters, insertion data, build inputs, patches, catalogs and production verification.
