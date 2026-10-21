import json
import os

from src.Core.abstract_manager import abstract_manager


class settings_manager(abstract_manager):
    """
    Менеджер настроек: загружает JSON-файл с настройками
    и преобразует его в словарь.
    """

    DEFAULT_FILE = "settings.json"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        super().__init__()
        self.__settings: dict = {}
        self.file_name = self.DEFAULT_FILE
        self._initialized = True

    def load(self, file_name: str = "") -> None:
        if file_name:
            self.file_name = file_name

        if not self.file_name:
            raise ValueError("Не задан путь к файлу настроек")

        if not os.path.isfile(self.file_name):
            raise FileNotFoundError(f"Файл настроек не найден: {self.file_name}")

        with open(self.file_name, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.is_loaded = True

    def convert(self) -> bool:
        if not self.is_loaded:
            return False
        try:
            self.__settings = dict(self.data) if self.data else {}
            return True
        except (TypeError, ValueError):
            return False

    @property
    def settings(self) -> dict:
        return self.__settings
