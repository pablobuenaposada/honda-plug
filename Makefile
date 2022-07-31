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
	PYTHONPATH=src venv/bin/pytest src/tests

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/tests:
	 docker compose up -d db django
	 docker exec honda-django-1 make tests

docker/format/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make format/check'

docker/migrations/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make migrations/check'

docker/run/shell:
	docker exec -it honda_django_1 bash

docker/run/prod:
	docker-compose -f docker-compose.prod.yml up --build