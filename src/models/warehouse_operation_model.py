from datetime import datetime
from enum import Enum
from typing import Optional

from src.abstract import abstract_model
from src.exceptions import TypeException, ValueException
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model


class OperationType(Enum):
    """Тип складской операции"""
    DEPOSIT = "DEPOSIT"      # Поступление (приход)
    WITHDRAW = "WITHDRAW"    # Списание (расход)


class warehouse_operation_model(abstract_model):
    """
    Модель складской операции (движения).
    Хранит информацию о поступлении или списании номенклатуры.
    """

    def __init__(
        self,
        operation_type: OperationType,
        quantity: float,
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        date: Optional[datetime] = None,
        description: str = "",
    ):
        super().__init__()

        if not isinstance(operation_type, OperationType):
            raise TypeException("operation_type", "OperationType", type(operation_type).__name__)
        self.__operation_type = operation_type

        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "количество должно быть > 0")
        self.__quantity = float(quantity)

        if not isinstance(warehouse, warehouse_model):
            raise TypeException("warehouse", "warehouse_model", type(warehouse).__name__)
        self.__warehouse = warehouse

        if not isinstance(nomenclature, nomenclature_model):
            raise TypeException("nomenclature", "nomenclature_model", type(nomenclature).__name__)
        self.__nomenclature = nomenclature

        if date is None:
            date = datetime.now()
        if not isinstance(date, datetime):
            raise TypeException("date", "datetime", type(date).__name__)
        self.__date = date

        if not isinstance(description, str):
            raise TypeException("description", "str", type(description).__name__)
        self.__description = description

    @property
    def operation_type(self) -> OperationType:
        return self.__operation_type

    @operation_type.setter
    def operation_type(self, value: OperationType):
        if not isinstance(value, OperationType):
            raise TypeException("operation_type", "OperationType", type(value).__name__)
        self.__operation_type = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeException("quantity", "int | float", type(value).__name__)
        if value <= 0:
            raise ValueException("quantity", "количество должно быть > 0")
        self.__quantity = float(value)

    @property
    def warehouse(self) -> warehouse_model:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        if not isinstance(value, warehouse_model):
            raise TypeException("warehouse", "warehouse_model", type(value).__name__)
        self.__warehouse = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        if not isinstance(value, nomenclature_model):
            raise TypeException("nomenclature", "nomenclature_model", type(value).__name__)
        self.__nomenclature = value

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        if not isinstance(value, datetime):
            raise TypeException("date", "datetime", type(value).__name__)
        self.__date = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeException("description", "str", type(value).__name__)
        self.__description = value

    def is_deposit(self) -> bool:
        """Проверяет, является ли операция поступлением"""
        return self.__operation_type == OperationType.DEPOSIT

    def is_withdraw(self) -> bool:
        """Проверяет, является ли операция списанием"""
        return self.__operation_type == OperationType.WITHDRAW

    def __str__(self):
        op_type = "Приход" if self.is_deposit() else "Расход"
        return (
            f"warehouse_operation_model(date={self.__date.strftime('%Y-%m-%d %H:%M')}, "
            f"type={op_type}, quantity={self.__quantity}, "
            f"warehouse={self.__warehouse.name!r}, nomenclature={self.__nomenclature.name!r})"
        )
