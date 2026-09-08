PYTHON ?= python3
CATALOG ?= rom_catalog.template.json
OUTPUT ?= output

.PHONY: all verify roundtrip audit candidates addresses equivalence pointers ownership

all:
	$(PYTHON) tools/run_full_pipeline.py --catalog $(CATALOG) --output $(OUTPUT)

verify:
	$(PYTHON) tools/verify_outputs.py --catalog $(CATALOG) --output $(OUTPUT)

roundtrip:
	$(PYTHON) tools/lossless_roundtrip.py --catalog $(CATALOG) --report $(OUTPUT)/MULTI-REGION/REV-MIXED/ROM-REPRODUCIBILITY/lossless_roundtrip_report.json

audit:
	$(PYTHON) tools/crystal_rom_audit.py --catalog $(CATALOG) --output $(OUTPUT)

candidates:
	$(PYTHON) tools/scan_candidates.py --catalog $(CATALOG) --output $(OUTPUT)

addresses:
	$(PYTHON) tools/address_map.py --catalog $(CATALOG) --output $(OUTPUT)

equivalence:
	$(PYTHON) tools/cross_version_equivalence.py --catalog $(CATALOG) --output $(OUTPUT)

pointers:
	$(PYTHON) tools/pointer_sweep_summary.py --catalog $(CATALOG) --output $(OUTPUT)

ownership:
	$(PYTHON) tools/seed_bank_ownership.py --catalog $(CATALOG) --roles upstream_bank_roles.csv --output $(OUTPUT)
	$(PYTHON) tools/seed_page_ownership.py --catalog $(CATALOG) --roles upstream_bank_roles.csv --output $(OUTPUT)
