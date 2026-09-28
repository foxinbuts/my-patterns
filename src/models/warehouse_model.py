from abc import abstractmethod
from cmath import isinf

from src.abstract import abstract_model
from src.exceptions import TypeException, ValueException, LengthException

class warehouse_model(abstract_model):
    MAX_NAME_LENGTH = 50
    MAX_ADDRESS_LENGTH = 255

    def __init__(self, name: str, address: str = ""):
        super().__init__()
        if not isinstance(name, str):
            raise TypeException("name", "str", type(name).__name__)
        if not name or not name.strip():
            raise ValueException("name", "наименование склада не может быть пустым")
        if len(name) > self.MAX_NAME_LENGTH:
            raise LengthException("name", self.MAX_NAME_LENGTH, len(name))
        self.name = name.strip()

        if not isinstance(address, str):
            raise TypeException("address", "str", type(address).__name__)
        if len(address) > self.MAX_ADDRESS_LENGTH:
            raise LengthException("name", self.MAX_ADDRESS_LENGTH, len(address))
        self.__address = address.strip()

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        if not isinstance(value, str):
            raise TypeException("address", "str", type(value).__name__)
        if len(value) > self.MAX_ADDRESS_LENGTH:
            raise LengthException("address", self.MAX_ADDRESS_LENGTH, len(value))
        self.__address = value.strip()

    def __str__(self):
        return f"warehouse_model(id={self.id}, name={self.name!r}, address={self.address!r})"
