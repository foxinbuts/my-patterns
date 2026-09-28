from abc import ABC
import uuid

class abstract_model(ABC):
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__name = ""

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            from src.exceptions import ArgumentException
            raise ArgumentException("name должен быть строкой")
        self.__name = value

    def __eq__(self, other):
        if not isinstance(other, abstract_model):
            return False
        return self.__id == other.id

    def __hash__(self):
        return hash(self.__id)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.__id}, name={self.__name!r})"

    def __repr__(self):
        return self.__str__()
