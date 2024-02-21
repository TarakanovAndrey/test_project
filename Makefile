install:
	poetry install

dev:
	poetry run flask --app balance_calc:app --debug run

PORT ?= 8000

start:
	poetry run gunicorn -w 2 -k gevent --worker-connections 1000 -b 0.0.0.0:$(PORT) balance_calc:app

lint:
	poetry run flake8 balance_calc

test:
	poetry run pytest
