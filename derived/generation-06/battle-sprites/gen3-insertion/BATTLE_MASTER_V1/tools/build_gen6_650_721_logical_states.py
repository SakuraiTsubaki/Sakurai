#!/usr/bin/env python3
"""Build the Generation VI No.650-721 logical visual-state inventory.

This inventory is intentionally generation-scoped. It must not import later-game
forms into XY/ORAS. Archive/member coordinates remain a separate mapping layer.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


SPECIES = {
    650: "Chespin", 651: "Quilladin", 652: "Chesnaught", 653: "Fennekin",
    654: "Braixen", 655: "Delphox", 656: "Froakie", 657: "Frogadier",
    658: "Greninja", 659: "Bunnelby", 660: "Diggersby", 661: "Fletchling",
    662: "Fletchinder", 663: "Talonflame", 664: "Scatterbug", 665: "Spewpa",
    666: "Vivillon", 667: "Litleo", 668: "Pyroar", 669: "Flabébé",
    670: "Floette", 671: "Florges", 672: "Skiddo", 673: "Gogoat",
    674: "Pancham", 675: "Pangoro", 676: "Furfrou", 677: "Espurr",
    678: "Meowstic", 679: "Honedge", 680: "Doublade", 681: "Aegislash",
    682: "Spritzee", 683: "Aromatisse", 684: "Swirlix", 685: "Slurpuff",
    686: "Inkay", 687: "Malamar", 688: "Binacle", 689: "Barbaracle",
    690: "Skrelp", 691: "Dragalge", 692: "Clauncher", 693: "Clawitzer",
    694: "Helioptile", 695: "Heliolisk", 696: "Tyrunt", 697: "Tyrantrum",
    698: "Amaura", 699: "Aurorus", 700: "Sylveon", 701: "Hawlucha",
    702: "Dedenne", 703: "Carbink", 704: "Goomy", 705: "Sliggoo",
    706: "Goodra", 707: "Klefki", 708: "Phantump", 709: "Trevenant",
    710: "Pumpkaboo", 711: "Gourgeist", 712: "Bergmite", 713: "Avalugg",
    714: "Noibat", 715: "Noivern", 716: "Xerneas", 717: "Yveltal",
    718: "Zygarde", 719: "Diancie", 720: "Hoopa", 721: "Volcanion",
}

VIVILLON_PATTERNS = [
    "Icy Snow Pattern", "Polar Pattern", "Tundra Pattern", "Continental Pattern",
    "Garden Pattern", "Elegant Pattern", "Meadow Pattern", "Modern Pattern",
    "Marine Pattern", "Archipelago Pattern", "High Plains Pattern",
    "Sandstorm Pattern", "River Pattern", "Monsoon Pattern", "Savanna Pattern",
    "Sun Pattern", "Ocean Pattern", "Jungle Pattern", "Fancy Pattern",
    "Poké Ball Pattern",
]

FLOWER_COLORS = ["Red Flower", "Yellow Flower", "Orange Flower", "Blue Flower", "White Flower"]

FURFROU_FORMS = [
    "Natural Form", "Heart Trim", "Star Trim", "Diamond Trim", "Debutante Trim",
    "Matron Trim", "Dandy Trim", "La Reine Trim", "Kabuki Trim", "Pharaoh Trim",
]

SIZE_FORMS = ["Small Size", "Average Size", "Large Size", "Super Size"]

SOURCES = {
    "vivillon": "https://bulbapedia.bulbagarden.net/wiki/Vivillon_(Pok%C3%A9mon)",
    "gender": "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_with_gender_differences",
    "flabebe": "https://bulbapedia.bulbagarden.net/wiki/Flab%C3%A9b%C3%A9_(Pok%C3%A9mon)",
    "floette": "https://bulbapedia.bulbagarden.net/wiki/Floette_(Pok%C3%A9mon)",
    "florges": "https://bulbapedia.bulbagarden.net/wiki/Florges_(Pok%C3%A9mon)",
    "furfrou": "https://bulbapedia.bulbagarden.net/wiki/Furfrou_(Pok%C3%A9mon)",
    "aegislash": "https://bulbapedia.bulbagarden.net/wiki/Aegislash_(Pok%C3%A9mon)",
    "pumpkaboo": "https://bulbapedia.bulbagarden.net/wiki/Pumpkaboo_(Pok%C3%A9mon)",
    "gourgeist": "https://bulbapedia.bulbagarden.net/wiki/Gourgeist_(Pok%C3%A9mon)",
    "xerneas": "https://bulbapedia.bulbagarden.net/wiki/Xerneas_(Pok%C3%A9mon)",
    "zygarde": "https://bulbapedia.bulbagarden.net/wiki/Zygarde_(Pok%C3%A9mon)",
    "diancie": "https://bulbapedia.bulbagarden.net/wiki/Diancie_(Pok%C3%A9mon)",
    "hoopa": "https://bulbapedia.bulbagarden.net/wiki/Hoopa_(Pok%C3%A9mon)",
}

COLUMNS = [
    "national_dex", "species", "logical_state", "state_kind", "xy_scope",
    "oras_scope", "gen3_battle_target_required", "archive_mapping_status",
    "notes", "source_reference",
]


def state(name: str, kind: str, *, xy: str = "supported-gen6",
          oras: str = "supported-gen6", target: str = "yes", notes: str = "",
          source: str = "") -> dict[str, str]:
    return {
        "logical_state": name,
        "state_kind": kind,
        "xy_scope": xy,
        "oras_scope": oras,
        "gen3_battle_target_required": target,
        "archive_mapping_status": "unresolved",
        "notes": notes,
        "source_reference": source,
    }


def states_for(dex: int) -> list[dict[str, str]]:
    if dex == 666:
        return [state(x, "pattern", notes="All 20 Generation VI Vivillon patterns are distinct visual states.", source=SOURCES["vivillon"]) for x in VIVILLON_PATTERNS]
    if dex in (668, 678):
        return [state("Male", "gender", source=SOURCES["gender"]), state("Female", "gender", source=SOURCES["gender"])]
    if dex == 669:
        return [state(x, "flower-color", source=SOURCES["flabebe"]) for x in FLOWER_COLORS]
    if dex == 670:
        regular = [state(x, "flower-color", source=SOURCES["floette"]) for x in FLOWER_COLORS]
        regular.append(state(
            "Eternal Flower", "special-form",
            notes="Present in Generation VI game data but not legitimately obtainable in Generation VI; preserve as a data-defined visual state.",
            source=SOURCES["floette"],
        ))
        return regular
    if dex == 671:
        return [state(x, "flower-color", source=SOURCES["florges"]) for x in FLOWER_COLORS]
    if dex == 676:
        return [state(x, "trim", notes="Natural Form plus nine Generation VI trims; retain every distinct visual state.", source=SOURCES["furfrou"]) for x in FURFROU_FORMS]
    if dex == 681:
        return [
            state("Shield Forme", "battle-form", notes="Battle-visible form; requires an independent logical target.", source=SOURCES["aegislash"]),
            state("Blade Forme", "battle-form", notes="Battle-visible form; requires an independent logical target.", source=SOURCES["aegislash"]),
        ]
    if dex in (710, 711):
        src = SOURCES["pumpkaboo"] if dex == 710 else SOURCES["gourgeist"]
        return [state(x, "size-form", notes="Use Generation VI-era names Small/Average/Large/Super Size; later naming is not backported.", source=src) for x in SIZE_FORMS]
    if dex == 716:
        return [
            state("Neutral Mode", "mode", target="no", notes="Out-of-battle visual mode; retain as provenance/source state, not the canonical Gen III battle sprite.", source=SOURCES["xerneas"]),
            state("Active Mode", "mode", target="yes", notes="Xerneas appears in Active Mode in battles; canonical Gen III battle target.", source=SOURCES["xerneas"]),
        ]
    if dex == 718:
        return [state("50% Forme", "gen6-only-form", notes="Generation VI has only the 50% Forme. 10% and Complete Formes were introduced in Sun/Moon and are excluded.", source=SOURCES["zygarde"])]
    if dex == 719:
        return [
            state("Diancie", "base-form", source=SOURCES["diancie"]),
            state("Mega Diancie", "mega-evolution", xy="not-in-XY", oras="ORAS-only", notes="Mega Diancie was introduced in Omega Ruby and Alpha Sapphire.", source=SOURCES["diancie"]),
        ]
    if dex == 720:
        return [
            state("Hoopa Confined", "base-form", source=SOURCES["hoopa"]),
            state("Hoopa Unbound", "alternate-form", xy="not-in-XY", oras="ORAS-only", notes="Hoopa Unbound was introduced in ORAS; transformation uses the Prison Bottle.", source=SOURCES["hoopa"]),
        ]
    return [state("Default", "default")]


def build_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for dex in range(650, 722):
        for visual in states_for(dex):
            rows.append({"national_dex": dex, "species": SPECIES[dex], **visual})
    return rows


def validate(rows: list[dict[str, str | int]]) -> None:
    assert set(SPECIES) == set(range(650, 722))
    assert len(rows) == 125, len(rows)
    assert sum(row["gen3_battle_target_required"] == "yes" for row in rows) == 124
    assert sum(row["gen3_battle_target_required"] == "no" for row in rows) == 1
    assert len([r for r in rows if r["national_dex"] == 666]) == 20
    assert len([r for r in rows if r["national_dex"] == 670]) == 6
    assert len([r for r in rows if r["national_dex"] == 676]) == 10
    assert len([r for r in rows if r["national_dex"] == 681]) == 2
    assert len([r for r in rows if r["national_dex"] == 710]) == 4
    assert len([r for r in rows if r["national_dex"] == 711]) == 4
    assert [r["logical_state"] for r in rows if r["national_dex"] == 718] == ["50% Forme"]
    oras_only = [r for r in rows if r["oras_scope"] == "ORAS-only"]
    assert {(r["national_dex"], r["logical_state"]) for r in oras_only} == {
        (719, "Mega Diancie"), (720, "Hoopa Unbound")
    }


def render_csv(rows: list[dict[str, str | int]]) -> str:
    from io import StringIO
    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = build_rows()
    validate(rows)
    text = render_csv(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    print(f"PASS rows={len(rows)} battle_targets=124 source_only_states=1")
    print(f"sha256={digest}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
