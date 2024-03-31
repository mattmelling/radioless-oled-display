import os
import time

from datetime import datetime

from luma.core.render import canvas
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

from .asterisk import AsteriskManager
from .astdb import AllstarDatabase
from .qso import RxScreen, TxScreen
from .idle import IdleScreen, NoConnectionScreen
from .screensaver import ScreenSaver

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

    tx = None
    rx = None
    idle = IdleScreen(ast)
    nocon = NoConnectionScreen(ast)
    screensaver = None

    last_activity = datetime.now()
    screensaver_timeout = 60

    while True:
        with canvas(device) as draw:
            since_last = (datetime.now() - last_activity).seconds
            if ast.tx:
                if tx is None:
                    tx = TxScreen(ast)
                tx.render(draw)
                last_activity = datetime.now()
                continue
            else:
                tx = None

            if ast.rx:
                if rx is None:
                    rx = RxScreen(ast, astdb)
                rx.render(draw)
                last_activity = datetime.now()
                continue
            else:
                rx = None

            if since_last > screensaver_timeout and screensaver is None:
                screensaver = ScreenSaver()
            elif since_last < screensaver_timeout:
                screensaver = None

            if screensaver is not None:
                screensaver.render(draw)
                continue

            if ast.numlinks > 0:
                idle.render(draw)
            else:
                nocon.render(draw)

            time.sleep(0.1)
