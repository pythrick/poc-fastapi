SHELL := /bin/bash
.PHONY: all test init lint build run down lock clean

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

all: all test init lint build run down lock clean

test:
	docker-compose run web pytest

init:
	cp .sample.conf local.conf
	cp .sample.env .env
	docker-compose build
	docker-compose run web pre-commit install -t pre-commit
	docker-compose run web pre-commit install -t pre-push

lint:
	docker-compose run web isort .
	docker-compose run web black .
	docker-compose run web flake8
	docker-compose run web mypy
	sudo chown -R $(USER). .

build:
	docker-compose build

run:
	docker-compose up

down:
	docker-compose down

lock:
	docker-compose run web poetry lock

clean:
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
