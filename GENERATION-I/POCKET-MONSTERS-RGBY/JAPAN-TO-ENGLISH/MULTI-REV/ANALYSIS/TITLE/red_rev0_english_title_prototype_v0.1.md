# INVALID — Pocket Monsters Aka English Title Prototype v0.1

**Do not use this prototype.**

This first Red title prototype incorrectly assumed that the English and Japanese ROMs stored the Pokémon logo at the same file offset (`0x10419`). The English logo actually resides at file offset `0x11380` (ROM address `04:5380`).

The corrected implementation is `red_english_title_corrected_v0.2` and should be treated as the current valid title work.
