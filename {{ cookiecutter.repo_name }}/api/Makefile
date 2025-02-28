
###############################################################################
# GLOBALS                                                                     #
###############################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME := $(shell basename $(shell dirname $(subst -,_,$(PROJECT_DIR))))
PROJECT_TASK_DIR = "$(PROJECT_DIR)/assets"
PYTHON_INTERPRETER = python
REQUIREMENTS_FILE = $(PROJECT_DIR)/requirements.txt
REQUIREMENTS_DEPLOYMENT_FILE = $(PROJECT_DIR)/requirements-deploy.txt

LOCAL_DEVELOPMENT_DIR_PATH="$(PROJECT_DIR)/assets"

INPUT_APP_PORT=8000
OUTPUT_APP_PORT=8000
APP_WEBSERVER_URL="http://localhost:$(INPUT_APP_PORT)"

ENV ?= "prod"
APPLICATION_NAME={{ cookiecutter.application_name }}
REGION_NAME=us-west-2
DOCKER_PLATFORM=linux/amd64


###############################################################################
# MISCELLANEOUS COMMANDS                                                      #
###############################################################################

# -------------------- Functions for cleaning repository ----------------------

## Removes artifacts from the build stage, and other common Python artifacts.
clean: clean-pyc clean-build clean-test

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

## Remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

###############################################################################
# PROJECT-SPECIFIC COMMANDS                                                   #
###############################################################################

## Show the set of input parameters
show-params:
	@ printf "\n-------- GENERAL ---------------\n"
	@ echo "PROJECT_DIR:                       $(PROJECT_DIR)"
	@ echo "PROJECT_NAME:                      $(PROJECT_NAME)"
	@ echo "REQUIREMENTS_FILE:                 $(REQUIREMENTS_FILE)"
	@ echo "REQUIREMENTS_DEPLOYMENT_FILE:      $(REQUIREMENTS_DEPLOYMENT_FILE)"
	@ echo "LOCAL_DEVELOPMENT_DIR_PATH:        $(LOCAL_DEVELOPMENT_DIR_PATH)"
	@ echo "ENV:                               $(ENV)"
	@ echo "REGION_NAME:                       $(REGION_NAME)"
	@ printf "\n-----------------------\n"

## Upgrade pip
pip-upgrade:
	@	pip install --upgrade pip

## Create Poetry lock file
poetry-create-lock-file:
	@	poetry lock

## Create package requirements file
poetry-create-requirements-file:
	@	poetry export \
		-f requirements.txt \
		--output $(REQUIREMENTS_FILE) \
		--without-hashes

## Install dependencies of the project
poetry-install-dependencies:
	@	poetry config virtualenvs.create false && \
		poetry install --no-interaction --no-ansi --no-root

## Clean Docker images
docker-prune:
	@	docker system prune -f

###############################################################################
# APP-SPECIFIC COMMANDS                                                       #
###############################################################################

API_DOCKER_PROJECT_NAME="$(PROJECT_NAME)"
API_SERVICE_NAME="api"

## App - Build Docker image
app-build: docker-prune
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(API_DOCKER_PROJECT_NAME) \
		build $(API_SERVICE_NAME)

## App - Run the API service
app-start: app-build app-stop
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		HUGGINGFACE_API_TOKEN=$(HUGGINGFACE_API_TOKEN) \
		docker compose \
		--project-name $(API_DOCKER_PROJECT_NAME) \
		up -d $(API_SERVICE_NAME)

## App - Stop the API service
app-stop:
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(API_DOCKER_PROJECT_NAME) \
		down $(API_SERVICE_NAME)
	@	$(MAKE) docker-prune

## App - Login
app-login:
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(API_DOCKER_PROJECT_NAME) \
		exec $(API_SERVICE_NAME) \
		/bin/zsh

## Open API in web browser
api-web:
	@	python -m webbrowser "$(APP_WEBSERVER_URL)/docs"

###############################################################################
# LOCAL DEVELOPMENT-SPECIFIC COMMANDS                                         #
###############################################################################

LOCAL_DEV_DOCKER_PROJECT_NAME="$(PROJECT_NAME)_local_dev"
LOCAL_DEV_SERVICE_NAME="local-dev"

## App - Build Docker image
docker-local-dev-build: docker-prune
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(LOCAL_DEV_DOCKER_PROJECT_NAME) \
		build $(LOCAL_DEV_SERVICE_NAME)

## App - Run the API service
docker-local-dev-start: docker-local-dev-build docker-local-dev-stop
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(LOCAL_DEV_DOCKER_PROJECT_NAME) \
		up -d $(LOCAL_DEV_SERVICE_NAME)

## App - Stop the API service
docker-local-dev-stop:
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(LOCAL_DEV_DOCKER_PROJECT_NAME) \
		down $(LOCAL_DEV_SERVICE_NAME)
	@	$(MAKE) docker-prune

## App - Login
docker-local-dev-login:
	@	cd $(LOCAL_DEVELOPMENT_DIR_PATH) && \
		docker compose \
		--project-name $(LOCAL_DEV_DOCKER_PROJECT_NAME) \
		exec $(LOCAL_DEV_SERVICE_NAME) \
		/bin/zsh

###############################################################################
# Unit Tests and Code checking                                                #
###############################################################################

## Run all Python unit tests with verbose output and logs
test:
	python -m pytest -v -s

## Stops both the API service and the local development service
all-stop: app-stop docker-local-dev-stop
	@	echo "All services are down"

## Starts both the API service and the local development service
all-start: app-start docker-local-dev-start
	@	echo "All services are up!"


###############################################################################
# DOCKER IMAGE BUILD AND DEPLOYMENT                                           #
###############################################################################

## Install dependencies for deploying the Docker image
deployment-install-dependencies:
	@	$(PYTHON_INTERPRETER) -m pip install -r $(REQUIREMENTS_DEPLOYMENT_FILE)

## Build the Deployment image
deployment-image-build: show-params docker-prune deployment-install-dependencies
	@	$(PYTHON_INTERPRETER) "$(PROJECT_TASK_DIR)/docker_push.py" \
		--push "False" \
		--remove-image "False" \
		--application $(APPLICATION_NAME) \
		--environment-name $(ENV) \
		--region-name $(REGION_NAME) \
		--platform $(DOCKER_PLATFORM)
	@	$(MAKE) docker-prune

## Build and push Docker image to registry
deployment-image-push: show-params docker-prune deployment-install-dependencies
	@	$(PYTHON_INTERPRETER) "$(PROJECT_TASK_DIR)/docker_push.py" \
		--push "True" \
		--remove-image "True" \
		--application $(APPLICATION_NAME) \
		--environment-name $(ENV) \
		--region-name $(REGION_NAME) \
		--platform $(DOCKER_PLATFORM)
	@	$(MAKE) docker-prune


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

TARGET_MAX_CHAR_NUM=35

## Show help with `make help`
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
		-v indent=$(TARGET_MAX_CHAR_NUM) \
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
