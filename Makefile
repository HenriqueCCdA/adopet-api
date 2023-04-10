SHELL := /bin/bash

PHONNY: init
init:
	@python -m venv .venv
	@source .venv/bin/activate
	@.venv/bin/python -m pip -U
	@pip install pip-tools
	@pip-sync requirements.txt requirements.dev.txt --pip-args --no-deps
	@precommit install
	@cp .env-sample .env


PHONNY: create_admin
create_admin:
	@.venv/bin/python manage.py createsuperuser

PHONNY: docker_up_db
docker_up_db:
	@docker compose up -d database


PHONNY: docker_build
docker_build:
	@docker compose build

PHONNY: docker_build_and_up_dev
docker_build_and_up:
	@docker compose build
	@docker compose up -d

PHONNY: docker_up
docker_up:
	@docker compose up -d

PHONNY: docker_down_dev
docker_down:
	@docker compose down

PHONNY: docker_makemigrations
docker_makemigrations:
	@docker compose exec app ./manage.py makemigrations

PHONNY: docker_migrate
docker_migrate:
	@docker compose exec app ./manage.py migrate

PHONNY: docker_create_admin
docker_create_admin:
	@docker compose exec -it app ./manage.py createsuperuser

# Docker pytest

PHONNY: docker_pytest
docker_pytest:
	@docker compose run app pytest -s

#
PHONNY: linter
linter:
	@.venv/bin/pflake8

PHONNY: fmt
fmt:
	@.venv/bin/isort adopet
	@.venv/bin/black adopet

PHONNY: mkvenv
mkvenv:
	@python -m venv .venv --upgrade-deps


clean:
	@find ./web_server/ -name '*.pyc' -exec rm -f {} \;
	@find ./web_server/ -name '__pycache__' -exec rm -rf {} \;
	@find ./web_server/ -name '*.mo' -exec rm -rf {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf htmlcov
