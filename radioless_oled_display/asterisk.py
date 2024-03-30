import pystrix


class AsteriskManager:
    def __init__(self, hostname='localhost', port=5038, username='admin', password='password'):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._rx = False
        self._tx = False
        self._rxnode = None
        self._links = set()
        self._numlinks = 0
        self._manager = pystrix.ami.Manager()

    def start(self):
        self._manager.connect(self._hostname, port=self._port)
        challenge_response = self._manager.send_action(pystrix.ami.core.Challenge())
        login_action = pystrix.ami.core.Login(self._username, self._password,
                                              challenge=challenge_response.result['Challenge'])
        self._manager.send_action(login_action)
        self._manager.register_callback('RPT_TXKEYED', self.handle_txkeyed)
        self._manager.register_callback('RPT_ETXKEYED', self.handle_etxkeyed)
        self._manager.register_callback('RPT_RXKEYED', self.handle_rxkeyed)
        self._manager.register_callback('RPT_ALINKS', self.handle_alinks)
        self._manager.register_callback('RPT_NUMLINKS', self.handle_numlinks)
        self._manager.monitor_connection()

    def handle_txkeyed(self, event, manager):
        self._rx = event['EventValue'] == '1'
        if not self._rx:
            self._rxnode = None

    def handle_etxkeyed(self, event, manager):
        self._rx = False

    def handle_rxkeyed(self, event, manager):
        self._tx = event['EventValue'] == '1'

    def handle_alinks(self, event, manager):
        self._rxnode = event['EventValue'].split(',')[1][:-2]

    def handle_numlinks(self, event, manager):
        self._numlinks = int(event['EventValue'])

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
