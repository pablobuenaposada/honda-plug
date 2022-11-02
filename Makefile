DOCKER_IMAGE=honda-plug
TEST_ENV_VARS:=$(shell cat .env.test | xargs)

venv:
	python3.10 -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black src
	venv/bin/isort src
	venv/bin/flake8 src

format/check: venv
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose src --check
	venv/bin/isort --df -c src
	venv/bin/flake8 src

migrations/check:
	$(TEST_ENV_VARS) venv/bin/python src/manage.py makemigrations --check --dry-run

migrate:
	venv/bin/python src/manage.py collectstatic --noinput

gunicorn:
	venv/bin/gunicorn src.main.wsgi:application --bind 0.0.0.0:8000 --pythonpath=src

tests: venv
	venv/bin/pip install -r requirements-tests.txt
	$(TEST_ENV_VARS) PYTHONPATH=src venv/bin/pytest src/tests

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/tests:
	 docker compose up -d --force-recreate db django
	 docker exec $(DOCKER_IMAGE)-django-1 make tests

docker/format/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make format/check'

docker/migrations/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make migrations/check'

docker/run/shell:
	docker exec -it honda-django-1 bash

docker/run/prod:
	docker compose -f docker-compose.prod.yml up -d --build

docker/run/local:
	docker compose -f docker-compose.yml up --force-recreate -d --build

docker/run/backup-db:
	docker exec -t honda-db-1 pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql

docker/run/client/epc:
	docker compose -f docker-compose.scripts.prod.yml up epc -d --build
