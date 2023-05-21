import json
from typing import Any

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

    def save(self, key: str, value: Any):
        self._config[key] = value
        with open(key, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=4)


