# Secondary Research Seeds

These sources are useful leads for format/tool discovery but are not authoritative implementation evidence. Every claim derived from them must be rechecked against verified local target material before being promoted to Observed or later status.

## pkNX

Repository: `kwsch/pkNX`

Why useful:

- Public tooling explicitly supports data dumping for Pokémon Scarlet / Violet and Pokémon Legends: Z-A.
- Its source contains version/file-count heuristics and game-specific loading code that may help identify expected resource families.

Cautions:

- Public source may lag the newest official patch. For example, visible Z-A heuristics include a Ver. 2.0.0 boundary while this project currently targets official Ver. 2.0.2 as the current comparison target.
- File-count heuristics are not identity proof.
- Tool-specific names are not automatically original game symbols or canonical format names.

## Community Z-A unpacking research

Public community projects describe candidate `TRPFS` / `TRPFD` / pack relationships and candidate resource extensions. Treat these only as hypotheses to test against verified local Z-A material.

## Adoption rule

A secondary-source claim is adopted only when at least one of the following is satisfied:

1. independently reproduced from a verified local target;
2. corroborated by a first-party or platform specification where applicable;
3. cross-validated by multiple independent technical sources and then locally verified.

Until then, record it as `candidate`, `secondary`, or `unverified`.
