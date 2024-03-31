import socket

from .qso import QsoScreen
from .text import Text, ScrollText

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

class IdleScreen(QsoScreen):
    def __init__(self, ast):
        QsoScreen.__init__(self, ast)

    def update(self):
        QsoScreen.update(self)
        text = f'{get_ip()} | Nodes: {self.ast.numlinks} | Local: {self.ast.numalinks}'

        if not self.has_renderer('info_text') or self._renderers['info_text'].text != text:
            self.add_renderer('info_text', ScrollText(text, self.fonts['Terminus', 12], (2, 40)))

class NoConnectionScreen(QsoScreen):
    def __init__(self, ast):
        QsoScreen.__init__(self, ast)
        self.add_renderer('no_connection', Text('No Link', self.fonts['Terminus', 12], (2, 20)))
        self.add_renderer('ip_address', Text(get_ip(), self.fonts['Terminus', 12], (2, 30)))
