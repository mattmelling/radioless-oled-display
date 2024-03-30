from datetime import datetime
from .fonts import FontManager

class TextScrollAnimation:
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

class TextAnimation:
    def __init__(self, text, font, at):
        self._text = text
        self._font = font
        self._at = at

    def render(self, draw):
        draw.text((self._at[0], self._at[1]), self._text, font=self._font, fill='white')

    @property
    def text(self):
        return self._text

class RightAlignedTextAnimation:
    def __init__(self, text, font, at):
        self._text = text
        self._font = font

        x, y, lx, ly = font.getbbox(text)
        self._at = (lx, at[1])

    def render(self, draw):
        draw.text((draw.im.size[0] - self._at[0], self._at[1]), self._text, font=self._font, fill='white')

class TimeAnimation(TextAnimation):
    def __init__(self, font, at):
        TextAnimation.__init__(self, '', font, at)

    def render(self, draw):
        self._text = datetime.now().strftime('%H:%M:%S')
        TextAnimation.render(self, draw)

class DateAnimation(RightAlignedTextAnimation):
    def __init__(self, font, at):
        RightAlignedTextAnimation.__init__(self, ' ' * 10, font, at)

    def render(self, draw):
        self._text = datetime.now().strftime('%Y-%m-%d')
        RightAlignedTextAnimation.render(self, draw)

class Renderer:

    def __init__(self):
        self._fonts = FontManager()
        self._renderers = {}

        self.add_renderer('time', TimeAnimation(self._fonts['Terminus', 12], (2, 50)))
        self.add_renderer('date', DateAnimation(self._fonts['Terminus', 12], (2, 50)))

    def add_renderer(self, name, renderer):
        self._renderers[name] = renderer

    def remove_renderer(self, name):
        if name in self._renderers:
            del self._renderers[name]

    def has_renderer(self, name):
        return name in self._renderers

    def render(self, draw):
        for key, renderer in self._renderers.items():
            renderer.render(draw)

    def set_info_text(self, text, scroll=False):
        if text is None:
            self.remove_renderer('info_text')
        elif 'info_text' not in self._renderers or self._renderers['info_text'].text != text:
            font = self._fonts['Terminus', 12]
            if scroll:
                self.add_renderer('info_text', TextScrollAnimation(text, font, (2, 37)))
            else:
                self.add_renderer('info_text', TextAnimation(text, font, (2, 37)))

    def set_calling_node(self, text):
        if text is not None:
            self.add_renderer('calling_node', TextAnimation(text, self._fonts['DejaVu Sans Mono', 24], (2, 10)))
        else:
            self.remove_renderer('calling_node')

    def set_rx(self, rx):
        if rx:
            self.add_renderer('rx', TextAnimation('RX', self._fonts['Terminus', 12], (4, 0)))
        else:
            self.remove_renderer('rx')

    def set_tx(self, tx):
        if tx:
            self.add_renderer('tx', TextAnimation('TX', self._fonts['Terminus', 12], (18, 0)))
        else:
            self.remove_renderer('tx')

    def set_callsign(self, callsign):
        if callsign is not None:
            self.add_renderer('callsign', RightAlignedTextAnimation(callsign, self._fonts['Terminus', 12], (18, 0)))
        else:
            self.remove_renderer(callsign)
