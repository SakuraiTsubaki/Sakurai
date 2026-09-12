# Pokémon Ruby — canonical source library

This is the canonical research root for the currently supplied Pokémon Ruby GBA source set.

Original ROM binaries are local/read-only inputs and are never committed to GitHub.

## v4 identity model

Two identities are kept separate:

- **RELEASE** = one distinct Ruby software/build identity.
- **DUMP** = one exact observed source file, identified by complete hashes and provenance.

Canonical release path:

`LIBRARY/GEN-03/GBA/RUBY/RELEASES/<RELEASE-ID>/...`

Canonical observed-file path:

`LIBRARY/GEN-03/GBA/RUBY/RELEASES/<RELEASE-ID>/DUMPS/PROJECT-<SHA1-8>/...`

## Current release bindings

| RELEASE-ID | Game code | Header version | Market/language | Build |
|---|---|---:|---|---|
| `AXVJ-R0` | AXVJ | 0 | JP / ja | retail |
| `AXVE-R0` | AXVE | 0 | US / en | retail |
| `AXVE-R1` | AXVE | 1 | EU / en | retail |
| `AXVE-R2` | AXVE | 2 | US+EU / en | retail |
| `AXVD-R0` | AXVD | 0 | EU / de | retail |
| `AXVD-R0-DEBUG` | AXVD | 0 | EU / de | debug |
| `AXVD-R1` | AXVD | 1 | EU / de | retail |
| `AXVF-R0` | AXVF | 0 | EU / fr | retail |
| `AXVF-R1` | AXVF | 1 | EU / fr | retail |
| `AXVI-R0` | AXVI | 0 | EU / it | retail |
| `AXVI-R1` | AXVI | 1 | EU / it | retail |
| `AXVS-R0` | AXVS | 0 | EU / es | retail |
| `AXVS-R1` | AXVS | 1 | EU / es | retail |

`AXVD-R0-DEBUG` is an intentional exceptional suffix. The German retail and debug builds share the native GBA code `AXVD` and header version `0`, so native code/version alone does not uniquely identify one build. The suffix preserves the repository invariant that one release ID means one build identity.

A Japanese Ruby Rev 1 build is known outside the currently supplied source set, but no live release directory is created until an exact source file is supplied and verified.

## Comparison ownership

The existing 13-ROM bank/disassembly survey is owned by:

`LIBRARY/GEN-03/GBA/RUBY/COMPARISONS/SOURCE-SET-2026-09-12/`

This replaces legacy pseudo-owners such as `MULTI`, `REV-ALL`, and `ALL-RELEASES`.

## Derived modernization work

Modernization, expansion, localization, patches, and other transformations do **not** belong under this source library. They belong under repository-level `PROJECTS/<PROJECT-ID>/`, with manifests locking the exact Ruby release/dump inputs.
