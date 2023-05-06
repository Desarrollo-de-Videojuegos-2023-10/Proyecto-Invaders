import json

class ConfigService:
    def __init__(self) -> None:
        self._config = dict()

    def get(self, key:str) -> dict:
        if key not in self._config:
            self._config[key] = self._load_config(key)
        return self._config[key]

    def _load_config(self, key:str) -> dict:
        with open(key, "r", encoding="utf-8") as f:
            return json.load(f)