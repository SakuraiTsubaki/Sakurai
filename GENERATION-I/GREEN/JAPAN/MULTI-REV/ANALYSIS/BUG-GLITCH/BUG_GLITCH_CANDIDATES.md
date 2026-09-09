# Bug / glitch / anomaly candidate ledger

This ledger separates confirmed revision behavior from shared candidate bugs that still require reproduction.

| ID | Area | Revisions | Classification | Evidence / next validation |
|---|---|---|---|---|
| GRN-REV-HAZE-001 | Haze / status handling | Rev0 vs RevA | confirmed revision logic fix-shaped change | Rev A adds Freeze to old-status mask used to invalidate selected move after Haze clears status. Reproduce with frozen target + Haze turn-order test. |
| GRN-REV-TRAP-001 | Battle Core / trapping move | Rev0 vs RevA | confirmed revision behavior change | Rev A writes `CANNOT_MOVE` when enemy trapping state prevents player action. Build scripted Wrap/Bind test in both revisions. |
| GRN-REV-MENU-001 | Battle item menu | RevA only | confirmed state-clear addition | Rev A clears `wMenuItemToSwap`; test stale item-swap state before/after battle item menu entry. |
| GRN-REV-SERIAL-001 | serial transfer | Rev0 vs RevA | confirmed structural revision change | 18-byte Rev0-only receive redirection block removed and serial2 routine group reordered. Link-cable regression test required. |
| GRN-REV-CORRUPT-001 | cable club | Rev0 only | confirmed removed guard/error path | Rev0 trainer-name `'Ａ'` corruption check + fatal warning loop removed in RevA. Determine reachable trigger with crafted serial packet. |
| GRN-CAND-CABLE-001 | cable club enemy data buffer clear | both | source-annotated bug candidate | Source says `$13B` clear length does not reach `wTrainerHeaderPtr`, leaving buffer data. Verify exact WRAM bytes across repeated exchanges. |
| GRN-CAND-SERIAL-002 | unused serial helper | Rev0 only | source-annotated dead/buggy code | `UnusedSerialFunction` contains source comment `bug: fallthrough`; function removed in RevA. Confirm no callers in symbol/xref pass. |
| GRN-CAND-LINK-003 | trapping move + Metronome/Mirror Move | both | source-annotated desync candidate | Source says missing MIRROR MOVE check might cause link desync. Reproduce with two-instance deterministic link test. |
| GRN-INTENT-RST-001 | RST38 / low vectors | both | intentional unreachable anomaly | RST38 jumps to `$F080` echo RAM; source labels vectors unused. Keep documented; do not change without proving reachability. |

## Rule for later fixes

A candidate moves to CONFIRMED only after: (1) static path is understood, (2) a reproducible input/state is recorded, and (3) Rev0/RevA behavior is compared. Any patch should preserve an unmodified reference path and include a regression test.
