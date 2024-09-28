all_targets=micropython_rpi_theremin/ led_game/ ghost_detector/ tests/ deploy/

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
	export PYTHONPATH=./led_game; pytest tests/led_game 
	export PYTHONPATH=./ghost_detector; pytest tests/ghost_detector 

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

micro-cap: micro-cleanup-all micro-common
	mpremote fs cp micropython_rpi_theremin/main_cap.py :main.py 
	mpremote reset

ghost-detector: micro-cleanup-all micro-common
	mpremote fs cp ghost_detector/base.py :base.py 
	mpremote fs cp ghost_detector/ghost_detector_logic.py :ghost_detector_logic.py 
	mpremote fs cp ghost_detector/hardware_gd.py :hardware_gd.py 
	mpremote fs cp ghost_detector/main.py :main.py 
	mpremote reset

led-game: micro-cleanup-all micro-common
	mpremote fs cp led_game/base.py :base.py 
	mpremote fs cp led_game/hardware.py :hardware.py 
	mpremote fs cp led_game/game_engine.py :game_engine.py 
	mpremote fs cp led_game/main.py :main.py 
	mpremote reset