.PHONY: black black_check coverage isort isort_check lint mypy ruff safety unittests yamllint

help: ## display available commands with description
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

black:  ## run black
	black .

black-check:  ## run isort check
	black . --check

ruff:  ## run flake8
	 ruff vater tests

integration-tests:  ## run integration tests
	 pytest tests/integration_tests.py -s -vv

isort:  ## run isort
	isort .

isort-check:  ## run isort check
	isort . --check

lint: mypy ruff isort-check black-check ## run all linters

mypy:  ## run mypy
	mypy vater

safety:  ## run safety check
	safety check -r requirements.txt -r requirements-dev.txt

unit-tests:  ## run pytest with coverage and -s flag for debugging
	pytest --cov=vater tests/ -s -vv
