all_targets=micropython_rpi_theremin/ led_game/ tests/ deploy/

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
	export PYTHONPATH=./led_game; pytest tests/ 

all: lint test

micro-cleanup-all:
	mpremote run deploy/cleanup.py

micro-common: 
	mpremote fs cp python_dummies/typing.py :typing.py 
	mpremote fs cp python_dummies/abc.py :abc.py 
	mpremote fs mkdir collections 
	mpremote fs cp python_dummies/collections/abc.py :collections/abc.py 

micro-theremin: micro-cleanup-all micro-common
	mpremote fs cp micropython_rpi_theremin/main.py :main.py 
	mpremote reset
	
micro-pwm: micro-cleanup-all micro-common
	mpremote fs cp micropython_rpi_theremin/main_pwm.py :main.py 
	mpremote reset

led-game: micro-cleanup-all micro-common
	mpremote fs cp led_game/base.py :base.py 
	mpremote fs cp led_game/hardware.py :hardware.py 
	mpremote fs cp led_game/game_engine.py :game_engine.py 
	mpremote fs cp led_game/main.py :main.py 
	mpremote reset