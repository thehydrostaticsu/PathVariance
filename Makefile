PYTHON ?= python
export PYTHONPATH := src

.DEFAULT_GOAL := help

.PHONY: help test verify run clean

help:  ## Show this help
	@echo "PathVariance targets:"
	@echo "  make test    run the unittest suite"
	@echo "  make verify  run the quality gate in scripts/verify.py"
	@echo "  make run     run the full report against the sample export"
	@echo "  make clean   remove Python caches and build artifacts"

test:  ## Run the test suite
	$(PYTHON) -m unittest discover -s tests -v

verify:  ## Run the quality gate
	$(PYTHON) scripts/verify.py

run:  ## Run the report against the sample export
