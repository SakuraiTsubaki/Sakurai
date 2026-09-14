# Japanese Bank 00 — map/NPC text-script dispatcher

This range begins immediately after `FadeOutAudio` and ends immediately before `DisplayStartMenu`.

## ROM-verified range

| Build | Range | Size | SHA-1 | Next routine |
|---|---:|---:|---|---|
| V1.0 | `$13F1-$15DD` | 493 bytes | `200e56efe44859bde9aa7bace1aa4737a2820a4b` | `DisplayStartMenu` at `$15DE` |
| V1.1 | `$13DF-$15CB` | 493 bytes | `b27c2fcf6b1f7eb52f48b9763cbff1cdb4441c92` | `DisplayStartMenu` at `$15CC` |

An aligned comparison finds 45 differing bytes. They resolve to relocated Bank 00 targets, revision-specific helper addresses, and revision-specific banked targets; the dispatcher structure and embedded Japanese text payloads are unchanged.

## Recovered source

`home/jp_text_script.asm` reconstructs:

- `DisplayTextID` and map text-pointer lookup
- special text IDs for Start Menu, Safari game over, fainted/blackout, and Repel expiry
- NPC facing update and sprite text-ID lookup
- special text-script dispatch for marts, Pokémon Centers, PC scripts, vending machine, prize vendor, and Cable Club
- dialogue hold/close flow and original NPC facing restoration
- map/sprite graphics reload after closing a text box
- Poké Mart item-list setup and common greeting text
- Pokémon Center dispatch
- Safari/fainted/blackout/Repel common messages

Japanese encoded text remains explicit byte data until the project-wide Japanese charmap/text macro layer is complete.

## Graphics note

This range controls dialogue and sprite-state restoration but contains no sprite artwork. No PNG is emitted for this range; actual graphics banks will carry both source graphics data and viewable PNG assets.
