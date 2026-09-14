# GSCRGBY project principles

## Goal

Reconstruct Generation II Kanto inside a Generation I RGBY engine and data model. The target is not a graphical reskin and not a restoration of Generation I Kanto. Generation II-era Kanto geography, changed routes, removed or added facilities, buildings, interiors, NPC roles, and gameplay meaning are preserved, while representation and implementation follow Generation I constraints and conventions.

## Engine-first reverse port

Generation II data is not copied directly. Maps, tilesets, blocks, collisions, warps, objects, scripts, events, text, sprites, and storage layouts are reinterpreted into Generation I-compatible forms. When an exact visual copy conflicts with Generation I limits, preserve player-facing structure, navigation, function, and recognition before pixel identity.

## Map policy

Do not shrink project maps merely to fit existing data. Expansion is permitted. If a larger map, tileset, block set, event set, or object set risks overlapping existing ROM data, locate and allocate free banks or otherwise extend safely. Any structural adjustment must preserve the Generation II-era spatial role and connectivity of the place.

## Content preservation

Generation I/II differences are content, not errors. Places removed by Generation II remain removed unless a separate integrated event requires an explicit additional representation. New Generation II facilities and routes are retained and re-expressed in Generation I style. RGBY and GSC version differences are tracked explicitly rather than collapsed into one representative version.

## Workflow

Work region by region: source analysis, tile/block mapping, map reconstruction, collision, connections and warps, NPC/object placement, event conversion, then testing. Prefer proving the full pipeline on simpler roads or towns before expanding to complex cities and dungeons. Automate repetitive extraction, coordinate normalization, and mapping where useful, but keep design judgments explicit.

## Validation

A map is not complete because it renders. Test movement, collision, entrances, exits, boundary transitions, spawn coordinates, NPC placement, event flags, one-time triggers, and full progression order. Document conversions and exceptions so the same rule is not rediscovered repeatedly.
