# Silver v6 artifact ownership

The eight supplied Silver ROMs remain local, read-only inputs. GitHub stores only non-ROM evidence and derived/reusable work.

## Sakurai

- Canonical release and dump identity.
- ROM header and native structure facts.
- Per-bank cryptographic fingerprints and cross-release equality/difference evidence.
- Text/data reverse engineering, semantic domain research, comparison reports, modernization design and verification evidence.

## Tsubaki

- Exact source locks that point back to Sakurai identities.
- Extraction/rebuild/conversion tooling that emits no original ROM image.
- Production-safe normalized/converted assets, implementation inputs, target bindings, patches, build metadata and regression evidence.

## Routing invariant

Release-specific facts stay in `LIBRARY/GEN-02/SILVER/SOURCE/GBC/CART/<RELEASE-ID>/`. Exact observed dump facts stay below `DUMPS/<DUMP-ID>/`. Cross-release bank relations stay in `LIBRARY/GEN-02/SILVER/COMPARE/`. Modernization work stays in `PROJECTS/GEN-02/SILVER-MODERNIZATION/`.
