CONDA_ENV ?= sage-diff
CONDA_BASE := $(shell conda info --base)
CONDA_ENV_PREFIX := $(CONDA_BASE)/envs/$(CONDA_ENV)
ENV_PATH := $(CONDA_ENV_PREFIX)/bin:$(PATH)
PYTHON := $(CONDA_ENV_PREFIX)/bin/python

.PHONY: env env-update lint python test test-one

env:
	@conda env create -f environment.yml

env-update:
	@conda env update -n $(CONDA_ENV) -f environment.yml

python:
	@PATH="$(ENV_PATH)" "$(PYTHON)"

lint:
	@PATH="$(ENV_PATH)" ruff check src tests

test:
	@PATH="$(ENV_PATH)" "$(PYTHON)" -m pytest

test-one:
	@PATH="$(ENV_PATH)" "$(PYTHON)" -m pytest $(TEST)
