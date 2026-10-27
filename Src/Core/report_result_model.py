from Src.Core.entity_model import entity_model

"""
Модель хранения результата формирования отчета
"""

class report_result_model(entity_model):
    __text:str = ""
    __binary:list


    def __init__(self, text:str = "", binary:list = None):
        if binary is None:
            binary = []
        self.__text = text if len(binary) == 0 else ""
        self.__binary = binary if len(text.strip()) == 0 else []

    @property
    def text(self) -> str:
        return self.__text

    @property
    def binary(self) -> list:
        return self.__binary
