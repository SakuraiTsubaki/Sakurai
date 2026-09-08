# RBY title trainer + passing Pokémon analysis

## Scope

This analysis covers the Japanese **Pocket Monsters Red / Green / Blue** title-screen trainer and cycling Pokémon mechanism.
Japanese Pikachu/English Yellow use a separate Pikachu-centered title implementation.

## 1. The trainer and the Pokémon are rendered by different hardware paths

The trainer is made from **35 Game Boy OBJ tiles (5 × 7 = 40 × 56 px)** and is rendered through OAM.
The Pokémon is loaded through the normal species front-sprite pipeline (`GetMonHeader` → `LoadFrontSpriteByMonIndex`) into the background tilemap.

That separation is what makes the title effect possible: SCX can scroll the Pokémon/background band while the trainer OBJ remains stationary.

## 2. Japanese Red/Green versus Japanese Blue

### Japanese Red / Green legacy composition
- trainer graphic: file `0x11711`, length `0x230`
- trainer top-left display coordinate: approximately `(40, 80)`
- Pokémon tilemap anchor: tile `(9,10)` = pixel `(72,80)`
- visual composition: **trainer left / Pokémon right**
- simple raster scrolling in fixed 8-pixel steps
- no English/Blue-style animated Title Ball

### Japanese Blue revised composition
- trainer graphic: file `0x12AA1`, length `0x230`
- trainer top-left display coordinate: approximately `(82,80)`
- Pokémon tilemap anchor: tile `(5,10)` = pixel `(40,80)`
- visual composition: **Pokémon left / trainer right**
- revised Poké Ball handling/animation
- revised variable-speed title scrolling

The Japanese Blue trainer block is byte-for-byte identical to the supplied English Red/Blue trainer block.

## 3. Raster split

The title code writes `rSCX` at scanline `$48` (72) and restores it at `$88` (136).

Therefore:
- top logo area stays fixed
- middle 64-pixel band is horizontally scrolled
- bottom copyright area stays fixed
- the trainer stays fixed because it is OAM, not background

This is the actual mechanism behind the "Pokémon passing by the trainer" effect.

## 4. Pokémon selection

After the fixed initial species, the code uses the low four bits of the RNG to select one of 16 candidates.
If it selects the Pokémon currently displayed, it retries.

### Red
Charmander, Squirtle, Bulbasaur, Weedle, Nidoran♂, Scyther, Pikachu, Clefairy, Rhydon, Abra, Gastly, Ditto, Pidgeotto, Onix, Ponyta, Magikarp

### Green
Bulbasaur, Charmander, Squirtle, Caterpie, Nidoran♀, Pinsir, Pikachu, Clefairy, Rhydon, Abra, Gastly, Ditto, Pidgeotto, Onix, Ponyta, Magikarp

### Blue
Squirtle, Charmander, Bulbasaur, Mankey, Hitmonlee, Vulpix, Chansey, Aerodactyl, Jolteon, Snorlax, Gloom, Poliwag, Doduo, Porygon, Gengar, Raichu

Red and Green deliberately differ in several paired choices such as Weedle/Caterpie, Nidoran♂/Nidoran♀, and Scyther/Pinsir.
Blue uses a substantially different 16-species set.

## 5. Project rule

Because the Japanese ROMs are the actual source games, these title differences should **not** be normalized to the English Red/Blue arrangement.

- Red: preserve Japanese Red legacy composition/behavior.
- Green: preserve Japanese Green legacy composition/behavior.
- Blue: preserve Japanese Blue revised composition/behavior.
- Pikachu: analyze and preserve its independent Pikachu title system separately.

English localization should change language-dependent title assets without erasing these version-specific behaviors.
