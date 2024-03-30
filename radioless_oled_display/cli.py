import os
import time

from luma.core.render import canvas
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

from .asterisk import AsteriskManager
from .renderer import Renderer
from .astdb import AllstarDatabase

def get_device():
    if os.environ.get('LUMA_DEVICE', 'pygame') == 'ssd1306':
        serial = i2c(port=1, address=0x3c)
        return ssd1306(serial_interface=serial, width=128, height=64)

    from luma.emulator.device import pygame
    return pygame(width=128, height=64)

def main():
    print('Connecting to Asterisk')
    ast = AsteriskManager(hostname=os.environ.get('ASTERISK_HOSTNAME', 'localhost'),
                          port=int(os.environ.get('ASTERISK_PORT', '5038')),
                          username=os.environ.get('ASTERISK_USERNAME', 'admin'),
                          password=os.environ.get('ASTERISK_PASSWORD', 'password'))
    ast.start()
    astdb = AllstarDatabase(os.environ.get('ASTDB', '/var/log/asterisk/astdb.txt'))

    print('Acquiring device')
    device = get_device()
    device.show()

    print('Starting render loop')
    renderer = Renderer()
    renderer.set_callsign(f'{os.environ.get("ASL_CALLSIGN", "")} {os.environ.get("ASL_NODE", "")}')

    while True:
        with canvas(device) as draw:

            if ast.rxnode is not None:
                node = astdb[ast.rxnode]
                if node is not None:
                    callsign, frequency, location = node
                    renderer.set_info_text(f'{callsign} - {location}')
                else:
                    renderer.set_info_text(None)
            else:
                renderer.set_info_text(None)

            renderer.set_tx(ast.tx)
            renderer.set_rx(ast.rx)
            renderer.set_calling_node(ast.rxnode)

            renderer.render(draw)
            time.sleep(0.1)
