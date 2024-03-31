import os
import random

try:
    import importlib_resources as resources
except ModuleNotFoundError:
    import importlib.resources as resources

from datetime import datetime

from PIL import Image

from . import images
from .screen import Screen
from .text import Text

class ScreenSaver(Screen):
    def __init__(self):
        Screen.__init__(self)
        self._screen = random.choice([
            TimeScreenSaver,
            CallsignScreenSaver,
            LogoScreenSaver
        ])()

    def render(self, draw):
        self._screen.render(draw)

class BouncingTextScreenSaver(Screen):
    def __init__(self, text):
        Screen.__init__(self)
        self._x = 1
        self._y = 1
        self._font = self.fonts['DejaVu Sans Mono', 24]
        self._text = text
        x, y, self._lx, self._ly = self._font.getbbox(self._text)
        self._dx = -1
        self._dy = -1

    def render(self, draw):
        Screen.render(self, draw)

        if self._x <= 0 or (self._x + self._lx) >= draw.im.size[0]:
            self._dx *= -1

        if self._y <= 0 or (self._y + self._ly) >= draw.im.size[1]:
            self._dy *= -1

        self._x += self._dx
        self._y += self._dy

        self.add_renderer('text', Text(self._text, self._font, (self._x, self._y)))

class TimeScreenSaver(BouncingTextScreenSaver):
    def __init__(self):
        BouncingTextScreenSaver.__init__(self, ' ' * 5)

    def update(self):
        self._text = datetime.now().strftime('%H:%M')

class CallsignScreenSaver(BouncingTextScreenSaver):
    def __init__(self):
        BouncingTextScreenSaver.__init__(self, os.environ.get('ASL_CALLSIGN', ''))

class LogoScreenSaver(Screen):
    def __init__(self):
        Screen.__init__(self)
        img = (resources.files(images) / 'logo.png')
        with img.open('rb') as f:
            image = Image.open(f)
            pixels = set()
            for x in range(image.width):
                for y in range(image.height):
                    r, g, b, a = image.getpixel((x, y))
                    if a > 100:
                        pixels.add((x, y))

        self.drawn = set()
        self.undrawn = pixels

        self.mode = 'draw'

    def render(self, draw):
        if self.mode == 'draw':
            pixel = random.choice(list(self.undrawn))
            self.undrawn.remove(pixel)
            self.drawn.add(pixel)

            if len(self.undrawn) == 0:
                self.mode = 'undraw'
        else:
            pixel = random.choice(list(self.drawn))
            self.drawn.remove(pixel)
            self.undrawn.add(pixel)

            if len(self.drawn) == 0:
                self.mode = 'draw'

        for x, y in self.drawn:
            draw.point([(x, y)], fill='white')
