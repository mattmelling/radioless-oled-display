.PHONY: install
install:
	apt-get install -y python3-setuptools libopenjp2-7 xfonts-terminus fonts-dejavu
	pip3 install .
	cp radioless-oled-display.service /etc/systemd/system/
	systemctl enable radioless-oled-display.service
	systemctl daemon-reload
