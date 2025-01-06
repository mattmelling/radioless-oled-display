.PHONY: install
install:
	mkdir -p /opt/radioless-oled-display
	pip3 install --target /opt/radioless-oled-display .
	cp radioless-oled-display.service /etc/systemd/system/
	systemctl enable radioless-oled-display.service
	systemctl daemon-reload
	systemctl restart radioless-oled-display
