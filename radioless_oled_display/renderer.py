
class Renderable:
    def render(self, draw):
        pass

class Renderer(Renderable):

    def __init__(self):
        self._renderers = {}

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
