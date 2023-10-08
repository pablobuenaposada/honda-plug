DOCKER_IMAGE=honda-plug
TEST_ENV_VARS:=$(shell cat .env.test | xargs)

venv:
	python3.10 -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black src
	venv/bin/ruff src --fix

format/check: venv
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose src --check
	venv/bin/ruff src

migrations/check:
	$(TEST_ENV_VARS) venv/bin/python src/manage.py makemigrations --check --dry-run

migrate:
	venv/bin/python src/manage.py collectstatic --noinput

gunicorn:
	venv/bin/gunicorn src.main.wsgi:application --bind 0.0.0.0:8000 --pythonpath=src

certificate:
	sudo ufw allow 80/tcp
	sudo certbot certonly --standalone --cert-name hondaplug -d hondaplug.com
	sudo ufw delete allow 80/tcp

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
	docker exec -it honda-plug-django-1 bash

docker/run/prod:
	crontab $(shell pwd)/cron/cron
	docker compose -f docker-compose.prod.yml up --force-recreate -d --build

docker/run/local:
	docker compose -f docker-compose.yml up --force-recreate -d --build

# example: make docker/run/local/restore-db FILE=/dump_29-11-2022_14_23_27.sql PASSWORD=whatever
docker/run/local/restore-db:
	PGPASSWORD=$(PASSWORD) psql -U postgres -h localhost -d honda_plug_test -f $(FILE)
	PGPASSWORD=$(PASSWORD) psql -h localhost -U postgres -c 'SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '\''honda_plug_test'\'';'
	PGPASSWORD=$(PASSWORD) psql -h localhost -U postgres -c 'DROP DATABASE honda_plug_test;'
	PGPASSWORD=$(PASSWORD) psql -h localhost -U postgres -c 'ALTER DATABASE honda_plug RENAME TO honda_plug_test;'

docker/run/backup-db:
	docker exec -t honda-plug-db-1 pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql


