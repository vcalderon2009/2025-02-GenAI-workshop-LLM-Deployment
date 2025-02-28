.PHONY: init plan deploy validate help

###############################################################################
# PROJECT VARIABLES                                                           #
###############################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME := $(shell basename $(subst -,_,$(PROJECT_DIR)))

ENV ?= "prod"
ENV_DIRECTORY = $(PROJECT_DIR)/envs/$(ENV)

## Show the set of input parameters
show-params:
	@ printf "\n-------- GENERAL ---------------\n"
	@ echo "PROJECT_DIR:                       $(PROJECT_DIR)"
	@ echo "PROJECT_NAME:                      $(PROJECT_NAME)"
	@ echo "ENV:                               $(ENV)"
	@ echo "ENV_DIRECTORY:                     $(ENV_DIRECTORY)"
	@ printf "\n-----------------------\n"

###############################################################################
# MISCELLANEOUS COMMANDS                                                      #
###############################################################################

# -------------------- Functions for cleaning repository ----------------------

## Removes artifacts from the build stage, and other common Python artifacts.
clean: clean-build clean-pyc clean-test clean-terraform-lock

## Removes Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## Remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## Remove terraform lock files
clean-terraform-lock:
	find . -name '.terraform' -exec rm -fr {} +
	find . -name '.terraform.lock.hcl' -exec rm -fr {} +

## Remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

# -------------------- Functions for validating variables ---------------------

# Function to check whether environment variables are set.
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

###############################################################################
# TERRAFORM VALIDATION AND DEPLOYMENT                                         #
###############################################################################

## Initialize the Terraform plan
init: show-params clean
	@	cd $(ENV_DIRECTORY) && \
		terraform init --migrate-state

## Generate a speculative Terraform execution plan
plan: validate
	@	cd $(ENV_DIRECTORY) && \
		terraform plan

## Deploy the Terraform plan
deploy: show-params plan
	@	cd $(ENV_DIRECTORY) && \
		terraform apply -auto-approve

## Destro the Terraform plan
destroy: show-params init
	@	cd $(ENV_DIRECTORY) && \
		terraform destroy

## Validate Terraform execution plan
validate: init
	@	cd $(ENV_DIRECTORY) && \
		terraform validate

## Visualize the Terraform plan
graph: show-params
	@	cd $(ENV_DIRECTORY) && \
		terraform graph

## Show the Terraform plan
show-plan: init
	@	cd $(ENV_DIRECTORY) && \
		terraform show

###############################################################################
# Self Documenting Commands                                                   #
###############################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
