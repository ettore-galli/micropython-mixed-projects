
install:
	pip install .
	pip install ."[development]"
	pip install ."[micropython_deploy]"
	pip install ."[format]"
	pip install ."[lint]"
	pip install ."[test]"

lint:
	black micropython_rpi_theremin/ tests/ deploy/
	ruff check micropython_rpi_theremin/ tests/ deploy/
	mypy micropython_rpi_theremin/ tests/ deploy/

test:
	pytest tests/ 

all: lint test

micro-cleanup-all:
	mpremote run deploy/cleanup.py

micro: micro-cleanup-all
	mpremote fs cp micropython_rpi_theremin/main.py :main.py # || true
	mpremote fs cp micropython_rpi_theremin/typing.py :typing.py # || true
	mpremote fs mkdir collections # || true
	mpremote fs cp micropython_rpi_theremin/collections/abc.py :collections/abc.py # || true
	mpremote reset

