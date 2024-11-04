sketch=Blink/Blink.ino
port=/dev/cu.usbmodem11401
fully_qualified_board_name=arduino:mbed_rp2040:pico

deploy:
	arduino-cli compile --upload --verbose \
		--fqbn $(fully_qualified_board_name) \
		$(sketch) \
		--port $(port)


monitor:
	arduino-cli monitor --port $(port)