# Japanese Bank 00 — player sprite reset and audio fade

This range immediately follows the sprite decompression engine and ends immediately before the Bank 00 text-script engine.

## ROM-verified ranges

### `ResetPlayerSpriteData`

| Build | Range | Size | SHA-1 |
|---|---:|---:|---|
| V1.0 | `$136B-$139B` | 49 bytes | `38ebab1590e33aac5fbffb6742c7b39e70eb9a57` |
| V1.1 | `$1359-$1389` | 49 bytes | `fc891158c3b1556d2d034c7f93797c58b2673d80` |

An aligned comparison finds three differing bytes. They are address operands produced by the V1.1 `$12` relocation and its relocated `FillMemory` target; the routine logic is unchanged.

The routine clears the two player sprite-state structures, restores picture/image-base IDs to 1, and sets the player screen position to Y=`$3C`, X=`$40`.

### `FadeOutAudio`

| Build | Range | Size | SHA-1 |
|---|---:|---:|---|
| V1.0 | `$139C-$13F0` | 85 bytes | `9445144ef1028e44b5b168e18108641dfea4fe59` |
| V1.1 | `$138A-$13DE` | 85 bytes | `c8bc1e456a39b3ec6cead91a4d245d2fc18fb691` |

The aligned blocks differ in two bytes, both belonging to the relocated `PlaySound` address operand. The fade algorithm and state layout are otherwise identical.

`FadeOutAudio` keeps full volume (`$77`) when no fade is requested, decrements the fade counter, lowers both master-volume nybbles step by step, stops current music when volume reaches zero, restores the saved audio bank, and starts the queued sound/music ID.

## Source and symbols

Structured source:

- `home/jp_reset_player_sprite.asm`
- `home/jp_fade_audio.asm`

Newly mapped state includes the player sprite structures at `$C100` / `$C200`, sprite-state length `$10`, `wStatusFlags2` at `$D6AB`, and `rAUDVOL` at `$FF24`.

## Next boundary

The next Bank 00 code starts with the text-script engine (`DisplayTextID`) at:

- V1.0 `$13F1`
- V1.1 `$13DF`

Neither range above contains sprite artwork or other graphics payload, so no PNG is generated for this step. The PNG requirement applies when actual graphics data is reconstructed.
