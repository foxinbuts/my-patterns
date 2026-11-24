from typing import Dict, List, Type

from src.abstract import abstract_model
from src.models.group_model import group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.technology_card_model import technology_card_model
from src.models.warehouse_operation_model import warehouse_operation_model


class ModelRegistry:
    """Реестр DOMAIN моделей."""

    _registry: Dict[str, Type[abstract_model]] = {
        "nomenclature": nomenclature_model,
        "group": group_model,
        "range": range_model,
        "technology_card": technology_card_model,
        "warehouse_operation": warehouse_operation_model,
    }

    _data_stores: Dict[str, List[abstract_model]] = {
        "nomenclature": [],
        "group": [],
        "range": [],
        "technology_card": [],
        "warehouse_operation": [],
    }

    @classmethod
    def get_model_class(cls, model_type: str) -> Type[abstract_model]:
        if model_type not in cls._registry:
            raise ValueError(f"Неизвестный тип модели: {model_type}. Доступные: {list(cls._registry.keys())}")
        return cls._registry[model_type]

    @classmethod
    def get_data_store(cls, model_type: str) -> List[abstract_model]:
        if model_type not in cls._data_stores:
            cls._data_stores[model_type] = []
        return cls._data_stores[model_type]

    @classmethod
    def set_data_store(cls, model_type: str, data: List[abstract_model]) -> None:
        cls._data_stores[model_type] = data

    @classmethod
    def add_item(cls, model_type: str, item: abstract_model) -> None:
        if model_type not in cls._data_stores:
            cls._data_stores[model_type] = []
        cls._data_stores[model_type].append(item)

    @classmethod
    def get_available_types(cls) -> List[str]:
        return list(cls._registry.keys())
