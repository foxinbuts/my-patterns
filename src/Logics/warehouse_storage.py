from typing import Dict, Tuple

from src.exceptions import TypeException, ValueException
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model


class warehouse_storage:
    """
    Хранилище остатков номенклатуры на складах.
    Обеспечивает учет поступлений, списаний и получение актуального сальдо.
    """

    def __init__(self):
        # ключ: (warehouse.id, nomenclature.id), значение: float
        self.__balances: Dict[Tuple[object, object], float] = {}

    def get_balance(
        self,
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
    ) -> float:
        """Получить текущий остаток номенклатуры на складе."""
        self._validate_pair(warehouse, nomenclature)
        key = (warehouse.id, nomenclature.id)
        return self.__balances.get(key, 0.0)

    def set_balance(
        self,
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        value: float,
    ) -> None:
        """Установить точный остаток номенклатуры на складе."""
        self._validate_pair(warehouse, nomenclature)
        if not isinstance(value, (int, float)):
            raise TypeException("value", "int | float", type(value).__name__)
        key = (warehouse.id, nomenclature.id)
        self.__balances[key] = float(value)

    def deposit(
        self,
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        quantity: float,
    ) -> None:
        """Поступление номенклатуры на склад."""
        self._validate_pair(warehouse, nomenclature)
        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "количество поступления должно быть > 0")

        current = self.get_balance(warehouse, nomenclature)
        self.set_balance(warehouse, nomenclature, current + float(quantity))

    def withdraw(
        self,
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        quantity: float,
        strategy: "abstract_writeoff_strategy",  # type: ignore
    ) -> bool:
        """Списание номенклатуры со склада по заданной стратегии."""
        from src.Logics.writeoff_strategy import abstract_writeoff_strategy

        self._validate_pair(warehouse, nomenclature)
        if not isinstance(strategy, abstract_writeoff_strategy):
            raise TypeException("strategy", "abstract_writeoff_strategy", type(strategy).__name__)

        return strategy.write_off(self, warehouse, nomenclature, quantity)

    def clear(self) -> None:
        """Очистить все остатки."""
        self.__balances.clear()

    @staticmethod
    def _validate_pair(warehouse: warehouse_model, nomenclature: nomenclature_model) -> None:
        if not isinstance(warehouse, warehouse_model):
            raise TypeException("warehouse", "warehouse_model", type(warehouse).__name__)
        if not isinstance(nomenclature, nomenclature_model):
            raise TypeException("nomenclature", "nomenclature_model", type(nomenclature).__name__)
