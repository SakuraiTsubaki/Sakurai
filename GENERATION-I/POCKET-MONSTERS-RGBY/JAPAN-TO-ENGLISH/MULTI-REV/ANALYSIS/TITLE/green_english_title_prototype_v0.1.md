# INVALID — Pocket Monsters Green English Title Prototype v0.1

**Do not use this prototype.**

This first Green title prototype inherited the same incorrect assumption as the early Red work: it treated `0x10419` as the English Pokémon-logo source offset. The verified English logo source is file offset `0x11380` (ROM address `04:5380`).

The corrected implementation is `green_english_title_corrected_v0.2` and should be treated as the current valid title work.
