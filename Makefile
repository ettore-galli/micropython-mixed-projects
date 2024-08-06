
install:
	pip install .
	pip install ."[development]"
	pip install ."[micropython_deploy]"
	pip install ."[format]"
	pip install ."[lint]"
	pip install ."[test]"

lint:
	black micropython_rpi_theremin/ tests/  
	ruff check micropython_rpi_theremin/ tests/ 
	mypy micropython_rpi_theremin/ tests/ 

test:
	pytest tests/ 

all: lint test

micro-del:

	mpremote fs rm collections/abc.py || true
	mpremote fs rmdir collections || true
	mpremote fs rm main.py || true
	mpremote fs rm typing.py || true

micro: micro-del
	mpremote fs cp micropython_rpi_theremin/main.py :main.py || true
	mpremote fs cp micropython_rpi_theremin/typing.py :typing.py || true
	mpremote fs mkdir collections || true
	mpremote fs cp micropython_rpi_theremin/collections/abc.py :collections/abc.py || true
	mpremote reset

