export PROJECTNAME=$(shell basename "$(PWD)")
PYTHON_INTERPRETER = python3

.SILENT: ;               # no need for @

requirements: ## Install Python Dependencies
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

clean: ## Delete all compiled Python files
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint: black ## Lint using flake8
	flake8 data --exclude raw

black: ## Runs black for code formatting
	black data --exclude raw

run-ingest: ## Runs Data Ingester
	cd data && python3 data_ingester.py

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo