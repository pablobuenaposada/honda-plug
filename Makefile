export DJANGO_SETTINGS_MODULE=main.settings

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

tests: venv
	venv/bin/pip install -r requirements-tests.txt
	PYTHONPATH=src venv/bin/pytest src/tests

docker/build:
	docker build --no-cache	--tag=honda .

docker/tests:
	 docker run honda /bin/sh -c 'make tests'

docker/format/check:
	 docker run honda /bin/sh -c 'make format/check'

docker/migrations/check:
	 docker run honda /bin/sh -c 'make migrations/check'