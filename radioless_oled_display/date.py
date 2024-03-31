from datetime import datetime

from .text import Text, RightAlignedText
from .screen import Screen

class Time(Text):
    def __init__(self, font, at):
        Text.__init__(self, '', font, at)

    def render(self, draw):
        self._text = datetime.now().strftime('%H:%M:%S')
        Text.render(self, draw)

class Date(RightAlignedText):
    def __init__(self, font, at):
        RightAlignedText.__init__(self, ' ' * 10, font, at)

    def render(self, draw):
        self._text = datetime.now().strftime('%Y-%m-%d')
        RightAlignedText.render(self, draw)

class DateTimeScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.add_renderer('time', Time(self.fonts['Terminus', 12], (2, 50)))
        self.add_renderer('date', Date(self.fonts['Terminus', 12], (2, 50)))
