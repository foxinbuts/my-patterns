from typing import Any, Callable, Dict, List, Type, TypeVar
from src.abstract import abstract_model
from src.filtering.filter_dto import FilterCondition, FilterDTO
from src.filtering.filter_types import FilterType


T = TypeVar('T', bound=abstract_model)


class FilterPrototype:
    """
    Паттерн Прототип для создания фильтров.
    Позволяет создавать и настраивать фильтры для различных моделей.
    """

    def __init__(self):
        self._dto = FilterDTO()

    def clone(self) -> 'FilterPrototype':
        """Создает копию прототипа"""
        new_prototype = FilterPrototype()
        new_prototype._dto = FilterDTO(
            conditions=[
                FilterCondition(cond.field_name, cond.filter_type, cond.value)
                for cond in self._dto.conditions
            ]
        )
        return new_prototype

    def add_condition(self, field_name: str, filter_type: FilterType, value: Any) -> 'FilterPrototype':
        """Добавляет условие фильтрации (поддерживает вложенность через точку)"""
        self._dto.add_condition(field_name, filter_type, value)
        return self

    def equals(self, field_name: str, value: Any) -> 'FilterPrototype':
        """Условие полного совпадения"""
        return self.add_condition(field_name, FilterType.EQUALS, value)

    def like(self, field_name: str, value: str) -> 'FilterPrototype':
        """Условие вхождения строки"""
        return self.add_condition(field_name, FilterType.LIKE, value)

    def get_dto(self) -> FilterDTO:
        """Возвращает DTO с условиями фильтрации"""
        return self._dto

    def apply(self, data: List[T]) -> List[T]:
        """
        Применяет фильтр к списку объектов.
        Поддерживает вложенные поля через точечную нотацию.
        """
        if self._dto.is_empty():
            return data

        return [item for item in data if self._matches_all_conditions(item)]

    def _matches_all_conditions(self, item: T) -> bool:
        """Проверяет, соответствует ли объект всем условиям"""
        return all(
            self._matches_condition(item, condition)
            for condition in self._dto.conditions
        )

    def _matches_condition(self, item: T, condition: FilterCondition) -> bool:
        """Проверяет соответствие одному условию"""
        field_value = self._get_nested_value(item, condition.field_name)

        if field_value is None:
            return False

        if condition.filter_type == FilterType.EQUALS:
            return field_value == condition.value
        elif condition.filter_type == FilterType.LIKE:
            if not isinstance(field_value, str) or not isinstance(condition.value, str):
                return False
            return condition.value.lower() in field_value.lower()

        return False

    def _get_nested_value(self, obj: Any, field_path: str) -> Any:
        """
        Получает значение вложенного поля через точечную нотацию.
        Например: "group.name" -> obj.group.name
        """
        fields = field_path.split('.')
        current = obj

        for field_name in fields:
            if current is None:
                return None

            # Пробуем получить как атрибут
            if hasattr(current, field_name):
                current = getattr(current, field_name)
            # Пробуем как свойство
            elif hasattr(current, f'_{obj.__class__.__name__}__{field_name}'):
                current = getattr(current, f'_{obj.__class__.__name__}__{field_name}')
            else:
                return None

        return current


class FilterPrototypeFactory:
    """
    Фабрика для создания прототипов фильтров для различных моделей.
    """

    _prototypes: Dict[Type[abstract_model], FilterPrototype] = {}

    @classmethod
    def register(cls, model_type: Type[T], prototype: FilterPrototype) -> None:
        """Регистрирует прототип для модели"""
        cls._prototypes[model_type] = prototype

    @classmethod
    def create(cls, model_type: Type[T]) -> FilterPrototype:
        """Создает прототип для указанной модели"""
        if model_type not in cls._prototypes:
            # Если прототип не зарегистрирован, создаем базовый
            return FilterPrototype()

        return cls._prototypes[model_type].clone()

    @classmethod
    def get_registered_models(cls) -> List[Type[abstract_model]]:
        """Возвращает список зарегистрированных моделей"""
        return list(cls._prototypes.keys())


def _matches_condition(self, item: T, condition: FilterCondition) -> bool:
    """Проверяет соответствие одному условию"""
    field_value = self._get_nested_value(item, condition.field_name)

    if field_value is None:
        return False

    if condition.filter_type == FilterType.EQUALS:
        return field_value == condition.value
    elif condition.filter_type == FilterType.LIKE:
        if not isinstance(field_value, str) or not isinstance(condition.value, str):
            return False
        return condition.value.lower() in field_value.lower()
    elif condition.filter_type == FilterType.LESS_THAN:
        return field_value < condition.value
    elif condition.filter_type == FilterType.LESS_OR_EQUAL:
        return field_value <= condition.value
    elif condition.filter_type == FilterType.GREATER_THAN:
        return field_value > condition.value
    elif condition.filter_type == FilterType.GREATER_OR_EQUAL:
        return field_value >= condition.value

    return False
