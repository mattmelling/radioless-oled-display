class AllstarDatabase:
    def __init__(self, filename):
        self._nodes = {}
        with open(filename) as f:
            for line in (l.strip() for l in f.readlines()):
                if len(line) == 0 or line[0] == ';':
                    continue
                pieces = line.split('|')
                self._nodes[pieces[0]] = (pieces[1], pieces[2], pieces[3] if len(pieces) == 4 else None)

    def __getitem__(self, key):
        return self._nodes.get(key, None)
