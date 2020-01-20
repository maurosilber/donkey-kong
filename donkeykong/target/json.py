import json

from .local_target import LocalTarget


class LocalJSON(LocalTarget):
    def open(self):
        with open(self.path, 'r') as f:
            return json.load(f)

    def save(self, data, **kwargs):
        with open(self.path, 'w') as f:
            json.dump(data, f, **kwargs)
