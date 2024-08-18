all_targets=micropython_rpi_theremin/ led_ui/ tests/ deploy/

install:
	pip install .
	pip install ."[development]"
	pip install ."[micropython_deploy]"
	pip install ."[format]"
	pip install ."[lint]"
	pip install ."[test]"

lint:
	black $(all_targets)
	ruff check $(all_targets)
	mypy $(all_targets)

test:
	pytest tests/ 

all: lint test

micro-cleanup-all:
	mpremote run deploy/cleanup.py

micro-common: 
	mpremote fs cp python_dummies/typing.py :typing.py 
	mpremote fs mkdir collections 
	mpremote fs cp python_dummies/collections/abc.py :collections/abc.py 

micro-theremin: micro-cleanup-all micro-common
	mpremote fs cp micropython_rpi_theremin/main.py :main.py 
	mpremote reset
	
micro-pwm: micro-cleanup-all micro-common
	mpremote fs cp micropython_rpi_theremin/main_pwm.py :main.py 
	mpremote reset

led-ui: micro-cleanup-all micro-common
	mpremote fs cp led_ui/main.py :main.py 
	mpremote reset