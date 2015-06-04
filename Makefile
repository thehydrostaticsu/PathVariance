PYTHON ?= python
export PYTHONPATH := src

.DEFAULT_GOAL := help

.PHONY: help test verify run clean

help:  ## Show this help
