# Later-generation exclusions

## Rule

This project reconstructs **Generation VI as it actually existed in Pokémon X, Pokémon Y, Pokémon Omega Ruby, and Pokémon Alpha Sapphire**. Later games may add new forms, Mega Evolutions, names, mechanics, or availability to Generation VI species. Those later additions must never be backported into the Generation VI `BATTLE_MASTER_V1` unless they were already present in Generation VI game data.

This file exists because current reference pages naturally combine modern information with historical Generation VI information.

## Explicit exclusions / historical boundaries

### Zygarde

Generation VI contains only the form later called **Zygarde 50% Forme**.

Exclude from Generation VI:

- Zygarde 10% Forme
- Zygarde Complete Forme
- Zygarde Cells / Cores as Pokémon battle-form targets
- Power Construct form behavior
- Mega Zygarde

The 10% and Complete Formes were introduced in Pokémon Sun and Moon. Mega Zygarde is later still.

Reference: https://bulbapedia.bulbagarden.net/wiki/Zygarde_(Pok%C3%A9mon)

### Floette

**Eternal Flower Floette is not excluded.** It is present in Generation VI game data and therefore belongs in the source/data inventory, with its then-unobtainable status recorded.

Exclude from Generation VI:

- Mega Floette
- Floettite
- any Pokémon Legends: Z-A-specific Mega behavior or availability

Mega Floette was introduced in Pokémon Legends: Z-A, long after Generation VI.

Reference: https://bulbapedia.bulbagarden.net/wiki/Floette_(Pok%C3%A9mon)

### Pyroar

Generation VI contains the visually distinct male and female Pyroar states.

Exclude from Generation VI:

- Mega Pyroar
- Pyroarite

Mega Pyroar was introduced in Pokémon Legends: Z-A.

Reference: https://bulbapedia.bulbagarden.net/wiki/Pyroar_(Pok%C3%A9mon)

### Pumpkaboo / Gourgeist naming

For Generation VI provenance and logical-state labels, retain the period-appropriate English size names:

- Small Size
- Average Size
- Large Size
- Super Size

Do not silently replace these with later Pokémon Legends: Z-A naming in Generation VI manifests.

References:

- https://bulbapedia.bulbagarden.net/wiki/Pumpkaboo_(Pok%C3%A9mon)
- https://bulbapedia.bulbagarden.net/wiki/Gourgeist_(Pok%C3%A9mon)

### Diancie

**Mega Diancie is part of Generation VI**, but it is an **ORAS addition**, not an XY state.

Do not exclude it from the Generation VI project; instead preserve the title boundary:

- X/Y: Mega Diancie not present
- Omega Ruby/Alpha Sapphire: Mega Diancie present

Reference: https://bulbapedia.bulbagarden.net/wiki/Diancie_(Pok%C3%A9mon)

### Hoopa

**Hoopa Unbound is part of Generation VI**, but it is an **ORAS addition** associated with the Prison Bottle.

Preserve the title boundary:

- X/Y: Hoopa Unbound not present
- Omega Ruby/Alpha Sapphire: Hoopa Unbound present

References:

- https://bulbapedia.bulbagarden.net/wiki/Hoopa_(Pok%C3%A9mon)
- https://bulbapedia.bulbagarden.net/wiki/Prison_Bottle

## Acceptance rule

A current reference page mentioning a form is never sufficient proof that the form belongs to Generation VI.

Before adding any state to this master, record at least:

1. first core-series game in which the state was implemented;
2. whether it existed in XY, ORAS, both, or only as unused/data-only material;
3. whether the state is actually battle-visible;
4. whether it has a distinct model, texture, material/visibility state, or camera/pose requirement;
5. archive/member evidence when available.

If the implementation generation is later than Generation VI and there is no Generation VI data evidence, the state is excluded from this master.
