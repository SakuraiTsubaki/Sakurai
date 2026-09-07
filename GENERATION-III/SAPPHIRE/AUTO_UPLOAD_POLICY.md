# SAPPHIRE automatic GitHub routing policy

This project uses two repositories with distinct roles.

## SakuraiTsubaki/Sakurai

Public analysis/research repository.

Store here:
- ROM structure audits and engine-limit reports;
- surveys, comparisons and technical analysis;
- architecture notes that are safe to publish;
- source citations and verification notes.

## SakuraiTsubaki/Tsubaki

Private working-assets repository.

Store here:
- implementation source and generators;
- manifests and generated parameter data;
- patches and relocation/build tooling;
- work-in-progress technical assets and regression artifacts.

## Exclusions

Original commercial ROM images and other non-redistributable copyrighted binaries are never committed to either repository.

## SAPPHIRE baseline

Current implementation baseline: Pokémon Sapphire Version (USA) Rev-0, SHA-1 `3ccbbd45f8553c36463f13b938e833f652b793e4`.

During active SAPPHIRE work, safe deliverables are routed to the appropriate repository automatically according to the rules above.