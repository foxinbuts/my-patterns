from abc import ABC, abstractmethod
import uuid

class arguments_exception(Exception):
    __stack_trace:str = ""
    __massage:str = ""
    __field:str = ""

class abstact_model(ABC):
    def __init__(self):
        self.__unique_code = str(uuid.uuid4())

    def get_unique_code(self):
        return self.__unique_code

    def __init__(self, message: str = "", stack_trace: str = ""):
        self.__massage__ = message.strip()
        self.__stack_trace = stack_trace.strip()

    def __str__(self):
        return f"Ошибка в аргументах: {self.__massage__}\n{self.__stack_trace}"

    @property
    def unique_code(self):
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        if value.strip() == "":
            raise arguments_exception(
                f"Уникальный код не может быть пустым {self.__field}!\n"
            )

        self.__unique_code = value.strip()