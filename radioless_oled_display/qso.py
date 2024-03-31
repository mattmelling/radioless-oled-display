from datetime import datetime

from .screen import Screen
from .status import StatusScreen
from .text import Text, ScrollText

class QsoScreen(StatusScreen):
    def __init__(self, ast):
        StatusScreen.__init__(self, ast)

class RxScreen(QsoScreen):
    def __init__(self, ast, astdb):
        QsoScreen.__init__(self, ast)
        self.astdb = astdb

    def update(self):
        QsoScreen.update(self)
        if self.ast.rxnode is not None:
            self.add_renderer('calling_node', Text(self.ast.rxnode, self.fonts['DejaVu Sans Mono', 24], (2, 10)))

            node = self.astdb[self.ast.rxnode]
            if node is not None:
                callsign, frequency, location = node
                txt = f'{callsign} - {location}'
                if not self.has_renderer('rx_scroll') or self._renderers['rx_scroll'].text != txt:
                    self.add_renderer('rx_scroll', ScrollText(txt, self.fonts['Terminus', 12], (2, 37)))
        else:
            self.remove_renderer('calling_node')
            self.remove_renderer('rx_scroll')


class TxScreen(QsoScreen):
    def __init__(self, ast):
        QsoScreen.__init__(self, ast)
        self._start = datetime.now()

    def reset(self):
        self._start = datetime.now()

    def update(self):
        QsoScreen.update(self)
        d = datetime.now() - self._start
        s = f'{int(d.seconds / 60):02d}:{(d.seconds % 60):02d}'
        self.add_renderer('tot', Text(s, self.fonts['DejaVu Sans Mono', 24], (2, 10)))
