import os

from .date import DateTimeScreen
from .text import Text, RightAlignedText

class StatusScreen(DateTimeScreen):
    def __init__(self, ast):
        self.ast = ast
        DateTimeScreen.__init__(self)

        callsign = os.environ.get('ASL_CALLSIGN', '')
        node = os.environ.get('ASL_NODE', '')
        self.add_renderer('status_callsign',
                          RightAlignedText(f'{callsign} {node}'.strip(),
                                           self.fonts['Terminus', 12],
                                           (18, 0)))

    def update(self):
        if self.ast.rx:
            if not self.has_renderer('rx'):
                self.add_renderer('rx', Text('RX', self.fonts['Terminus', 12], (4, 0)))
        else:
            self.remove_renderer('rx')

        if self.ast.tx:
            if not self.has_renderer('tx'):
                self.add_renderer('tx', Text('TX', self.fonts['Terminus', 12], (18, 0)))
        else:
            self.remove_renderer('tx')
