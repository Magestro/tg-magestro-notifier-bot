import os
import json

class Json():
    path = os.getcwd() + '/storage.json'

    def save(self, name, flat):
        data = self.read()
        if name not in data.keys:
            data[name] = {}
        data['name']

    def write(self, data):
        with open(self.path, 'w') as outfile:
            json.dump(data, outfile)

    def read(self):
        with open(self.path) as f:
            data = json.load(f)

        return data