
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

micro:
	mpremote fs cp micropython_rpi_theremin/main.py :main.py
	mpremote fs cp micropython_rpi_theremin/typing.py :typing.py
	mpremote reset

