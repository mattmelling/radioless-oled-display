import pystrix
import logging

logger = logging.getLogger('AsteriskManager')

class AsteriskManager:
    def __init__(self, hostname='localhost', port=5038, username='admin', password='password', node=None):
        self._node = node
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._rx = False
        self._tx = False
        self._rxnode = None
        self._links = set()
        self._numlinks = 0
        self._numalinks = 0
        self._manager = pystrix.ami.Manager()

    def start(self):
        self._manager.connect(self._hostname, port=self._port)
        challenge_response = self._manager.send_action(pystrix.ami.core.Challenge())
        login_action = pystrix.ami.core.Login(self._username, self._password,
                                              challenge=challenge_response.result['Challenge'])
        self._manager.send_action(login_action)
        self._manager.register_callback('RPT_TXKEYED', self.handle_txkeyed)
        self._manager.register_callback('RPT_RXKEYED', self.handle_rxkeyed)
        self._manager.register_callback('RPT_ALINKS', self.handle_alinks)
        self._manager.register_callback('RPT_NUMLINKS', self.handle_numlinks)
        self._manager.register_callback('RPT_NUMALINKS', self.handle_numalinks)
        self._manager.monitor_connection()

    def handle_txkeyed(self, event, manager):
        if event['Node'] != self._node:
            return
        logger.debug(event)
        self._tx = int(event['EventValue']) == 1

    def handle_rxkeyed(self, event, manager):
        if event['Node'] != self._node:
            return
        logger.debug(event)
        self._rx = int(event['EventValue']) == 1

    def handle_alinks(self, event, manager):
        if event['Node'] != self._node:
            return
        logger.debug(event)

        nodes = event['EventValue'].split(',')[1:]
        if len(nodes) == 0:
            return

        rx = None
        for node in nodes:
            nn = node[:-2]
            key = node[-1]
            if key == 'K':
                rx = nn

        self._tx = rx is not None
        if self._tx:
            self._rx = False
        self._rxnode = rx

    def handle_numlinks(self, event, manager):
        if event['Node'] != self._node:
            return
        logger.debug(event)
        self._numlinks = int(event['EventValue'])

    def handle_numalinks(self, event, manager):
        if event['Node'] != self._node:
            return
        logger.debug(event)
        self._numalinks = int(event['EventValue'])

    @property
    def rx(self):
        return self._rx

    @property
    def tx(self):
        return self._tx

    @property
    def rxnode(self):
        return self._rxnode

    @property
    def numlinks(self):
        return self._numlinks

    @property
    def numalinks(self):
        return self._numalinks
