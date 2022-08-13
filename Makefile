export DJANGO_SETTINGS_MODULE=main.settings
DOCKER_IMAGE=honda-plug

venv:
	python3.10 -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black src
	venv/bin/isort src

format/check: venv
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose src --check
	venv/bin/isort --df -c src

migrations/check:
	venv/bin/python src/manage.py makemigrations --check --dry-run

migrate:
	venv/bin/python src/manage.py collectstatic --noinput

gunicorn:
	venv/bin/gunicorn src.main.wsgi:application --bind 0.0.0.0:8000 --pythonpath=src

tests: venv
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/dotenv ".env.test" && PYTHONPATH=src venv/bin/pytest src/tests

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/tests:
	 docker compose up -d db django
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
	docker compose -f docker-compose.yml up -d --build

docker/run/backup-db:
	docker exec -t honda-db-1 pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql

docker/run/client/epc-data:
	docker compose -f docker-compose.scripts.prod.yml up epc-data -d --build

docker/run/client/hondapartsnow:
	docker compose -f docker-compose.scripts.prod.yml up hondapartsnow -d --build

docker/run/client/amayama:
	docker compose -f docker-compose.scripts.prod.yml up amayama -d --build

docker/run/client/tegiwa:
	docker compose -f docker-compose.scripts.prod.yml up tegiwa -d --build

docker/run/client/clockwisemotion:
	docker compose -f docker-compose.scripts.prod.yml up clockwisemotion -d --build