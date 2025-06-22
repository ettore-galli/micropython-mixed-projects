all_targets=micropython_rpi_theremin/ led_game/ deploy/ rpi_client/ control_demo/ tests/

install:
	pip install .
	pip install ."[development]"
	pip install ."[micropython_deploy]"
	pip install ."[format]"
	pip install ."[lint]"
	pip install ."[test]"

lint:
	black $(all_targets)
	ruff check $(all_targets) --exclude control_demo/microdot
	mypy $(all_targets) --exclude 'microdot'

make lint-fix:
	black $(all_targets)
	ruff check $(all_targets) --fix
	mypy $(all_targets)

test:
	export PYTHONPATH=ghost_detector:led_game:control_demo; pytest tests 

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

led-game: micro-cleanup-all micro-common
	mpremote fs cp led_game/base.py :base.py 
	mpremote fs cp led_game/hardware.py :hardware.py 
	mpremote fs cp led_game/game_engine.py :game_engine.py 
	mpremote fs cp led_game/main.py :main.py 
	mpremote reset

rpi-client-config:
	mpremote fs cp rpi_client/config.json :config.json 
	mpremote reset

rpi-client-code: micro-cleanup-all micro-common
	mpremote fs cp rpi_client/main.py :main.py 
	mpremote fs mkdir rpi_client 
	mpremote fs cp rpi_client/base.py :rpi_client/base.py 
	mpremote fs cp rpi_client/config_reader.py :rpi_client/config_reader.py 
	mpremote fs cp rpi_client/ssd1306.py :rpi_client/ssd1306.py 
	mpremote fs cp rpi_client/display.py :rpi_client/display.py
	mpremote reset

rpi-client: rpi-client-code rpi-client-config
	
display-demo: micro-cleanup-all micro-common
	mpremote fs cp rpi_client/display_demo.py :main.py 
	mpremote fs mkdir rpi_client 
	mpremote fs cp rpi_client/base.py :rpi_client/base.py 
	mpremote fs cp rpi_client/ssd1306.py :rpi_client/ssd1306.py 
	mpremote fs cp rpi_client/display.py :rpi_client/display.py
	mpremote fs cp rpi_client/display_big_text.py :rpi_client/display_big_text.py
	mpremote reset

partial_deploy_warning:
	@echo ------------------------------------------------
	@echo "WARNING! Deployed only code files; cleanup and" 
	@echo "run full deploy in case of dirty files"
	@echo ------------------------------------------------

microdot:
	deploy/safe_putdir.sh microdot
	mpremote fs cp control_demo/microdot/__init__.py :microdot/__init__.py 
	mpremote fs cp control_demo/microdot/microdot.py :microdot/microdot.py 

control-demo-web:
	deploy/safe_putdir.sh web
	mpremote fs cp control_demo/web/index.html :web/index.html 

control-demo-code:
	mpremote fs cp control_demo/control_demo_base.py :control_demo_base.py 
	mpremote fs cp control_demo/control_demo_hardware.py :control_demo_hardware.py 
	mpremote fs cp control_demo/control_demo_engine.py :control_demo_engine.py 
	mpremote fs cp control_demo/control_demo_server.py :control_demo_server.py 
	mpremote fs cp control_demo/control_demo_data.py :control_demo_data.py 
	mpremote fs cp control_demo/main.py :main.py 

control-demo-data-env:
	deploy/safe_putdir.sh data

control-demo-dev: \
	control-demo-web \
	control-demo-code

	@make partial_deploy_warning
	mpremote reset

control-demo-full: \
	micro-cleanup-all \
	micro-common \
	microdot \
	control-demo-web \
	control-demo-code \
	control-demo-data-env

	mpremote reset