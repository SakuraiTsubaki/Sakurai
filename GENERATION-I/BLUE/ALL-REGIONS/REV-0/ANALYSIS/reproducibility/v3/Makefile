PYTHON ?= python3
.PHONY: analyze verify
analyze:
	$(PYTHON) scripts/build_v3_analysis.py
verify: analyze
	$(PYTHON) tests/verify_v3.py
