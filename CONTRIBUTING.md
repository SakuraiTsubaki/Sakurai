# Contributing

Contributions should improve the accuracy, traceability, reproducibility, or clarity of Sakurai's curated research/control material.

## Before contributing

- Read `README.md` and `INFRA/DOCS/REPOSITORY_OVERVIEW.md` to confirm that the work belongs in Sakurai.
- Follow the current canonical owner path documented in `STRUCTURE.md`.
- Identify the exact generation, game, release, revision, dump, project, comparison, reference, or target when applicable.
- Check `INFRA/DOCS/PROJECT_STANDARDS.md`, `INFRA/DOCS/RESEARCH_GUIDE.md`, and `INFRA/DOCS/VERIFICATION.md` before promoting a claim.

## Contribution rules

- Separate verified findings from hypotheses and imported assumptions.
- Record provenance, citations, commands, hashes, offsets, symbols, repository revisions, or other evidence when practical.
- Preserve real regional, language, revision, update, and release differences.
- Do not collapse distinct targets without verified equivalence.
- Prefer small, reviewable commits with one coherent purpose.
- Update documentation or manifests when identity, provenance, or verification state changes.
- Do not create parallel history/migration trees solely to preserve an old layout; Git history is the historical record.
- Do not commit complete playable ROM image files.
- When an artifact also belongs in Tsubaki, keep semantic coordinates and provenance consistent across the pair.

## Pull requests

A pull request should explain:

1. what changed;
2. which target/coordinate it affects;
3. what evidence supports the change;
4. how it was verified;
5. any remaining uncertainty or limitations.

See `INFRA/DOCS/README.md`, `INFRA/DOCS/WORKFLOW.md`, `INFRA/DOCS/PAIRING.md`, and `INFRA/MANIFESTS/README.md` for the repository-wide workflow.
