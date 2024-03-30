from PIL import ImageFont
import subprocess

class FontManager:
    def __init__(self):
        self._fonts = {}

    def __getitem__(self, key):
        name, size = key
        if key in self._fonts:
            return self._fonts[key]
        self._fonts[key] = self.get_font(name, size)
        return self._fonts[key]

    def find(self, name):
        path = subprocess.check_output(['fc-match', '-f', '%{file}', name])
        print(path)
        return path.decode('utf-8')

    def get_font(self, name, size):
        return ImageFont.truetype(self.find(name), size)
