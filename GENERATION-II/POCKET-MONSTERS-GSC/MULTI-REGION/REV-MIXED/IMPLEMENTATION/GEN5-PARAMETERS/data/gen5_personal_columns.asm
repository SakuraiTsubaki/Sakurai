; Generated local binaries come from tools/build_gen2_personal_tables.py.
; Each table is deliberately kept below one 16 KiB ROMX bank.

SECTION "Gen5 Personal Base Stats", ROMX
Gen5PersonalBaseStats::
	INCBIN "data/gen5/personal_columns/base_stats.bin"

SECTION "Gen5 Personal Types", ROMX
Gen5PersonalTypes::
	INCBIN "data/gen5/personal_columns/types.bin"

SECTION "Gen5 Personal Catch Rate", ROMX
Gen5PersonalCatchRate::
	INCBIN "data/gen5/personal_columns/catch_rate.bin"

SECTION "Gen5 Personal EV Yield", ROMX
Gen5PersonalEVYield::
	INCBIN "data/gen5/personal_columns/ev_yield.bin"

SECTION "Gen5 Personal Held Items", ROMX
Gen5PersonalHeldItems::
	INCBIN "data/gen5/personal_columns/held_items.bin"

SECTION "Gen5 Personal Gender", ROMX
Gen5PersonalGenderRatio::
	INCBIN "data/gen5/personal_columns/gender_ratio.bin"

SECTION "Gen5 Personal Hatch", ROMX
Gen5PersonalHatchCounter::
	INCBIN "data/gen5/personal_columns/hatch_counter.bin"

SECTION "Gen5 Personal Friendship", ROMX
Gen5PersonalBaseFriendship::
	INCBIN "data/gen5/personal_columns/base_friendship.bin"

SECTION "Gen5 Personal Growth", ROMX
Gen5PersonalGrowthRate::
	INCBIN "data/gen5/personal_columns/growth_rate.bin"

SECTION "Gen5 Personal Egg Groups", ROMX
Gen5PersonalEggGroups::
	INCBIN "data/gen5/personal_columns/egg_groups.bin"

SECTION "Gen5 Personal Abilities", ROMX
Gen5PersonalAbilities::
	INCBIN "data/gen5/personal_columns/abilities.bin"

SECTION "Gen5 Personal Escape Rate", ROMX
Gen5PersonalEscapeRate::
	INCBIN "data/gen5/personal_columns/escape_rate.bin"

SECTION "Gen5 Personal Form Route", ROMX
Gen5PersonalFormRoute::
	INCBIN "data/gen5/personal_columns/form_route.bin"

SECTION "Gen5 Personal Body Color", ROMX
Gen5PersonalBodyColor::
	INCBIN "data/gen5/personal_columns/body_color.bin"

SECTION "Gen5 Personal Base EXP", ROMX
Gen5PersonalBaseExp::
	INCBIN "data/gen5/personal_columns/base_exp_u16.bin"

SECTION "Gen5 Personal Height", ROMX
Gen5PersonalHeight::
	INCBIN "data/gen5/personal_columns/height.bin"

SECTION "Gen5 Personal Weight", ROMX
Gen5PersonalWeight::
	INCBIN "data/gen5/personal_columns/weight.bin"

SECTION "Gen5 Personal TMHM", ROMX
Gen5PersonalTMHM::
	INCBIN "data/gen5/personal_columns/tm_hm.bin"

SECTION "Gen5 Personal Tutor", ROMX
Gen5PersonalTutor::
	INCBIN "data/gen5/personal_columns/tutor.bin"
