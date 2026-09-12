# Pocket Monsters Green — disassembly work baseline

Date: 2026-09-09

## Scope

The local research package covers both uploaded Japanese Green revisions, 32 banks each (64 bank images total). It has two layers:

1. **Linear LR35902 listing** — every ROM byte is visited in bank/address order for audit navigation. This intentionally does not claim every byte is executable code.
2. **Lossless byte layer** — local-only reversible source used to prove complete byte coverage and round-trip identity.

The local lossless layer rebuilt both source ROMs byte-for-byte and matched their original SHA-1 values. Verification rebuild binaries were deleted after comparison.

## Semantic layer

The exact-hash `Narishma-gb/pokegreen` disassembly is used as a structural/symbol reference for code/data boundaries, named functions, tables and revision conditionals. Deep Rev0/RevA audits currently cover banks `00`, `01`, `04`, `09`, and `0F`.

A major result is that large raw byte-diff counts do not equal the amount of unique logic change. Small source edits in ROM0, bank1 and Battle Core relocate later labels and therefore alter many call/jump/pointer operands across otherwise unchanged banks.

## Repository policy

This repository stores the reusable analysis tool, manifests/classification and reports. It does **not** store uploaded ROM binaries or the local byte-exact reversible ROM dump/listing layer.

See `ANALYSIS/BANK-SURVEY/BANK_AUDIT_TRACKER.csv` and the per-bank deep audit reports for the current semantic status.
