.DEFAULT_GOAL := help

.PHONY: init
init: ## Setup the requirements
	$(info --- Setup ---)
	@poetry install

.PHONY: run
run: ## Run the code
	$(info --- Python Run ---)
	@poetry run python -m src.main

.PHONY: style
style: init ## Run check
	$(info -- Check Python ruff and fix the issues --)
	@poetry run ruff check --fix src/

.PHONY: tests
tests: init ## Run tests
	$(info --- Python Tests ---)
	@poetry run python -m pytest

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
