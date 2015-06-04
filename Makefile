PYTHON ?= python
export PYTHONPATH := src

.DEFAULT_GOAL := help

.PHONY: help test verify run clean

help:  ## Show this help
	@echo "PathVariance targets:"
	@echo "  make test    run the unittest suite"
