import os
import random
import itertools
import math

from datetime import datetime

try:
    import importlib_resources as resources
except ModuleNotFoundError:
    import importlib.resources as resources

from PIL import Image

from . import images
from .screen import Screen
from .text import Text

logos = [
    'logo.png',
    'pi.png',
    'linside.png',
    'asterisk.png'
]

class ScreenSaver(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.reset()

    def select_screen(self):
        self._screen = random.choice([
            TimeScreenSaver,
            CallsignScreenSaver,
            LogoScreenSaver,
            RotatingImageScreenSaver,
            ClockScreenSaver
        ])()

    def reset(self):
        self._start = datetime.now()
        self.select_screen()

    def update(self):
        Screen.update(self)
        d = datetime.now() - self._start

        if d.seconds == 0:
            return

        if d.seconds > 120:
            self.reset()

    def render(self, draw):
        Screen.render(self, draw)
        if self._screen is not None:
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
        self._img = Image.open(resources.files(images) / random.choice(logos))
        self._x = 0

    def draw(self, draw, d):
        size = self._img.size
        for x, y in itertools.product(range(size[0]), range(size[1])):
            pixel = self._img.getpixel((x, y))
            if pixel[3] > 150:
                draw.point((d + x, y), fill='white')

    def render(self, draw):
        offset = draw.im.size[0]
        if self._x < -offset:
            self._x = 0
        self.draw(draw, self._x)
        self.draw(draw, self._x + offset)
        self._x -= 1

class RotatingImageScreenSaver(Screen):
    def __init__(self):
        Screen.__init__(self)
        self._t = 0
        self._img = Image.open(resources.files(images) / random.choice(logos))

    def render(self, draw):
        size = self._img.size
        img = self._img.rotate(self._t, resample=Image.BILINEAR)
        for x, y in itertools.product(range(size[0]), range(size[1])):
            pixel = img.getpixel((x, y))
            if pixel[3] > 150:
                draw.point((x, y), fill='white')
        self._t += 1

class ClockScreenSaver(Screen):
    """
    From luma-examples
    """

    def __init__(self):
        Screen.__init__(self)

    def posn(self, angle, arm_length):
        dx = int(math.cos(math.radians(angle)) * arm_length)
        dy = int(math.sin(math.radians(angle)) * arm_length)
        return dx, dy

    def render(self, draw):
        now = datetime.now()
        today_date = now.strftime("%d %b %y")
        today_time = now.strftime("%H:%M:%S")

        margin = 4

        cx = 30
        cy = draw.im.size[1] / 2

        left = cx - cy
        right = cx + cy

        hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
        hrs = self.posn(hrs_angle, cy - margin - 7)

        min_angle = 270 + (6 * now.minute)
        mins = self.posn(min_angle, cy - margin - 2)

        sec_angle = 270 + (6 * now.second)
        secs = self.posn(sec_angle, cy - margin - 2)

        draw.ellipse((left + margin, margin, right - margin, draw.im.size[1] - margin), outline="white")
        draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill="white")
        draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill="white")
        draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="red")
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill="white", outline="white")
        draw.text((2 * (cx + margin), cy - 8), today_date, fill="yellow")
        draw.text((2 * (cx + margin), cy + 2), today_time, fill="yellow")
