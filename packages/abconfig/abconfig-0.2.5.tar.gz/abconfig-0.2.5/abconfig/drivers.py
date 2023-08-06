import yaml

try:
    import ujson as json
except ImportError:
    import json

from .base import FileDriver


class Yaml(FileDriver):
    def handle(self) -> dict:
        with open(self.filepath, 'r') as f:
            return yaml.load(f)


class Json(FileDriver):
    def handle(self) -> dict:
        with open(self.filepath, 'r') as f:
            return json.load(f)

