from .renderer import Renderable

class Text(Renderable):
    def __init__(self, text, font, at):
        self._text = text
        self._font = font
        self._at = at

    def render(self, draw):
        draw.text((self._at[0], self._at[1]), self._text, font=self._font, fill='white')

    @property
    def text(self):
        return self._text

class RightAlignedText(Renderable):
    def __init__(self, text, font, at):
        self._text = text
        self._font = font

        x, y, lx, ly = font.getbbox(text)
        self._at = (lx, at[1])

    def render(self, draw):
        draw.text((draw.im.size[0] - self._at[0], self._at[1]), self._text, font=self._font, fill='white')

class ScrollText:
    def __init__(self, text, font, at):
        self._text = text
        self._font = font
        self._x = 0
        self._at = at

        x, y, lx, ly = font.getbbox(text)
        self._lx = lx

    def render(self, draw):
        if self._x + self._lx < 0:
            self._x = draw.im.size[0]

        draw.text((self._at[0] + self._x, self._at[1]), self._text, font=self._font, fill='white')

        self._x -= 2

    @property
    def text(self):
        return self._text
