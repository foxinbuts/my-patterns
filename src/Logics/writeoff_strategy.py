from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.exceptions import StockBlockedException, TypeException, ValueException
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model

if TYPE_CHECKING:
    from src.Logics.warehouse_storage import warehouse_storage


class abstract_writeoff_strategy(ABC):
    """
    Абстрактная стратегия списания номенклатуры (паттерн Strategy).
    Определяет единый интерфейс списания запасов со склада.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Наименование стратегии списания."""
        ...

    @abstractmethod
    def write_off(
        self,
        storage: "warehouse_storage",
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        quantity: float,
    ) -> bool:
        """
        Выполнить списание номенклатуры со склада.

        :param storage: экземпляр хранилища остатков
        :param warehouse: склад списания
        :param nomenclature: номенклатура
        :param quantity: списываемое количество (> 0)
        :return: True при успешном списании
        """
        ...


class block_writeoff_strategy(abstract_writeoff_strategy):
    """
    Вариант списания 'С блокировкой в случае недостатка остатков'.
    Блокировка осуществляется, если текущий остаток номенклатуры на складе
    меньше требуемого для списания.
    """

    @property
    def name(self) -> str:
        return "С блокировкой в случае недостатка остатков"

    def write_off(
        self,
        storage: "warehouse_storage",
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        quantity: float,
    ) -> bool:
        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "списываемое количество должно быть > 0")

        current_balance = storage.get_balance(warehouse, nomenclature)
        if current_balance < quantity:
            raise StockBlockedException(
                f"Недостаточно остатка номенклатуры '{nomenclature.name}' на складе '{warehouse.name}': "
                f"требуется {quantity}, доступно {current_balance}"
            )

        storage.set_balance(warehouse, nomenclature, current_balance - float(quantity))
        return True


class saldo_writeoff_strategy(abstract_writeoff_strategy):
    """
    Вариант списания 'Под сальдо'.
    Списание осуществляется без блокировки (в минус), остаток на складе меняется.
    """

    @property
    def name(self) -> str:
        return "Под сальдо"

    def write_off(
        self,
        storage: "warehouse_storage",
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        quantity: float,
    ) -> bool:
        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "списываемое количество должно быть > 0")

        current_balance = storage.get_balance(warehouse, nomenclature)
        storage.set_balance(warehouse, nomenclature, current_balance - float(quantity))
        return True
