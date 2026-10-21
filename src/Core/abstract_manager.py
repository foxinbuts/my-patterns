from abc import ABC, abstractmethod


class abstract_manager(ABC):
    """Абстрактный класс для загрузки и обработки данных."""

    def __init__(self):
        self.__file_name: str = ""
        self.__is_loaded: bool = False
        self.__data: list = []

    @abstractmethod
    def load(self, file_name: str = "") -> None:
        """Загрузить данные из файла."""
        ...

    @abstractmethod
    def convert(self) -> bool:
        """Преобразовать загруженные данные."""
        ...

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str) -> None:
        self.__file_name = value

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, value: list) -> None:
        self.__data = value

    @property
    def is_loaded(self) -> bool:
        return self.__is_loaded

    @is_loaded.setter
    def is_loaded(self, value: bool) -> None:
        self.__is_loaded = value
