from .fonts import FontManager
from .renderer import Renderer

class Screen(Renderer):
    def __init__(self):
        Renderer.__init__(self)
        self.fonts = FontManager()

    def update(self):
        pass

    def render(self, draw):
        self.update()
        Renderer.render(self, draw)
