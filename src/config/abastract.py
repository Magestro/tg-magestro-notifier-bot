import json


class AbstractConfig:
    def __init__(self, config_file=None):
        self._read_file(config_file)

    def _read_file(self, filename):
        with open(filename) as fh:
            fcont = fh.read()
        self._assign(json.loads(fcont))

    def _assign(self, fjson):
        raise Exception("method not implemented")
