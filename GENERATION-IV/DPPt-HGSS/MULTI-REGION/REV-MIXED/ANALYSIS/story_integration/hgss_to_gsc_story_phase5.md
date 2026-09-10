# HGSS → GSC Story Integration — Phase 5

## Scope
Ecruteak Gym → Routes 38–39 → Moomoo Farm → Olivine/Lighthouse → Routes 40–41 → Cianwood → Suicune/Eusine → Chuck → SecretPotion → Amphy recovery → Jasmine.

The 28-row detailed event matrix is in `hgss_to_gsc_story_phase5.csv`.

## Direct uploaded-ROM verification

Uploaded Korean ROM headers:
- HeartGold: `POKEMON HG`, game code `IPKK`, 128 MiB
- SoulSilver: `POKEMON SS`, game code `IPGK`, 128 MiB

The complete field-script NARC `a/0/1/2` is byte-identical between the two uploaded Korean ROMs:
- size: `372012`
- SHA-1: `0b911f52fda9c9324295a9bc7db2350433097529`
- members: `965`

This is stronger than checking only the Phase 5 members: **the entire checked field-script NARC is common between these uploaded HG/SS builds**. This does not imply that text, encounters, maps, graphics, audio, mascot data, or other NARCs are identical.

### Phase 5 member checks
| Index | Role | Size | Korean HG/SS member SHA-1 | HG=SS |
|---:|---|---:|---|---|
| 66 | D27R0107 — Olivine Lighthouse top/Jasmine | 640 | `68e86d6218c86bd5ce934b02d9008d106a433a5c` | Yes |
| 247 | R38 — Route 38 | 60 | `b6273d2d132808bf1dbc31bda58cef8dd81fe532` | Yes |
| 249 | R39 — Route 39/Baoba | 1244 | `ccb9f7ef33ce9bb186dfb07db0f7fa20a1e7ef7c` | Yes |
| 250 | R39R0101 — Moomoo Farm house | 432 | `105ce8a4eafcbf1540f21e7c4b1fcf56902dbb6c` | Yes |
| 251 | R39R0201 — Moomoo Farm stable | 932 | `c34f538edb627abec764ee271a231630da5bbc4c` | Yes |
| 252 | R42 — next Suicune waypoint | 936 | `1b02603d85c3b43d956e9c71aa2c43e9ea2b5672` | Yes |
| 875 | T24 — Cianwood City/Suicune/Eusine/Fly | 1432 | `3b2f56a8072d93763598dfcca94e168aa775ee8d` | Yes |
| 877 | T24GYM0101 — Cianwood Gym/Chuck | 424 | `f42822b2fff17f42c7807f8a6919351c3523e194` | Yes |
| 881 | T24R0501 — Cianwood Pharmacy | 176 | `c280c3200c85bdea2ecc4460bdfe556e2eb882bf` | Yes |
| 913 | T26GYM0101 — Olivine Gym/Jasmine | 1488 | `902dbb04bb136d96b30aa5ba341db4be86ea4425` | Yes |
| 922 | T27GYM0101 — Ecruteak Gym/Morty | 736 | `06b387ce2d20de68e6422ecb8798768929795ec7` | Yes |

## Major integration decisions

### Morty: preserve G/S freedom
Gold/Silver do not use Crystal's pre-beast-release forced-ejection scene in Ecruteak Gym. Crystal does, and HGSS likewise has an init condition that sends `VAR_UNK_4079 == 0` to a forced-leave script.

The integrated target should not erase the older G/S route. If Morty is beaten before the expanded Burned Tower story, later Eusine/Morty dialogue adapts; the legendary-beast event remains playable.

Rewards are conflict-free: Fog Badge + TM30 Shadow Ball.

### Midgame badge order must remain flexible
Do **not** hard-code:
`Morty → Chuck → Jasmine → Pryce`.

HGSS itself tracks a midgame badge counter and Rocket-takeover state. The correct integrated architecture is fact-driven:
- which badges are owned;
- whether Amphy is healed;
- whether Jasmine has returned;
- whether Rocket escalation threshold is reached.

Chuck is not required to obtain or return the SecretPotion. He is mainly the source of Storm Badge and HM02 Fly convenience.

### Moomoo Farm: seven-feed quest, different item/reward identities
Crystal explicitly uses a counter with milestones at 3, 5 and 7 Berries. HGSS also requires seven feeds, but uses Oran Berries.

Keep a shared `MOOMOO_FEED_COUNT = 0..7`, while preserving source provenance:
- GSC input: legacy `BERRY`
- HGSS input: `ORAN_BERRY`

Integrated acceptance of either item is a **project compatibility rule**, not an original rule of either version.

Reward conflict:
- GSC/Crystal: TM13 Snore
- HGSS: TM83 Natural Gift

Both remain. Neither overwrites the other.

### Route 39 Baoba / Safari Zone seed
HGSS adds Baoba to Route 39. He explains his new Safari Zone project and registers his Pokégear number. A later call announces the opening and points the player toward the Cianwood-side cavern route.

This is stored as a separate HGSS side-story chain and does not replace Moomoo Farm or Route 39 events.

### Jasmine / Amphy / SecretPotion
Use an atomic quest state:

`JASMINE_AT_LIGHTHOUSE`
→ `AMPHY_SICKNESS_EXPLAINED`
→ `SECRETPOTION_AVAILABLE`
→ `SECRETPOTION_OBTAINED`
→ `AMPHY_HEALED`
→ `JASMINE_AT_GYM`

The medicine handoff transaction must:
1. consume SecretPotion;
2. mark Amphy healthy;
3. advance the Lighthouse scene;
4. remove Jasmine from the Lighthouse;
5. enable Jasmine in the Gym.

Save/reload must never produce a half-healed state or duplicate Jasmine.

Jasmine remains challengeable once she returns regardless of whether Chuck was beaten.

Reward is conflict-free: Mineral Badge + TM23 Iron Tail.

### Cianwood Suicune/Eusine
Crystal and HGSS share a strong common backbone:
`Burned Tower release → Cianwood Suicune → Eusine battle → Route 42`.

Use one Cianwood event and one Eusine story battle rather than duplicating them.

After Route 42 the chains diverge:
- Crystal → Route 36 / Crystal tower conclusion
- HGSS → Vermilion → Route 14 → Route 25

Keep separate waypoint flags plus one global `SUICUNE_CAUGHT`.

If Suicune is caught on one valid branch, later nodes become Eusine epilogue/dialogue-only and cannot spawn a second catchable Suicune.

### Chuck
Preserve both pieces of authored content:
- GSC/Crystal: Strength/boulder Gym and Chuck's boulder-breaking character feat
- HGSS: waterfall/winch Gym mechanism

The best integration is HGSS's expanded approach puzzle plus the retained GSC boulder feat before battle.

Critical TM identity collision:
- GSC TM01 = DynamicPunch
- HGSS TM01 = Focus Punch

Never relabel the legacy TM01 slot. The Gen IV TM table must be expanded/namespaced before Focus Punch is added.

HM02 Fly from Chuck's wife is shared and needs only one claimed flag.

## Source references used

### `pret/pokegold`
- `maps/EcruteakGym.asm`

### `pret/pokecrystal`
- `maps/EcruteakGym.asm`
- `maps/Route39Barn.asm`
- `maps/Route39Farmhouse.asm`
- `maps/OlivineLighthouse6F.asm`
- `maps/CianwoodPharmacy.asm`
- `maps/CianwoodCity.asm`
- `maps/CianwoodGym.asm`
- `maps/OlivineGym.asm`
- Crystal Route 42 / Route 36 Suicune scripts

### `pret/pokeheartgold`
- `scr_seq_0922_T27GYM0101.s`
- `scr_seq_0247_R38.s`
- `scr_seq_0249_R39.s`
- `scr_seq_0250_R39R0101.s`
- `scr_seq_0251_R39R0201.s`
- `scr_seq_0252_R42.s`
- `scr_seq_0875_T24.s`
- `scr_seq_0877_T24GYM0101.s`
- `scr_seq_0881_T24R0501.s`
- `scr_seq_0066_D27R0107.s`
- `scr_seq_0913_T26GYM0101.s`
- `include/constants/items.h`
- Baoba phone scripts/message data

## Phase 5 integrated route

`Burned Tower / optional Morty-order handling`
→ `Fog Badge + TM30`
→ `Route 38`
→ `Route 39 Baoba side event + Moomoo Farm`
→ `Olivine / Lighthouse / Jasmine request`
→ `Routes 40–41`
→ `Cianwood Suicune`
→ `Eusine battle`
→ `Route 42 Suicune next-state armed`
→ `Chuck at any valid time`
→ `SecretPotion`
→ `return by Surf or Fly`
→ `Amphy healed`
→ `Jasmine returns`
→ `Jasmine challenge at any valid time`.

## Deferred, not omitted
- complete Routes 47/48 and HGSS Safari Zone implementation;
- Route 42 → Mahogany main-story pass;
- Crystal Route36/Tin Tower Suicune conclusion;
- HGSS Kanto Suicune continuation;
- Pryce and Lake of Rage / Rocket Hideout;
- exact map/graphics/sound conversion for both Gym puzzle variants;
- postgame leader phone/rematch/trade content.

These are kept separate so the Phase 5 state machine does not prematurely collapse later events.
