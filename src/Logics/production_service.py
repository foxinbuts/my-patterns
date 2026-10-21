from typing import Any, Dict, Optional

from src.exceptions import StockBlockedException, TypeException, ValueException
from src.Logics.warehouse_storage import warehouse_storage
from src.Logics.writeoff_strategy import (
    abstract_writeoff_strategy,
    block_writeoff_strategy,
)
from src.models.nomenclature_model import nomenclature_model
from src.models.technology_card_model import technology_card_model
from src.models.warehouse_model import warehouse_model


class production_service:
    """
    Сервис производственного учета (паттерн Facade / Service).
    Реализует операции согласно разделу 2 ТЗ:
    - Технологическая карта (обработка и расчет потребностей);
    - Приготовление полуфабриката;
    - Приготовление блюда;
    - Выпуск продукции;
    - Утилизация продукции;
    с поддержкой стратегий списания (с блокировкой при недостатке остатков / под сальдо).
    """

    def __init__(self, storage: Optional[warehouse_storage] = None):
        if storage is not None and not isinstance(storage, warehouse_storage):
            raise TypeException("storage", "warehouse_storage", type(storage).__name__)
        self.__storage = storage if storage is not None else warehouse_storage()

    @property
    def storage(self) -> warehouse_storage:
        """Хранилище остатков склада."""
        return self.__storage

    def release_production(
        self,
        card: technology_card_model,
        quantity: float,
        warehouse: warehouse_model,
        strategy: Optional[abstract_writeoff_strategy] = None,
    ) -> Dict[str, Any]:
        """
        Операция 'Выпуск продукции':
        1. Рассчитывает сырье по технологической карте (включая составные рецепты Composite).
        2. Проверяет наличие остатков и списывает сырье согласно выбранной стратегии списания.
        3. Приходует готовую продукцию на указанный склад.
        """
        if not isinstance(card, technology_card_model):
            raise TypeException("card", "technology_card_model", type(card).__name__)
        if not isinstance(warehouse, warehouse_model):
            raise TypeException("warehouse", "warehouse_model", type(warehouse).__name__)
        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "выпускаемое количество должно быть > 0")

        if strategy is None:
            strategy = block_writeoff_strategy()
        elif not isinstance(strategy, abstract_writeoff_strategy):
            raise TypeException("strategy", "abstract_writeoff_strategy", type(strategy).__name__)

        # 1. Расчет потребностей
        required_materials = card.calculate_gross_requirements(quantity)

        # 2. Атомарная проверка: если стратегия с блокировкой, сначала проверяем ВСЕ позиции
        if isinstance(strategy, block_writeoff_strategy):
            for nom, req_qty in required_materials.items():
                curr = self.__storage.get_balance(warehouse, nom)
                if curr < req_qty:
                    raise StockBlockedException(
                        f"Блокировка выпуска продукции '{card.target.name}': "
                        f"недостаточно сырья '{nom.name}' на складе '{warehouse.name}' "
                        f"(требуется: {req_qty}, доступно: {curr})"
                    )

        # 3. Списание сырья
        for nom, req_qty in required_materials.items():
            strategy.write_off(self.__storage, warehouse, nom, req_qty)

        # 4. Поступление готовой продукции
        self.__storage.deposit(warehouse, card.target, quantity)

        return {
            "operation": "release_production",
            "target": card.target,
            "quantity": float(quantity),
            "warehouse": warehouse,
            "strategy": strategy.name,
            "materials_used": required_materials,
            "status": "success",
        }

    def cook_semi_finished(
        self,
        card: technology_card_model,
        quantity: float,
        warehouse: warehouse_model,
        strategy: Optional[abstract_writeoff_strategy] = None,
    ) -> Dict[str, Any]:
        """Операция 'Приготовление полуфабриката'."""
        res = self.release_production(card, quantity, warehouse, strategy)
        res["operation"] = "cook_semi_finished"
        return res

    def cook_dish(
        self,
        card: technology_card_model,
        quantity: float,
        warehouse: warehouse_model,
        strategy: Optional[abstract_writeoff_strategy] = None,
    ) -> Dict[str, Any]:
        """Операция 'Приготовление блюда'."""
        res = self.release_production(card, quantity, warehouse, strategy)
        res["operation"] = "cook_dish"
        return res

    def utilize_production(
        self,
        warehouse: warehouse_model,
        nomenclature: nomenclature_model,
        quantity: float,
        strategy: Optional[abstract_writeoff_strategy] = None,
        reason: str = "Брак / истек срок годности",
    ) -> Dict[str, Any]:
        """
        Операция 'Утилизация продукции':
        Списание бракованной или испорченной продукции со склада.
        """
        if not isinstance(warehouse, warehouse_model):
            raise TypeException("warehouse", "warehouse_model", type(warehouse).__name__)
        if not isinstance(nomenclature, nomenclature_model):
            raise TypeException("nomenclature", "nomenclature_model", type(nomenclature).__name__)
        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "количество для утилизации должно быть > 0")

        if strategy is None:
            strategy = block_writeoff_strategy()
        elif not isinstance(strategy, abstract_writeoff_strategy):
            raise TypeException("strategy", "abstract_writeoff_strategy", type(strategy).__name__)

        strategy.write_off(self.__storage, warehouse, nomenclature, quantity)

        return {
            "operation": "utilize_production",
            "warehouse": warehouse,
            "nomenclature": nomenclature,
            "quantity": float(quantity),
            "reason": reason,
            "strategy": strategy.name,
            "status": "utilized",
        }
